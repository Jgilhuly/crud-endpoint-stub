import React, { useState, useEffect } from 'react';
import { User, UserCreate } from '../types';

interface UserFormProps {
  user?: User | null;
  onSubmit: (data: UserCreate) => void;
  onClose: () => void;
}

const UserForm: React.FC<UserFormProps> = ({ user, onSubmit, onClose }) => {
  const [formData, setFormData] = useState<UserCreate>({
    name: '',
    email: '',
    password: '',
  });

  useEffect(() => {
    if (user) {
      setFormData({
        name: user.name,
        email: user.email,
        password: '', // Don't populate password for security
      });
    }
  }, [user]);

  const handleInputChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    const { name, value } = e.target;
    setFormData(prev => ({ ...prev, [name]: value }));
  };

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    if (formData.name.trim() && formData.email.trim() && formData.password.trim()) {
      onSubmit(formData);
    }
  };

  return (
    <div className="modal-overlay" onClick={onClose}>
      <div className="modal" onClick={(e) => e.stopPropagation()}>
        <div className="modal-header">
          <h3 className="modal-title">
            {user ? 'Edit User' : 'Add New User'}
          </h3>
          <button className="modal-close" onClick={onClose}>
            ×
          </button>
        </div>

        <form onSubmit={handleSubmit}>
          <div className="form-group">
            <label className="form-label" htmlFor="name">
              Name *
            </label>
            <input
              type="text"
              id="name"
              name="name"
              className="form-input"
              value={formData.name}
              onChange={handleInputChange}
              required
            />
          </div>

          <div className="form-group">
            <label className="form-label" htmlFor="email">
              Email *
            </label>
            <input
              type="email"
              id="email"
              name="email"
              className="form-input"
              value={formData.email}
              onChange={handleInputChange}
              required
            />
          </div>

          <div className="form-group">
            <label className="form-label" htmlFor="password">
              Password *
            </label>
            <input
              type="password"
              id="password"
              name="password"
              className="form-input"
              value={formData.password}
              onChange={handleInputChange}
              required
              placeholder={user ? "Enter new password to update" : "Enter password"}
            />
          </div>

          <div className="d-flex gap-2 justify-between">
            <button type="button" className="btn btn-secondary" onClick={onClose}>
              Cancel
            </button>
            <button type="submit" className="btn btn-primary">
              {user ? 'Update User' : 'Create User'}
            </button>
          </div>
        </form>
      </div>
    </div>
  );
};

export default UserForm;
