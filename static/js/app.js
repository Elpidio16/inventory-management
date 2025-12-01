// Tab Management
function showTab(tabName) {
    // Hide all tabs
    const tabs = document.querySelectorAll('.tab-content');
    tabs.forEach(tab => tab.classList.remove('active'));

    // Remove active class from nav links
    const navLinks = document.querySelectorAll('.nav-link');
    navLinks.forEach(link => link.classList.remove('active'));

    // Show selected tab
    const tabElement = document.getElementById(tabName);
    if (tabElement) {
        tabElement.classList.add('active');
    }

    // Add active class to clicked nav link
    event.target.classList.add('active');

    // Load data for specific tabs
    if (tabName === 'dashboard') {
        loadDashboard();
    } else if (tabName === 'products') {
        loadCategoriesForProduct();
    } else if (tabName === 'transaction') {
        loadProductsForTransaction();
        loadRecentTransactions();
    } else if (tabName === 'categories') {
        loadCategories();
    }
}

// Dashboard Functions
function loadDashboard() {
    axios.get('/api/inventory/stats')
        .then(response => {
            const data = response.data;
            document.getElementById('totalProducts').textContent = data.total_products;
            document.getElementById('totalQuantity').textContent = data.total_quantity;
            document.getElementById('totalPrice').textContent = '$' + data.total_price.toFixed(2);
            document.getElementById('totalCategories').textContent = data.categories.length;

            // Build inventory by category table
            let html = '';
            if (data.categories.length === 0) {
                html = '<p class="empty-state">No categories or products found. Create a category and add products to get started.</p>';
            } else {
                data.categories.forEach(category => {
                    html += `
                        <div class="category-section">
                            <h4>${category.name}</h4>
                            <p class="category-meta">${category.product_count} products | ${category.total_quantity} items in stock</p>
                            <table class="table">
                                <thead>
                                    <tr>
                                        <th>Product</th>
                                        <th>Price</th>
                                        <th>Quantity</th>
                                        <th>Value</th>
                                    </tr>
                                </thead>
                                <tbody>
                    `;
                    category.products.forEach(product => {
                        const value = (product.price * product.quantity).toFixed(2);
                        html += `
                            <tr>
                                <td>${product.name}</td>
                                <td>$${product.price.toFixed(2)}</td>
                                <td>${product.quantity}</td>
                                <td>$${value}</td>
                            </tr>
                        `;
                    });
                    html += `
                                </tbody>
                            </table>
                        </div>
                    `;
                });
            }
            document.getElementById('inventoryByCategory').innerHTML = html;
        })
        .catch(error => {
            console.error('Error loading dashboard:', error);
            document.getElementById('inventoryByCategory').innerHTML = '<p class="error">Error loading inventory data</p>';
        });
}

function refreshDashboard() {
    loadDashboard();
    showMessage('Dashboard refreshed!', 'success', 'productMessage');
}

// Product Functions
function loadCategoriesForProduct() {
    axios.get('/api/categories')
        .then(response => {
            const select = document.getElementById('productCategory');
            select.innerHTML = '<option value="">Select a category</option>';
            response.data.forEach(category => {
                select.innerHTML += `<option value="${category.id}">${category.name}</option>`;
            });
        })
        .catch(error => console.error('Error loading categories:', error));
}

function addProduct(event) {
    event.preventDefault();

    const formData = {
        name: document.getElementById('productName').value,
        sku: document.getElementById('productSku').value,
        price: parseFloat(document.getElementById('productPrice').value),
        category_id: document.getElementById('productCategory').value,
        description: document.getElementById('productDescription').value
    };

    axios.post('/api/products', formData)
        .then(response => {
            document.getElementById('productForm').reset();
            showMessage('Product added successfully!', 'success', 'productMessage');
            loadDashboard();
        })
        .catch(error => {
            const message = error.response?.data?.error || 'Error adding product';
            showMessage(message, 'error', 'productMessage');
        });
}

// Transaction Functions
function loadProductsForTransaction() {
    axios.get('/api/products')
        .then(response => {
            const select = document.getElementById('transactionProduct');
            select.innerHTML = '<option value="">Select a product</option>';
            response.data.forEach(product => {
                select.innerHTML += `<option value="${product.id}">${product.name} ($${product.price.toFixed(2)})</option>`;
            });
        })
        .catch(error => console.error('Error loading products:', error));
}

function recordTransaction(event) {
    event.preventDefault();

    const formData = {
        product_id: document.getElementById('transactionProduct').value,
        type: document.getElementById('transactionType').value,
        quantity: parseInt(document.getElementById('transactionQuantity').value),
        reason: document.getElementById('transactionReason').value,
        notes: document.getElementById('transactionNotes').value
    };

    axios.post('/api/transactions', formData)
        .then(response => {
            document.getElementById('transactionForm').reset();
            showMessage(`${formData.type === 'ENTRY' ? 'Entry' : 'Sale'} recorded successfully!`, 'success', 'transactionMessage');
            loadRecentTransactions();
            loadDashboard();
        })
        .catch(error => {
            const message = error.response?.data?.error || 'Error recording transaction';
            showMessage(message, 'error', 'transactionMessage');
        });
}

