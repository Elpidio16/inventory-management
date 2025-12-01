from flask import Blueprint, jsonify
from app import db
from models import Product, Inventory, Category, Transaction

inventory_bp = Blueprint('inventory', __name__, url_prefix='/api/inventory')

@inventory_bp.route('/stats', methods=['GET'])
def get_inventory_stats():
    """Get comprehensive inventory statistics"""
    try:
        # Get total products
        total_products = Product.query.count()
        
        # Get all inventory records
        inventories = Inventory.query.all()
        total_quantity = sum(inv.quantity for inv in inventories)
        
        # Get all products with their inventory and prices
        products = Product.query.all()
        total_price = sum(p.price * (p.inventory.quantity if p.inventory else 0) for p in products)
        
        # Get categories with their products
        categories = Category.query.all()
        categories_data = []
        
        for cat in categories:
            cat_products = Product.query.filter_by(category_id=cat.id).all()
            cat_total_quantity = sum(p.inventory.quantity if p.inventory else 0 for p in cat_products)
            
            categories_data.append({
                'id': cat.id,
                'name': cat.name,
                'description': cat.description,
                'product_count': len(cat_products),
                'total_quantity': cat_total_quantity,
                'products': [
                    {
                        'id': p.id,
                        'name': p.name,
                        'price': p.price,
                        'quantity': p.inventory.quantity if p.inventory else 0,
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

@inventory_bp.route('/summary', methods=['GET'])
def get_inventory_summary():
    """Get quick inventory summary"""
    try:
        inventories = Inventory.query.all()
        total_items = sum(inv.quantity for inv in inventories)
        
        products = Product.query.all()
        total_value = sum(p.price * (p.inventory.quantity if p.inventory else 0) for p in products)
        
        return jsonify({
            'total_products': Product.query.count(),
            'total_items_in_stock': total_items,
            'total_inventory_value': round(total_value, 2),
            'categories_count': Category.query.count()
        }), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@inventory_bp.route('/transactions-summary', methods=['GET'])
def get_transactions_summary():
    """Get transactions summary"""
    try:
        total_entries = Transaction.query.filter_by(type='ENTRY').count()
        total_exits = Transaction.query.filter_by(type='EXIT').count()
        
        return jsonify({
            'total_entries': total_entries,
            'total_exits': total_exits,
            'total_transactions': total_entries + total_exits
        }), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@inventory_bp.route('/low-stock', methods=['GET'])
def get_low_stock_products():
    """Get products with low stock (quantity < 10)"""
    try:
        threshold = request.args.get('threshold', 10, type=int)
        
        low_stock = []
        products = Product.query.all()
        
        for p in products:
            quantity = p.inventory.quantity if p.inventory else 0
            if quantity < threshold:
                low_stock.append({
                    'id': p.id,
                    'name': p.name,
                    'sku': p.sku,
                    'quantity': quantity,
                    'price': p.price,
                    'category': p.category.name if p.category else ''
                })
        
        return jsonify({
            'threshold': threshold,
            'count': len(low_stock),
            'products': low_stock
        }), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500
