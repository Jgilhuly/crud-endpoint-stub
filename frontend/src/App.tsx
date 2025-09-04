import React, { useState } from 'react';
import './styles/App.css';
import ProductList from './components/ProductList';
import UserList from './components/UserList';
import ThemeToggle from './components/ThemeToggle';

type TabType = 'products' | 'users';

function App() {
  const [activeTab, setActiveTab] = useState<TabType>('products');

  return (
    <div className="App">
      <nav className="nav">
        <div className="nav-container">
          <h1 className="nav-title">CRUD Management System</h1>
          <div className="nav-controls">
            <div className="nav-tabs">
              <button
                className={`nav-tab ${activeTab === 'products' ? 'active' : ''}`}
                onClick={() => setActiveTab('products')}
              >
                Products
              </button>
              <button
                className={`nav-tab ${activeTab === 'users' ? 'active' : ''}`}
                onClick={() => setActiveTab('users')}
              >
                Users
              </button>
            </div>
            <ThemeToggle />
          </div>
        </div>
      </nav>

      <div className="container">
        {activeTab === 'products' ? <ProductList /> : <UserList />}
      </div>
    </div>
  );
}

export default App;
