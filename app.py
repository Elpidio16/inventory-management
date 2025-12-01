from flask import Flask, render_template, request, jsonify
from flask_cors import CORS
from dotenv import load_dotenv
from database import (
    get_all_data, add_category, get_categories, delete_category,
    add_product, get_products, delete_product,
    add_transaction, get_transactions, get_inventory_stats
)

# Load environment variables
load_dotenv()

# Initialize Flask app
app = Flask(__name__)
CORS(app)

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
        categories = get_categories()
        return jsonify(categories), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/categories', methods=['POST'])
def create_category_endpoint():
    """Create a new category"""
    try:
        data = request.get_json()
        
        if not data or 'name' not in data:
            return jsonify({'error': 'Category name is required'}), 400
        
        category, error = add_category(data['name'], data.get('description', ''))
        
        if error:
            return jsonify({'error': error}), 400
        
        return jsonify(category), 201
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/categories/<category_id>', methods=['DELETE'])
def delete_category_endpoint(category_id):
    """Delete a category"""
    try:
        success, error = delete_category(category_id)
        
        if not success:
            return jsonify({'error': error}), 400
        
        return jsonify({'message': 'Category deleted successfully'}), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

# Products endpoints
@app.route('/api/products', methods=['GET'])
def get_products_endpoint():
    """Get all products"""
    try:
        products = get_products()
        return jsonify(products), 200
    except Exception as e:
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
        
        product, error = add_product(
            data['name'],
            data['sku'],
            data['price'],
            data['category_id'],
            data.get('description', '')
        )
        
        if error:
            return jsonify({'error': error}), 400
        
        return jsonify(product), 201
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/products/<product_id>', methods=['DELETE'])
def delete_product_endpoint(product_id):
    """Delete a product"""
    try:
        success, error = delete_product(product_id)
        
        if not success:
            return jsonify({'error': error}), 400
        
        return jsonify({'message': 'Product deleted successfully'}), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

# Transactions endpoints
@app.route('/api/transactions', methods=['GET'])
def get_transactions_endpoint():
    """Get all transactions"""
    try:
        transactions = get_transactions()
        return jsonify(transactions), 200
    except Exception as e:
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
        
        try:
            quantity = int(data['quantity'])
        except ValueError:
            return jsonify({'error': 'Invalid quantity value'}), 400
        
        transaction, error = add_transaction(
            data['product_id'],
            data['type'],
            quantity,
            data.get('reason', ''),
            data.get('notes', '')
        )
        
        if error:
            return jsonify({'error': error}), 400
        
        return jsonify(transaction), 201
    except Exception as e:
        return jsonify({'error': str(e)}), 500

# Inventory stats endpoint
@app.route('/api/inventory/stats', methods=['GET'])
def get_inventory_stats_endpoint():
    """Get comprehensive inventory statistics"""
    try:
        stats = get_inventory_stats()
        return jsonify(stats), 200
    except Exception as e:
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
