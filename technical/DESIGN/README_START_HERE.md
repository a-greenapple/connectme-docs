# 🎉 ConnectMe Healthcare Platform - START HERE!

## ✅ EVERYTHING IS READY!

All code has been implemented. Frontend dependencies are installed. Environment is configured. You're ready to test!

---

## 🚀 QUICK START (2 minutes)

### Option 1: Automated Script (Recommended)

```bash
cd /Users/ssiva/Documents/1_Data/AI/abce/connectme
./START_TESTING.sh
```

This script will:
- ✅ Check all prerequisites
- ✅ Start Django backend (port 8000)
- ✅ Start Next.js frontend (port 3000)
- ✅ Open browser automatically
- ✅ Display all URLs and credentials

### Option 2: Manual Start

```bash
# Terminal 1 - Backend
cd /Users/ssiva/Documents/1_Data/AI/abce/connectme/backend
venv/bin/python manage.py runserver 8000

# Terminal 2 - Frontend
cd /Users/ssiva/Documents/1_Data/AI/abce/connectme/frontend
npm run dev

# Open browser
open http://localhost:3000
```

---

## 🔐 TEST CREDENTIALS

**Keycloak Login:**
- Username: `testuser`
- Password: `testpass123`

**Django Admin:**
- URL: http://localhost:8000/admin/
- Username: `admin`
- Password: `admin123`

---

## 🧪 TESTING CHECKLIST

### 1. Verify Keycloak is Accessible

```bash
curl https://api.connectme.totesoft.com/realms/connectme/.well-known/openid-configuration
```

**Expected:** JSON response with endpoints  
**If fails:** See section "Setting Up Keycloak" below

### 2. Test Login
- Open: http://localhost:3000
- Should redirect to `/login`
- Enter: `testuser` / `testpass123`
- Should redirect to `/dashboard`

### 3. Test Dashboard
- Should see welcome message with username
- Should see "Search Claims" card
- Should see user account info at bottom

### 4. Test Claims Search
- Click "Search Claims" or navigate to `/claims`
- Enter dates:
  - First Service Date: `2025-05-01`
  - Last Service Date: `2025-05-02`
- Click "Search Claims"
- Should see 3 claims in table

### 5. Test Claims Table
- Verify 3 claims display:
  - FC11920066
  - FC14745726
  - FC14745727
- Click column headers to sort
- Click "Export CSV" - should download file

### 6. Test Claim Details
- Click "View Details" on any claim
- Modal should open
- Should show JSON response
- "Download JSON" should work

### 7. Test Logout
- Click "Logout" in navbar
- Should redirect to `/login`
- Try to access `/claims` - should redirect to login

---

## ⚠️ KEYCLOAK SETUP (If Needed)

If Keycloak is not accessible at `https://api.connectme.totesoft.com`, you have two options:

### Option A: Ask Your Admin

Request:
1. Keycloak realm name: `connectme`
2. Client ID: `connectme-frontend`
3. Test user credentials
4. Access to create/modify clients

### Option B: Run Local Keycloak (Docker)

```bash
# Run Keycloak
docker run -d \
  --name keycloak \
  -p 8080:8080 \
  -e KEYCLOAK_ADMIN=admin \
  -e KEYCLOAK_ADMIN_PASSWORD=admin \
  quay.io/keycloak/keycloak:latest \
  start-dev

# Wait 30 seconds
sleep 30

# Access admin console
open http://localhost:8080
# Login: admin / admin
```

**Then configure:**
1. Create realm: `connectme`
2. Create client: `connectme-frontend`
   - Client protocol: `openid-connect`
   - Access Type: `public`
   - Valid Redirect URIs: `http://localhost:3000/*`
   - Web Origins: `http://localhost:3000`
3. Create user: `testuser`
   - Set password: `testpass123`
   - Temporary: `OFF`

**Update frontend/.env.local:**
```bash
NEXT_PUBLIC_KEYCLOAK_URL=http://localhost:8080
```

**Restart frontend:**
```bash
cd frontend
npm run dev
```

---

## 🐛 TROUBLESHOOTING

### Backend won't start

**Check:**
```bash
cd backend
venv/bin/python manage.py check
```

