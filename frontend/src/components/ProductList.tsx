import React, { useState, useEffect } from 'react';
import { Product } from '../types';
import { productApi } from '../services/api';
import ProductForm from './ProductForm';

const ProductList: React.FC = () => {
  const [products, setProducts] = useState<Product[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);
  const [showForm, setShowForm] = useState(false);
  const [editingProduct, setEditingProduct] = useState<Product | null>(null);

  useEffect(() => {
    loadProducts();
  }, []);

  const loadProducts = async () => {
    try {
      setLoading(true);
      const data = await productApi.getAll();
      setProducts(data);
      setError(null);
    } catch (err) {
      setError('Failed to load products');
      console.error(err);
    } finally {
      setLoading(false);
    }
  };

  const handleDelete = async (id: number) => {
    if (window.confirm('Are you sure you want to delete this product?')) {
      try {
        await productApi.delete(id);
        setProducts(products.filter(product => product.id !== id));
      } catch (err) {
        setError('Failed to delete product');
        console.error(err);
      }
    }
  };

  const handleEdit = (product: Product) => {
    setEditingProduct(product);
    setShowForm(true);
  };

  const handleFormClose = () => {
    setShowForm(false);
    setEditingProduct(null);
  };

  const handleFormSubmit = async (productData: any) => {
    try {
      if (editingProduct) {
        const updatedProduct = await productApi.update(editingProduct.id, productData);
        setProducts(products.map(p => p.id === editingProduct.id ? updatedProduct : p));
      } else {
        const newProduct = await productApi.create(productData);
        setProducts([...products, newProduct]);
      }
      handleFormClose();
    } catch (err) {
      setError('Failed to save product');
      console.error(err);
    }
  };

  const formatDate = (dateString: string) => {
    return new Date(dateString).toLocaleDateString();
  };

  if (loading) {
    return <div className="text-center">Loading products...</div>;
  }

  return (
    <div className="card">
      <div className="section-header">
        <h2 className="section-title">Products</h2>
        <button 
          className="btn btn-primary" 
          onClick={() => setShowForm(true)}
        >
          Add Product
        </button>
      </div>

      {error && (
        <div className="alert alert-danger mb-3">
          {error}
        </div>
      )}

      {products.length === 0 ? (
        <div className="text-center">
          <p>No products found. Create your first product!</p>
        </div>
      ) : (
        <table className="table">
          <thead>
            <tr>
              <th>Name</th>
              <th>Description</th>
              <th>Price</th>
              <th>Category</th>
              <th>Tags</th>
              <th>Stock</th>
              <th>Created</th>
              <th>Actions</th>
            </tr>
          </thead>
          <tbody>
            {products.map((product) => (
              <tr key={product.id}>
                <td>{product.name}</td>
                <td>{product.description}</td>
                <td>${product.price.toFixed(2)}</td>
                <td>{product.category}</td>
                <td>
                  <div className="tags">
                    {product.tags.map((tag, index) => (
                      <span key={index} className="tag">{tag}</span>
                    ))}
                  </div>
                </td>
                <td>
                  <span className={`status-badge ${product.in_stock ? 'status-in-stock' : 'status-out-of-stock'}`}>
                    {product.in_stock ? 'In Stock' : 'Out of Stock'}
                  </span>
                </td>
                <td>{formatDate(product.created_at)}</td>
                <td>
                  <div className="d-flex gap-2">
                    <button
                      className="btn btn-secondary btn-sm"
                      onClick={() => handleEdit(product)}
                    >
                      Edit
                    </button>
                    <button
                      className="btn btn-danger btn-sm"
                      onClick={() => handleDelete(product.id)}
                    >
                      Delete
                    </button>
                  </div>
                </td>
              </tr>
            ))}
          </tbody>
        </table>
      )}

      {showForm && (
        <ProductForm
          product={editingProduct}
          onSubmit={handleFormSubmit}
          onClose={handleFormClose}
        />
      )}
    </div>
  );
};

export default ProductList;
