# Migration to Neon PostgreSQL - Setup Instructions

## Step 1: Create Neon Database

1. Go to https://console.neon.tech (or create account)
2. Create a new project
3. Copy the connection string (looks like: `postgresql://user:password@host/database`)

## Step 2: Configure Vercel

1. Go to https://vercel.com/dashboard
2. Select your "inventory-management" project
3. Go to Settings → Environment Variables
4. Add new variable:
   - Name: `DATABASE_URL`
   - Value: `postgresql://user:password@host/database` (from Neon)
   - Select: Production, Preview, Development

## Step 3: Deploy

The app is ready to deploy. Just push to main:
```
git push origin main
```

Vercel will:
1. Read DATABASE_URL from environment
2. Connect to Neon PostgreSQL
3. Create tables automatically on first request
4. Your app is live!

## Important Notes

- The SQLAlchemy models in `db.py` match the JSON schema you had
- All API endpoints are identical (same request/response format)
- No frontend changes needed
- Data is now persistent in PostgreSQL instead of JSON files

## Local Development

For local testing, you can either:
- Use SQLite (current setup with sqlite:///inventory.db)
- Or set DATABASE_URL to a local PostgreSQL server
- Or use Neon's connection string locally too

## Rollback

If needed, the old JSON database code is in `database.py` (for reference).
The SQLite version is backed up as `app_sqlite.py`.
