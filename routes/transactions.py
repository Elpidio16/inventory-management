from flask import Blueprint, request, jsonify
from app import db
from models import Transaction, Product, Inventory

transactions_bp = Blueprint('transactions', __name__, url_prefix='/api/transactions')

@transactions_bp.route('', methods=['GET'])
def get_transactions():
    """Get all transactions"""
    try:
        transactions = Transaction.query.order_by(Transaction.created_at.desc()).all()
        return jsonify([t.to_dict() for t in transactions]), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@transactions_bp.route('', methods=['POST'])
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
        product = Product.query.get(data['product_id'])
        if not product:
            return jsonify({'error': 'Product not found'}), 404
        
        # Check if inventory exists
        inventory = Inventory.query.filter_by(product_id=data['product_id']).first()
        if not inventory:
            # Create inventory if it doesn't exist
            inventory = Inventory(product_id=data['product_id'], quantity=0)
            db.session.add(inventory)
        
        # Validate quantity
        quantity = int(data['quantity'])
        if quantity <= 0:
            return jsonify({'error': 'Quantity must be greater than 0'}), 400
        
        # For EXIT, check if enough inventory exists
        if data['type'] == 'EXIT' and inventory.quantity < quantity:
            return jsonify({'error': f'Insufficient inventory. Available: {inventory.quantity}'}), 400
        
        # Create transaction
        transaction = Transaction(
            product_id=data['product_id'],
            type=data['type'],
            quantity=quantity,
            reason=data.get('reason', ''),
            notes=data.get('notes', '')
        )
        
        # Update inventory
        if data['type'] == 'ENTRY':
            inventory.quantity += quantity
        else:  # EXIT
            inventory.quantity -= quantity
        
        db.session.add(transaction)
        db.session.commit()
        
        return jsonify(transaction.to_dict()), 201
    except ValueError:
        return jsonify({'error': 'Invalid quantity value'}), 400
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

@transactions_bp.route('/<transaction_id>', methods=['GET'])
def get_transaction(transaction_id):
    """Get a specific transaction"""
    try:
        transaction = Transaction.query.get(transaction_id)
        if not transaction:
            return jsonify({'error': 'Transaction not found'}), 404
        return jsonify(transaction.to_dict()), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@transactions_bp.route('/<transaction_id>', methods=['DELETE'])
def delete_transaction(transaction_id):
    """Delete a transaction (reverses inventory update)"""
    try:
        transaction = Transaction.query.get(transaction_id)
        if not transaction:
            return jsonify({'error': 'Transaction not found'}), 404
        
        # Reverse inventory change
        inventory = Inventory.query.filter_by(product_id=transaction.product_id).first()
        if inventory:
            if transaction.type == 'ENTRY':
                inventory.quantity -= transaction.quantity
            else:  # EXIT
                inventory.quantity += transaction.quantity
            inventory.quantity = max(0, inventory.quantity)
        
        db.session.delete(transaction)
        db.session.commit()
        return jsonify({'message': 'Transaction deleted successfully'}), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500
