# Product CRUD API

A simple FastAPI-based REST API for managing products with full CRUD operations.

## Features

- **Create** new products
- **Read** all products or get a specific product by ID
- **Update** existing products
- **Delete** products
- In-memory database with sample data
- Automatic API documentation with Swagger UI
- Health check endpoint

## Tech Stack

- **FastAPI** - Modern, fast web framework for building APIs
- **Pydantic** - Data validation using Python type annotations
- **Uvicorn** - ASGI server for running FastAPI applications

## Installation

1. Clone the repository:
```bash
git clone <your-repo-url>
cd crud-endpoint-stub
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

## Running the Application

Start the development server:
```bash
python main.py
```

The API will be available at:
- **API Base URL**: http://localhost:8000
- **Interactive Documentation**: http://localhost:8000/docs
- **Alternative Documentation**: http://localhost:8000/redoc

## API Endpoints

### Health Check
- `GET /health` - Check API health status

### Products
- `GET /products` - Get all products
- `POST /products` - Create a new product
- `PUT /products/{product_id}` - Update an existing product
- `DELETE /products/{product_id}` - Delete a product

## Product Model

```json
{
  "id": 1,
  "name": "Product Name",
  "description": "Product description",
  "price": 99.99,
  "category": "Electronics",
  "tags": ["tag1", "tag2"],
  "in_stock": true,
  "created_at": "2024-01-01T00:00:00"
}
```

## Sample Data

The application comes with sample products pre-loaded:
- Wireless Headphones
- Coffee Maker
- Laptop Stand

## Development

This project uses an in-memory database for simplicity. In a production environment, you would want to replace the `InMemoryDatabase` class with a proper database connection (e.g., PostgreSQL, MySQL, or MongoDB).

## License

MIT License
