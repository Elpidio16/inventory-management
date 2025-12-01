from flask import Flask, render_template, request, jsonify
from flask_cors import CORS
from dotenv import load_dotenv
from db import db, init_db, Category, Product, Inventory, Transaction
from datetime import datetime
import os

# Load environment variables
load_dotenv()

# Initialize Flask app
app = Flask(__name__)
CORS(app)

# Configure database
DATABASE_URL = os.environ.get('DATABASE_URL', 'postgresql://localhost/inventory_db')
app.config['SQLALCHEMY_DATABASE_URI'] = DATABASE_URL
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db.init_app(app)

# Flag to track if DB is initialized
_db_initialized = False

def ensure_db_initialized():
    """Safely initialize database on first request"""
    global _db_initialized
    if not _db_initialized:
        try:
            init_db(app)
            _db_initialized = True
            print("Database initialized successfully")
        except Exception as e:
            print(f"Warning: Could not initialize database: {e}")
            _db_initialized = False

# Initialize DB on first request (not on module load)
@app.before_request
def before_request():
    """Ensure database is initialized before each request"""
    ensure_db_initialized()

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
def get_categories_endpoint():
    """Get all categories"""
    try:
        categories = Category.query.all()
        return jsonify([cat.to_dict() for cat in categories]), 200
    except Exception as e:
        print(f"Error: {e}")
        return jsonify({'error': str(e)}), 500

@app.route('/api/categories', methods=['POST'])
def create_category_endpoint():
    """Create a new category"""
    try:
        data = request.get_json()
        
        if not data or 'name' not in data:
            return jsonify({'error': 'Category name is required'}), 400
        
        # Check if category exists
        existing = Category.query.filter_by(name=data['name']).first()
        if existing:
            return jsonify({'error': 'Category already exists'}), 400
        
        category = Category(
            name=data['name'],
            description=data.get('description', '')
        )
        db.session.add(category)
        db.session.commit()
        
        return jsonify(category.to_dict()), 201
    except Exception as e:
        db.session.rollback()
        print(f"Error: {e}")
        return jsonify({'error': str(e)}), 500

@app.route('/api/categories/<category_id>', methods=['DELETE'])
def delete_category_endpoint(category_id):
    """Delete a category"""
    try:
        category = Category.query.get(category_id)
        if not category:
            return jsonify({'error': 'Category not found'}), 404
        
        # Check if category has products
        if category.products:
            return jsonify({'error': 'Cannot delete category with existing products'}), 400
        
        db.session.delete(category)
        db.session.commit()
        
        return jsonify({'message': 'Category deleted successfully'}), 200
    except Exception as e:
        db.session.rollback()
        print(f"Error: {e}")
        return jsonify({'error': str(e)}), 500

# Products endpoints
@app.route('/api/products', methods=['GET'])
def get_products_endpoint():
    """Get all products"""
    try:
        products = Product.query.all()
        return jsonify([prod.to_dict() for prod in products]), 200
    except Exception as e:
        print(f"Error: {e}")
        return jsonify({'error': str(e)}), 500

@app.route('/api/products', methods=['POST'])
def create_product_endpoint():
    """Create a new product"""
    try:
        data = request.get_json()
        
        # Validate required fields
        required_fields = ['name', 'sku', 'price', 'category_id']
        if not all(field in data for field in required_fields):
            return jsonify({'error': 'Missing required fields'}), 400
        
        # Check if SKU exists
        existing_sku = Product.query.filter_by(sku=data['sku']).first()
        if existing_sku:
            return jsonify({'error': 'Product with this Product Code already exists'}), 400
        
        # Check if category exists
        category = Category.query.get(data['category_id'])
        if not category:
            return jsonify({'error': 'Category not found'}), 400
        
        product = Product(
            name=data['name'],
            sku=data['sku'],
            price=float(data['price']),
            category_id=data['category_id'],
            description=data.get('description', '')
        )
        db.session.add(product)
        db.session.flush()  # Get the product ID before committing
        
        # Create inventory record
        inventory = Inventory(product_id=product.id)
        db.session.add(inventory)
        db.session.commit()
        
        product.inventory = inventory
        return jsonify(product.to_dict()), 201
    except Exception as e:
        db.session.rollback()
        print(f"Error: {e}")
        return jsonify({'error': str(e)}), 500

