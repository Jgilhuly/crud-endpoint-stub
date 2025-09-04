"""FastAPI application for Product CRUD operations."""
from typing import List
import uvicorn

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware

from models import Product, ProductCreate, ProductUpdate, User, UserCreate, UserUpdate
from database import db

app = FastAPI(
    title="Product CRUD API",
    description="A simple CRUD API for managing products",
    version="1.0.0"
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],  # React dev server
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/")
def read_root():
    """Root endpoint returning welcome message."""
    return {"message": "Welcome to the Product CRUD API"}


@app.get("/health")
def health_check():
    """Health check endpoint."""
    return {"status": "healthy"}


@app.get("/products", response_model=List[Product])
def get_products():
    """Get all products"""
    return db.get_all_products()


@app.post("/products", response_model=Product)
def create_product(product: ProductCreate):
    """Create a new product"""
    # TODO: Add validation logic here
    return db.create_product(product)


@app.put("/products/{product_id}", response_model=Product)
def update_product(product_id: int, product_update: ProductUpdate):
    """Update an existing product"""
    # TODO: Add validation and error handling
    updated_product = db.update_product(product_id, product_update)
    if not updated_product:
        raise HTTPException(status_code=404, detail="Product not found")
    return updated_product



@app.delete("/products/{product_id}")
def delete_product(product_id: int):
    """Delete a product"""
    # TODO: Add proper response handling
    success = db.delete_product(product_id)
    if not success:
        raise HTTPException(status_code=404, detail="Product not found")
    return {"message": "Product deleted successfully"}

@app.post("/users", response_model=User)
def create_user(user: UserCreate):
    """Create a new user"""
    return db.create_user(user)

@app.delete("/users/{user_id}")
def delete_user(user_id: int):
    """Delete a user"""
    return db.delete_user(user_id)

@app.get("/users", response_model=List[User])
def get_users():
    """Get all users"""
    return db.get_all_users()


@app.get("/users/{user_id}", response_model=User)
def get_user(user_id: int):
    """Get a user by ID"""
    user = db.get_user(user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user


@app.put("/users/{user_id}", response_model=User)
def update_user(user_id: int, user_update: UserUpdate):
    """Update an existing user"""
    updated_user = db.update_user(user_id, user_update)
    if not updated_user:
        raise HTTPException(status_code=404, detail="User not found")
    return updated_user


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
