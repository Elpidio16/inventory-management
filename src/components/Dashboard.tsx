'use client';

import React, { useEffect, useState } from 'react';
import axios from 'axios';

interface InventoryStats {
  totalProducts: number;
  totalQuantity: number;
  totalPrice: number;
  categories: Array<{
    id: string;
    name: string;
    description?: string;
    productCount: number;
    totalQuantity: number;
    products: Array<{
      id: string;
      name: string;
      price: number;
      quantity: number;
    }>;
  }>;
}

export default function Dashboard() {
  const [stats, setStats] = useState<InventoryStats | null>(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState('');

  useEffect(() => {
    fetchStats();
  }, []);

  const fetchStats = async () => {
    try {
      setLoading(true);
      const response = await axios.get('/api/inventory/stats');
      setStats(response.data);
    } catch (err) {
      setError('Failed to load inventory statistics');
      console.error(err);
    } finally {
      setLoading(false);
    }
  };

  if (loading) {
    return <div className="p-8 text-center">Loading inventory...</div>;
  }

  if (error) {
    return <div className="p-8 text-center text-red-600">{error}</div>;
  }

  return (
    <div className="min-h-screen bg-gray-50 p-8">
      <div className="max-w-7xl mx-auto">
        <h1 className="text-4xl font-bold mb-8 text-gray-900">Inventory Dashboard</h1>

        {/* Summary Cards */}
        <div className="grid grid-cols-1 md:grid-cols-3 gap-6 mb-8">
          <div className="bg-white rounded-lg shadow p-6">
            <h2 className="text-sm font-medium text-gray-500 mb-2">Total Products</h2>
            <p className="text-3xl font-bold text-blue-600">{stats?.totalProducts}</p>
          </div>
          <div className="bg-white rounded-lg shadow p-6">
            <h2 className="text-sm font-medium text-gray-500 mb-2">Total Inventory</h2>
            <p className="text-3xl font-bold text-green-600">{stats?.totalQuantity}</p>
          </div>
          <div className="bg-white rounded-lg shadow p-6">
            <h2 className="text-sm font-medium text-gray-500 mb-2">Total Inventory Value</h2>
            <p className="text-3xl font-bold text-purple-600">
              ${stats?.totalPrice.toFixed(2)}
            </p>
          </div>
        </div>

        {/* Categories Section */}
        <div className="bg-white rounded-lg shadow overflow-hidden">
          <div className="px-6 py-4 border-b border-gray-200">
            <h2 className="text-2xl font-bold text-gray-900">Categories</h2>
          </div>

          {stats?.categories.map((category) => (
            <div key={category.id} className="border-b border-gray-200 last:border-b-0">
              <div className="px-6 py-4 bg-gray-50">
                <h3 className="text-lg font-semibold text-gray-900">{category.name}</h3>
                <p className="text-sm text-gray-600 mt-1">
                  {category.productCount} products | {category.totalQuantity} items in stock
                </p>
              </div>

              <div className="px-6 py-4">
                <table className="w-full">
                  <thead className="bg-gray-50 border-b">
                    <tr>
                      <th className="text-left py-3 px-4 text-sm font-semibold text-gray-900">Product</th>
                      <th className="text-left py-3 px-4 text-sm font-semibold text-gray-900">Price</th>
                      <th className="text-left py-3 px-4 text-sm font-semibold text-gray-900">Quantity</th>
                      <th className="text-left py-3 px-4 text-sm font-semibold text-gray-900">Value</th>
                    </tr>
                  </thead>
                  <tbody>
                    {category.products.map((product) => (
                      <tr key={product.id} className="border-b hover:bg-gray-50">
                        <td className="py-3 px-4 text-gray-900">{product.name}</td>
                        <td className="py-3 px-4 text-gray-900">${product.price.toFixed(2)}</td>
                        <td className="py-3 px-4 text-gray-900">{product.quantity}</td>
                        <td className="py-3 px-4 text-gray-900">
                          ${(product.price * product.quantity).toFixed(2)}
                        </td>
                      </tr>
                    ))}
                  </tbody>
                </table>
              </div>
            </div>
          ))}
        </div>
      </div>
    </div>
  );
}
