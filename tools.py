"""
Tool calling functions for the chat agent.
These functions connect the AI agent to the pet shop API.
"""

import os
from typing import List, Optional

import httpx

# Import observability
try:
    from observability import get_tracer, record_tool_call

    OBSERVABILITY_ENABLED = True
    tracer = get_tracer(__name__)
except ImportError:
    OBSERVABILITY_ENABLED = False


# Get API base URL from environment or default to localhost
API_BASE_URL = os.getenv("API_BASE_URL", "http://localhost:8000")


async def browse_pets_tool(
    pet_type: Optional[str] = None,
    max_price: Optional[float] = None,
    min_age_months: Optional[int] = None,
    max_age_months: Optional[int] = None,
) -> dict:
    """
    Browse available pets in the shop with optional filters.

    Args:
        pet_type: Filter by pet type (dog, cat, bird, fish, rabbit, hamster)
        max_price: Maximum price filter
        min_age_months: Minimum age in months
        max_age_months: Maximum age in months

    Returns:
        Dictionary with list of available pets and summary message
    """
    # Start tracing span
    if OBSERVABILITY_ENABLED:
        with tracer.start_as_current_span("browse_pets_tool") as span:
            span.set_attribute("pet_type", pet_type or "all")
            span.set_attribute("max_price", max_price or 0)
            result = await _browse_pets_impl(pet_type, max_price, min_age_months, max_age_months)
            record_tool_call("browse_pets", result.get("total", 0) > 0)
            return result
    else:
        return await _browse_pets_impl(pet_type, max_price, min_age_months, max_age_months)


async def _browse_pets_impl(pet_type, max_price, min_age_months, max_age_months) -> dict:
    async with httpx.AsyncClient() as client:
        params = {"available_only": True}
        if pet_type:
            # Validate pet_type against allowed values
            valid_types = ["dog", "cat", "bird", "fish", "rabbit", "hamster"]
            if pet_type.lower() not in valid_types:
                return {
                    "pets": [],
                    "message": f"Invalid pet type '{pet_type}'. Valid types: {', '.join(valid_types)}",
                    "total": 0,
                }
            params["pet_type"] = pet_type.lower()
        if max_price is not None:
            params["max_price"] = max_price
        if min_age_months is not None:
            params["min_age_months"] = min_age_months
        if max_age_months is not None:
            params["max_age_months"] = max_age_months

        try:
            response = await client.get(f"{API_BASE_URL}/pets", params=params)
            response.raise_for_status()
            data = response.json()

            pets = data.get("pets", [])
            total = data.get("total", 0)

            if total == 0:
                message = "No pets found matching your criteria. Try adjusting your filters."
            else:
                message = f"Found {total} pet(s) matching your criteria."
                if pet_type:
                    message += f" (Type: {pet_type})"

            return {"pets": pets, "message": message, "total": total}
        except httpx.HTTPError as e:
            return {"pets": [], "message": f"Error browsing pets: {str(e)}", "total": 0}


async def place_order_tool(
    customer_name: str, customer_email: str, customer_phone: str, delivery_address: str, pet_ids: List[str]
) -> dict:
    """
    Place an order for one or more pets.

    Args:
        customer_name: Customer's full name
        customer_email: Customer's email address
        customer_phone: Customer's phone number
        delivery_address: Delivery address
        pet_ids: List of pet IDs to order

    Returns:
        Dictionary with order confirmation details
    """
    async with httpx.AsyncClient() as client:
        order_data = {
            "customer_name": customer_name,
            "customer_email": customer_email,
            "customer_phone": customer_phone,
            "delivery_address": delivery_address,
            "pet_ids": pet_ids,
        }

        try:
            response = await client.post(f"{API_BASE_URL}/orders", json=order_data)
            response.raise_for_status()
            order = response.json()

            order_id = order.get("id")
            total_amount = order.get("total_amount")
            items_count = len(order.get("items", []))

            message = (
                f"✓ Order confirmed! Order ID: {order_id}\n"
                f"Total: ${total_amount:.2f} for {items_count} pet(s)\n"
                f"Delivery to: {delivery_address}\n"
                f"You will receive a confirmation email at {customer_email}"
            )

            return {
                "success": True,
                "order_id": order_id,
                "total_amount": total_amount,
                "message": message,
                "order": order,
            }
        except httpx.HTTPStatusError as e:
            try:
                error_detail = e.response.json().get("detail", str(e))
            except (ValueError, KeyError):
                error_detail = str(e)
            return {
                "success": False,
                "order_id": None,
                "total_amount": 0,
                "message": f"Failed to place order: {error_detail}",
            }
        except httpx.HTTPError as e:
            return {"success": False, "order_id": None, "total_amount": 0, "message": f"Error placing order: {str(e)}"}


