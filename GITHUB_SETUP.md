# GitHub & Vercel Setup Instructions for Elpidio16

Complete guide to set up your GitHub repository and deploy to Vercel.

## Step 1: Initialize Local Git Repository

```bash
cd c:\Users\ElpidioLissassi\Documents\PROJET

# Initialize git
git init

# Add all files
git add .

# Initial commit
git commit -m "Initial commit: Inventory Management System"
```

## Step 2: Create GitHub Repository

1. Go to https://github.com/new
2. Fill in details:
   - **Owner**: Elpidio16 (your account)
   - **Repository name**: `inventory-management`
   - **Description**: "Inventory Management System with entries and exits tracking"
   - **Visibility**: Public (or Private if preferred)
   - **Initialize with**: No (we already have files)
3. Click **Create repository**

## Step 3: Connect Local Repository to GitHub

```bash
# Add remote (replace ELPIDIO16 with your actual GitHub username if different)
git remote add origin https://github.com/Elpidio16/inventory-management.git

# Rename branch to main (if still on master)
git branch -M main

# Push code to GitHub
git push -u origin main
```

## Step 4: Set Up PostgreSQL Database

Choose one option:

### Option A: Supabase (Recommended - Free)
1. Go to https://supabase.com
2. Sign in with GitHub account (Elpidio16)
3. Create new project → Select PostgreSQL
4. Go to Settings → Database
5. Copy "Connection pooling" URI
6. Save for Step 6

### Option B: Railway
1. Go to https://railway.app
2. New Project → PostgreSQL
3. Get DATABASE_URL from Variables
4. Save for Step 6

### Option C: Local PostgreSQL
```sql
-- Create database
CREATE DATABASE inventory_db;

-- Connection string
postgresql://user:password@localhost:5432/inventory_db
```

## Step 5: Create Vercel Project

1. Go to https://vercel.com
2. Sign in with GitHub (use Elpidio16 account)
3. Click **Add New** → **Project**
4. Select **Import Git Repository**
5. Choose `Elpidio16/inventory-management`
6. Click **Import**
7. Configuration:
   - Framework Preset: **Next.js**
   - Root Directory: **/** (leave default)
8. Click **Continue**

## Step 6: Add Environment Variables to Vercel

In Vercel project settings, add:

**Name**: `DATABASE_URL`  
**Value**: Your PostgreSQL connection string from Step 4

Example:
```
postgresql://username:password@host:5432/database_name
```

Click **Add** and then **Deploy**

## Step 7: Configure GitHub Secrets

1. Go to: https://github.com/Elpidio16/inventory-management/settings
2. Click **Secrets and variables** → **Actions**
3. Click **New repository secret**

Add these 4 secrets:

### Secret 1: VERCEL_TOKEN
1. Go to https://vercel.com/account/tokens
2. Click **Create Token**
3. Name it: `github-deployment`
4. Copy the token
5. In GitHub:
   - Name: `VERCEL_TOKEN`
   - Secret: (paste token)
   - Click **Add secret**

### Secret 2: VERCEL_ORG_ID
1. In Vercel, go to Settings (top right) → Account
2. Under "Team/Organization ID", copy the ID
3. In GitHub:
   - Name: `VERCEL_ORG_ID`
   - Secret: (paste ID)
   - Click **Add secret**

### Secret 3: VERCEL_PROJECT_ID
1. In Vercel project settings, find **Project ID**
2. In GitHub:
   - Name: `VERCEL_PROJECT_ID`
   - Secret: (paste ID)
   - Click **Add secret**

### Secret 4: DATABASE_URL
1. Use same value from Step 6
2. In GitHub:
   - Name: `DATABASE_URL`
   - Secret: (paste connection string)
   - Click **Add secret**

## Step 8: Test Deployment

```bash
# Make a small test change
echo "# Test deployment" >> README.md

# Commit and push
git add README.md
git commit -m "Test: Trigger GitHub Actions"
git push origin main
```

## Step 9: Monitor Deployment

1. **GitHub Actions**:
   - Go to: https://github.com/Elpidio16/inventory-management/actions
   - Watch the deployment workflow run
   - Should complete in 2-5 minutes

2. **Vercel Dashboard**:
   - Go to: https://vercel.com/dashboard
   - Click on `inventory-management` project
   - View live deployment URL
   - Check deployment logs

## Step 10: Initialize Database

Once deployed, run migrations:

```bash
npm run db:push
```

Or from any Next.js API route (runs automatically on build).

## Verification Checklist

- [ ] Repository created on GitHub (Elpidio16)
- [ ] Code pushed to `main` branch
- [ ] PostgreSQL database created and accessible
- [ ] Vercel project created
- [ ] DATABASE_URL added to Vercel environment
- [ ] All 4 GitHub secrets configured
- [ ] GitHub Actions workflow completed successfully
- [ ] Application deployed to Vercel URL
- [ ] Can access at `https://your-project.vercel.app`

## Automatic Deployment from Now On

Every time you push to the `main` branch:

```bash
git add .
git commit -m "Your changes"
git push origin main
```

The GitHub Actions workflow will automatically:
1. Run tests and build
2. Deploy to Vercel
3. Your changes go live in seconds

## Useful Links

- **Your GitHub Repo**: https://github.com/Elpidio16/inventory-management
- **Your Vercel Dashboard**: https://vercel.com/dashboard
- **GitHub Actions**: https://github.com/Elpidio16/inventory-management/actions
- **Deployment Guide**: See DEPLOYMENT.md in project root

## Troubleshooting

### GitHub push fails
```bash
# Verify remote URL
git remote -v

# Update if needed
git remote remove origin
git remote add origin https://github.com/Elpidio16/inventory-management.git
```

### Actions workflow fails
- Check GitHub Secrets are all set
- Verify DATABASE_URL is correct
- Check Vercel project is connected

### Deployment doesn't start
- Wait a moment for Actions to trigger
- Refresh the Actions page
- Check for any error messages

### Can't access deployed site
- Wait 1-2 minutes for Vercel to build
- Check Vercel dashboard for errors
- Verify environment variables in Vercel

## Support

- **Vercel Help**: https://vercel.com/support
- **GitHub Docs**: https://docs.github.com
- **Next.js Community**: https://nextjs.org/community

---

**Project**: Inventory Management System  
**GitHub User**: Elpidio16  
**Created**: December 1, 2025
