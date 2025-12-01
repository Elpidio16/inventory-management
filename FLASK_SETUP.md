# Flask Setup Guide for Inventory Management System

Quick start guide for setting up and running the Flask application.

## Prerequisites

- Python 3.8 or higher
- PostgreSQL database (or SQLite for testing)
- pip (Python package manager)
- Git

## Step 1: Clone Repository (After Pushing to GitHub)

```bash
git clone https://github.com/Elpidio16/inventory-management.git
cd inventory-management
```

## Step 2: Create Virtual Environment

**On Windows:**
```bash
python -m venv venv
venv\Scripts\activate
```

**On macOS/Linux:**
```bash
python3 -m venv venv
source venv/bin/activate
```

## Step 3: Install Dependencies

```bash
pip install -r requirements.txt
```

## Step 4: Create Environment File

Create `.env` file in project root:

```env
# Database Configuration
DATABASE_URL=postgresql://user:password@localhost:5432/inventory_db

# Flask Configuration
FLASK_ENV=development
FLASK_APP=app.py
```

### Database URL Examples

**PostgreSQL (Local):**
```
postgresql://postgres:password@localhost:5432/inventory_db
```

**PostgreSQL (Supabase):**
```
postgresql://[user]:[password]@[host]:[port]/[database]?sslmode=require
```

**SQLite (Testing Only):**
```
sqlite:///inventory.db
```

## Step 5: Initialize Database

```bash
# Create tables and load sample data
python init_db.py
```

You should see: "Database initialized with sample data!"

## Step 6: Run Development Server

```bash
python app.py
```

Output will show:
```
* Running on http://127.0.0.1:5000
```

Open http://localhost:5000 in your browser.

## Step 7: Start Using the Application

### Dashboard
- View inventory statistics
- See products by category
- Check inventory values

### Add Product
- Create new products
- Assign to categories
- Set prices and SKU

### Record Transaction
- Record item entries
- Record item exits
- Track transaction history

### Manage Categories
- Create product categories
- Organize products
- Delete categories

## Database Setup Options

### Option A: PostgreSQL (Recommended)

**Using Supabase (Free):**
1. Go to https://supabase.com
2. Sign up with GitHub (Elpidio16)
3. Create new project
4. Copy connection string
5. Add to `.env` as DATABASE_URL

**Using Local PostgreSQL:**
1. Install PostgreSQL
2. Create database:
   ```sql
   CREATE DATABASE inventory_db;
   ```
3. Use connection string:
   ```
   postgresql://postgres:password@localhost:5432/inventory_db
   ```

### Option B: SQLite (Testing)

For quick testing without PostgreSQL:
```env
DATABASE_URL=sqlite:///inventory.db
```

## Project Commands

### Development
```bash
# Run development server
python app.py

# With automatic reload
FLASK_ENV=development python app.py
```

### Database
```bash
# Initialize database
python init_db.py

# Reset database
rm inventory.db  # for SQLite
```

### Production
```bash
# Install production server
pip install gunicorn

# Run with Gunicorn
gunicorn app:app --bind 0.0.0.0:5000
```

## File Structure

```
.
├── app.py                    # Main Flask application
├── models.py                 # Database models
├── config.py                 # Configuration
├── init_db.py               # Database initialization
├── routes/                  # API routes
│   ├── categories.py
│   ├── products.py
│   ├── transactions.py
│   └── inventory.py
├── templates/
│   └── index.html           # Main template
├── static/
│   ├── css/style.css
│   └── js/app.js
├── .env                     # Environment variables
└── requirements.txt         # Dependencies
```

## Troubleshooting

### "No module named 'flask'"
```bash
pip install -r requirements.txt
```

### "could not connect to database"
- Check DATABASE_URL in .env
- Verify PostgreSQL is running
- Check database exists
- Verify credentials

### "Port 5000 already in use"
Change port in app.py:
```python
app.run(debug=True, port=5001)
```

### Virtual environment not activating
```bash
# Windows
venv\Scripts\activate

# macOS/Linux
source venv/bin/activate
```

## Next Steps

1. ✅ Install Python and dependencies
2. ✅ Set up PostgreSQL database
3. ✅ Create .env file with DATABASE_URL
4. ✅ Initialize database (python init_db.py)
5. ✅ Run development server (python app.py)
6. ✅ Test at http://localhost:5000
7. 📋 Push code to GitHub
8. 📋 Deploy to Vercel (see GITHUB_SETUP.md)

## Deployment to Vercel

See `GITHUB_SETUP.md` for instructions to:
- Push code to GitHub
- Connect to Vercel
- Set up GitHub Actions
- Configure automatic deployment

## API Documentation

All API endpoints return JSON:

```bash
# Get all categories
curl http://localhost:5000/api/categories

# Create product
curl -X POST http://localhost:5000/api/products \
  -H "Content-Type: application/json" \
  -d '{"name":"Test","sku":"TEST1","price":99.99,"category_id":"..."}'

# Record transaction
curl -X POST http://localhost:5000/api/transactions \
  -H "Content-Type: application/json" \
  -d '{"product_id":"...","type":"ENTRY","quantity":10}'
```

## Support & Resources

- **Flask Documentation**: https://flask.palletsprojects.com
- **SQLAlchemy**: https://www.sqlalchemy.org
- **PostgreSQL**: https://www.postgresql.org
- **Supabase**: https://supabase.com

---

**GitHub**: https://github.com/Elpidio16/inventory-management  
**Environment**: Python 3.8+  
**Last Updated**: December 1, 2025
