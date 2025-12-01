from flask import Flask, render_template, request, jsonify
from flask_cors import CORS
from datetime import datetime
import os
import uuid
import sqlite3
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Initialize Flask app
app = Flask(__name__)
CORS(app)

# Database setup
DB_PATH = 'inventory.db'

def init_db():
    """Initialize SQLite database with tables"""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    # Create categories table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS categories (
            id TEXT PRIMARY KEY,
            name TEXT UNIQUE NOT NULL,
            description TEXT,
            created_at TEXT,
            updated_at TEXT
        )
    ''')
    
    # Create products table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS products (
            id TEXT PRIMARY KEY,
            name TEXT NOT NULL,
            description TEXT,
            sku TEXT UNIQUE NOT NULL,
            price REAL NOT NULL,
            category_id TEXT NOT NULL,
            created_at TEXT,
            updated_at TEXT,
            FOREIGN KEY (category_id) REFERENCES categories(id)
        )
    ''')
    
    # Create inventory table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS inventory (
            id TEXT PRIMARY KEY,
            product_id TEXT UNIQUE NOT NULL,
            quantity INTEGER DEFAULT 0,
            last_updated TEXT,
            FOREIGN KEY (product_id) REFERENCES products(id)
        )
    ''')
    
    # Create transactions table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS transactions (
            id TEXT PRIMARY KEY,
            product_id TEXT NOT NULL,
            type TEXT NOT NULL,
            quantity INTEGER NOT NULL,
            reason TEXT,
            notes TEXT,
            created_at TEXT,
            updated_at TEXT,
            FOREIGN KEY (product_id) REFERENCES products(id)
        )
    ''')
    
    conn.commit()
    conn.close()

def get_db_connection():
    """Get SQLite database connection"""
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn

# Initialize database on startup
with app.app_context():
    init_db()

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
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM categories ORDER BY created_at DESC')
        categories = [dict(row) for row in cursor.fetchall()]
        conn.close()
        return jsonify(categories), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/categories', methods=['POST'])
def create_category():
    """Create a new category"""
    try:
        data = request.get_json()
        
        if not data or 'name' not in data:
            return jsonify({'error': 'Category name is required'}), 400
        
        category_id = str(uuid.uuid4())
        now = datetime.utcnow().isoformat()
        
        conn = get_db_connection()
        cursor = conn.cursor()
        
        try:
            cursor.execute('''
                INSERT INTO categories (id, name, description, created_at, updated_at)
                VALUES (?, ?, ?, ?, ?)
            ''', (category_id, data['name'], data.get('description', ''), now, now))
            conn.commit()
        except sqlite3.IntegrityError:
            conn.close()
            return jsonify({'error': 'Category already exists'}), 400
        
        category = {
            'id': category_id,
            'name': data['name'],
            'description': data.get('description', ''),
            'created_at': now,
            'updated_at': now
        }
        conn.close()
        return jsonify(category), 201
    except Exception as e:
        return jsonify({'error': str(e)}), 500

# Products endpoints
@app.route('/api/products', methods=['GET'])
def get_products():
    """Get all products with inventory"""
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        
        cursor.execute('SELECT * FROM products ORDER BY created_at DESC')
        products = [dict(row) for row in cursor.fetchall()]
        
        # Get inventory for each product
        for product in products:
            cursor.execute('SELECT * FROM inventory WHERE product_id = ?', (product['id'],))
            inv_row = cursor.fetchone()
            product['inventory'] = dict(inv_row) if inv_row else {'quantity': 0, 'last_updated': None}
        
        conn.close()
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
        
        product_id = str(uuid.uuid4())
        inventory_id = str(uuid.uuid4())
        now = datetime.utcnow().isoformat()
        
        conn = get_db_connection()
        cursor = conn.cursor()
        
        try:
            # Insert product
            cursor.execute('''
                INSERT INTO products (id, name, description, sku, price, category_id, created_at, updated_at)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?)
            ''', (product_id, data['name'], data.get('description', ''), data['sku'], 
                  float(data['price']), data['category_id'], now, now))
            
            # Insert inventory record
            cursor.execute('''
                INSERT INTO inventory (id, product_id, quantity, last_updated)
                VALUES (?, ?, ?, ?)
            ''', (inventory_id, product_id, 0, now))
            
            conn.commit()
        except sqlite3.IntegrityError as e:
            conn.close()
            if 'sku' in str(e):
                return jsonify({'error': 'Product with this Product Code already exists'}), 400
            elif 'category_id' in str(e):
                return jsonify({'error': 'Category not found'}), 404
            return jsonify({'error': str(e)}), 400
        
        product = {
            'id': product_id,
            'name': data['name'],
            'description': data.get('description', ''),
            'sku': data['sku'],
            'price': float(data['price']),
            'category_id': data['category_id'],
            'created_at': now,
            'updated_at': now,
            'inventory': {'id': inventory_id, 'product_id': product_id, 'quantity': 0, 'last_updated': now}
        }
        conn.close()
        return jsonify(product), 201
    except Exception as e:
        return jsonify({'error': str(e)}), 500

