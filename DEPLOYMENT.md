# Vercel Deployment Guide for Elpidio16

This guide walks you through deploying the Inventory Management System to Vercel with automated GitHub Actions.

## Prerequisites

- GitHub account (Elpidio16) ✓
- Vercel account (free tier available)
- PostgreSQL database (can use Railway, Supabase, or AWS RDS)
- Repository pushed to GitHub

## Step-by-Step Deployment

### Phase 1: Create Vercel Project

1. **Sign in to Vercel**
   - Go to https://vercel.com
   - Sign in with GitHub account (Elpidio16)

2. **Import Project**
   - Click "New Project"
   - Select "Import Git Repository"
   - Choose `Elpidio16/inventory-management` repository
   - Click "Import"

3. **Configure Project**
   - **Framework Preset**: Select "Next.js"
   - **Root Directory**: Leave as "/" (if at root)
   - Click "Continue"

4. **Environment Variables**
   - Add environment variable:
     - Name: `DATABASE_URL`
     - Value: Your PostgreSQL connection string
   - Click "Add"
   - Click "Deploy"

### Phase 2: Set Up GitHub Repository

1. **Initialize Local Git**
   ```bash
   cd inventory-management
   git init
   git add .
   git commit -m "Initial commit: Inventory Management System"
   ```

2. **Create GitHub Repository**
   - Go to https://github.com/new
   - Repository name: `inventory-management`
   - Description: "Inventory Management System with entries and exits tracking"
   - Set to Public (or Private)
   - Click "Create repository"

3. **Push to GitHub**
   ```bash
   git remote add origin https://github.com/Elpidio16/inventory-management.git
   git branch -M main
   git push -u origin main
   ```

### Phase 3: Configure GitHub Secrets

1. **Go to Repository Settings**
   - https://github.com/Elpidio16/inventory-management/settings

2. **Navigate to Secrets and Variables → Actions**

3. **Add Secrets**

   Create the following secrets (get values from Vercel):

   **VERCEL_TOKEN**
   - Go to https://vercel.com/account/tokens
   - Click "Create"
   - Copy the token
   - Paste in GitHub secret

   **VERCEL_ORG_ID**
   - Get from Vercel project URL: `vercel.com/elpidio16/inventory-management/settings`
   - The team/org slug is your org ID

   **VERCEL_PROJECT_ID**
   - Get from Vercel dashboard
   - Project settings → Project ID

   **DATABASE_URL**
   - Your PostgreSQL connection string
   - Format: `postgresql://user:password@host:port/database`

### Phase 4: Set Up PostgreSQL Database

#### Option A: Using Supabase (Recommended - Free Tier)

1. Go to https://supabase.com
2. Click "Start your project"
3. Sign in with GitHub
4. Create new project:
   - Name: `inventory-management`
   - Password: Generate strong password
   - Region: Choose closest to you
   - Click "Create new project"

5. Get connection string:
   - Go to Project Settings → Database
   - Copy "Connection pooling" URI
   - Use for DATABASE_URL

#### Option B: Using Railway

1. Go to https://railway.app
2. Click "Start a New Project"
3. Select "PostgreSQL"
4. Get DATABASE_URL from Variables tab

#### Option C: Local PostgreSQL

```sql
-- Create database
CREATE DATABASE inventory_db;

-- Connection string format
postgresql://user:password@localhost:5432/inventory_db
```

### Phase 5: Verify GitHub Actions Workflow

1. **Check Workflow File**
   - File: `.github/workflows/deploy.yml`
   - This will automatically run on every push to `main`

2. **Test Deployment**
   ```bash
   # Make a small change
   echo "# Updated" >> README.md
   git add .
   git commit -m "Test deployment"
   git push origin main
   ```

3. **Monitor Deployment**
   - Go to GitHub → Actions tab
   - Watch the deployment workflow
   - Should complete in 2-5 minutes

4. **Check Vercel**
   - Go to https://vercel.com/dashboard
   - Click your project
   - View deployment status and URL

### Phase 6: Run Database Migrations

1. **Push Schema to Database**
   ```bash
   npm run db:push
   ```

2. **Verify in Production** (if using Vercel):
   - The DATABASE_URL environment variable will be used automatically
   - Migrations happen during `npm run build`

## Automated Deployment Flow

```
Your Code Changes
    ↓
git push origin main
    ↓
GitHub Actions Triggered
    ↓
1. Checkout code
2. Setup Node.js
3. Install dependencies
4. Build project
5. Install Vercel CLI
6. Deploy to Vercel
    ↓
✅ Live at vercel.com/your-domain
```

## Monitoring and Management

### GitHub Actions
- https://github.com/Elpidio16/inventory-management/actions
- See all deployments
- View build logs
- Check for failures

### Vercel Dashboard
- https://vercel.com/dashboard
- Monitor performance
- View analytics
- Manage domains
- Configure settings

### Environment Variables
- Update in Vercel dashboard
- Changes take effect on next deployment
- Or redeploy current build

## Troubleshooting Deployment

### Build Fails
- Check GitHub Actions logs for errors
- Most common: Missing environment variables
- Solution: Add all required secrets to GitHub

### Database Connection Error
- Verify DATABASE_URL is correct
- Check database is accessible
- Ensure IP whitelist includes Vercel (use 0.0.0.0/0 for testing)

### Types Error After Deployment
- Run `npm run build` locally to test
- Check `tsconfig.json` is correct
- Ensure all imports are proper

### Vercel Deployment Stuck
- Check build logs in Vercel dashboard
- Trigger redeploy manually
- Check available disk space

## Production Checklist

- [ ] Database set up and accessible
- [ ] All secrets added to GitHub
- [ ] Environment variables configured in Vercel
- [ ] First deployment successful
- [ ] Application loads and works
- [ ] Database migrations applied
- [ ] Custom domain configured (optional)
- [ ] Analytics enabled in Vercel

## Custom Domain Setup (Optional)

1. In Vercel dashboard, go to Settings → Domains
2. Add your custom domain
3. Update DNS records with provided values
4. Wait for DNS propagation (5-30 minutes)

## Rollback Procedure

If deployment issues occur:

1. Go to Vercel dashboard
2. Click on project → Deployments
3. Find previous working deployment
4. Click "Promote to Production"

## Support

- Vercel Docs: https://vercel.com/docs
- Next.js Docs: https://nextjs.org/docs
- Prisma Docs: https://www.prisma.io/docs
- GitHub Actions: https://docs.github.com/actions

---

**Your Project URL**: Will be shown in Vercel dashboard after first deployment  
**Repository**: https://github.com/Elpidio16/inventory-management  
**Last Updated**: December 1, 2025
