# 🎉 Complete Setup & Test Guide

## ✅ FRONTEND IMPLEMENTATION COMPLETE!

All frontend files have been created. You now have a complete, working application!

---

## 📁 Files Created (Frontend)

### Authentication & API
- ✅ `src/lib/keycloak.ts` - Keycloak service
- ✅ `src/lib/api.ts` - API client with auto token injection
- ✅ `src/contexts/AuthContext.tsx` - Auth context provider

### Pages
- ✅ `src/app/login/page.tsx` - Login page
- ✅ `src/app/dashboard/page.tsx` - Dashboard with quick actions
- ✅ `src/app/claims/page.tsx` - Claims search page

### Components
- ✅ `src/components/Navbar.tsx` - Navigation with logout
- ✅ `src/components/claims/ClaimsSearchForm.tsx` - Search form
- ✅ `src/components/claims/ClaimsTable.tsx` - Results table with sorting/export
- ✅ `src/components/claims/ClaimDetailsModal.tsx` - Details modal

### Configuration
- ✅ `src/app/layout.tsx` - Updated with AuthProvider
- ✅ `ENV_SETUP_GUIDE.md` - Environment setup instructions

---

## 🚀 SETUP INSTRUCTIONS

### Step 1: Install Frontend Dependencies

```bash
cd /Users/ssiva/Documents/1_Data/AI/abce/connectme/frontend

# Install dependencies
npm install axios @headlessui/react

# If axios is already installed, just add headlessui
npm install @headlessui/react
```

### Step 2: Create Environment File

Create `frontend/.env.local`:

```bash
# For local testing with production Keycloak
NEXT_PUBLIC_API_URL=http://localhost:8000
NEXT_PUBLIC_KEYCLOAK_URL=https://api.connectme.totesoft.com
NEXT_PUBLIC_KEYCLOAK_REALM=connectme
NEXT_PUBLIC_KEYCLOAK_CLIENT_ID=connectme-frontend
```

### Step 3: Start Backend Server

```bash
cd /Users/ssiva/Documents/1_Data/AI/abce/connectme/backend

# Start Django
venv/bin/python manage.py runserver 8000
```

### Step 4: Start Frontend Server

```bash
cd /Users/ssiva/Documents/1_Data/AI/abce/connectme/frontend

# Start Next.js
npm run dev
```

---

## 🧪 TESTING KEYCLOAK

### Option A: Using Existing Production Keycloak

If your Keycloak is already at `https://api.connectme.totesoft.com`:

1. **Verify Keycloak is accessible:**
   ```bash
   curl https://api.connectme.totesoft.com/realms/connectme/.well-known/openid-configuration
   ```

2. **Test token retrieval:**
   ```bash
   curl -X POST https://api.connectme.totesoft.com/realms/connectme/protocol/openid-connect/token \
     -H "Content-Type: application/x-www-form-urlencoded" \
     -d "client_id=connectme-frontend" \
     -d "username=testuser" \
     -d "password=testpass123" \
     -d "grant_type=password"
   ```

3. **If successful**, you'll get a JSON response with `access_token`

4. **If it fails**, you need to set up Keycloak (see Option B)

### Option B: Set Up Local Keycloak (Docker)

```bash
# Run Keycloak in Docker
docker run -d \
  --name keycloak \
  -p 8080:8080 \
  -e KEYCLOAK_ADMIN=admin \
  -e KEYCLOAK_ADMIN_PASSWORD=admin \
  quay.io/keycloak/keycloak:latest \
  start-dev

# Wait 30 seconds for Keycloak to start
sleep 30

# Access admin console
open http://localhost:8080
# Login: admin / admin
```

**Then configure:**
1. Create realm: `connectme`
2. Create client: `connectme-frontend`
   - Access Type: `public`
   - Valid Redirect URIs: `http://localhost:3000/*`
   - Web Origins: `http://localhost:3000`
3. Create user: `testuser`
   - Set password: `testpass123` (temporary: OFF)

**Update frontend .env.local:**
```bash
NEXT_PUBLIC_KEYCLOAK_URL=http://localhost:8080
```

---

## 🎯 END-TO-END TEST

### 1. Access Application
```bash
open http://localhost:3000
```

### 2. Login
- Should redirect to `/login`
- Enter credentials:
  - Username: `testuser`
  - Password: `testpass123`
- Click "Sign in"

### 3. Dashboard
- Should see welcome message
- Should see user name and email
- Should see "Search Claims" card