# Transactions endpoints
@app.route('/api/transactions', methods=['GET'])
def get_transactions():
    """Get all transactions"""
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM transactions ORDER BY created_at DESC')
        transactions = [dict(row) for row in cursor.fetchall()]
        conn.close()
        return jsonify(transactions), 200
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
        
        # Validate quantity
        try:
            quantity = int(data['quantity'])
            if quantity <= 0:
                return jsonify({'error': 'Quantity must be greater than 0'}), 400
        except ValueError:
            return jsonify({'error': 'Invalid quantity value'}), 400
        
        conn = get_db_connection()
        cursor = conn.cursor()
        
        # Check if product exists and get current inventory
        cursor.execute('SELECT id FROM products WHERE id = ?', (data['product_id'],))
        if not cursor.fetchone():
            conn.close()
            return jsonify({'error': 'Product not found'}), 404
        
        cursor.execute('SELECT quantity FROM inventory WHERE product_id = ?', (data['product_id'],))
        inv_row = cursor.fetchone()
        current_qty = inv_row['quantity'] if inv_row else 0
        
        # Check inventory for EXIT
        if data['type'] == 'EXIT' and current_qty < quantity:
            conn.close()
            return jsonify({'error': f'Insufficient inventory. Available: {current_qty}'}), 400
        
        # Create transaction
        transaction_id = str(uuid.uuid4())
        now = datetime.utcnow().isoformat()
        
        try:
            cursor.execute('''
                INSERT INTO transactions (id, product_id, type, quantity, reason, notes, created_at, updated_at)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?)
            ''', (transaction_id, data['product_id'], data['type'], quantity, 
                  data.get('reason', ''), data.get('notes', ''), now, now))
            
            # Update inventory
            new_qty = current_qty + quantity if data['type'] == 'ENTRY' else current_qty - quantity
            cursor.execute('UPDATE inventory SET quantity = ?, last_updated = ? WHERE product_id = ?',
                          (new_qty, now, data['product_id']))
            
            conn.commit()
        except Exception as e:
            conn.close()
            return jsonify({'error': str(e)}), 500
        
        transaction = {
            'id': transaction_id,
            'product_id': data['product_id'],
            'type': data['type'],
            'quantity': quantity,
            'reason': data.get('reason', ''),
            'notes': data.get('notes', ''),
            'created_at': now,
            'updated_at': now
        }
        conn.close()
        return jsonify(transaction), 201
    except Exception as e:
        return jsonify({'error': str(e)}), 500

# Inventory stats endpoint
@app.route('/api/inventory/stats', methods=['GET'])
def get_inventory_stats():
    """Get comprehensive inventory statistics"""
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        
        # Get all products with inventory
        cursor.execute('''
            SELECT p.*, i.quantity 
            FROM products p 
            LEFT JOIN inventory i ON p.id = i.product_id
            ORDER BY p.created_at DESC
        ''')
        products = [dict(row) for row in cursor.fetchall()]
        
        # Get all categories
        cursor.execute('SELECT * FROM categories ORDER BY created_at DESC')
        categories = [dict(row) for row in cursor.fetchall()]
        
        # Calculate stats
        total_products = len(products)
        total_quantity = sum(p.get('quantity', 0) or 0 for p in products)
        total_price = sum(p['price'] * (p.get('quantity', 0) or 0) for p in products)
        
        # Build categories with products
        categories_data = []
        for cat in categories:
            cat_products = [p for p in products if p['category_id'] == cat['id']]
            cat_total_qty = sum(p.get('quantity', 0) or 0 for p in cat_products)
            
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
                        'quantity': p.get('quantity', 0) or 0
                    }
                    for p in cat_products
                ]
            })
        
        conn.close()
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
