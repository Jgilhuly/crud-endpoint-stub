"""Unit tests for the FastAPI CRUD application."""
import pytest
import requests
from main import app
from database import InMemoryDatabase
from models import ProductCreate, ProductUpdate, UserCreate, UserUpdate


class TestProductEndpoints:
    """Test cases for product-related endpoints."""

    def setup_method(self):
        """Set up fresh database for each test."""
        # Reset the database to a clean state
        from main import db
        db.products = []
        db.users = []
        db.next_product_id = 1
        db.next_user_id = 1
        db._init_sample_data()
        self.base_url = "http://localhost:8000"

    def test_read_root(self):
        """Test the root endpoint."""
        response = requests.get(f"{self.base_url}/")
        assert response.status_code == 200
        assert response.json() == {"message": "Welcome to the Product CRUD API"}

    def test_health_check(self):
        """Test the health check endpoint."""
        response = requests.get(f"{self.base_url}/health")
        assert response.status_code == 200
        assert response.json() == {"status": "healthy"}

    def test_get_products_empty(self):
        """Test getting all products when database is empty."""
        # Clear the database
        from main import db
        db.products = []
        response = self.client.get("/products")
        assert response.status_code == 200
        assert response.json() == []

    def test_get_products_with_data(self):
        """Test getting all products when database has data."""
        response = self.client.get("/products")
        assert response.status_code == 200
        products = response.json()
        assert len(products) > 0
        assert "id" in products[0]
        assert "name" in products[0]
        assert "description" in products[0]
        assert "price" in products[0]

    def test_get_product_existing(self):
        """Test getting a specific product that exists."""
        # First get all products to find an existing ID
        response = self.client.get("/products")
        products = response.json()
        if products:
            product_id = products[0]["id"]
            response = self.client.get(f"/products/{product_id}")
            assert response.status_code == 200
            product = response.json()
            assert product["id"] == product_id

    def test_get_product_not_found(self):
        """Test getting a product that doesn't exist."""
        response = self.client.get("/products/99999")
        assert response.status_code == 404
        assert response.json()["detail"] == "Product not found"

    def test_create_product(self):
        """Test creating a new product."""
        product_data = {
            "name": "Test Product",
            "description": "A test product for unit testing",
            "price": 29.99,
            "category": "Test",
            "tags": ["test", "unit"],
            "in_stock": True
        }
        response = self.client.post("/products", json=product_data)
        assert response.status_code == 200
        product = response.json()
        assert product["name"] == product_data["name"]
        assert product["description"] == product_data["description"]
        assert product["price"] == product_data["price"]
        assert "id" in product

    def test_create_product_missing_required_fields(self):
        """Test creating a product with missing required fields."""
        product_data = {
            "name": "Test Product"
            # Missing description, price, category
        }
        response = self.client.post("/products", json=product_data)
        assert response.status_code == 422  # Validation error

    def test_update_product_existing(self):
        """Test updating an existing product."""
        # First create a product
        product_data = {
            "name": "Original Name",
            "description": "Original description",
            "price": 10.0,
            "category": "Original"
        }
        create_response = self.client.post("/products", json=product_data)
        product_id = create_response.json()["id"]

        # Update the product
        update_data = {
            "name": "Updated Name",
            "price": 20.0
        }
        response = self.client.put(f"/products/{product_id}", json=update_data)
        assert response.status_code == 200
        updated_product = response.json()
        assert updated_product["name"] == "Updated Name"
        assert updated_product["price"] == 20.0
        assert updated_product["description"] == "Original description"  # Should remain unchanged

    def test_update_product_not_found(self):
        """Test updating a product that doesn't exist."""
        update_data = {
            "name": "Updated Name"
        }
        response = self.client.put("/products/99999", json=update_data)
        assert response.status_code == 404
        assert response.json()["detail"] == "Product not found"

    def test_delete_product_existing(self):
        """Test deleting an existing product."""
        # First create a product
        product_data = {
            "name": "To Delete",
            "description": "Will be deleted",
            "price": 5.0,
            "category": "Test"
        }
        create_response = self.client.post("/products", json=product_data)
        product_id = create_response.json()["id"]

        # Delete the product
        response = self.client.delete(f"/products/{product_id}")
        assert response.status_code == 200
        assert response.json()["message"] == "Product deleted successfully"

        # Verify it's gone
        get_response = self.client.get(f"/products/{product_id}")
        assert get_response.status_code == 404

    def test_delete_product_not_found(self):
        """Test deleting a product that doesn't exist."""
        response = self.client.delete("/products/99999")
        assert response.status_code == 404
        assert response.json()["detail"] == "Product not found"


