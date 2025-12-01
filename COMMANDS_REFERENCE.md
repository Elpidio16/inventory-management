# Flask Inventory Management - Command Reference

Quick reference for all commands and operations.

## Setup Commands

### 1. Initial Setup
```bash
# Navigate to project
cd c:\Users\ElpidioLissassi\Documents\PROJET

# Create virtual environment
python -m venv venv

# Activate virtual environment
venv\Scripts\activate
```

### 2. Install Dependencies
```bash
pip install -r requirements.txt
```

### 3. Configure Database
```bash
# Create .env file with:
DATABASE_URL=postgresql://user:password@localhost:5432/inventory_db
FLASK_ENV=development
```

### 4. Initialize Database
```bash
# Create tables and load sample data
python init_db.py
```

## Development Commands

### Run Development Server
```bash
python app.py
```

Browser: http://localhost:5000

### Run with Specific Port
```bash
# In app.py, change port:
app.run(debug=True, port=5001)
```

### Check Dependencies
```bash
pip list
```

### Update Dependencies
```bash
pip install -r requirements.txt --upgrade
```

## Database Commands

### Reset Database (SQLite)
```bash
del inventory.db
python init_db.py
```

### Reset Database (PostgreSQL)
```bash
# In PostgreSQL CLI:
DROP DATABASE inventory_db;
CREATE DATABASE inventory_db;

# Then:
python init_db.py
```

### Connect to Database
```bash
# PostgreSQL
psql -U postgres -d inventory_db

# SQLite
sqlite3 inventory.db
```

## Git/GitHub Commands

### Initialize Git
```bash
git init
git add .
git commit -m "Initial commit: Flask Inventory Management"
```

### Connect to GitHub
```bash
git remote add origin https://github.com/Elpidio16/inventory-management.git
git branch -M main
git push -u origin main
```

### Push Changes
```bash
git add .
git commit -m "Your commit message"
git push origin main
```

## Production Commands

### Install Production Server
```bash
pip install gunicorn
```

### Run with Gunicorn
```bash
gunicorn app:app --bind 0.0.0.0:5000
```

### Build for Production
```bash
pip freeze > requirements.txt
```

## Docker Commands (Optional)

### Build Docker Image
```bash
docker build -t inventory-management .
```

### Run Docker Container
```bash
docker run -e DATABASE_URL=postgresql://... \
  -p 5000:5000 \
  inventory-management
```

## Testing Commands

### Test API Endpoints
```bash
# Get all categories
curl http://localhost:5000/api/categories

# Get all products
curl http://localhost:5000/api/products

# Get inventory stats
curl http://localhost:5000/api/inventory/stats

# Create category
curl -X POST http://localhost:5000/api/categories \
  -H "Content-Type: application/json" \
  -d '{"name":"Electronics","description":"Electronic devices"}'

# Create product
curl -X POST http://localhost:5000/api/products \
  -H "Content-Type: application/json" \
  -d '{
    "name":"Laptop",
    "sku":"LAPTOP001",
    "price":999.99,
    "category_id":"<category_id>"
  }'

# Record transaction
curl -X POST http://localhost:5000/api/transactions \
  -H "Content-Type: application/json" \
  -d '{
    "product_id":"<product_id>",
    "type":"ENTRY",
    "quantity":10,
    "reason":"Purchase Order"
  }'
```

## Virtual Environment Commands

### List Installed Packages
```bash
pip list
```

### Freeze Dependencies
```bash
pip freeze > requirements.txt
```

### Install Specific Version
```bash
pip install Flask==3.0.0
```

### Uninstall Package
```bash
pip uninstall package_name
```

### Deactivate Virtual Environment
```bash
deactivate
```

## File Management Commands

### List Files
```bash
# Windows
dir

# Windows (tree view)
tree /F

# Show specific files
dir *.py
dir routes\
```

### Create Directories
```bash
mkdir templates
mkdir static
mkdir routes
```

### View File Contents
```bash
type app.py
type requirements.txt
```

## Environment Variable Commands

### View Environment Variables
```bash
# Windows
echo %DATABASE_URL%

# Linux/macOS
echo $DATABASE_URL
```

### Set Temporary Environment Variable
```bash
# Windows
set DATABASE_URL=postgresql://localhost/inventory_db

# Linux/macOS
export DATABASE_URL=postgresql://localhost/inventory_db
```

## Troubleshooting Commands

### Check Python Version
```bash
python --version
```

### Check pip Version
```bash
pip --version
```

### Verify Virtual Environment
```bash
which python  # Linux/macOS
where python  # Windows
```

### Clear pip Cache
```bash
pip cache purge
```

### Reinstall all Dependencies
```bash
pip install --force-reinstall -r requirements.txt
```

### Check Flask Installation
```bash
python -c "import flask; print(flask.__version__)"
```

### Debug Mode
```python
# In app.py:
app.run(debug=True)  # Enables auto-reload and error pages
```

## Deployment Commands

### Deploy to Vercel
```bash
# Install Vercel CLI
npm install -g vercel

# Login
vercel login

# Deploy
vercel --prod
```

### GitHub Actions Test
```bash
# Push to main to trigger workflow
git push origin main

# View logs at:
# https://github.com/Elpidio16/inventory-management/actions
```

## Useful Tool Commands

### Text Editor (VS Code)
```bash
# Open current directory
code .

# Open specific file
code app.py
```

### PostgreSQL Commands
```bash
# Connect to database
psql -U postgres

# List databases
\l

# Connect to database
\c inventory_db

# List tables
\dt

# Quit
\q
```

## Common Workflows

### Complete Development Setup
```bash
cd c:\Users\ElpidioLissassi\Documents\PROJET
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
python init_db.py
python app.py
```

### Update and Deploy
```bash
venv\Scripts\activate
pip install -r requirements.txt
python app.py  # Test locally

git add .
git commit -m "Update: [description]"
git push origin main
# GitHub Actions will auto-deploy to Vercel
```

### Reset Everything
```bash
deactivate
rmdir /s venv
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
python init_db.py
python app.py
```

## Help Commands

### Flask Help
```bash
flask --help
```

### Pip Help
```bash
pip help
```

### Python Help
```bash
python --help
```

---

**Updated**: December 1, 2025  
**Framework**: Flask 3.0.0  
**Language**: Python 3.8+
