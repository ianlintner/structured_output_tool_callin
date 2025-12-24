"""
FastAPI REST API for Pet Shop ordering service.
Provides endpoints for browsing pets, creating orders, and checking order status.
"""
from fastapi import FastAPI, HTTPException, status
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager
from typing import Optional, List
import os
from datetime import datetime
import uuid

from database import connect_to_mongo, close_mongo_connection, get_database
from models import (
    Pet, Order, CustomerInfo, OrderItem, OrderStatus,
    BrowsePetsInput, PlaceOrderInput, CheckOrderStatusInput,
    PetInventoryResponse, OrderStatusResponse
)


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Application lifespan manager"""
    # Startup
    await connect_to_mongo()
    yield
    # Shutdown
    await close_mongo_connection()


# Initialize FastAPI app
app = FastAPI(
    title="Pet Shop API",
    description="REST API for pet shop ordering and inventory management",
    version="1.0.0",
    lifespan=lifespan
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/")
async def root():
    """Root endpoint"""
    return {
        "message": "Pet Shop API",
        "version": "1.0.0",
        "endpoints": {
            "pets": "/pets",
            "orders": "/orders",
            "docs": "/docs"
        }
    }


@app.get("/health")
async def health_check():
    """Health check endpoint"""
    db = await get_database()
    try:
        await db.command('ping')
        return {"status": "healthy", "database": "connected"}
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail=f"Database connection failed: {str(e)}"
        )


@app.get("/pets", response_model=PetInventoryResponse)
async def get_pets(
    pet_type: Optional[str] = None,
    max_price: Optional[float] = None,
    min_age_months: Optional[int] = None,
    max_age_months: Optional[int] = None,
    available_only: bool = True
):
    """
    Get list of pets with optional filters.
    
    Query Parameters:
    - pet_type: Filter by pet type (dog, cat, bird, fish, rabbit, hamster)
    - max_price: Maximum price filter
    - min_age_months: Minimum age in months
    - max_age_months: Maximum age in months
    - available_only: Only show available pets (default: True)
    """
    db = await get_database()
    pets_collection = db.pets
    
    # Build query filter
    query = {}
    if available_only:
        query["available"] = True
    if pet_type:
        query["type"] = pet_type.lower()
    if max_price is not None:
        query["price"] = {"$lte": max_price}
    if min_age_months is not None:
        query.setdefault("age_months", {})["$gte"] = min_age_months
    if max_age_months is not None:
        query.setdefault("age_months", {})["$lte"] = max_age_months
    
    # Query database
    cursor = pets_collection.find(query)
    pets_list = await cursor.to_list(length=100)
    
    # Convert to Pydantic models
    pets = [Pet(**pet) for pet in pets_list]
    
    return PetInventoryResponse(
        pets=pets,
        total=len(pets),
        filtered_by_type=pet_type if pet_type else None
    )


@app.get("/pets/{pet_id}", response_model=Pet)
async def get_pet_by_id(pet_id: str):
    """Get a specific pet by ID"""
    db = await get_database()
    pets_collection = db.pets
    
    pet_data = await pets_collection.find_one({"id": pet_id})
    if not pet_data:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Pet with ID {pet_id} not found"
        )
    
    return Pet(**pet_data)


@app.post("/orders", response_model=Order, status_code=status.HTTP_201_CREATED)
async def create_order(order_input: PlaceOrderInput):
    """
    Create a new pet order.
    
    Request body should include:
    - customer_name: Customer's full name
    - customer_email: Customer's email
    - customer_phone: Customer's phone number
    - delivery_address: Delivery address
    - pet_ids: List of pet IDs to order
    """
    db = await get_database()
    pets_collection = db.pets
    orders_collection = db.orders
    
    # Validate all pets exist and are available
    order_items = []
    total_amount = 0.0
    
    for pet_id in order_input.pet_ids:
        pet_data = await pets_collection.find_one({"id": pet_id, "available": True})
        if not pet_data:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Pet {pet_id} is not available"
            )
        
        order_items.append(OrderItem(
            pet_id=pet_data["id"],
            pet_name=pet_data["name"],
            price=pet_data["price"]
        ))
        total_amount += pet_data["price"]
    
    # Create order
    order_id = f"ORD-{uuid.uuid4().hex[:8].upper()}"
    customer = CustomerInfo(
        name=order_input.customer_name,
        email=order_input.customer_email,
        phone=order_input.customer_phone,
        address=order_input.delivery_address
    )
    
    order = Order(
        id=order_id,
        customer=customer,
        items=order_items,
        total_amount=total_amount,
        status=OrderStatus.PENDING,
        created_at=datetime.utcnow(),
        updated_at=datetime.utcnow()
    )
    
    # Save to database
    await orders_collection.insert_one(order.model_dump())
    
    # Mark pets as unavailable
    for pet_id in order_input.pet_ids:
        await pets_collection.update_one(
            {"id": pet_id},
            {"$set": {"available": False}}
        )
    
    return order


@app.get("/orders/{order_id}", response_model=Order)
async def get_order(order_id: str):
    """Get order details by order ID"""
    db = await get_database()
    orders_collection = db.orders
    
    order_data = await orders_collection.find_one({"id": order_id})
    if not order_data:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Order {order_id} not found"
        )
    
    return Order(**order_data)


@app.get("/orders/{order_id}/status", response_model=OrderStatusResponse)
async def get_order_status(order_id: str):
    """Get simplified order status"""
    db = await get_database()
    orders_collection = db.orders
    
    order_data = await orders_collection.find_one({"id": order_id})
    if not order_data:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Order {order_id} not found"
        )
    
    order = Order(**order_data)
    return OrderStatusResponse(
        order_id=order.id,
        status=order.status,
        customer_name=order.customer.name,
        total_amount=order.total_amount,
        created_at=order.created_at,
        items_count=len(order.items)
    )


@app.put("/orders/{order_id}/status")
async def update_order_status(order_id: str, new_status: OrderStatus):
    """Update order status (for testing/admin purposes)"""
    db = await get_database()
    orders_collection = db.orders
    
    result = await orders_collection.update_one(
        {"id": order_id},
        {"$set": {"status": new_status.value, "updated_at": datetime.utcnow()}}
    )
    
    if result.matched_count == 0:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Order {order_id} not found"
        )
    
    return {"message": f"Order {order_id} status updated to {new_status.value}"}


if __name__ == "__main__":
    import uvicorn
    
    host = os.getenv("API_HOST", "0.0.0.0")
    port = int(os.getenv("API_PORT", "8000"))
    
    uvicorn.run(app, host=host, port=port)
