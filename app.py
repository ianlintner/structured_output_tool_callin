"""
Chainlit chat application for Pet Shop ordering and support.
Uses Azure OpenAI with structured outputs and tool calling.
"""

import json
import os

import chainlit as cl
from dotenv import load_dotenv
from openai import AsyncAzureOpenAI

from tools import TOOLS_DEFINITIONS, TOOLS_MAP

load_dotenv()

# Initialize Azure OpenAI client
client = AsyncAzureOpenAI(
    api_key=os.getenv("AZURE_OPENAI_API_KEY"),
    api_version=os.getenv("AZURE_OPENAI_API_VERSION", "2024-02-15-preview"),
    azure_endpoint=os.getenv("AZURE_OPENAI_ENDPOINT"),
)

DEPLOYMENT_NAME = os.getenv("AZURE_OPENAI_DEPLOYMENT", "gpt-4")

# System prompt for the pet shop assistant
SYSTEM_PROMPT = """You are a helpful and friendly pet shop assistant. Your role is to help customers:

1. Browse available pets in our inventory
2. Get detailed information about specific pets
3. Place orders for pets they want to purchase
4. Check the status of their existing orders

Key Guidelines:
- Be warm, friendly, and professional
- When customers ask to see pets, use the browse_pets tool with appropriate filters
- Present pet information clearly with names, types, prices, ages, and descriptions
- When customers want to order, collect all required information: name, email, phone, and delivery address
- Use the place_order tool once you have all customer information and pet selections
- For order status inquiries, use the check_order_status tool with the order ID
- Confirm details before placing orders
- Provide clear pricing information
- If a customer is unsure, offer suggestions based on their preferences

Available pet types: dog, cat, bird, fish, rabbit, hamster

Always be helpful and make the shopping experience enjoyable!"""


@cl.on_chat_start
async def start():
    """Initialize the chat session"""
    # Initialize message history
    cl.user_session.set("message_history", [{"role": "system", "content": SYSTEM_PROMPT}])

    # Send welcome message
    welcome_message = """# 🐾 Welcome to Pet Paradise! 🐾

I'm your pet shop assistant, here to help you find your perfect companion!

**What I can help you with:**
- 🔍 Browse our available pets (dogs, cats, birds, fish, rabbits, hamsters)
- 📋 Get detailed information about any pet
- 🛒 Place orders for pets you'd like to adopt
- 📦 Check the status of your orders

**How to get started:**
- Ask to see available pets: "Show me dogs" or "What pets do you have?"
- Filter by criteria: "Show me cats under $500"
- Order pets: "I'd like to order the Golden Retriever"
- Check orders: "What's the status of my order ORD-12345?"

What would you like to do today?"""

    await cl.Message(content=welcome_message).send()


@cl.on_message
async def main(message: cl.Message):
    """Handle incoming messages"""
    # Get message history
    message_history = cl.user_session.get("message_history")

    # Add user message to history
    message_history.append({"role": "user", "content": message.content})

    # Create a message to show we're processing
    response_message = cl.Message(content="")
    await response_message.send()

    # Call Azure OpenAI with tool calling
    current_content = ""
    tool_calls_made = []

    try:
        # Make initial API call
        response = await client.chat.completions.create(
            model=DEPLOYMENT_NAME,
            messages=message_history,
            tools=TOOLS_DEFINITIONS,
            tool_choice="auto",
            temperature=0.7,
            max_tokens=1500,
        )

        assistant_message = response.choices[0].message

        # Check if the assistant wants to call tools
        if assistant_message.tool_calls:
            # Add assistant message with tool calls to history
            message_history.append(
                {
                    "role": "assistant",
                    "content": assistant_message.content,
                    "tool_calls": [
                        {
                            "id": tc.id,
                            "type": tc.type,
                            "function": {"name": tc.function.name, "arguments": tc.function.arguments},
                        }
                        for tc in assistant_message.tool_calls
                    ],
                }
            )

            # Execute each tool call
            for tool_call in assistant_message.tool_calls:
                function_name = tool_call.function.name
                function_args = json.loads(tool_call.function.arguments)

                # Show which tool is being called
                current_content += f"🔧 Using tool: {function_name}...\n\n"
                await response_message.update()

                # Execute the tool
                if function_name in TOOLS_MAP:
                    function_to_call = TOOLS_MAP[function_name]
                    tool_response = await function_to_call(**function_args)

                    # Add tool response to message history
                    message_history.append(
                        {
                            "role": "tool",
                            "tool_call_id": tool_call.id,
                            "name": function_name,
                            "content": json.dumps(tool_response),
                        }
                    )

                    tool_calls_made.append({"function": function_name, "result": tool_response})
                else:
                    # Unknown function
                    message_history.append(
                        {
                            "role": "tool",
                            "tool_call_id": tool_call.id,
                            "name": function_name,
                            "content": json.dumps({"error": f"Unknown function: {function_name}"}),
                        }
                    )

            # Make a second API call to get the final response
            second_response = await client.chat.completions.create(
                model=DEPLOYMENT_NAME, messages=message_history, temperature=0.7, max_tokens=1500
            )

            final_message = second_response.choices[0].message
            current_content = final_message.content

            # Add final response to history
            message_history.append({"role": "assistant", "content": final_message.content})
        else:
            # No tool calls, just use the response directly
            current_content = assistant_message.content
            message_history.append({"role": "assistant", "content": assistant_message.content})

        # Update the message with final content
        response_message.content = current_content
        await response_message.update()

    except Exception as e:
        error_message = f"❌ Sorry, I encountered an error: {str(e)}\n\nPlease try again or rephrase your request."
        response_message.content = error_message
        await response_message.update()

        # Add error to history
        message_history.append({"role": "assistant", "content": error_message})

    # Save updated history
    cl.user_session.set("message_history", message_history)


if __name__ == "__main__":
    # This is just for reference; Chainlit is typically run with: chainlit run app.py
    pass