class TestUserEndpoints:
    """Test cases for user-related endpoints."""

    def setup_method(self):
        """Set up fresh database for each test."""
        # Reset the database to a clean state
        from main import db
        db.products = []
        db.users = []
        db.next_product_id = 1
        db.next_user_id = 1
        db._init_sample_data()
        self.client = httpx.AsyncClient(app=app, base_url="http://test")

    def test_get_users_empty(self):
        """Test getting all users when database is empty."""
        # Clear the users database
        from main import db
        db.users = []
        response = self.client.get("/users")
        assert response.status_code == 200
        assert response.json() == []

    def test_get_users_with_data(self):
        """Test getting all users when database has data."""
        # First create a user
        user_data = {
            "name": "Test User",
            "email": "test@example.com",
            "password": "password123"
        }
        self.client.post("/users", json=user_data)

        response = self.client.get("/users")
        assert response.status_code == 200
        users = response.json()
        assert len(users) > 0
        assert "id" in users[0]
        assert "name" in users[0]
        assert "email" in users[0]

    def test_get_user_existing(self):
        """Test getting a specific user that exists."""
        # First create a user
        user_data = {
            "name": "Test User",
            "email": "test@example.com",
            "password": "password123"
        }
        create_response = self.client.post("/users", json=user_data)
        user_id = create_response.json()["id"]

        response = self.client.get(f"/users/{user_id}")
        assert response.status_code == 200
        user = response.json()
        assert user["id"] == user_id
        assert user["name"] == user_data["name"]
        assert user["email"] == user_data["email"]

    def test_get_user_not_found(self):
        """Test getting a user that doesn't exist."""
        response = self.client.get("/users/99999")
        assert response.status_code == 404
        assert response.json()["detail"] == "User not found"

    def test_create_user(self):
        """Test creating a new user."""
        user_data = {
            "name": "New User",
            "email": "newuser@example.com",
            "password": "securepassword"
        }
        response = self.client.post("/users", json=user_data)
        assert response.status_code == 200
        user = response.json()
        assert user["name"] == user_data["name"]
        assert user["email"] == user_data["email"]
        assert user["password"] == user_data["password"]
        assert "id" in user

    def test_create_user_missing_required_fields(self):
        """Test creating a user with missing required fields."""
        user_data = {
            "name": "Test User"
            # Missing email and password
        }
        response = self.client.post("/users", json=user_data)
        assert response.status_code == 422  # Validation error

    def test_update_user_existing(self):
        """Test updating an existing user."""
        # First create a user
        user_data = {
            "name": "Original Name",
            "email": "original@example.com",
            "password": "originalpass"
        }
        create_response = self.client.post("/users", json=user_data)
        user_id = create_response.json()["id"]

        # Update the user
        update_data = {
            "name": "Updated Name",
            "email": "updated@example.com"
        }
        response = self.client.put(f"/users/{user_id}", json=update_data)
        assert response.status_code == 200
        updated_user = response.json()
        assert updated_user["name"] == "Updated Name"
        assert updated_user["email"] == "updated@example.com"
        assert updated_user["password"] == "originalpass"  # Should remain unchanged

    def test_update_user_not_found(self):
        """Test updating a user that doesn't exist."""
        update_data = {
            "name": "Updated Name"
        }
        response = self.client.put("/users/99999", json=update_data)
        assert response.status_code == 404
        assert response.json()["detail"] == "User not found"

    def test_delete_user_existing(self):
        """Test deleting an existing user."""
        # First create a user
        user_data = {
            "name": "To Delete",
            "email": "delete@example.com",
            "password": "password123"
        }
        create_response = self.client.post("/users", json=user_data)
        user_id = create_response.json()["id"]

        # Delete the user
        response = self.client.delete(f"/users/{user_id}")
        assert response.status_code == 200
        assert response.json()["message"] == "User deleted successfully"

        # Verify it's gone
        get_response = self.client.get(f"/users/{user_id}")
        assert get_response.status_code == 404

    def test_delete_user_not_found(self):
        """Test deleting a user that doesn't exist."""
        response = self.client.delete("/users/99999")
        assert response.status_code == 404
        assert response.json()["detail"] == "User not found"


class TestDatabaseIntegration:
    """Integration tests for database operations."""

    def setup_method(self):
        """Set up fresh database for each test."""
        from main import db
        db.products = []
        db.users = []
        db.next_product_id = 1
        db.next_user_id = 1
        db._init_sample_data()
        self.client = httpx.AsyncClient(app=app, base_url="http://test")

    def test_product_crud_operations(self):
        """Test complete CRUD operations for products."""
        # Create
        product_data = {
            "name": "Integration Test Product",
            "description": "Testing full CRUD cycle",
            "price": 99.99,
            "category": "Integration",
            "tags": ["test", "integration"]
        }
        create_response = self.client.post("/products", json=product_data)
        assert create_response.status_code == 200
        product_id = create_response.json()["id"]

        # Read
        get_response = self.client.get(f"/products/{product_id}")
        assert get_response.status_code == 200
        assert get_response.json()["name"] == product_data["name"]

        # Update
        update_data = {"price": 149.99, "category": "Updated"}
        update_response = self.client.put(f"/products/{product_id}", json=update_data)
        assert update_response.status_code == 200
        assert update_response.json()["price"] == 149.99

        # Delete
        delete_response = self.client.delete(f"/products/{product_id}")
        assert delete_response.status_code == 200

        # Verify deletion
        verify_response = self.client.get(f"/products/{product_id}")
        assert verify_response.status_code == 404

    def test_user_crud_operations(self):
        """Test complete CRUD operations for users."""
        # Create
        user_data = {
            "name": "Integration Test User",
            "email": "integration@example.com",
            "password": "securepass123"
        }
        create_response = self.client.post("/users", json=user_data)
        assert create_response.status_code == 200
        user_id = create_response.json()["id"]

        # Read
        get_response = self.client.get(f"/users/{user_id}")
        assert get_response.status_code == 200
        assert get_response.json()["name"] == user_data["name"]

        # Update
        update_data = {"name": "Updated Integration User", "email": "updated@example.com"}
        update_response = self.client.put(f"/users/{user_id}", json=update_data)
        assert update_response.status_code == 200
        assert update_response.json()["name"] == "Updated Integration User"

        # Delete
        delete_response = self.client.delete(f"/users/{user_id}")
        assert delete_response.status_code == 200

        # Verify deletion
        verify_response = self.client.get(f"/users/{user_id}")
        assert verify_response.status_code == 404


if __name__ == "__main__":
    pytest.main([__file__])
