"""Simple unit tests for the CRUD API application."""
import pytest
from main import app
from database import InMemoryDatabase
from models import ProductCreate, ProductUpdate, UserCreate, UserUpdate


class TestDatabaseOperations:
    """Test database operations directly."""

    def setup_method(self):
        """Set up fresh database for each test."""
        self.db = InMemoryDatabase()

    def test_create_product(self):
        """Test creating a product."""
        product_data = ProductCreate(
            name="Test Product",
            description="A test product",
            price=29.99,
            category="Test"
        )
        product = self.db.create_product(product_data)
        assert product.name == "Test Product"
        assert product.price == 29.99
        assert product.id == 1

    def test_get_product(self):
        """Test getting a product."""
        # Create a product first
        product_data = ProductCreate(
            name="Test Product",
            description="A test product",
            price=29.99,
            category="Test"
        )
        created_product = self.db.create_product(product_data)
        
        # Get the product
        retrieved_product = self.db.get_product(created_product.id)
        assert retrieved_product is not None
        assert retrieved_product.name == "Test Product"

    def test_get_product_not_found(self):
        """Test getting a non-existent product."""
        product = self.db.get_product(999)
        assert product is None

    def test_update_product(self):
        """Test updating a product."""
        # Create a product first
        product_data = ProductCreate(
            name="Original Name",
            description="Original description",
            price=10.0,
            category="Original"
        )
        created_product = self.db.create_product(product_data)
        
        # Update the product
        update_data = ProductUpdate(name="Updated Name", price=20.0)
        updated_product = self.db.update_product(created_product.id, update_data)
        
        assert updated_product is not None
        assert updated_product.name == "Updated Name"
        assert updated_product.price == 20.0
        assert updated_product.description == "Original description"  # Should remain unchanged

    def test_delete_product(self):
        """Test deleting a product."""
        # Create a product first
        product_data = ProductCreate(
            name="To Delete",
            description="Will be deleted",
            price=5.0,
            category="Test"
        )
        created_product = self.db.create_product(product_data)
        
        # Delete the product
        success = self.db.delete_product(created_product.id)
        assert success is True
        
        # Verify it's gone
        retrieved_product = self.db.get_product(created_product.id)
        assert retrieved_product is None

    def test_create_user(self):
        """Test creating a user."""
        user_data = UserCreate(
            name="Test User",
            email="test@example.com",
            password="password123"
        )
        user = self.db.create_user(user_data)
        assert user.name == "Test User"
        assert user.email == "test@example.com"
        assert user.id == 1

    def test_get_user(self):
        """Test getting a user."""
        # Create a user first
        user_data = UserCreate(
            name="Test User",
            email="test@example.com",
            password="password123"
        )
        created_user = self.db.create_user(user_data)
        
        # Get the user
        retrieved_user = self.db.get_user(created_user.id)
        assert retrieved_user is not None
        assert retrieved_user.name == "Test User"

    def test_get_user_not_found(self):
        """Test getting a non-existent user."""
        user = self.db.get_user(999)
        assert user is None

    def test_update_user(self):
        """Test updating a user."""
        # Create a user first
        user_data = UserCreate(
            name="Original Name",
            email="original@example.com",
            password="originalpass"
        )
        created_user = self.db.create_user(user_data)
        
        # Update the user
        update_data = UserUpdate(name="Updated Name", email="updated@example.com")
        updated_user = self.db.update_user(created_user.id, update_data)
        
        assert updated_user is not None
        assert updated_user.name == "Updated Name"
        assert updated_user.email == "updated@example.com"
        assert updated_user.password == "originalpass"  # Should remain unchanged

    def test_delete_user(self):
        """Test deleting a user."""
        # Create a user first
        user_data = UserCreate(
            name="To Delete",
            email="delete@example.com",
            password="password123"
        )
        created_user = self.db.create_user(user_data)
        
        # Delete the user
        success = self.db.delete_user(created_user.id)
        assert success is True
        
        # Verify it's gone
        retrieved_user = self.db.get_user(created_user.id)
        assert retrieved_user is None


class TestModelValidation:
    """Test Pydantic model validation."""

    def test_product_create_validation(self):
        """Test ProductCreate model validation."""
        # Valid product
        product = ProductCreate(
            name="Valid Product",
            description="Valid description",
            price=99.99,
            category="Valid"
        )
        assert product.name == "Valid Product"
        assert product.price == 99.99

    def test_product_update_validation(self):
        """Test ProductUpdate model validation."""
        # Valid update with partial data
        update = ProductUpdate(name="Updated Name")
        assert update.name == "Updated Name"
        assert update.description is None  # Should be None when not provided

    def test_user_create_validation(self):
        """Test UserCreate model validation."""
        # Valid user
        user = UserCreate(
            name="Valid User",
            email="valid@example.com",
            password="validpass"
        )
        assert user.name == "Valid User"
        assert user.email == "valid@example.com"

    def test_user_update_validation(self):
        """Test UserUpdate model validation."""
        # Valid update with partial data
        update = UserUpdate(name="Updated Name")
        assert update.name == "Updated Name"
        assert update.email is None  # Should be None when not provided


if __name__ == "__main__":
    pytest.main([__file__])
