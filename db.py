"""
Database models and configuration for Neon PostgreSQL
"""
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
import uuid
import os

# Initialize SQLAlchemy
db = SQLAlchemy()

class Category(db.Model):
    """Category model"""
    __tablename__ = 'categories'
    
    id = db.Column(db.String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    name = db.Column(db.String(255), unique=True, nullable=False)
    description = db.Column(db.Text, default='')
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    products = db.relationship('Product', backref='category', lazy=True, cascade='all, delete-orphan')
    
    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'description': self.description,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None
        }

class Product(db.Model):
    """Product model"""
    __tablename__ = 'products'
    
    id = db.Column(db.String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    name = db.Column(db.String(255), nullable=False)
    sku = db.Column(db.String(100), unique=True, nullable=False)
    price = db.Column(db.Float, nullable=False)
    description = db.Column(db.Text, default='')
    category_id = db.Column(db.String(36), db.ForeignKey('categories.id'), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    inventory = db.relationship('Inventory', backref='product', uselist=False, cascade='all, delete-orphan')
    transactions = db.relationship('Transaction', backref='product', lazy=True, cascade='all, delete-orphan')
    
    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'sku': self.sku,
            'price': self.price,
            'description': self.description,
            'category_id': self.category_id,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None,
            'inventory': self.inventory.to_dict() if self.inventory else {'quantity': 0}
        }

class Inventory(db.Model):
    """Inventory model"""
    __tablename__ = 'inventory'
    
    id = db.Column(db.String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    product_id = db.Column(db.String(36), db.ForeignKey('products.id'), nullable=False, unique=True)
    quantity = db.Column(db.Integer, default=0)
    last_updated = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    def to_dict(self):
        return {
            'id': self.id,
            'product_id': self.product_id,
            'quantity': self.quantity,
            'last_updated': self.last_updated.isoformat() if self.last_updated else None
        }

class Transaction(db.Model):
    """Transaction model (ENTRY/EXIT)"""
    __tablename__ = 'transactions'
    
    id = db.Column(db.String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    product_id = db.Column(db.String(36), db.ForeignKey('products.id'), nullable=False)
    product = db.relationship('Product', lazy='joined')
    type = db.Column(db.String(10), nullable=False)  # ENTRY or EXIT
    quantity = db.Column(db.Integer, nullable=False)
    reason = db.Column(db.String(255), default='')
    notes = db.Column(db.Text, default='')
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    def to_dict(self):
        return {
            'id': self.id,
            'product_id': self.product_id,
            'product': self.product.to_dict() if self.product else None,
            'type': self.type,
            'quantity': self.quantity,
            'reason': self.reason,
            'notes': self.notes,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None
        }

def init_db(app):
    """Initialize database safely"""
    try:
        with app.app_context():
            db.create_all()
            print("Database tables created successfully")
            return True
    except Exception as e:
        print(f"Error initializing database: {e}")
        return False
