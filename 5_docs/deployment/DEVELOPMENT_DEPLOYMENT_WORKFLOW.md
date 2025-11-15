# Development & Deployment Workflow

**Purpose**: Establish a proper local → CI/CD → production workflow

---

## 🔄 Current vs. Proper Workflow

### ❌ Current State (Inconsistent)
```
Developer ──┬──> Local Changes
            │
            ├──> Direct SSH Edits on Remote Server ⚠️
            │
            └──> Manual file copies via SCP ⚠️

Result: Code out of sync, hardcoded values, no testing
```

### ✅ Proper Workflow (What We're Implementing)
```
1. Local Development (Your Mac)
   ├── Write code
   ├── Write tests
   ├── Run tests locally
   └── Commit to Git

2. Git Push to GitHub
   ↓

3. CI/CD Pipeline (GitHub Actions)
   ├── Run automated tests
   ├── Check linting
   ├── Build verification
   └── Generate coverage reports

4. If Tests Pass → Auto-Deploy to Production
   ├── SSH to remote server
   ├── Pull latest code
   ├── Run migrations
   ├── Restart services
   └── Health check

5. Monitor & Verify
   └── Check health endpoints
```

---

## 🚀 Step-by-Step Setup

### Step 1: Set Up GitHub Secrets

Go to your GitHub repository:
1. Navigate to **Settings** → **Secrets and variables** → **Actions**
2. Add these secrets:

```
PRODUCTION_HOST       = 20.84.160.240
PRODUCTION_USER       = connectme
SSH_PRIVATE_KEY       = [Contents of ~/Documents/Access/cursor/id_rsa_Debian]
```

To get SSH private key:
```bash
cat ~/Documents/Access/cursor/id_rsa_Debian
# Copy entire output including BEGIN and END lines
```

### Step 2: Initialize Git Repositories (If Not Already)

**Backend:**
```bash
cd connectme-backend
git init
git remote add origin git@github.com:a-greenapple/connectme-backend.git
git add .
git commit -m "Initial commit with tests and CI/CD"
git push -u origin main
```

**Frontend:**
```bash
cd connectme-frontend
git init
git remote add origin git@github.com:a-greenapple/connectme-frontend.git
git add .
git commit -m "Initial commit with tests and CI/CD"
git push -u origin main
```

### Step 3: Verify GitHub Actions Work

After pushing, check:
- Go to **Actions** tab in GitHub
- Verify workflows run automatically
- Check test results

---

## 📝 Daily Development Workflow

### Making Changes

```bash
# 1. Start on your Mac
cd /Users/ssiva/Documents/1_Data/AI/abce/connectme

# 2. Create a feature branch (recommended)
git checkout -b feature/my-new-feature

# 3. Make your changes
# Edit files in connectme-backend/ or connectme-frontend/

# 4. Run tests locally
cd connectme-backend
pytest
# or
cd connectme-frontend
npm test

# 5. If tests pass, commit
git add .
git commit -m "Add new feature: description"

# 6. Push to GitHub
git push origin feature/my-new-feature

# 7. GitHub Actions automatically:
#    - Runs tests
#    - Checks linting
#    - Builds code

# 8. Create Pull Request on GitHub
#    - Review changes
#    - Wait for CI checks ✅
#    - Merge to main

# 9. Auto-deployment (if configured)
#    - Merging to main triggers deployment
#    - Or add [deploy-backend] or [deploy-frontend] in commit message
```

### Deployment Triggers

**Automatic Deployment:**
```bash
# Deploy backend when merging to main
git commit -m "[deploy-backend] Fix bug in claims search"

# Deploy frontend when merging to main
git commit -m "[deploy-frontend] Update bulk upload UI"

# Deploy both
git commit -m "[deploy-backend][deploy-frontend] Update API and UI"
```

**Manual Deployment:**
- Go to GitHub → Actions → Deploy to Production
- Click "Run workflow" → Select branch → Run

---

## 🧪 Testing Before Deployment

### Local Testing (Required)

**Backend:**
```bash
cd connectme-backend
source venv/bin/activate

# Run all tests
pytest

# Run specific tests
pytest apps/claims/tests/test_api.py

# Run with coverage
pytest --cov=apps --cov-report=html

# Check if coverage meets threshold (70%+)
```

**Frontend:**
```bash
cd connectme-frontend

# Run tests
npm test

# Run with coverage
npm test -- --coverage

# Build test
npm run build
```

### CI Testing (Automatic)

When you push to GitHub:
1. **Backend Tests** workflow runs
   - PostgreSQL & Redis services start
   - Tests run with coverage
   - Results shown in PR

2. **Frontend Tests** workflow runs
   - Jest tests run
   - Build verification
   - Coverage uploaded

---

## 🔒 Environment Variables

### Local Development

**Backend (.env.local):**
```env
DEBUG=True
SECRET_KEY=local-dev-secret-key
DATABASE_URL=postgresql://user:pass@localhost:5432/connectme
REDIS_URL=redis://localhost:6379/0
```

**Frontend (.env.local):**
```env
NEXT_PUBLIC_API_BASE_URL=http://localhost:8000
NEXT_PUBLIC_API_URL=http://localhost:8000
```

### Production (Already on Server)

**Backend (.env):**
```env
DEBUG=False
SECRET_KEY=[from server]
DATABASE_URL=postgresql://...
ALLOWED_HOSTS=connectme.be.totesoft.com,20.84.160.240
```

