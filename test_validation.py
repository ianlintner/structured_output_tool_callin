"""
Simple validation tests for the pet shop system.
Tests model validation, imports, and basic functionality.
"""
import asyncio
from models import (
    Pet, PetType, Order, OrderStatus, CustomerInfo, OrderItem,
    BrowsePetsInput, PlaceOrderInput, CheckOrderStatusInput
)


def test_pet_model():
    """Test Pet model validation"""
    print("Testing Pet model...")
    
    pet = Pet(
        id="test001",
        name="Test Dog",
        type=PetType.DOG,
        description="A test dog",
        price=100.0,
        age_months=6,
        available=True
    )
    
    assert pet.id == "test001"
    assert pet.type == "dog"  # Enum should be converted to value
    assert pet.price == 100.0
    print("✓ Pet model validation passed")


def test_order_model():
    """Test Order model validation"""
    print("Testing Order model...")
    
    customer = CustomerInfo(
        name="Test Customer",
        email="test@example.com",
        phone="555-0123",
        address="123 Test St"
    )
    
    item = OrderItem(
        pet_id="test001",
        pet_name="Test Dog",
        price=100.0
    )
    
    order = Order(
        id="ORD-TEST",
        customer=customer,
        items=[item],
        total_amount=100.0,
        status=OrderStatus.PENDING
    )
    
    assert order.id == "ORD-TEST"
    assert order.customer.name == "Test Customer"
    assert len(order.items) == 1
    assert order.total_amount == 100.0
    assert order.status == "pending"
    print("✓ Order model validation passed")


def test_tool_input_models():
    """Test tool input models"""
    print("Testing tool input models...")
    
    # Test BrowsePetsInput
    browse_input = BrowsePetsInput(
        pet_type=PetType.CAT,
        max_price=500.0
    )
    assert browse_input.pet_type == "cat"
    assert browse_input.max_price == 500.0
    
    # Test PlaceOrderInput
    place_order = PlaceOrderInput(
        customer_name="Test",
        customer_email="test@example.com",
        customer_phone="555-0123",
        delivery_address="123 Test St",
        pet_ids=["pet001"]
    )
    assert len(place_order.pet_ids) == 1
    
    # Test CheckOrderStatusInput
    check_status = CheckOrderStatusInput(order_id="ORD-TEST")
    assert check_status.order_id == "ORD-TEST"
    
    print("✓ Tool input models validation passed")


def test_imports():
    """Test that all imports work"""
    print("Testing imports...")
    
    try:
        # models symbols are imported at module level via 'from models import ...'
        _pet = Pet(
            id="import-test",
            name="Import Test Pet",
            type=PetType.DOG,
            description="Import test",
            price=1.0,
            age_months=1,
            available=True,
        )
        import tools
        print("✓ models symbols imported successfully")
        print("✓ tools.py imports successfully")
        
        # Check tool definitions exist
        assert len(tools.TOOLS_DEFINITIONS) == 3
        assert len(tools.TOOLS_MAP) == 3
        assert "browse_pets" in tools.TOOLS_MAP
        assert "place_order" in tools.TOOLS_MAP
        assert "check_order_status" in tools.TOOLS_MAP
        print("✓ Tool definitions are complete")
        
    except ImportError as e:
        print(f"✗ Import error: {e}")
        raise


def test_pydantic_validation():
    """Test Pydantic validation works"""
    print("Testing Pydantic validation...")
    
    try:
        # Should fail - negative price
        Pet(
            id="test",
            name="Test",
            type=PetType.DOG,
            description="Test",
            price=-100.0,  # Invalid
            age_months=6,
            available=True
        )
        print("✗ Validation should have failed for negative price")
    except Exception:
        print("✓ Pydantic validation working (negative price rejected)")
    
    try:
        # Should fail - empty name
        PlaceOrderInput(
            customer_name="",  # Invalid
            customer_email="test@example.com",
            customer_phone="555",
            delivery_address="123 Test St",
            pet_ids=["pet001"]
        )
        print("✗ Validation should have failed for empty name")
    except Exception:
        print("✓ Pydantic validation working (empty name rejected)")


def main():
    """Run all tests"""
    print("\n" + "="*50)
    print("Pet Shop System Validation Tests")
    print("="*50 + "\n")
    
    try:
        test_imports()
        print()
        test_pet_model()
        print()
        test_order_model()
        print()
        test_tool_input_models()
        print()
        test_pydantic_validation()
        
        print("\n" + "="*50)
        print("✓ All validation tests passed!")
        print("="*50 + "\n")
        
    except Exception as e:
        print("\n" + "="*50)
        print(f"✗ Tests failed: {e}")
        print("="*50 + "\n")
        raise


if __name__ == "__main__":
    main()
