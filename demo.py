"""
Example usage and demo of the Pet Shop system.
This script demonstrates the structured output and tool calling capabilities.
"""

import asyncio
import json

from models import Pet, PetType, PlaceOrderInput


def demo_structured_models():
    """Demonstrate Pydantic structured models"""
    print("\n" + "=" * 60)
    print("DEMO: Structured Output Models with Pydantic")
    print("=" * 60 + "\n")

    # Create a pet using structured model
    print("1. Creating a Pet with structured model:")
    pet = Pet(
        id="demo001",
        name="Golden Retriever Puppy",
        type=PetType.DOG,
        description="Friendly and playful Golden Retriever puppy",
        price=1200.00,
        age_months=3,
        available=True,
    )
    print(f"   Pet created: {pet.name} (${pet.price})")
    print(f"   Type-safe enum: {pet.type} (type: {type(pet.type).__name__})")
    print(f"   JSON output:\n   {pet.model_dump_json(indent=2)}\n")

    # Create order input (for tool calling)
    print("2. Creating structured input for tool calling:")
    order_input = PlaceOrderInput(
        customer_name="John Doe",
        customer_email="john@example.com",
        customer_phone="555-0123",
        delivery_address="123 Main St, City, ST 12345",
        pet_ids=["demo001"],
    )
    print(f"   Order input validated and ready")
    print(f"   JSON for API:\n   {order_input.model_dump_json(indent=2)}\n")

    # Show validation in action
    print("3. Demonstrating validation:")
    try:
        invalid_pet = Pet(
            id="demo002",
            name="Invalid Pet",
            type=PetType.CAT,
            description="Test",
            price=-100.0,  # Invalid negative price
            age_months=5,
            available=True,
        )
    except Exception as e:
        print(f"   ✓ Validation caught error: {type(e).__name__}")
        print(f"   ✓ Invalid data rejected (negative price)\n")


def demo_tool_definitions():
    """Demonstrate tool calling definitions for Azure OpenAI"""
    print("\n" + "=" * 60)
    print("DEMO: Tool Calling Definitions for Azure OpenAI")
    print("=" * 60 + "\n")

    from tools import TOOLS_DEFINITIONS

    print("Available tools for AI agent:\n")
    for i, tool in enumerate(TOOLS_DEFINITIONS, 1):
        func = tool["function"]
        print(f"{i}. {func['name']}")
        print(f"   Description: {func['description']}")
        print(f"   Parameters: {list(func['parameters']['properties'].keys())}")
        print()

    print("These tools enable the AI to:")
    print("  • Browse pets with filters")
    print("  • Place orders with validation")
    print("  • Check order status")
    print("  • All with structured, type-safe inputs and outputs\n")


def demo_conversation_flow():
    """Demonstrate a typical conversation flow"""
    print("\n" + "=" * 60)
    print("DEMO: Typical Conversation Flow")
    print("=" * 60 + "\n")

    print("Example conversation with the AI assistant:\n")

    conversation = [
        {"role": "user", "message": "Show me available dogs under $1000"},
        {
            "role": "assistant",
            "action": "Calls browse_pets tool",
            "params": {"pet_type": "dog", "max_price": 1000.0},
            "response": "I found 1 dog under $1000: Beagle for $950",
        },
        {"role": "user", "message": "I'd like to order the Beagle"},
        {
            "role": "assistant",
            "action": "Asks for customer information",
            "response": "Great choice! I'll need some information to complete your order...",
        },
        {
            "role": "user",
            "message": "My name is Sarah Smith, email sarah@email.com, phone 555-1234, address 456 Oak Ave",
        },
        {
            "role": "assistant",
            "action": "Calls place_order tool",
            "params": {
                "customer_name": "Sarah Smith",
                "customer_email": "sarah@email.com",
                "customer_phone": "555-1234",
                "delivery_address": "456 Oak Ave",
                "pet_ids": ["pet003"],
            },
            "response": "✓ Order confirmed! Order ID: ORD-ABC123XY",
        },
    ]

    for step in conversation:
        if step["role"] == "user":
            print(f"👤 User: {step['message']}")
        else:
            print(f"🤖 Assistant:")
            if "action" in step:
                print(f"   Action: {step['action']}")
            if "params" in step:
                print(f"   Params: {json.dumps(step['params'], indent=10)}")
            print(f"   → {step['response']}")
        print()


