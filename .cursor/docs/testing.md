# Testing Documentation

This document describes the testing setup for the CRUD API application.

## Test Structure

The application includes comprehensive unit tests for all API endpoints:

### Test Files
- `test_main.py` - Main test file containing all endpoint tests

### Test Classes
- `TestProductEndpoints` - Tests for product-related endpoints
- `TestUserEndpoints` - Tests for user-related endpoints  
- `TestDatabaseIntegration` - Integration tests for complete CRUD operations

## Running Tests

### Install Dependencies
```bash
pip install -r requirements.txt
```

### Run All Tests
```bash
pytest
```

### Run Specific Test Classes
```bash
# Run only product tests
pytest test_main.py::TestProductEndpoints

# Run only user tests
pytest test_main.py::TestUserEndpoints

# Run only integration tests
pytest test_main.py::TestDatabaseIntegration
```

### Run Specific Test Methods
```bash
# Run a specific test
pytest test_main.py::TestProductEndpoints::test_create_product

# Run tests matching a pattern
pytest -k "create"
```

### Verbose Output
```bash
pytest -v
```

### Coverage Report (if pytest-cov is installed)
```bash
pytest --cov=main --cov-report=html
```

## Test Coverage

The tests cover:

### Product Endpoints
- ✅ GET `/` - Root endpoint
- ✅ GET `/health` - Health check
- ✅ GET `/products` - List all products
- ✅ GET `/products/{id}` - Get specific product
- ✅ POST `/products` - Create new product
- ✅ PUT `/products/{id}` - Update existing product
- ✅ DELETE `/products/{id}` - Delete product

### User Endpoints
- ✅ GET `/users` - List all users
- ✅ GET `/users/{id}` - Get specific user
- ✅ POST `/users` - Create new user
- ✅ PUT `/users/{id}` - Update existing user
- ✅ DELETE `/users/{id}` - Delete user

### Test Scenarios
- ✅ Happy path scenarios
- ✅ Error handling (404, 422 validation errors)
- ✅ Missing required fields
- ✅ Non-existent resources
- ✅ Complete CRUD cycles

## Test Database

Tests use a fresh in-memory database instance for each test method to ensure isolation. The database is reset in the `setup_method` of each test class.

## Dependencies

Testing dependencies are included in `requirements.txt`:
- `pytest` - Test framework
- `httpx` - HTTP client for testing FastAPI
- `pytest-asyncio` - Async test support

## Best Practices

1. **Test Isolation**: Each test uses a fresh database state
2. **Descriptive Names**: Test methods have clear, descriptive names
3. **Comprehensive Coverage**: Tests cover both success and error scenarios
4. **Documentation**: Each test method includes docstrings explaining its purpose
5. **Assertions**: Tests include multiple assertions to verify complete functionality