### 4. Search Claims
- Click "Search Claims" or navigate to `/claims`
- Enter dates:
  - First Service Date: `2025-05-01`
  - Last Service Date: `2025-05-02`
- Click "Search Claims"

### 5. View Results
- Should see 3 claims (from our test):
  - FC11920066
  - FC14745726
  - FC14745727
- Table should be sortable
- "Export CSV" button should work

### 6. View Details
- Click "View Details" on any claim
- Modal should open
- Should show detailed JSON response
- "Download JSON" button should work

### 7. Logout
- Click "Logout" button in navbar
- Should redirect to login page
- Trying to access `/claims` should redirect to login

---

## 🐛 TROUBLESHOOTING

### "Cannot connect to backend"

**Check:**
```bash
# Is Django running?
curl http://localhost:8000/api/v1/claims/

# Should return: {"detail": "Authentication credentials were not provided."}
```

**Fix:** Start Django backend
```bash
cd backend
venv/bin/python manage.py runserver 8000
```

### "Keycloak authentication failed"

**Check:**
```bash
# Can you reach Keycloak?
curl https://api.connectme.totesoft.com/realms/connectme/.well-known/openid-configuration

# Test login
curl -X POST https://api.connectme.totesoft.com/realms/connectme/protocol/openid-connect/token \
  -d "client_id=connectme-frontend" \
  -d "username=testuser" \
  -d "password=testpass123" \
  -d "grant_type=password"
```

**Fix:** 
- Verify Keycloak URL in `.env.local`
- Verify user exists in Keycloak
- Check realm and client_id match

### "Module not found: axios"

**Fix:**
```bash
cd frontend
npm install axios @headlessui/react
```

### CORS Errors

**Fix in Django settings:**
```python
# backend/config/settings.py
CORS_ALLOWED_ORIGINS = [
    "http://localhost:3000",
    "https://connectme.totesoft.com",
]
CORS_ALLOW_CREDENTIALS = True
```

### "401 Unauthorized" on API calls

**Check:**
1. Token is being sent (check Network tab in browser)
2. Token is not expired
3. Keycloak public key is accessible
4. Django can reach Keycloak

**Django logs should show:**
```
INFO Authentication successful!
```

---

## 📊 VERIFICATION CHECKLIST

### Backend
- [ ] Django running on port 8000
- [ ] Can access http://localhost:8000/admin/
- [ ] UHC credentials configured
- [ ] RSM practice configured (TIN: 854203105)

### Keycloak
- [ ] Keycloak accessible
- [ ] Realm "connectme" exists
- [ ] Client "connectme-frontend" exists
- [ ] Test user exists
- [ ] Can get token via curl/Postman

### Frontend
- [ ] Dependencies installed (axios, @headlessui/react)
- [ ] .env.local created with correct values
- [ ] Next.js running on port 3000
- [ ] Can access http://localhost:3000

### Integration
- [ ] Login works
- [ ] Dashboard loads
- [ ] Claims search works
- [ ] Results display correctly
- [ ] Details modal works
- [ ] CSV export works
- [ ] Logout works

---

## 🎊 SUCCESS METRICS

Once everything is working, you should be able to:

✅ **Login** - Authenticate with Keycloak  
✅ **Navigate** - Move between Dashboard and Claims  
✅ **Search** - Query UHC claims by date range  
✅ **View** - See claim results in sortable table  
✅ **Details** - Open modal with full claim information  
✅ **Export** - Download results as CSV  
✅ **Secure** - All API calls authenticated with JWT  
✅ **Logout** - End session and clear tokens  

---

## 📞 NEXT STEPS AFTER TESTING

### 1. Add More Features
- Pagination for > 50 claims
- Advanced patient filters
- Claim history/tracking
- Bulk CSV upload
- Eligibility checking
- Cost estimation

### 2. Deployment
- Deploy backend to production
- Deploy frontend to hosting
- Configure production Keycloak
- Set up SSL/HTTPS
- Configure CORS for production domains

### 3. Monitoring
- Set up error tracking (Sentry)
- Add analytics
- Monitor API usage
- Track user sessions

---

## 🚀 YOU'RE READY TO TEST!

Everything is now in place. Follow the setup instructions above and test the complete flow!

**Questions?** Refer to:
- `KEYCLOAK_SETUP_GUIDE.md` - Keycloak configuration
- `KEYCLOAK_INTEGRATION_GUIDE.md` - Authentication details
- `WORKFLOW_TRANSACTION_SEQUENCE.md` - UHC API workflow
- `UHC_API_SUCCESS.md` - UHC API test results

**Good luck! 🎉**