def demo_structured_outputs_benefits():
    """Show benefits of structured outputs"""
    print("\n" + "=" * 60)
    print("DEMO: Benefits of Structured Outputs")
    print("=" * 60 + "\n")

    benefits = [
        {
            "benefit": "Type Safety",
            "example": "PetType enum ensures only valid pet types (dog, cat, bird, fish, rabbit, hamster)",
        },
        {"benefit": "Validation", "example": "Price must be > 0, age must be >= 0, email format validated"},
        {"benefit": "Auto Documentation", "example": "Pydantic models auto-generate OpenAPI/JSON schemas"},
        {"benefit": "IDE Support", "example": "Full autocomplete and type hints in VS Code/PyCharm"},
        {"benefit": "Serialization", "example": "Easy JSON/dict conversion with .model_dump() and .model_dump_json()"},
        {
            "benefit": "API Integration",
            "example": "FastAPI automatically validates requests/responses using these models",
        },
        {"benefit": "AI Tool Calling", "example": "Azure OpenAI can call tools with guaranteed valid parameters"},
    ]

    for i, item in enumerate(benefits, 1):
        print(f"{i}. {item['benefit']}")
        print(f"   → {item['example']}\n")


def demo_azure_openai_integration():
    """Show how Azure OpenAI integrates with the system"""
    print("\n" + "=" * 60)
    print("DEMO: Azure OpenAI Integration Flow")
    print("=" * 60 + "\n")

    print("Integration Architecture:\n")

    print("1️⃣  User sends message via Chainlit chat")
    print("   ↓")
    print("2️⃣  Message sent to Azure OpenAI with tool definitions")
    print("   ↓")
    print("3️⃣  Azure OpenAI decides which tool to call (if any)")
    print("   ↓")
    print("4️⃣  Tool parameters validated with Pydantic models")
    print("   ↓")
    print("5️⃣  Tool makes REST API call to FastAPI backend")
    print("   ↓")
    print("6️⃣  FastAPI validates request with Pydantic models")
    print("   ↓")
    print("7️⃣  MongoDB operation executed")
    print("   ↓")
    print("8️⃣  Response validated with Pydantic models")
    print("   ↓")
    print("9️⃣  Tool returns structured result to Azure OpenAI")
    print("   ↓")
    print("🔟 Azure OpenAI generates natural language response")
    print("   ↓")
    print("1️⃣1️⃣  User sees friendly message in Chainlit\n")

    print("Key Features:")
    print("  ✓ End-to-end type safety")
    print("  ✓ Automatic validation at every step")
    print("  ✓ Structured outputs from AI")
    print("  ✓ Clean separation of concerns")
    print("  ✓ Testable components\n")


def main():
    """Run all demos"""
    print("\n" + "=" * 60)
    print("🐾 PET PARADISE SHOP - SYSTEM DEMONSTRATION 🐾")
    print("=" * 60)

    demo_structured_models()
    demo_tool_definitions()
    demo_conversation_flow()
    demo_structured_outputs_benefits()
    demo_azure_openai_integration()

    print("\n" + "=" * 60)
    print("Demo Complete!")
    print("=" * 60 + "\n")

    print("To run the actual system:")
    print("  1. Configure .env with your Azure OpenAI credentials")
    print("  2. Start MongoDB")
    print("  3. Run: python api.py (in one terminal)")
    print("  4. Run: chainlit run app.py (in another terminal)")
    print("  5. Open http://localhost:8001 and start chatting!\n")

    print("Or use the startup script:")
    print("  ./start.sh\n")


if __name__ == "__main__":
    main()