@app.route('/api/products/<product_id>', methods=['DELETE'])
def delete_product_endpoint(product_id):
    """Delete a product"""
    try:
        product = Product.query.get(product_id)
        if not product:
            return jsonify({'error': 'Product not found'}), 404
        
        db.session.delete(product)
        db.session.commit()
        
        return jsonify({'message': 'Product deleted successfully'}), 200
    except Exception as e:
        db.session.rollback()
        print(f"Error: {e}")
        return jsonify({'error': str(e)}), 500

# Transactions endpoints
@app.route('/api/transactions', methods=['GET'])
def get_transactions_endpoint():
    """Get all transactions"""
    try:
        transactions = Transaction.query.options(db.joinedload(Transaction.product)).order_by(Transaction.created_at.desc()).all()
        return jsonify([trans.to_dict() for trans in transactions]), 200
    except Exception as e:
        print(f"Error: {e}")
        return jsonify({'error': str(e)}), 500

@app.route('/api/transactions', methods=['POST'])
def create_transaction_endpoint():
    """Create a new transaction"""
    try:
        data = request.get_json()
        
        # Validate required fields
        required_fields = ['product_id', 'type', 'quantity']
        if not all(field in data for field in required_fields):
            return jsonify({'error': 'Missing required fields'}), 400
        
        # Get product
        product = Product.query.get(data['product_id'])
        if not product:
            return jsonify({'error': 'Product not found'}), 404
        
        # Validate transaction type
        if data['type'] not in ['ENTRY', 'EXIT']:
            return jsonify({'error': 'Invalid transaction type'}), 400
        
        # Validate quantity
        try:
            quantity = int(data['quantity'])
            if quantity <= 0:
                return jsonify({'error': 'Quantity must be greater than 0'}), 400
        except ValueError:
            return jsonify({'error': 'Invalid quantity value'}), 400
        
        # Check inventory for EXIT
        if data['type'] == 'EXIT':
            if product.inventory.quantity < quantity:
                return jsonify({'error': f'Insufficient inventory. Available: {product.inventory.quantity}'}), 400
        
        # Create transaction
        transaction = Transaction(
            product_id=data['product_id'],
            type=data['type'],
            quantity=quantity,
            reason=data.get('reason', ''),
            notes=data.get('notes', '')
        )
        db.session.add(transaction)
        
        # Update inventory
        if data['type'] == 'ENTRY':
            product.inventory.quantity += quantity
        else:
            product.inventory.quantity -= quantity
        product.inventory.last_updated = datetime.utcnow()
        
        db.session.commit()
        
        return jsonify(transaction.to_dict()), 201
    except Exception as e:
        db.session.rollback()
        print(f"Error: {e}")
        return jsonify({'error': str(e)}), 500

# Inventory stats endpoint
@app.route('/api/inventory/stats', methods=['GET'])
def get_inventory_stats_endpoint():
    """Get comprehensive inventory statistics"""
    try:
        # Get all data
        categories = Category.query.all()
        products = Product.query.all()
        
        total_products = len(products)
        total_quantity = sum(p.inventory.quantity for p in products if p.inventory)
        total_price = sum(p.price * p.inventory.quantity for p in products if p.inventory)
        
        # Build categories with products
        categories_data = []
        for cat in categories:
            cat_products = [p for p in products if p.category_id == cat.id]
            cat_total_qty = sum(p.inventory.quantity for p in cat_products if p.inventory)
            
            categories_data.append({
                'id': cat.id,
                'name': cat.name,
                'description': cat.description,
                'product_count': len(cat_products),
                'total_quantity': cat_total_qty,
                'products': [
                    {
                        'id': p.id,
                        'name': p.name,
                        'price': p.price,
                        'quantity': p.inventory.quantity if p.inventory else 0
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
        print(f"Error: {e}")
        return jsonify({'error': str(e)}), 500

# Error handlers
@app.errorhandler(404)
def not_found(error):
    return jsonify({'error': 'Not found'}), 404

@app.errorhandler(500)
def server_error(error):
    print(f"Server error: {error}")
    return jsonify({'error': 'Internal server error'}), 500

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
