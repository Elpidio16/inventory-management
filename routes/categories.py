from flask import Blueprint, request, jsonify
from app import db
from models import Category

categories_bp = Blueprint('categories', __name__, url_prefix='/api/categories')

@categories_bp.route('', methods=['GET'])
def get_categories():
    """Get all categories"""
    try:
        categories = Category.query.all()
        return jsonify([cat.to_dict() for cat in categories]), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@categories_bp.route('', methods=['POST'])
def create_category():
    """Create a new category"""
    try:
        data = request.get_json()
        
        if not data or 'name' not in data:
            return jsonify({'error': 'Category name is required'}), 400
        
        # Check if category already exists
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
        return jsonify({'error': str(e)}), 500

@categories_bp.route('/<category_id>', methods=['GET'])
def get_category(category_id):
    """Get a specific category"""
    try:
        category = Category.query.get(category_id)
        if not category:
            return jsonify({'error': 'Category not found'}), 404
        return jsonify(category.to_dict()), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@categories_bp.route('/<category_id>', methods=['PUT'])
def update_category(category_id):
    """Update a category"""
    try:
        category = Category.query.get(category_id)
        if not category:
            return jsonify({'error': 'Category not found'}), 404
        
        data = request.get_json()
        
        if 'name' in data:
            # Check if new name already exists
            existing = Category.query.filter_by(name=data['name']).first()
            if existing and existing.id != category_id:
                return jsonify({'error': 'Category name already exists'}), 400
            category.name = data['name']
        
        if 'description' in data:
            category.description = data['description']
        
        db.session.commit()
        return jsonify(category.to_dict()), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

@categories_bp.route('/<category_id>', methods=['DELETE'])
def delete_category(category_id):
    """Delete a category"""
    try:
        category = Category.query.get(category_id)
        if not category:
            return jsonify({'error': 'Category not found'}), 404
        
        db.session.delete(category)
        db.session.commit()
        return jsonify({'message': 'Category deleted successfully'}), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500