**Frontend (.env.production):**
```env
NEXT_PUBLIC_API_BASE_URL=https://connectme.be.totesoft.com
NEXT_PUBLIC_API_URL=https://connectme.be.totesoft.com
```

---

## 📊 CI/CD Pipeline Details

### Workflows Created

1. **`.github/workflows/backend-tests.yml`**
   - Runs on: Push to main/develop, PRs
   - Services: PostgreSQL, Redis
   - Steps: Install deps, lint, test, coverage
   - Triggers: Backend file changes

2. **`.github/workflows/frontend-tests.yml`**
   - Runs on: Push to main/develop, PRs
   - Steps: Install deps, lint, test, build
   - Triggers: Frontend file changes

3. **`.github/workflows/deploy-production.yml`**
   - Runs on: Push to main (with deploy flag) or manual trigger
   - Jobs: Deploy backend, deploy frontend, health check
   - Uses SSH to connect to production server

### Pipeline Flow

```
Code Push
    ↓
GitHub detects push
    ↓
Trigger appropriate workflow(s)
    ↓
┌─────────────────┐
│ Backend Tests   │  (if backend files changed)
│ • PostgreSQL    │
│ • Redis         │
│ • Pytest        │
│ • Coverage      │
└─────────────────┘
    ↓
┌─────────────────┐
│ Frontend Tests  │  (if frontend files changed)
│ • Jest          │
│ • Build test    │
│ • Coverage      │
└─────────────────┘
    ↓
All Tests Pass? ──No──> ❌ Stop, fix issues
    │
    Yes
    ↓
Deploy to Production (if main branch + deploy flag)
    ↓
Health Check
    ↓
✅ Complete
```

---

## 🛠️ Sync Local with Remote (One-Time)

Since we've been editing both locally and remotely, let's sync:

```bash
# 1. On your Mac, commit all local changes
cd /Users/ssiva/Documents/1_Data/AI/abce/connectme/connectme-backend
git add .
git commit -m "Sync local changes with remote"
git push origin main

cd /Users/ssiva/Documents/1_Data/AI/abce/connectme/connectme-frontend
git add .
git commit -m "Sync local changes with remote"
git push origin main

# 2. On remote server, pull latest from GitHub
ssh -i ~/Documents/Access/cursor/id_rsa_Debian connectme@20.84.160.240

cd /var/www/connectme-backend
git fetch origin
git reset --hard origin/main

cd /var/www/connectme-frontend
git fetch origin
git reset --hard origin/main
npm install
npm run build
pm2 restart connectme-frontend

# 3. From now on, ALWAYS develop locally first!
```

---

## 📁 .gitignore (Important!)

Make sure these files are NOT committed:

**Backend:**
```gitignore
# Python
*.pyc
__pycache__/
venv/
.env
.env.local

# Django
db.sqlite3
media/
staticfiles/
logs/

# IDE
.vscode/
.idea/

# OS
.DS_Store
```

**Frontend:**
```gitignore
# Dependencies
node_modules/

# Next.js
.next/
out/

# Environment
.env.local
.env.production.local

# IDE
.vscode/
.idea/

# OS
.DS_Store
```

---

## 🔍 Monitoring & Debugging

### Check CI/CD Status

**On GitHub:**
- Go to **Actions** tab
- See all workflow runs
- Click on any run to see details
- View logs for each step

**Health Checks:**
```bash
# Backend
curl https://connectme.be.totesoft.com/health/

# Frontend
curl https://connectme.apps.totesoft.com/
```

### View Remote Logs

```bash
# SSH to server
ssh -i ~/Documents/Access/cursor/id_rsa_Debian connectme@20.84.160.240

# Backend logs
tail -f /var/www/connectme-backend/logs/gunicorn-error.log

# Celery logs
tail -f /var/log/celery/celery.service.log

# Frontend logs
pm2 logs connectme-frontend
```

---

## ✅ Checklist for Each Change

Before pushing to production:

- [ ] Code written locally (on your Mac)
- [ ] Tests written and passing locally
- [ ] Linting passes (`flake8` for backend, `npm run lint` for frontend)
- [ ] Environment variables correct (no hardcoded URLs)
- [ ] Committed to feature branch
- [ ] Pushed to GitHub
- [ ] CI tests passing (green checkmarks)
- [ ] Pull request created and reviewed
- [ ] Merged to main with deploy flag (if needed)
- [ ] Deployment successful
- [ ] Health check passes
- [ ] Verified on production

---

## 🎯 Benefits of This Workflow

1. **Consistency**: All environments use same code from Git
2. **Quality**: Tests run automatically before deployment
3. **Safety**: Can't deploy broken code
4. **Traceability**: Every change tracked in Git
5. **Rollback**: Easy to revert if something breaks
6. **Collaboration**: Multiple developers can work safely
7. **Documentation**: Git history shows what changed and why

---

## 📚 Quick Reference Commands

```bash
# Local development
git checkout -b feature/my-feature
# ... make changes ...
pytest  # or npm test
git commit -m "Description"
git push

# Deploy to production
git commit -m "[deploy-backend] Description"
git push origin main

# Sync local with remote
git pull origin main

# Check deployment status
# Go to: https://github.com/a-greenapple/connectme-backend/actions
```

---

**Status**: CI/CD Pipeline Ready ✅  
**Next Step**: Set up GitHub secrets and test first deployment!  
**Documentation**: Complete