**Common fixes:**
- Database not running: Start PostgreSQL
- Port in use: `lsof -ti:8000 | xargs kill -9`
- Missing dependencies: `venv/bin/pip install -r requirements.txt`

### Frontend won't start

**Check:**
```bash
cd frontend
npm run dev
```

**Common fixes:**
- Node modules: `npm install`
- Port in use: `lsof -ti:3000 | xargs kill -9`
- Missing @headlessui: `npm install @headlessui/react`

### Login fails

**Check Keycloak:**
```bash
curl -X POST https://api.connectme.totesoft.com/realms/connectme/protocol/openid-connect/token \
  -d "client_id=connectme-frontend" \
  -d "username=testuser" \
  -d "password=testpass123" \
  -d "grant_type=password"
```

**If fails:**
- Verify Keycloak URL
- Check realm name
- Verify client ID
- Confirm user exists

### API calls fail (401)

**Check:**
1. Token is being sent (Browser DevTools → Network → Headers)
2. Django logs show authentication attempt
3. Keycloak public key is accessible

**Fix:**
- Restart both servers
- Clear browser cache/cookies
- Check CORS settings in Django

### CORS errors

**Fix in backend/config/settings.py:**
```python
CORS_ALLOWED_ORIGINS = [
    "http://localhost:3000",
]
```

Restart Django.

---

## 📊 SUCCESS INDICATORS

✅ **Backend:** Logs show "Starting development server at http://127.0.0.1:8000/"  
✅ **Frontend:** Shows "ready - started server on 0.0.0.0:3000"  
✅ **Login:** Redirects to dashboard after login  
✅ **API:** Claims search returns results  
✅ **Auth:** Token visible in Network tab  
✅ **No console errors** in browser DevTools  

---

## 📚 DOCUMENTATION

Detailed guides available in project root:

- **Setup:** `COMPLETE_SETUP_AND_TEST_GUIDE.md`
- **Keycloak:** `KEYCLOAK_SETUP_GUIDE.md`
- **Summary:** `FINAL_IMPLEMENTATION_SUMMARY.md`
- **UHC API:** `UHC_API_SUCCESS.md`
- **Architecture:** `PROVIDER_ARCHITECTURE.md`

---

## 🎯 WHAT YOU'LL SEE

### Login Page
- Modern design with ConnectMe branding
- Username/password fields
- Error messages if login fails
- "Protected by Keycloak" badge

### Dashboard
- Welcome message with your name
- Quick action cards
- System status indicators
- Your account information

### Claims Search
- Date range pickers (required)
- Optional patient filters (collapsible)
- Search button with loading state
- Clear button to reset form

### Claims Results
- Sortable table with 3 claims
- Status badges (color-coded)
- Export CSV button
- View Details button per claim

### Claim Details Modal
- Full claim information
- JSON response viewer
- Download JSON button
- Close button

---

## 🔥 READY TO GO!

Everything is built and configured. Just run the start script:

```bash
cd /Users/ssiva/Documents/1_Data/AI/abce/connectme
./START_TESTING.sh
```

**Or manually:**
1. Start backend: `cd backend && venv/bin/python manage.py runserver 8000`
2. Start frontend: `cd frontend && npm run dev`
3. Open: http://localhost:3000
4. Login and test!

---

## 💡 TIPS

- **Keycloak First:** Verify Keycloak works before testing the app
- **Check Logs:** Both servers write to console - watch for errors
- **Browser DevTools:** Use Network tab to debug API calls
- **Django Admin:** Use http://localhost:8000/admin/ to inspect data

---

## 🆘 NEED HELP?

If you encounter issues:

1. **Check the logs:**
   - Backend: Terminal output or `backend.log`
   - Frontend: Terminal output or `frontend.log`

2. **Review documentation:**
   - `COMPLETE_SETUP_AND_TEST_GUIDE.md` - Full testing guide
   - `KEYCLOAK_SETUP_GUIDE.md` - Keycloak configuration

3. **Verify setup:**
   - Backend running on 8000?
   - Frontend running on 3000?
   - Keycloak accessible?
   - .env.local correct?

---

## 🎊 LET'S TEST!

You're all set. Run the start script and enjoy testing your complete healthcare platform!

```bash
./START_TESTING.sh
```

**Good luck! 🚀**

