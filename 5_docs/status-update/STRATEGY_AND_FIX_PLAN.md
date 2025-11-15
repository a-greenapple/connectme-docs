# Development Strategy & Fix Plan

## 🎯 Current Situation

### **What Happened:**
1. ✅ Local development worked fine
2. ❌ Deployed to production → issues started
3. ❌ Fixed issues directly on remote server
4. ❌ Local and remote code are now out of sync
5. ❌ No clear development workflow

### **Current Issues:**
- **403 Forbidden** on `/api/v1/claims/search/` - Authentication required
- **Code out of sync** between local and remote
- **Reactive fixes** instead of systematic approach

---

## 📋 Proper Development Workflow (Going Forward)

### **Phase 1: Fix Current Issues**

#### **Step 1: Fix 403 Authentication Error**
**Root Cause:** Claims endpoints require authentication but aren't properly configured

**Fix:**
- Check if Keycloak token is being sent
- Verify user permissions for claims access
- Add proper authentication decorators

#### **Step 2: Pull All Remote Changes to Local**
```bash
# Backend - commit remote changes
ssh server "cd /var/www/connectme-backend && git add . && git commit -m 'Production fixes' && git push"

# Frontend - already pushed
cd connectme-frontend && git pull origin main

# Backend - pull to local
cd connectme-backend && git pull origin main
```

#### **Step 3: Verify Local Environment Matches Production**
```bash
# Compare environment variables
# Compare dependencies
# Test locally
```

---

### **Phase 2: Establish Proper Workflow**

```
┌─────────────────────────────────────────────────────────┐
│                   DEVELOPMENT WORKFLOW                   │
└─────────────────────────────────────────────────────────┘

1. LOCAL DEVELOPMENT
   ├─ Make changes locally
   ├─ Test with ./service.sh local start
   ├─ Verify everything works
   └─ Run tests (if available)
      │
      ▼
2. GIT COMMIT
   ├─ git add .
   ├─ git commit -m "Feature: description"
   └─ git push origin main
      │
      ▼
3. DEPLOY TO PRODUCTION
   ├─ ./service.sh remote deploy
   ├─ Monitor: ./service.sh remote logs backend -f
   └─ Test on production
      │
      ▼
4. VERIFY & MONITOR
   ├─ ./service.sh remote status
   ├─ Check logs for errors
   └─ Test all functionality

NEVER EDIT DIRECTLY ON REMOTE SERVER!
```

---

### **Phase 3: Fix the 403 Error Properly**

#### **The Issue:**
The claims search endpoint requires authentication but the view isn't properly decorated.

#### **The Fix:**

**Option A: Make claims search public (for testing)**
```python
# In apps/claims/api_views.py
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny

@api_view(['POST'])
@permission_classes([AllowAny])  # For testing only!
def search_claims(request):
    # ... rest of the code
```

**Option B: Fix authentication properly (recommended)**
```python
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def search_claims(request):
    # ... rest of the code
```

Then ensure the frontend is sending the token correctly.

---

## 🔧 Immediate Action Plan

### **NOW - Fix the 403 Error:**

1. **Check if user is authenticated when calling the API**
   - Open browser DevTools → Network tab
   - Look at the request headers
   - Check if `Authorization: Bearer <token>` is present

2. **Temporarily allow unauthenticated access for testing**
   - Add `@permission_classes([AllowAny])` to claims views
   - Test if it works
   - Then fix authentication properly

3. **Commit all remote changes to git**
   - Push from remote server
   - Pull to local

4. **From now on: ONLY develop locally**

---

## 📊 Comparison: Before vs After

### **Before (Current - Bad):**
```
Developer → Edit on Remote → Hope it works → Fix errors on Remote → Repeat
                ↓
           Out of sync
                ↓
           No history
                ↓
         Can't rollback
```

### **After (Proper - Good):**
```
Developer → Edit Locally → Test Locally → Git Commit → Deploy → Monitor
     ↑          ↓              ↓             ↓           ↓
     │      Works great!   Can rollback   Automated   Logs
     │                                                   ↓
     └───────────────── Fix if needed ──────────────────┘
```

---

## 🎯 Next Steps (In Order)

### **RIGHT NOW:**

1. **Fix 403 Error** (5 minutes)
   ```bash
   # Add AllowAny to claims views temporarily
   # Test if search works
   ```

2. **Commit Remote Changes** (5 minutes)
   ```bash
   # Push all remote changes to GitHub
   # Pull to local
   ```

3. **Test Locally** (10 minutes)
   ```bash
   # Set up local environment
   # Run ./service.sh local start
   # Test claims search locally
   ```

### **THIS WEEK:**

4. **Fix Authentication Properly** (30 minutes)
   - Ensure Keycloak tokens are validated
   - Add proper permissions
   - Test authentication flow

5. **Add Automated Tests** (optional but recommended)
   - Test claims search
   - Test authentication
   - Test API endpoints

6. **Documentation** (30 minutes)
   - Update README with workflow
   - Document API endpoints
   - Add troubleshooting guide

---

## 🚨 Rules Going Forward

### **DO:**
- ✅ Develop and test locally first
- ✅ Commit to git after testing
- ✅ Use `./service.sh remote deploy` to deploy
- ✅ Monitor logs after deployment
- ✅ Document changes

### **DON'T:**
- ❌ Edit code directly on remote server
- ❌ Make untested changes
- ❌ Skip git commits
- ❌ Deploy without testing locally
- ❌ Ignore errors or warnings

---

## 📞 Emergency Procedures

### **If Production Breaks:**

1. **Check logs immediately:**
   ```bash
   ./service.sh remote logs backend -f
   ```

2. **Rollback if needed:**
   ```bash
   ssh server "cd /var/www/connectme-backend && git log -3"
   ssh server "cd /var/www/connectme-backend && git reset --hard <commit>"
   ./service.sh remote restart backend
   ```

3. **Fix locally and redeploy:**
   ```bash
   # Fix the issue locally
   # Test thoroughly
   # Deploy again
   ```

---

## 💡 Quick Reference

### **Local Development:**
```bash
./service.sh local start      # Start local servers
./service.sh local logs both  # View logs
./service.sh local stop       # Stop servers
```

### **Production Management:**
```bash
./service.sh remote status    # Check production
./service.sh remote deploy    # Deploy changes
./service.sh remote logs backend -f  # Follow logs
./service.sh remote restart   # Restart services
```

### **Git Workflow:**
```bash
git status                    # Check changes
git add .                     # Stage changes
git commit -m "message"       # Commit
git push origin main          # Push to GitHub
./service.sh remote deploy    # Deploy to production
```

---

**Last Updated:** January 10, 2025  
**Status:** 🔧 Fixing 403 Error → Then Establishing Proper Workflow

