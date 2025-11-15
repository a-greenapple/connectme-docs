# Git Branching Strategy for ConnectMe

## Overview

Implementing a two-branch deployment strategy:
- **`main`** → Pre-Production (active development, continuous testing)
- **`prod`** → Production (stable, production-ready code)

## Branch Structure

```
main (default branch)
├── Feature branches merge here
├── CI runs on every push
├── Auto-deploys to pre-prod (after CI passes)
└── Merge to prod → triggers production deployment

prod (production branch)
├── Only receives merges from main (via PR)
├── CI runs on PR
├── Auto-deploys to production on merge
└── Protected branch (requires PR approval)
```

## Workflow

### Development Cycle
1. **Develop on `main`** or feature branches
2. **CI runs** automatically on push to `main`
3. **Deploy to pre-prod** (manual or automatic after CI passes)
4. **Test in pre-prod** environment
5. **Create PR** from `main` to `prod` when ready for production
6. **Review & approve** PR
7. **Merge to `prod`** triggers production deployment

### Hotfix Cycle
1. **Branch from `prod`** for urgent fixes
2. **Create PR** to `prod`
3. **After production deployment**, merge `prod` back to `main` to sync

## Implementation Plan

### Step 1: Create `prod` Branch
```bash
cd /Users/ssiva/Documents/1_Data/AI/abce/connectme-backend
git checkout -b prod
git push -u origin prod
```

### Step 2: Update Workflows

#### A. Pre-Prod Deployment (main branch)
- Trigger: Push to `main` or manual
- Target: Pre-production environment

#### B. Production Deployment (prod branch)
- Trigger: Push to `prod` (after PR merge)
- Target: Production environment
- Requires: All CI checks pass

### Step 3: Configure Branch Protection

#### For `prod` branch:
- Require pull request reviews (1+ approvals)
- Require status checks to pass (CI must be green)
- Require branches to be up to date
- No direct pushes (only via PR)

#### For `main` branch (optional):
- Require status checks to pass (CI must be green)
- Allow direct pushes (for faster development)

## Current State Analysis

### What's Currently in GitHub
- **Branch:** `main`
- **Contains:** CI/CD workflows, updated dependencies
- **Missing:** New features (RBAC, API docs, audit logging, etc.)

### What's in Local Workspace
- **Location:** `/Users/ssiva/Documents/1_Data/AI/abce/connectme/connectme-backend/`
- **Contains:** All new features not yet pushed

### What's in Production
- **Likely:** Older version of `main` without recent CI/CD updates
- **Status:** Out of sync with current `main`

## Recommended Actions

### Option A: Create `prod` from Current Production Server
**Best if production is stable and you want to preserve its exact state**

```bash
# 1. SSH to production server
ssh user@production-server

# 2. Check current commit
cd /var/www/connectme-backend
git log -1 --oneline

# 3. Note the commit SHA, then locally:
cd /Users/ssiva/Documents/1_Data/AI/abce/connectme-backend
git fetch origin
git checkout -b prod <production-commit-sha>
git push -u origin prod
```

### Option B: Create `prod` from Current `main` (Recommended)
**Best if you want to start fresh with current CI/CD setup**

```bash
# 1. Create prod branch from current main
cd /Users/ssiva/Documents/1_Data/AI/abce/connectme-backend
git checkout main
git pull origin main
git checkout -b prod
git push -u origin prod

# 2. Set main as default branch for development
git checkout main
```

### Option C: Create `prod` from Last Stable Commit
**Best if recent commits on main are experimental**

```bash
# 1. Find last stable commit
cd /Users/ssiva/Documents/1_Data/AI/abce/connectme-backend
git log --oneline -10

# 2. Create prod from that commit
git checkout -b prod <stable-commit-sha>
git push -u origin prod

# 3. Return to main
git checkout main
```

## Deployment Workflows

### Pre-Production Workflow (`.github/workflows/deploy-preprod.yml`)
```yaml
name: Deploy Pre-Prod

on:
  push:
    branches: [ main ]  # Auto-deploy on push to main
  workflow_dispatch:    # Or manual trigger

jobs:
  deploy:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - name: Deploy to Pre-Prod
        # ... deployment steps
```

