export interface Product {
  id: number;
  name: string;
  description: string;
  price: number;
  category: string;
  tags: string[];
  in_stock: boolean;
  created_at: string;
}

export interface ProductCreate {
  name: string;
  description: string;
  price: number;
  category: string;
  tags: string[];
  in_stock: boolean;
}

export interface ProductUpdate {
  name?: string;
  description?: string;
  price?: number;
  category?: string;
  tags?: string[];
  in_stock?: boolean;
}

export interface User {
  id: number;
  name: string;
  email: string;
  password: string;
  created_at: string;
  updated_at: string;
}

export interface UserCreate {
  name: string;
  email: string;
  password: string;
}

export interface UserUpdate {
  name?: string;
  email?: string;
  password?: string;
  updated_at: string;
}
