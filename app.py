from flask import Flask, render_template, request, jsonify
from flask_cors import CORS
from datetime import datetime
import os
import uuid
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Initialize Flask app
app = Flask(__name__)
CORS(app)

# Simple in-memory database
DATA = {
    'categories': [],
    'products': [],
    'inventory': {},
    'transactions': []
}

# Home route
@app.route('/')
def index():
    """Render main dashboard page"""
    return render_template('index.html')

# Health check endpoint
@app.route('/api/health', methods=['GET'])
def health():
    """Health check endpoint"""
    return jsonify({'status': 'ok', 'message': 'Server is running'}), 200

# Categories endpoints
@app.route('/api/categories', methods=['GET'])
def get_categories():
    """Get all categories"""
    try:
        return jsonify(DATA['categories']), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/categories', methods=['POST'])
def create_category():
    """Create a new category"""
    try:
        data = request.get_json()
        
        if not data or 'name' not in data:
            return jsonify({'error': 'Category name is required'}), 400
        
        # Check if category already exists
        for cat in DATA['categories']:
            if cat['name'] == data['name']:
                return jsonify({'error': 'Category already exists'}), 400
        
        category = {
            'id': str(uuid.uuid4()),
            'name': data['name'],
            'description': data.get('description', ''),
            'created_at': datetime.utcnow().isoformat(),
            'updated_at': datetime.utcnow().isoformat(),
            'product_count': 0
        }
        
        DATA['categories'].append(category)
        return jsonify(category), 201
    except Exception as e:
        return jsonify({'error': str(e)}), 500

# Products endpoints
@app.route('/api/products', methods=['GET'])
def get_products():
    """Get all products"""
    try:
        products = []
        for p in DATA['products']:
            product = p.copy()
            product['inventory'] = DATA['inventory'].get(p['id'], {'quantity': 0})
            products.append(product)
        return jsonify(products), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/products', methods=['POST'])
def create_product():
    """Create a new product"""
    try:
        data = request.get_json()
        
        # Validate required fields
        required_fields = ['name', 'sku', 'price', 'category_id']
        if not all(field in data for field in required_fields):
            return jsonify({'error': 'Missing required fields'}), 400
        
        # Check if SKU already exists
        for prod in DATA['products']:
            if prod['sku'] == data['sku']:
                return jsonify({'error': 'Product with this SKU already exists'}), 400
        
        # Check if category exists
        category_exists = any(c['id'] == data['category_id'] for c in DATA['categories'])
        if not category_exists:
            return jsonify({'error': 'Category not found'}), 404
        
        product_id = str(uuid.uuid4())
        
        product = {
            'id': product_id,
            'name': data['name'],
            'description': data.get('description', ''),
            'sku': data['sku'],
            'price': float(data['price']),
            'category_id': data['category_id'],
            'created_at': datetime.utcnow().isoformat(),
            'updated_at': datetime.utcnow().isoformat()
        }
        
        # Create inventory record
        DATA['inventory'][product_id] = {
            'id': str(uuid.uuid4()),
            'product_id': product_id,
            'quantity': 0,
            'last_updated': datetime.utcnow().isoformat()
        }
        
        DATA['products'].append(product)
        product['inventory'] = DATA['inventory'][product_id]
        
        return jsonify(product), 201
    except Exception as e:
        return jsonify({'error': str(e)}), 500

# Transactions endpoints
@app.route('/api/transactions', methods=['GET'])
def get_transactions():
    """Get all transactions"""
    try:
        return jsonify(sorted(DATA['transactions'], key=lambda x: x['created_at'], reverse=True)), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/transactions', methods=['POST'])
def create_transaction():
    """Create a new transaction (entry or exit)"""
    try:
        data = request.get_json()
        
        # Validate required fields
        required_fields = ['product_id', 'type', 'quantity']
        if not all(field in data for field in required_fields):
            return jsonify({'error': 'Missing required fields'}), 400
        
        # Validate transaction type
        if data['type'] not in ['ENTRY', 'EXIT']:
            return jsonify({'error': 'Invalid transaction type. Use ENTRY or EXIT'}), 400
        
        # Check if product exists
        product = next((p for p in DATA['products'] if p['id'] == data['product_id']), None)
        if not product:
            return jsonify({'error': 'Product not found'}), 404
        
        # Validate quantity
        quantity = int(data['quantity'])
        if quantity <= 0:
            return jsonify({'error': 'Quantity must be greater than 0'}), 400
        
        # Check inventory for EXIT
        current_qty = DATA['inventory'][data['product_id']]['quantity']
        if data['type'] == 'EXIT' and current_qty < quantity:
            return jsonify({'error': f'Insufficient inventory. Available: {current_qty}'}), 400
        
        # Create transaction
        transaction = {
            'id': str(uuid.uuid4()),
            'product_id': data['product_id'],
            'type': data['type'],
            'quantity': quantity,
            'reason': data.get('reason', ''),
            'notes': data.get('notes', ''),
            'created_at': datetime.utcnow().isoformat(),
            'updated_at': datetime.utcnow().isoformat()
        }
        
        # Update inventory
        if data['type'] == 'ENTRY':
            DATA['inventory'][data['product_id']]['quantity'] += quantity
        else:  # EXIT
            DATA['inventory'][data['product_id']]['quantity'] -= quantity
        
        DATA['inventory'][data['product_id']]['last_updated'] = datetime.utcnow().isoformat()
        DATA['transactions'].append(transaction)
        
        return jsonify(transaction), 201
    except ValueError:
        return jsonify({'error': 'Invalid quantity value'}), 400
    except Exception as e:
        return jsonify({'error': str(e)}), 500

# Inventory stats endpoint
@app.route('/api/inventory/stats', methods=['GET'])
def get_inventory_stats():
    """Get comprehensive inventory statistics"""
    try:
        total_products = len(DATA['products'])
        total_quantity = sum(inv['quantity'] for inv in DATA['inventory'].values())
        total_price = sum(p['price'] * DATA['inventory'][p['id']]['quantity'] for p in DATA['products'])
        
        # Get categories with their products
        categories_data = []
        for cat in DATA['categories']:
            cat_products = [p for p in DATA['products'] if p['category_id'] == cat['id']]
            cat_total_quantity = sum(DATA['inventory'][p['id']]['quantity'] for p in cat_products)
            
            categories_data.append({
                'id': cat['id'],
                'name': cat['name'],
                'description': cat['description'],
                'product_count': len(cat_products),
                'total_quantity': cat_total_quantity,
                'products': [
                    {
                        'id': p['id'],
                        'name': p['name'],
                        'price': p['price'],
                        'quantity': DATA['inventory'][p['id']]['quantity'],
                    }
                    for p in cat_products
                ]
            })
        
        return jsonify({
            'total_products': total_products,
            'total_quantity': total_quantity,
            'total_price': round(total_price, 2),
            'categories': categories_data
        }), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

# Error handlers
@app.errorhandler(404)
def not_found(error):
    return jsonify({'error': 'Not found'}), 404

@app.errorhandler(500)
def server_error(error):
    return jsonify({'error': 'Internal server error'}), 500

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)

