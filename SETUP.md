# Inventory Management System - Setup Guide

This file contains initial setup instructions for the inventory management project.

## Quick Start

### 1. Install Dependencies
```bash
npm install
```

### 2. Configure Database
Create `.env.local` file in project root:
```env
DATABASE_URL=postgresql://user:password@localhost:5432/inventory_db
```

### 3. Setup Database
```bash
npm run db:push
```

### 4. Start Development Server
```bash
npm run dev
```

Visit `http://localhost:3000` to see your application.

## Available Scripts

- `npm run dev` - Start development server
- `npm run build` - Build for production
- `npm run start` - Start production server
- `npm run lint` - Run ESLint
- `npm run db:push` - Push schema changes to database
- `npm run db:studio` - Open Prisma Studio for data management

## Application Features

✅ **Inventory Dashboard**
- View total products, inventory quantity, and inventory value
- See products organized by categories with pricing

✅ **Product Management**
- Add new products with SKU, price, and category
- Organize products by categories

✅ **Transaction Tracking**
- Record product entries (incoming inventory)
- Record product exits (sales)
- Track transaction history with reasons and notes

## Project Structure

```
src/
├── app/
│   ├── api/                  # API routes
│   │   ├── categories/       # Category management
│   │   ├── products/         # Product CRUD
│   │   ├── transactions/     # Transaction recording
│   │   └── inventory/stats/  # Analytics
│   ├── page.tsx              # Main page with tabs
│   ├── layout.tsx            # Root layout
│   └── globals.css           # Tailwind styles
├── components/
│   ├── Dashboard.tsx         # Stats and overview
│   ├── ProductForm.tsx       # Add product form
│   └── TransactionForm.tsx   # Record transaction
└── lib/
    └── prisma.ts             # Prisma client

prisma/
└── schema.prisma             # Database schema

.github/workflows/
└── deploy.yml                # GitHub Actions for Vercel
```

## Database Schema

The application uses PostgreSQL with these main models:

- **Product**: Items in inventory
- **Category**: Product groupings
- **Inventory**: Current stock levels
- **Transaction**: Entry/Exit records

See `prisma/schema.prisma` for full details.

## Deployment

For Vercel deployment with GitHub Actions:

1. See `DEPLOYMENT.md` for detailed instructions
2. Requires: Vercel account, GitHub (Elpidio16), PostgreSQL

Quick summary:
- Push to GitHub main branch
- GitHub Actions triggers automatically
- Deploys to Vercel
- Database updates via environment variables

## Troubleshooting

### Dependencies not installing
```bash
rm -rf node_modules package-lock.json
npm install
```

### Database connection failing
- Check DATABASE_URL is correct
- Ensure PostgreSQL is running
- Verify database exists

### Compilation errors
```bash
npm run build
```

## Next Steps

1. ✅ Complete initial setup (npm install, database setup)
2. ✅ Test locally (npm run dev)
3. ✅ Create GitHub repository
4. ✅ Set up Vercel project
5. ✅ Configure GitHub Secrets
6. ✅ Push to GitHub and deploy

## Additional Resources

- **Next.js**: https://nextjs.org/docs
- **Prisma**: https://www.prisma.io/docs
- **Vercel**: https://vercel.com/docs
- **Tailwind CSS**: https://tailwindcss.com/docs

---

**GitHub**: https://github.com/Elpidio16/inventory-management
**Deployment**: See DEPLOYMENT.md
