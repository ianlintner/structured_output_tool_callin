"""
Pydantic models for structured outputs and data validation.
These models ensure type safety and validation for the pet shop system.
"""
from typing import Optional, List, Literal
from pydantic import BaseModel, Field, ConfigDict
from datetime import datetime
from enum import Enum


# Enums for type safety
class PetType(str, Enum):
    """Available pet types in the shop"""
    DOG = "dog"
    CAT = "cat"
    BIRD = "bird"
    FISH = "fish"
    RABBIT = "rabbit"
    HAMSTER = "hamster"


class OrderStatus(str, Enum):
    """Order status states"""
    PENDING = "pending"
    CONFIRMED = "confirmed"
    PROCESSING = "processing"
    SHIPPED = "shipped"
    DELIVERED = "delivered"
    CANCELLED = "cancelled"


# Pet Models
class Pet(BaseModel):
    """Pet model for inventory"""
    model_config = ConfigDict(use_enum_values=True)
    
    id: str = Field(description="Unique identifier for the pet")
    name: str = Field(description="Name/breed of the pet")
    type: PetType = Field(description="Type of pet")
    description: str = Field(description="Detailed description of the pet")
    price: float = Field(gt=0, description="Price in USD")
    age_months: int = Field(ge=0, description="Age in months")
    available: bool = Field(default=True, description="Availability status")
    image_url: Optional[str] = Field(None, description="URL to pet image")


class PetInventoryResponse(BaseModel):
    """Response model for pet inventory listing"""
    pets: List[Pet] = Field(description="List of available pets")
    total: int = Field(description="Total number of pets")
    filtered_by_type: Optional[PetType] = Field(None, description="Filter applied")


# Order Models
class OrderItem(BaseModel):
    """Individual item in an order"""
    pet_id: str = Field(description="ID of the pet being ordered")
    pet_name: str = Field(description="Name of the pet")
    price: float = Field(description="Price at time of order")


class CustomerInfo(BaseModel):
    """Customer information for order"""
    name: str = Field(min_length=1, description="Customer full name")
    email: str = Field(description="Customer email address")
    phone: str = Field(description="Customer phone number")
    address: str = Field(min_length=5, description="Delivery address")


class Order(BaseModel):
    """Order model"""
    model_config = ConfigDict(use_enum_values=True)
    
    id: str = Field(description="Unique order identifier")
    customer: CustomerInfo = Field(description="Customer information")
    items: List[OrderItem] = Field(min_length=1, description="List of ordered items")
    total_amount: float = Field(gt=0, description="Total order amount")
    status: OrderStatus = Field(default=OrderStatus.PENDING, description="Order status")
    created_at: datetime = Field(default_factory=datetime.utcnow, description="Order creation timestamp")
    updated_at: datetime = Field(default_factory=datetime.utcnow, description="Last update timestamp")


# Tool Calling Models (Structured Outputs for Azure OpenAI)
class BrowsePetsInput(BaseModel):
    """Input parameters for browsing pets"""
    pet_type: Optional[PetType] = Field(None, description="Filter by pet type")
    max_price: Optional[float] = Field(None, gt=0, description="Maximum price filter")
    min_age_months: Optional[int] = Field(None, ge=0, description="Minimum age in months")
    max_age_months: Optional[int] = Field(None, ge=0, description="Maximum age in months")


class PlaceOrderInput(BaseModel):
    """Input parameters for placing an order"""
    customer_name: str = Field(min_length=1, description="Customer full name")
    customer_email: str = Field(description="Customer email address")
    customer_phone: str = Field(description="Customer phone number")
    delivery_address: str = Field(min_length=5, description="Delivery address")
    pet_ids: List[str] = Field(min_length=1, description="List of pet IDs to order")


class CheckOrderStatusInput(BaseModel):
    """Input parameters for checking order status"""
    order_id: str = Field(description="Order ID to check")


class OrderStatusResponse(BaseModel):
    """Response for order status check"""
    model_config = ConfigDict(use_enum_values=True)
    
    order_id: str = Field(description="Order identifier")
    status: OrderStatus = Field(description="Current order status")
    customer_name: str = Field(description="Customer name")
    total_amount: float = Field(description="Total order amount")
    created_at: datetime = Field(description="Order creation time")
    items_count: int = Field(description="Number of items in order")


# Tool Response Models
class ToolResponse(BaseModel):
    """Generic tool response wrapper"""
    success: bool = Field(description="Whether the operation was successful")
    message: str = Field(description="Human-readable message about the result")
    data: Optional[dict] = Field(None, description="Additional response data")


class BrowsePetsOutput(BaseModel):
    """Output from browse pets tool"""
    pets: List[Pet] = Field(description="List of matching pets")
    message: str = Field(description="Summary message")


class PlaceOrderOutput(BaseModel):
    """Output from place order tool"""
    order_id: str = Field(description="Created order ID")
    total_amount: float = Field(description="Total order amount")
    message: str = Field(description="Confirmation message")