function loadRecentTransactions() {
    axios.get('/api/transactions')
        .then(response => {
            let html = '';
            if (response.data.length === 0) {
                html = '<p class="empty-state">No transactions recorded yet.</p>';
            } else {
                html = '<table class="table"><thead><tr><th>Date</th><th>Product</th><th>Type</th><th>Quantity</th><th>Reason</th></tr></thead><tbody>';
                response.data.slice(0, 10).forEach(transaction => {
                    const date = new Date(transaction.created_at).toLocaleDateString();
                    html += `
                        <tr>
                            <td>${date}</td>
                            <td>${transaction.product.name}</td>
                            <td><span class="badge ${transaction.type === 'ENTRY' ? 'badge-success' : 'badge-danger'}">${transaction.type}</span></td>
                            <td>${transaction.quantity}</td>
                            <td>${transaction.reason || '-'}</td>
                        </tr>
                    `;
                });
                html += '</tbody></table>';
            }
            document.getElementById('recentTransactions').innerHTML = html;
        })
        .catch(error => {
            console.error('Error loading transactions:', error);
            document.getElementById('recentTransactions').innerHTML = '<p class="error">Error loading transactions</p>';
        });
}

// Category Functions
function loadCategories() {
    axios.get('/api/categories')
        .then(response => {
            let html = '';
            if (response.data.length === 0) {
                html = '<p class="empty-state">No categories created yet. Add one below.</p>';
            } else {
                html = '<div class="categories-grid">';
                response.data.forEach(category => {
                    html += `
                        <div class="category-card">
                            <div class="category-header">
                                <h4>${category.name}</h4>
                                <button class="btn btn-danger" onclick="deleteCategory('${category.id}')">Delete</button>
                            </div>
                            <p class="category-description">${category.description || 'No description'}</p>
                            <p class="category-meta">${category.product_count} products</p>
                        </div>
                    `;
                });
                html += '</div>';
            }
            document.getElementById('categoriesList').innerHTML = html;
        })
        .catch(error => console.error('Error loading categories:', error));
}

function addCategory(event) {
    event.preventDefault();

    const formData = {
        name: document.getElementById('categoryName').value,
        description: document.getElementById('categoryDescription').value
    };

    axios.post('/api/categories', formData)
        .then(response => {
            document.getElementById('categoryForm').reset();
            showMessage('Category added successfully!', 'success', 'categoryMessage');
            loadCategories();
            loadCategoriesForProduct();
        })
        .catch(error => {
            const message = error.response?.data?.error || 'Error adding category';
            showMessage(message, 'error', 'categoryMessage');
        });
}

function deleteCategory(categoryId) {
    if (confirm('Are you sure you want to delete this category?')) {
        axios.delete(`/api/categories/${categoryId}`)
            .then(response => {
                showMessage('Category deleted successfully!', 'success', 'categoryMessage');
                loadCategories();
                loadCategoriesForProduct();
            })
            .catch(error => {
                const message = error.response?.data?.error || 'Error deleting category';
                showMessage(message, 'error', 'categoryMessage');
            });
    }
}

// Utility Functions
function showMessage(message, type, elementId) {
    const element = document.getElementById(elementId);
    element.textContent = message;
    element.className = `message ${type}`;
    element.style.display = 'block';

    setTimeout(() => {
        element.style.display = 'none';
    }, 3000);
}

// Initialize on page load
document.addEventListener('DOMContentLoaded', () => {
    // Set active nav link
    document.querySelector('.nav-link').classList.add('active');
    loadDashboard();
    loadCategoriesForProduct();
});

// Add CSS for badges and categories grid
const style = document.createElement('style');
style.textContent = `
    .badge {
        display: inline-block;
        padding: 0.25rem 0.75rem;
        border-radius: 9999px;
        font-size: 0.875rem;
        font-weight: 600;
    }
    
    .badge-success {
        background-color: #dcfce7;
        color: #166534;
    }
    
    .badge-danger {
        background-color: #fee2e2;
        color: #991b1b;
    }
    
    .categories-grid {
        display: grid;
        grid-template-columns: repeat(auto-fill, minmax(300px, 1fr));
        gap: 1.5rem;
    }
    
    .category-card {
        background: white;
        border: 1px solid var(--border-color);
        border-radius: 0.5rem;
        padding: 1.5rem;
        transition: transform 0.3s, box-shadow 0.3s;
    }
    
    .category-card:hover {
        transform: translateY(-4px);
        box-shadow: var(--shadow-lg);
    }
    
    .category-header {
        display: flex;
        justify-content: space-between;
        align-items: center;
        margin-bottom: 1rem;
    }
    
    .category-header h4 {
        margin: 0;
        color: var(--text-primary);
    }
    
    .category-description {
        color: var(--text-secondary);
        margin: 0.5rem 0;
        font-size: 0.875rem;
    }
    
    .category-meta {
        color: var(--primary-color);
        font-weight: 600;
        margin: 0;
        font-size: 0.875rem;
    }
    
    .category-section {
        margin-bottom: 2rem;
        padding-bottom: 1.5rem;
        border-bottom: 1px solid var(--border-color);
    }
    
    .category-section:last-child {
        border-bottom: none;
    }
    
    .category-section h4 {
        font-size: 1.1rem;
        margin-bottom: 0.5rem;
        color: var(--primary-color);
    }
`;
document.head.appendChild(style);
