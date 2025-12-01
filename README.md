# 📦 Inventory Management System

A comprehensive inventory management application to track product entries, exits, and maintain an organized inventory system.

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

- **Frontend**: Next.js 15 with React 19, TypeScript, Tailwind CSS
- **Backend**: Next.js API Routes with TypeScript
- **Database**: PostgreSQL with Prisma ORM
- **Deployment**: Vercel with GitHub Actions CI/CD
- **Charts**: Recharts for data visualization

## Project Structure

```
inventory-management/
├── src/
│   ├── app/
│   │   ├── api/
│   │   │   ├── categories/        # Category management API
│   │   │   ├── products/          # Product management API
│   │   │   ├── transactions/      # Transaction recording API
│   │   │   └── inventory/
│   │   │       └── stats/         # Inventory analytics API
│   │   ├── layout.tsx             # Root layout with navigation
│   │   ├── page.tsx               # Main dashboard page
│   │   └── globals.css            # Global styles
│   ├── components/
│   │   ├── Dashboard.tsx          # Main dashboard component
│   │   ├── ProductForm.tsx        # Add product form
│   │   └── TransactionForm.tsx    # Record transaction form
│   └── lib/
│       └── prisma.ts              # Prisma client configuration
├── prisma/
│   └── schema.prisma              # Database schema
├── .github/
│   └── workflows/
│       └── deploy.yml             # Vercel deployment workflow
├── .env.example                   # Environment variables template
├── package.json                   # Dependencies and scripts
├── tsconfig.json                  # TypeScript configuration
└── README.md                      # This file
```

## Database Schema

### Models

**Category**
- id: String (Primary Key)
- name: String (Unique)
- description: String
- products: Product[]
- timestamps

**Product**
- id: String (Primary Key)
- name: String
- description: String
- sku: String (Unique)
- price: Float
- categoryId: String (Foreign Key)
- inventory: Inventory
- transactions: Transaction[]
- timestamps

**Inventory**
- id: String (Primary Key)
- productId: String (Unique, Foreign Key)
- quantity: Int
- lastUpdated: DateTime

**Transaction**
- id: String (Primary Key)
- productId: String (Foreign Key)
- type: TransactionType (ENTRY | EXIT)
- quantity: Int
- reason: String
- notes: String
- timestamps

## Setup Instructions

### 1. Prerequisites

- Node.js >= 18.0.0
- PostgreSQL database
- npm or yarn package manager
- Vercel account (for deployment)
- GitHub account (Elpidio16)

### 2. Installation

```bash
# Clone the repository
git clone https://github.com/Elpidio16/inventory-management.git
cd inventory-management

# Install dependencies
npm install

# Install Prisma CLI
npm install -D prisma @prisma/client
```

### 3. Environment Setup

Create a `.env` file with your configuration:

```env
# Database
DATABASE_URL=postgresql://user:password@localhost:5432/inventory_db

# Vercel (optional, for deployment)
VERCEL_TOKEN=your_vercel_token_here
VERCEL_ORG_ID=your_org_id
VERCEL_PROJECT_ID=your_project_id
```

### 4. Database Setup

```bash
# Push schema to database
npm run db:push

# (Optional) Open Prisma Studio to manage data
npm run db:studio
```

### 5. Development

```bash
# Start development server
npm run dev

# Open http://localhost:3000 in your browser
```

## API Endpoints

### Categories
- `GET /api/categories` - List all categories
- `POST /api/categories` - Create a new category

### Products
- `GET /api/products` - List all products
- `POST /api/products` - Create a new product

### Transactions
- `GET /api/transactions` - List all transactions
- `POST /api/transactions` - Record a new transaction (entry or exit)

### Inventory Analytics
- `GET /api/inventory/stats` - Get inventory statistics and summaries

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

## GitHub Deployment Setup

### 1. Connect Repository to Vercel

```bash
# Initialize git repository
git init
git add .
git commit -m "Initial commit: Inventory Management System"

# Add GitHub remote
git remote add origin https://github.com/Elpidio16/inventory-management.git
git branch -M main
git push -u origin main
```

### 2. Configure GitHub Secrets

In your GitHub repository, add these secrets (Settings → Secrets and variables → Actions):

```
VERCEL_TOKEN          # Get from Vercel account settings
VERCEL_ORG_ID         # Your Vercel organization ID
VERCEL_PROJECT_ID     # Your Vercel project ID
DATABASE_URL          # Your PostgreSQL connection string
```

### 3. Automatic Deployment

The GitHub Actions workflow will:
- ✅ Trigger on every push to `main` branch
- ✅ Install dependencies
- ✅ Build the project
- ✅ Deploy to Vercel automatically
- ✅ Provide preview URLs for pull requests

## Build and Deployment

```bash
# Build for production
npm run build

# Start production server locally
npm start

# Lint code
npm run lint
```

## Troubleshooting

### Database Connection Issues
- Verify DATABASE_URL is correct
- Check PostgreSQL is running
- Ensure database exists

### Deployment Failures
- Check GitHub Actions logs
- Verify all secrets are set correctly
- Ensure NODE_ENV is production during build

### Missing Dependencies
```bash
npm install
npm install -D prisma @prisma/client
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

## License

MIT

## Support

For issues or questions, create an issue in the GitHub repository.

---

**Created for**: Elpidio16  
**Last Updated**: December 1, 2025
