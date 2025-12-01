import json
import os
from datetime import datetime
import uuid
from pathlib import Path

# Data file path - use /tmp for Vercel, local for development
DATA_DIR = Path(os.environ.get('DATA_DIR', '.')) / 'data'
DATA_DIR.mkdir(exist_ok=True)
DATA_FILE = DATA_DIR / 'inventory.json'

def init_data():
    """Initialize data file with empty structure"""
    if not DATA_FILE.exists():
        initial_data = {
            'categories': [],
            'products': [],
            'inventory': {},
            'transactions': []
        }
        save_data(initial_data)
    return load_data()

def load_data():
    """Load data from JSON file"""
    try:
        if DATA_FILE.exists():
            with open(DATA_FILE, 'r', encoding='utf-8') as f:
                return json.load(f)
        else:
            return {
                'categories': [],
                'products': [],
                'inventory': {},
                'transactions': []
            }
    except Exception as e:
        print(f"Error loading data: {e}")
        return {
            'categories': [],
            'products': [],
            'inventory': {},
            'transactions': []
        }

def save_data(data):
    """Save data to JSON file"""
    try:
        with open(DATA_FILE, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=2, ensure_ascii=False)
        return True
    except Exception as e:
        print(f"Error saving data: {e}")
        return False

def get_all_data():
    """Get all data"""
    return load_data()

def add_category(name, description=''):
    """Add a new category"""
    data = load_data()
    
    # Check if category exists
    if any(cat['name'] == name for cat in data['categories']):
        return None, 'Category already exists'
    
    category = {
        'id': str(uuid.uuid4()),
        'name': name,
        'description': description,
        'created_at': datetime.utcnow().isoformat(),
        'updated_at': datetime.utcnow().isoformat()
    }
    
    data['categories'].append(category)
    save_data(data)
    return category, None

def get_categories():
    """Get all categories"""
    data = load_data()
    return data['categories']

def delete_category(category_id):
    """Delete a category"""
    data = load_data()
    
    # Check if category has products
    if any(p['category_id'] == category_id for p in data['products']):
        return False, 'Cannot delete category with existing products'
    
    data['categories'] = [c for c in data['categories'] if c['id'] != category_id]
    save_data(data)
    return True, None

def add_product(name, sku, price, category_id, description=''):
    """Add a new product"""
    data = load_data()
    
    # Check if SKU exists
    if any(p['sku'] == sku for p in data['products']):
        return None, 'Product with this Product Code already exists'
    
    # Check if category exists
    if not any(c['id'] == category_id for c in data['categories']):
        return None, 'Category not found'
    
    product_id = str(uuid.uuid4())
    product = {
        'id': product_id,
        'name': name,
        'description': description,
        'sku': sku,
        'price': float(price),
        'category_id': category_id,
        'created_at': datetime.utcnow().isoformat(),
        'updated_at': datetime.utcnow().isoformat()
    }
    
    data['products'].append(product)
    
    # Create inventory record
    data['inventory'][product_id] = {
        'id': str(uuid.uuid4()),
        'product_id': product_id,
        'quantity': 0,
        'last_updated': datetime.utcnow().isoformat()
    }
    
    save_data(data)
    product['inventory'] = data['inventory'][product_id]
    return product, None

def get_products():
    """Get all products with inventory"""
    data = load_data()
    products = []
    for p in data['products']:
        product = p.copy()
        product['inventory'] = data['inventory'].get(p['id'], {'quantity': 0})
        products.append(product)
    return products

def delete_product(product_id):
    """Delete a product"""
    data = load_data()
    
    # Delete product transactions
    data['transactions'] = [t for t in data['transactions'] if t['product_id'] != product_id]
    
    # Delete product inventory
    if product_id in data['inventory']:
        del data['inventory'][product_id]
    
    # Delete product
    data['products'] = [p for p in data['products'] if p['id'] != product_id]
    
    save_data(data)
    return True, None

def add_transaction(product_id, transaction_type, quantity, reason='', notes=''):
    """Add a new transaction"""
    data = load_data()
    
    # Check if product exists
    if not any(p['id'] == product_id for p in data['products']):
        return None, 'Product not found'
    
    # Validate transaction type
    if transaction_type not in ['ENTRY', 'EXIT']:
        return None, 'Invalid transaction type'
    
    # Validate quantity
    if quantity <= 0:
        return None, 'Quantity must be greater than 0'
    
    # Check inventory for EXIT
    current_qty = data['inventory'][product_id]['quantity']
    if transaction_type == 'EXIT' and current_qty < quantity:
        return None, f'Insufficient inventory. Available: {current_qty}'
    
    transaction = {
        'id': str(uuid.uuid4()),
        'product_id': product_id,
        'type': transaction_type,
        'quantity': quantity,
        'reason': reason,
        'notes': notes,
        'created_at': datetime.utcnow().isoformat(),
        'updated_at': datetime.utcnow().isoformat()
    }
    
    # Update inventory
    if transaction_type == 'ENTRY':
        data['inventory'][product_id]['quantity'] += quantity
    else:
        data['inventory'][product_id]['quantity'] -= quantity
    
    data['inventory'][product_id]['last_updated'] = datetime.utcnow().isoformat()
    data['transactions'].append(transaction)
    
    save_data(data)
    return transaction, None

def get_transactions():
    """Get all transactions"""
    data = load_data()
    return sorted(data['transactions'], key=lambda x: x['created_at'], reverse=True)

def get_inventory_stats():
    """Get inventory statistics"""
    data = load_data()
    
    total_products = len(data['products'])
    total_quantity = sum(inv['quantity'] for inv in data['inventory'].values())
    total_price = sum(p['price'] * data['inventory'][p['id']]['quantity'] for p in data['products'])
    
    # Build categories with products
    categories_data = []
    for cat in data['categories']:
        cat_products = [p for p in data['products'] if p['category_id'] == cat['id']]
        cat_total_qty = sum(data['inventory'][p['id']]['quantity'] for p in cat_products)
        
        categories_data.append({
            'id': cat['id'],
            'name': cat['name'],
            'description': cat['description'],
            'product_count': len(cat_products),
            'total_quantity': cat_total_qty,
            'products': [
                {
                    'id': p['id'],
                    'name': p['name'],
                    'price': p['price'],
                    'quantity': data['inventory'][p['id']]['quantity']
                }
                for p in cat_products
            ]
        })
    
    return {
        'total_products': total_products,
        'total_quantity': total_quantity,
        'total_price': round(total_price, 2),
        'categories': categories_data
    }

# Initialize data on import
init_data()
