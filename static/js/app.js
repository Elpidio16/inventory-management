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
    } else if (tabName === 'manage-products') {
        loadProductsList();
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
            document.getElementById('totalPrice').textContent = data.total_price.toFixed(2) + ' FCFA';
            document.getElementById('totalCategories').textContent = data.categories.length;

            // Build inventory by category table
            let html = '';
            if (data.categories.length === 0) {
                html = '<p class="empty-state">Aucune catégorie ou produit trouvés. Créez une catégorie et ajoutez des produits pour commencer.</p>';
            } else {
                data.categories.forEach(category => {
                    html += `
                        <div class="category-section">
                            <h4>${category.name}</h4>
                            <p class="category-meta">${category.product_count} produits | ${category.total_quantity} articles en stock</p>
                            <table class="table">
                                <thead>
                                    <tr>
                                        <th>Produit</th>
                                        <th>Prix (FCFA)</th>
                                        <th>Quantité</th>
                                        <th>Valeur</th>
                                    </tr>
                                </thead>
                                <tbody>
                    `;
                    category.products.forEach(product => {
                        const value = (product.price * product.quantity).toFixed(2);
                        html += `
                            <tr>
                                <td>${product.name}</td>
                                <td>${product.price.toFixed(2)} FCFA</td>
                                <td>${product.quantity}</td>
                                <td>${value} FCFA</td>
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
            console.error('Erreur lors du chargement du tableau de bord:', error);
            document.getElementById('inventoryByCategory').innerHTML = '<p class="error">Erreur lors du chargement des données de stock</p>';
        });
}

function refreshDashboard() {
    loadDashboard();
    showMessage('Tableau de bord rafraîchi !', 'success', 'productMessage');
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
            showMessage('Produit ajouté avec succès !', 'success', 'productMessage');
            loadDashboard();
        })
        .catch(error => {
            const message = error.response?.data?.error || 'Erreur lors de l\'ajout du produit';
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
                select.innerHTML += `<option value="${product.id}">${product.name} (${product.price.toFixed(2)} FCFA)</option>`;
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
            showMessage(`${formData.type === 'ENTRY' ? 'Entrée' : 'Sortie'} enregistrée avec succès !`, 'success', 'transactionMessage');
            loadRecentTransactions();
            loadDashboard();
        })
        .catch(error => {
            const message = error.response?.data?.error || 'Erreur lors de l\'enregistrement de la transaction';
            showMessage(message, 'error', 'transactionMessage');
        });
}

function loadRecentTransactions() {
    axios.get('/api/transactions')
        .then(response => {
            let html = '';
            if (response.data.length === 0) {
                html = '<p class="empty-state">Aucune transaction enregistrée.</p>';
            } else {
                html = '<table class="table"><thead><tr><th>Date</th><th>Produit</th><th>Type</th><th>Quantité</th><th>Raison</th></tr></thead><tbody>';
                response.data.slice(0, 10).forEach(transaction => {
                    const date = new Date(transaction.created_at).toLocaleDateString('fr-FR');
                    html += `
                        <tr>
                            <td>${date}</td>
                            <td>${transaction.product.name}</td>
                            <td><span class="badge ${transaction.type === 'ENTRY' ? 'badge-success' : 'badge-danger'}">${transaction.type === 'ENTRY' ? 'Entrée' : 'Sortie'}</span></td>
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
            console.error('Erreur lors du chargement des transactions:', error);
            document.getElementById('recentTransactions').innerHTML = '<p class="error">Erreur lors du chargement des transactions</p>';
        });
}

// Category Functions
function loadCategories() {
    axios.get('/api/categories')
        .then(response => {
            let html = '';
            if (response.data.length === 0) {
                html = '<p class="empty-state">Aucune catégorie créée. Ajoutez-en une ci-dessous.</p>';
            } else {
                html = '<div class="categories-grid">';
                response.data.forEach(category => {
                    html += `
                        <div class="category-card">
                            <div class="category-header">
                                <h4>${category.name}</h4>
                                <button class="btn btn-danger" onclick="deleteCategory('${category.id}')">Supprimer</button>
                            </div>
                            <p class="category-description">${category.description || 'Aucune description'}</p>
                            <p class="category-meta">${category.product_count} produits</p>
                        </div>
                    `;
                });
                html += '</div>';
            }
            document.getElementById('categoriesList').innerHTML = html;
        })
        .catch(error => console.error('Erreur lors du chargement des catégories:', error));
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
            showMessage('Catégorie ajoutée avec succès !', 'success', 'categoryMessage');
            loadCategories();
            loadCategoriesForProduct();
        })
        .catch(error => {
            const message = error.response?.data?.error || 'Erreur lors de l\'ajout de la catégorie';
            showMessage(message, 'error', 'categoryMessage');
        });
}

function deleteCategory(categoryId) {
    if (confirm('Êtes-vous sûr de vouloir supprimer cette catégorie ?')) {
        axios.delete(`/api/categories/${categoryId}`)
            .then(response => {
                showMessage('Catégorie supprimée avec succès !', 'success', 'categoryMessage');
                loadCategories();
                loadCategoriesForProduct();
            })
            .catch(error => {
                const message = error.response?.data?.error || 'Erreur lors de la suppression de la catégorie';
                showMessage(message, 'error', 'categoryMessage');
            });
    }
}

function loadProductsList() {
    axios.get('/api/products')
        .then(response => {
            let html = '';
            if (response.data.length === 0) {
                html = '<p class="empty-state">Aucun produit créé. Ajoutez-en un dans l\'onglet "Ajouter un produit".</p>';
            } else {
                html = '<div class="products-grid">';
                response.data.forEach(product => {
                    const quantity = product.inventory?.quantity || 0;
                    const totalValue = (product.price * quantity).toFixed(2);
                    html += `
                        <div class="product-card">
                            <div class="product-header">
                                <h4>${product.name}</h4>
                                <button class="btn btn-danger" onclick="deleteProduct('${product.id}')">Supprimer</button>
                            </div>
                            <p class="product-info"><strong>Code :</strong> ${product.sku}</p>
                            <p class="product-info"><strong>Prix :</strong> ${product.price.toFixed(2)} FCFA</p>
                            <p class="product-info"><strong>Stock :</strong> ${quantity} unités</p>
                            <p class="product-info"><strong>Valeur :</strong> ${totalValue} FCFA</p>
                            <p class="product-description">${product.description || 'Aucune description'}</p>
                        </div>
                    `;
                });
                html += '</div>';
            }
            document.getElementById('productsList').innerHTML = html;
        })
        .catch(error => console.error('Erreur lors du chargement des produits:', error));
}

function deleteProduct(productId) {
    if (confirm('Êtes-vous sûr de vouloir supprimer ce produit ? Cela supprimera également toutes ses transactions.')) {
        axios.delete(`/api/products/${productId}`)
            .then(response => {
                showMessage('Produit supprimé avec succès !', 'success', 'productMessage');
                loadProductsList();
                loadProductsForTransaction();
            })
            .catch(error => {
                const message = error.response?.data?.error || 'Erreur lors de la suppression du produit';
                showMessage(message, 'error', 'productMessage');
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
