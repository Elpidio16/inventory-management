import os
from app import app
from models import db, Category, Product, Inventory, Transaction
from uuid import uuid4

def create_sample_data():
    """Create sample data for testing"""
    # Create categories
    categories_data = [
        {'name': 'Electronics', 'description': 'Electronic devices and accessories'},
        {'name': 'Clothing', 'description': 'Apparel and fashion items'},
        {'name': 'Food & Beverage', 'description': 'Food and drink products'},
        {'name': 'Office Supplies', 'description': 'Office equipment and supplies'},
    ]
    
    categories = []
    for cat_data in categories_data:
        cat = Category.query.filter_by(name=cat_data['name']).first()
        if not cat:
            cat = Category(name=cat_data['name'], description=cat_data['description'])
            db.session.add(cat)
        categories.append(cat)
    
    db.session.commit()
    
    # Create products
    products_data = [
        {'name': 'Laptop', 'sku': 'LAPTOP001', 'price': 999.99, 'category': categories[0]},
        {'name': 'Monitor', 'sku': 'MON001', 'price': 299.99, 'category': categories[0]},
        {'name': 'T-Shirt', 'sku': 'TSHIRT001', 'price': 29.99, 'category': categories[1]},
        {'name': 'Jeans', 'sku': 'JEANS001', 'price': 79.99, 'category': categories[1]},
        {'name': 'Coffee', 'sku': 'COFFEE001', 'price': 12.99, 'category': categories[2]},
        {'name': 'Notebook', 'sku': 'NOTE001', 'price': 5.99, 'category': categories[3]},
    ]
    
    for prod_data in products_data:
        prod = Product.query.filter_by(sku=prod_data['sku']).first()
        if not prod:
            prod = Product(
                name=prod_data['name'],
                sku=prod_data['sku'],
                price=prod_data['price'],
                category_id=prod_data['category'].id
            )
            db.session.add(prod)
            db.session.flush()
            
            # Create inventory
            inventory = Inventory(product_id=prod.id, quantity=0)
            db.session.add(inventory)
    
    db.session.commit()

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
        create_sample_data()
        print('Database initialized with sample data!')
