# CRUD Frontend

A React TypeScript frontend for managing Products and Users with full CRUD operations.

## Features

- **Products Management**: Create, read, update, and delete products
- **Users Management**: Create, read, update, and delete users
- **Responsive Design**: Works on desktop and mobile devices
- **Modal Forms**: Clean modal interfaces for creating and editing
- **Real-time Updates**: Immediate UI updates after CRUD operations

## Prerequisites

- Node.js (v14 or higher)
- npm or yarn
- Backend API running on `http://localhost:8000`

## Installation

1. Navigate to the frontend directory:
   ```bash
   cd frontend
   ```

2. Install dependencies:
   ```bash
   npm install
   ```

## Running the Application

1. Start the development server:
   ```bash
   npm start
   ```

2. Open [http://localhost:3000](http://localhost:3000) in your browser

## Project Structure

```
src/
├── components/          # React components
│   ├── ProductList.tsx  # Product listing and management
│   ├── ProductForm.tsx  # Product creation/editing form
│   ├── UserList.tsx     # User listing and management
│   └── UserForm.tsx     # User creation/editing form
├── services/            # API services
│   └── api.ts          # API functions for CRUD operations
├── styles/             # CSS styles
│   └── App.css         # Main stylesheet
├── types/              # TypeScript interfaces
│   └── index.ts        # Type definitions
└── App.tsx             # Main application component
```

## API Integration

The frontend connects to the FastAPI backend at `http://localhost:8000` and provides:

- **Products API**: Full CRUD operations for products
- **Users API**: Full CRUD operations for users

## Available Scripts

- `npm start` - Start development server
- `npm run build` - Build for production
- `npm test` - Run tests
- `npm run eject` - Eject from Create React App

## Technologies Used

- React 18
- TypeScript
- CSS3 (Custom styles)
- Fetch API for HTTP requests
