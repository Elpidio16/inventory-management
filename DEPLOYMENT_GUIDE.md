# Deployment Guide: GitHub & Vercel

## Step 1: Initialize Git Repository

```powershell
cd c:\Users\ElpidioLissassi\Documents\PROJET
git init
git config user.name "Elpidio16"
git config user.email "your-email@example.com"
```

## Step 2: Create .gitignore (if not exists)

The project already has a `.gitignore` file configured.

## Step 3: Add Files to Git

```powershell
git add .
git commit -m "Initial commit: Flask Inventory Management App"
```

## Step 4: Create GitHub Repository

1. Go to https://github.com/new
2. Create a new repository named: **inventory-management**
3. Set it to Public
4. Do NOT initialize with README (we already have one)
5. Click "Create repository"

## Step 5: Push to GitHub

```powershell
# Add the remote repository (replace with your repository URL)
git remote add origin https://github.com/Elpidio16/inventory-management.git

# Rename branch to main if needed
git branch -M main

# Push to GitHub
git push -u origin main
```

You'll be prompted for authentication:
- Use your GitHub username
- Use a Personal Access Token (PAT) as password
  - Go to https://github.com/settings/tokens
  - Create a new token with `repo` scope
  - Copy and paste it when prompted

## Step 6: Deploy to Vercel

### Option A: Using Vercel CLI (Recommended)

```powershell
# Install Vercel CLI globally (one time)
npm install -g vercel

# Navigate to project
cd c:\Users\ElpidioLissassi\Documents\PROJET

# Deploy
vercel
```

When prompted:
- Set project name: `inventory-management`
- Framework preset: `Other`
- Root directory: `./`
- Build command: (leave empty or use: `python init_db.py`)
- Output directory: (leave empty)

### Option B: Connect GitHub to Vercel (Easiest)

1. Go to https://vercel.com
2. Sign in with GitHub
3. Click "New Project"
4. Select your `inventory-management` repository
5. Configure:
   - Framework Preset: `Other`
   - Root Directory: `./`
   - Environment Variables:
     - `FLASK_ENV`: `production`
     - `DATABASE_URL`: `sqlite:///inventory.db` (or your database URL)
6. Click "Deploy"

Vercel will automatically:
- Deploy whenever you push to GitHub
- Run your app on a live URL (e.g., `inventory-management.vercel.app`)

## Step 7: Update vercel.json

The `vercel.json` file is already configured for Python/Flask deployment:

```json
{
  "buildCommand": "pip install -r requirements.txt",
  "outputDirectory": ".",
  "framework": "python",
  "env": {
    "FLASK_ENV": "production"
  }
}
```

## Testing Deployment

After deployment:
1. Visit your Vercel URL
2. Test the API endpoints:
   - `GET /api/health`
   - `POST /api/categories`
   - `POST /api/products`
   - `POST /api/transactions`

## Troubleshooting

If deployment fails:
1. Check Vercel build logs at https://vercel.com/dashboard
2. Ensure `requirements.txt` has all dependencies
3. Verify environment variables are set
4. Check that `app.py` starts correctly: `python app.py`

## Auto-Deployment

Once connected, every push to GitHub automatically triggers:
1. Code pulled from GitHub
2. Dependencies installed (`pip install -r requirements.txt`)
3. App deployed to Vercel
4. Live URL updated with new version

No manual deployment needed after initial setup!