### Production Workflow (`.github/workflows/deploy-prod.yml`)
```yaml
name: Deploy Production

on:
  push:
    branches: [ prod ]  # Auto-deploy on merge to prod

jobs:
  deploy:
    runs-on: ubuntu-latest
    environment:
      name: production
      url: https://connectme.be.totessoft.com
    steps:
      - uses: actions/checkout@v4
      - name: Deploy to Production
        # ... deployment steps
```

## Branch Protection Rules

### Configure via GitHub CLI
```bash
# Protect prod branch
gh api repos/a-greenapple/connectme-backend/branches/prod/protection \
  --method PUT \
  --field required_status_checks='{"strict":true,"contexts":["backend-tests"]}' \
  --field enforce_admins=true \
  --field required_pull_request_reviews='{"required_approving_review_count":1}' \
  --field restrictions=null

# Protect main branch (optional)
gh api repos/a-greenapple/connectme-backend/branches/main/protection \
  --method PUT \
  --field required_status_checks='{"strict":true,"contexts":["backend-tests"]}' \
  --field enforce_admins=false \
  --field required_pull_request_reviews=null \
  --field restrictions=null
```

### Configure via GitHub Web UI
1. Go to: https://github.com/a-greenapple/connectme-backend/settings/branches
2. Click "Add rule" for `prod` branch
3. Enable:
   - ✅ Require a pull request before merging
   - ✅ Require approvals (1)
   - ✅ Require status checks to pass before merging
   - ✅ Require branches to be up to date before merging
   - ✅ Include administrators (optional)

## Deployment Checklist

### Before Creating `prod` Branch
- [ ] Verify what's currently in production
- [ ] Decide which commit should be the `prod` baseline
- [ ] Backup current production state
- [ ] Document current production commit SHA

### After Creating `prod` Branch
- [ ] Update deployment workflows
- [ ] Configure branch protection rules
- [ ] Update documentation
- [ ] Test pre-prod deployment from `main`
- [ ] Test production deployment from `prod`
- [ ] Notify team of new workflow

## Future Workflow Example

### Scenario: Deploy New Feature

```bash
# 1. Develop on main
git checkout main
git pull origin main

# 2. Make changes
# ... edit files ...

# 3. Commit and push
git add .
git commit -m "Add new feature"
git push origin main

# 4. CI runs automatically, deploys to pre-prod
# Wait for: https://github.com/a-greenapple/connectme-backend/actions

# 5. Test in pre-prod
curl https://pre-prod.connectme.be.totessoft.com/healthz/

# 6. When ready for production, create PR
gh pr create --base prod --head main \
  --title "Release: New feature" \
  --body "Tested in pre-prod, ready for production"

# 7. Review and merge PR (via GitHub UI)
# This automatically triggers production deployment

# 8. Verify production
curl https://connectme.be.totessoft.com/healthz/
```

## Rollback Strategy

### Rollback Production
```bash
# Option 1: Revert the merge commit
git checkout prod
git revert -m 1 HEAD
git push origin prod
# This triggers automatic deployment of previous state

# Option 2: Reset to previous commit (use with caution)
git checkout prod
git reset --hard <previous-commit-sha>
git push --force origin prod
# Requires force push, use only in emergencies
```

### Rollback Pre-Prod
```bash
git checkout main
git revert HEAD
git push origin main
# Triggers automatic deployment
```

## Benefits of This Strategy

1. **Clear Separation**: Development vs. production code
2. **Gated Releases**: PR review before production
3. **Automated Testing**: CI runs on both branches
4. **Easy Rollback**: Simple git operations
5. **Audit Trail**: All production changes via PRs
6. **Flexibility**: Can hotfix production independently

## Monitoring

### Check Branch Status
```bash
# Compare branches
git log prod..main --oneline  # Commits in main not in prod
git log main..prod --oneline  # Commits in prod not in main

# Check deployment status
gh run list --branch main --limit 5
gh run list --branch prod --limit 5
```

---

**Ready to implement?** Choose an option (A, B, or C) and I'll execute the setup.

