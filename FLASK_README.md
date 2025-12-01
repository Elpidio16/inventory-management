# Inventory Management System - Flask Edition

A comprehensive inventory management application built with Flask for tracking product entries, exits, and maintaining an organized inventory system.

## Features

✅ **Product Management**
- Add and manage products with categories
- Track SKU and pricing information
- Organize products by categories

✅ **Inventory Tracking**
- Record product entries (incoming inventory)
- Record product exits (sales/outgoing inventory)
- View real-time inventory quantities
- Track inventory value

✅ **Dashboard Analytics**
- View total number of products
- Display total inventory quantity
- Calculate total inventory value
- Show products organized by categories with pricing

✅ **Comprehensive Reporting**
- Transaction history with dates and reasons
- Detailed inventory by category
- Product pricing and quantity tracking

## Tech Stack

- **Backend**: Flask with Python, SQLAlchemy ORM
- **Frontend**: HTML5, CSS3, JavaScript (Axios for API calls)
- **Database**: PostgreSQL
- **Deployment**: Vercel with GitHub Actions CI/CD

## Project Structure

```
inventory-management/
├── app.py                     # Main Flask application
├── models.py                  # SQLAlchemy database models
├── config.py                  # Configuration management
├── init_db.py                 # Database initialization script
├── routes/
│   ├── __init__.py
│   ├── categories.py          # Category management routes
│   ├── products.py            # Product management routes
│   ├── transactions.py        # Transaction recording routes
│   └── inventory.py           # Inventory analytics routes
├── templates/
│   └── index.html             # Main HTML template
├── static/
│   ├── css/
│   │   └── style.css          # Styling
│   └── js/
│       └── app.js             # Frontend JavaScript
├── .github/workflows/
│   └── deploy.yml             # GitHub Actions workflow
├── requirements.txt           # Python dependencies
├── Procfile                   # Heroku/Vercel deployment file
├── vercel.json                # Vercel configuration
├── .env.example               # Environment variables template
└── README.md                  # Documentation
```

## Database Models

The application uses PostgreSQL with these main models:

- **Category**: Product groupings
- **Product**: Items in inventory
- **Inventory**: Current stock levels
- **Transaction**: Entry/Exit records

## Setup Instructions

### 1. Prerequisites

- Python 3.8+
- PostgreSQL database
- pip package manager
- Virtual environment (recommended)
- GitHub account (Elpidio16)
- Vercel account (for deployment)

### 2. Installation

```bash
# Clone the repository (after pushing to GitHub)
git clone https://github.com/Elpidio16/inventory-management.git
cd inventory-management

# Create virtual environment
python -m venv venv

# Activate virtual environment
# On Windows:
venv\Scripts\activate
# On macOS/Linux:
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt
```

### 3. Environment Setup

Create a `.env` file in the project root:

```env
# Database
DATABASE_URL=postgresql://user:password@localhost:5432/inventory_db

# Flask
FLASK_ENV=development
FLASK_APP=app.py
```

### 4. Database Setup

```bash
# Initialize database with sample data
python init_db.py
```

### 5. Development

```bash
# Start Flask development server
python app.py

# Open http://localhost:5000 in your browser
```

## API Endpoints

### Categories
- `GET /api/categories` - List all categories
- `POST /api/categories` - Create a new category
- `GET /api/categories/<id>` - Get specific category
- `PUT /api/categories/<id>` - Update category
- `DELETE /api/categories/<id>` - Delete category

### Products
- `GET /api/products` - List all products
- `POST /api/products` - Create a new product
- `GET /api/products/<id>` - Get specific product
- `PUT /api/products/<id>` - Update product
- `DELETE /api/products/<id>` - Delete product

### Transactions
- `GET /api/transactions` - List all transactions
- `POST /api/transactions` - Record new transaction (entry or exit)
- `GET /api/transactions/<id>` - Get specific transaction
- `DELETE /api/transactions/<id>` - Delete transaction

### Inventory Analytics
- `GET /api/inventory/stats` - Get comprehensive inventory statistics
- `GET /api/inventory/summary` - Get quick summary
- `GET /api/inventory/transactions-summary` - Get transaction stats
- `GET /api/inventory/low-stock` - Get low stock products

## Using the Application

### 1. Dashboard Tab
View real-time inventory statistics:
- Total number of products
- Total inventory quantity
- Total inventory value
- Products organized by category with pricing

### 2. Add Product Tab
Create new products:
- Enter product name, SKU, and price
- Assign to a category
- Add optional description

### 3. Record Transaction Tab
Track inventory movement:
- Select transaction type (Entry/Exit)
- Choose product and quantity
- Optionally add reason and notes
- Updates inventory automatically

### 4. Manage Categories Tab
Organize product categories:
- Create new categories
- View all categories
- Delete categories

## GitHub Deployment Setup

See `GITHUB_SETUP.md` for detailed GitHub repository and Vercel deployment instructions for Elpidio16 account.

## Running in Production

```bash
# Build for production
pip install gunicorn

# Run with Gunicorn
gunicorn app:app --bind 0.0.0.0:5000
```

## Docker (Optional)

```bash
# Build Docker image
docker build -t inventory-management .

# Run container
docker run -e DATABASE_URL=postgresql://... -p 5000:5000 inventory-management
```

## Troubleshooting

### ModuleNotFoundError
```bash
pip install -r requirements.txt
```

### Database Connection Issues
- Verify DATABASE_URL is correct
- Check PostgreSQL is running
- Ensure database exists

### Port Already in Use
```bash
# Change port in app.py or use:
python app.py --port 5001
```

### Virtual Environment Issues
```bash
# Recreate virtual environment
rm -rf venv
python -m venv venv
source venv/bin/activate  # or venv\Scripts\activate on Windows
pip install -r requirements.txt
```

## Future Enhancements

- [ ] User authentication and role-based access
- [ ] Advanced search and filtering
- [ ] Export reports (CSV, PDF)
- [ ] Email notifications for low stock
- [ ] Barcode/QR code scanning
- [ ] Multi-location inventory tracking
- [ ] Supplier management
- [ ] Advanced analytics and forecasting
- [ ] REST API documentation (Swagger)
- [ ] Unit tests

## License

MIT

## Support

For issues or questions, create an issue in the GitHub repository.

---

**Created for**: Elpidio16  
**Framework**: Flask with SQLAlchemy  
**Last Updated**: December 1, 2025
