'use client';

import { useState } from 'react';
import Dashboard from '@/components/Dashboard';
import ProductForm from '@/components/ProductForm';
import TransactionForm from '@/components/TransactionForm';

export default function Home() {
  const [activeTab, setActiveTab] = useState('dashboard');
  const [refreshKey, setRefreshKey] = useState(0);

  const handleTransactionComplete = () => {
    setRefreshKey(prev => prev + 1);
  };

  return (
    <main className="min-h-screen bg-gray-100 p-8">
      <div className="max-w-7xl mx-auto">
        {/* Navigation Tabs */}
        <div className="flex gap-4 mb-8 bg-white rounded-lg shadow p-1">
          <button
            onClick={() => setActiveTab('dashboard')}
            className={`px-6 py-2 rounded font-medium transition ${
              activeTab === 'dashboard'
                ? 'bg-blue-600 text-white'
                : 'text-gray-700 hover:bg-gray-100'
            }`}
          >
            📊 Dashboard
          </button>
          <button
            onClick={() => setActiveTab('product')}
            className={`px-6 py-2 rounded font-medium transition ${
              activeTab === 'product'
                ? 'bg-blue-600 text-white'
                : 'text-gray-700 hover:bg-gray-100'
            }`}
          >
            ➕ Add Product
          </button>
          <button
            onClick={() => setActiveTab('transaction')}
            className={`px-6 py-2 rounded font-medium transition ${
              activeTab === 'transaction'
                ? 'bg-blue-600 text-white'
                : 'text-gray-700 hover:bg-gray-100'
            }`}
          >
            🔄 Record Transaction
          </button>
        </div>

        {/* Content */}
        <div key={refreshKey}>
          {activeTab === 'dashboard' && <Dashboard />}
          {activeTab === 'product' && <ProductForm />}
          {activeTab === 'transaction' && (
            <TransactionForm onTransactionComplete={handleTransactionComplete} />
          )}
        </div>
      </div>
    </main>
  );
}
