import React, { useState, useEffect } from 'react';
import { User } from '../types';
import { userApi } from '../services/api';
import UserForm from './UserForm';

const UserList: React.FC = () => {
  const [users, setUsers] = useState<User[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);
  const [showForm, setShowForm] = useState(false);
  const [editingUser, setEditingUser] = useState<User | null>(null);

  useEffect(() => {
    loadUsers();
  }, []);

  const loadUsers = async () => {
    try {
      setLoading(true);
      const data = await userApi.getAll();
      setUsers(data);
      setError(null);
    } catch (err) {
      setError('Failed to load users');
      console.error(err);
    } finally {
      setLoading(false);
    }
  };

  const handleDelete = async (id: number) => {
    if (window.confirm('Are you sure you want to delete this user?')) {
      try {
        await userApi.delete(id);
        setUsers(users.filter(user => user.id !== id));
      } catch (err) {
        setError('Failed to delete user');
        console.error(err);
      }
    }
  };

  const handleEdit = (user: User) => {
    setEditingUser(user);
    setShowForm(true);
  };

  const handleFormClose = () => {
    setShowForm(false);
    setEditingUser(null);
  };

  const handleFormSubmit = async (userData: any) => {
    try {
      if (editingUser) {
        const updatedUser = await userApi.update(editingUser.id, userData);
        setUsers(users.map(u => u.id === editingUser.id ? updatedUser : u));
      } else {
        const newUser = await userApi.create(userData);
        setUsers([...users, newUser]);
      }
      handleFormClose();
    } catch (err) {
      setError('Failed to save user');
      console.error(err);
    }
  };

  const formatDate = (dateString: string) => {
    return new Date(dateString).toLocaleDateString();
  };

  if (loading) {
    return <div className="text-center">Loading users...</div>;
  }

  return (
    <div className="card">
      <div className="section-header">
        <h2 className="section-title">Users</h2>
        <button 
          className="btn btn-primary" 
          onClick={() => setShowForm(true)}
        >
          Add User
        </button>
      </div>

      {error && (
        <div className="alert alert-danger mb-3">
          {error}
        </div>
      )}

      {users.length === 0 ? (
        <div className="text-center">
          <p>No users found. Create your first user!</p>
        </div>
      ) : (
        <table className="table">
          <thead>
            <tr>
              <th>Name</th>
              <th>Email</th>
              <th>Created</th>
              <th>Updated</th>
              <th>Actions</th>
            </tr>
          </thead>
          <tbody>
            {users.map((user) => (
              <tr key={user.id}>
                <td>{user.name}</td>
                <td>{user.email}</td>
                <td>{formatDate(user.created_at)}</td>
                <td>{formatDate(user.updated_at)}</td>
                <td>
                  <div className="d-flex gap-2">
                    <button
                      className="btn btn-secondary btn-sm"
                      onClick={() => handleEdit(user)}
                    >
                      Edit
                    </button>
                    <button
                      className="btn btn-danger btn-sm"
                      onClick={() => handleDelete(user.id)}
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
        <UserForm
          user={editingUser}
          onSubmit={handleFormSubmit}
          onClose={handleFormClose}
        />
      )}
    </div>
  );
};

export default UserList;