async def check_order_status_tool(order_id: str) -> dict:
    """
    Check the status of an existing order.

    Args:
        order_id: The order ID to check

    Returns:
        Dictionary with order status information
    """
    async with httpx.AsyncClient() as client:
        try:
            response = await client.get(f"{API_BASE_URL}/orders/{order_id}/status")
            response.raise_for_status()
            status_data = response.json()

            order_id = status_data.get("order_id")
            status = status_data.get("status")
            customer_name = status_data.get("customer_name")
            total_amount = status_data.get("total_amount")
            items_count = status_data.get("items_count")
            created_at = status_data.get("created_at")

            status_messages = {
                "pending": "📋 Your order is pending confirmation",
                "confirmed": "✓ Your order has been confirmed and is being prepared",
                "processing": "📦 Your order is being processed",
                "shipped": "🚚 Your order has been shipped and is on the way",
                "delivered": "✓ Your order has been delivered",
                "cancelled": "✗ Your order has been cancelled",
            }

            status_msg = status_messages.get(status, f"Status: {status}")

            message = (
                f"Order Status for {order_id}:\n"
                f"{status_msg}\n"
                f"Customer: {customer_name}\n"
                f"Items: {items_count} pet(s)\n"
                f"Total: ${total_amount:.2f}"
            )

            return {
                "success": True,
                "order_id": order_id,
                "status": status,
                "message": message,
                "details": status_data,
                "created_at": created_at,
            }
        except httpx.HTTPStatusError as e:
            if e.response.status_code == 404:
                return {
                    "success": False,
                    "order_id": order_id,
                    "status": None,
                    "message": f"Order {order_id} not found. Please check the order ID and try again.",
                }
            try:
                error_detail = e.response.json().get("detail", str(e))
            except (ValueError, KeyError):
                error_detail = str(e)
            return {
                "success": False,
                "order_id": order_id,
                "status": None,
                "message": f"Error checking order status: {error_detail}",
            }
        except httpx.HTTPError as e:
            return {
                "success": False,
                "order_id": order_id,
                "status": None,
                "message": f"Error checking order status: {str(e)}",
            }


# Tool definitions for Azure OpenAI function calling
TOOLS_DEFINITIONS = [
    {
        "type": "function",
        "function": {
            "name": "browse_pets",
            "description": "Browse available pets in the pet shop. Can filter by pet type, price range, and age range. Returns a list of pets matching the criteria.",
            "parameters": {
                "type": "object",
                "properties": {
                    "pet_type": {
                        "type": "string",
                        "enum": ["dog", "cat", "bird", "fish", "rabbit", "hamster"],
                        "description": "Filter by type of pet",
                    },
                    "max_price": {"type": "number", "description": "Maximum price in USD"},
                    "min_age_months": {"type": "integer", "description": "Minimum age in months"},
                    "max_age_months": {"type": "integer", "description": "Maximum age in months"},
                },
                "required": [],
            },
        },
    },
    {
        "type": "function",
        "function": {
            "name": "place_order",
            "description": "Place an order for one or more pets. Requires customer information and list of pet IDs to purchase. Returns order confirmation with order ID.",
            "parameters": {
                "type": "object",
                "properties": {
                    "customer_name": {"type": "string", "description": "Customer's full name"},
                    "customer_email": {"type": "string", "description": "Customer's email address"},
                    "customer_phone": {"type": "string", "description": "Customer's phone number"},
                    "delivery_address": {
                        "type": "string",
                        "description": "Full delivery address including street, city, state, and zip code",
                    },
                    "pet_ids": {
                        "type": "array",
                        "items": {"type": "string"},
                        "description": "List of pet IDs to order (e.g., ['pet001', 'pet002'])",
                    },
                },
                "required": ["customer_name", "customer_email", "customer_phone", "delivery_address", "pet_ids"],
            },
        },
    },
    {
        "type": "function",
        "function": {
            "name": "check_order_status",
            "description": "Check the current status of an existing order using the order ID. Returns order status, customer info, and tracking information.",
            "parameters": {
                "type": "object",
                "properties": {
                    "order_id": {"type": "string", "description": "The order ID to check (format: ORD-XXXXXXXX)"}
                },
                "required": ["order_id"],
            },
        },
    },
]


# Map function names to actual functions
TOOLS_MAP = {
    "browse_pets": browse_pets_tool,
    "place_order": place_order_tool,
    "check_order_status": check_order_status_tool,
}
