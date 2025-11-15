# 🚀 Start ConnectMe Platform - Quick Guide

## ✅ Keycloak Imported Successfully!

Great! Now let's start the servers and test everything.

---

## Step 1: Start Backend Server

Open a **NEW terminal window** and run:

```bash
cd /Users/ssiva/Documents/1_Data/AI/abce/connectme/backend
source venv/bin/activate  # or: ./venv/bin/activate
python manage.py runserver
```

**Expected output:**
```
Starting development server at http://127.0.0.1:8000/
Quit the server with CONTROL-C.
```

**Test it:** Open http://localhost:8000/admin/ in your browser

---

## Step 2: Start Frontend Server

Open **ANOTHER terminal window** and run:

```bash
cd /Users/ssiva/Documents/1_Data/AI/abce/connectme/frontend
npm run dev
```

**Expected output:**
```
✓ Ready in X.Xs
○ Local:        http://localhost:3000
```

**Test it:** Open http://localhost:3000 in your browser

---

## Step 3: Test the Complete Flow

### 3.1 Login to Keycloak Admin
1. Go to: https://auth.totesoft.com/admin/
2. Login with your admin credentials
3. Select realm: **connectme**
4. Verify:
   - ✅ Realm roles exist (admin, team_lead, analyst, etc.)
   - ✅ Client roles exist (claims:read, workflow:view, etc.)
   - ✅ Groups exist (team:RCM-East, team:RCM-West, etc.)

### 3.2 Create a Test User in Keycloak
1. In Keycloak Admin → Users → Add User
2. Username: `test.analyst`
3. Email: `analyst@test.com`
4. First Name: `Test`
5. Last Name: `Analyst`
6. Save

7. Set Password:
   - Credentials tab → Set Password
   - Password: `test123`
   - Temporary: OFF
   - Save

8. Assign Roles:
   - Role Mappings tab
   - Assign realm role: **analyst**
   - Filter by clients → Select **connectme-frontend**
   - Assign client roles:
     - ✅ claims:read
     - ✅ workflow:view_own
     - ✅ history:view_own

9. Assign to Group:
   - Groups tab → Join Group
   - Select: **team:RCM-East**

### 3.3 Test Frontend Login
1. Go to: http://localhost:3000
2. You should be redirected to login
3. Login with:
   - Username: `test.analyst`
   - Password: `test123`
4. You should see the dashboard!

### 3.4 Test Workflow Pages
After login, test these pages:
- **Dashboard**: http://localhost:3000/dashboard
- **Claims**: http://localhost:3000/claims
- **Workflow**: http://localhost:3000/workflow
- **Approvals**: http://localhost:3000/workflow/approvals

---

## Troubleshooting

### Frontend won't start?

**Make sure you're in the right directory:**
```bash
# ❌ WRONG - This won't work
cd /Users/ssiva/Documents/1_Data/AI/abce/connectme
npm run dev  # Error: no package.json

# ✅ CORRECT - Do this instead
cd /Users/ssiva/Documents/1_Data/AI/abce/connectme/frontend
npm run dev  # Works!
```

**If you see "port already in use":**
```bash
# Kill the process on port 3000
lsof -ti:3000 | xargs kill -9

# Then start again
npm run dev
```

### Backend won't start?

```bash
cd /Users/ssiva/Documents/1_Data/AI/abce/connectme/backend

# Activate virtual environment
source venv/bin/activate

# Install any missing dependencies
pip install -r requirements/base.txt

# Run migrations
python manage.py migrate

# Start server
python manage.py runserver
```

### Can't login?

**Check Keycloak is accessible:**
```bash
curl https://auth.totesoft.com
```

**Check .env.local in frontend:**
```bash
cat /Users/ssiva/Documents/1_Data/AI/abce/connectme/frontend/.env.local
```

Should contain:
```
NEXT_PUBLIC_API_URL=http://localhost:8000
NEXT_PUBLIC_KEYCLOAK_URL=https://auth.totesoft.com
NEXT_PUBLIC_KEYCLOAK_REALM=connectme
NEXT_PUBLIC_KEYCLOAK_CLIENT_ID=connectme-frontend
```

---

## Quick Command Reference

| Action | Command |
|--------|---------|
| Start Backend | `cd backend && source venv/bin/activate && python manage.py runserver` |
| Start Frontend | `cd frontend && npm run dev` |
| Check Backend | `curl http://localhost:8000/admin/` |
| Check Frontend | `curl http://localhost:3000` |
| Kill Frontend | `lsof -ti:3000 \| xargs kill -9` |
| Kill Backend | `lsof -ti:8000 \| xargs kill -9` |

---

## What to Test

### ✅ Backend APIs
```bash
# Test workflow dashboard (requires auth)
curl -H "Authorization: Bearer YOUR_TOKEN" \
  http://localhost:8000/api/v1/workflow/dashboard/

# Test teams list
curl -H "Authorization: Bearer YOUR_TOKEN" \
  http://localhost:8000/api/v1/workflow/teams/
```

### ✅ Frontend Pages
- [ ] Login page loads
- [ ] Can login with test user
- [ ] Dashboard shows stats
- [ ] Workflow page loads
- [ ] Approvals page loads
- [ ] Can logout

### ✅ Keycloak Integration
- [ ] Realm imported successfully
- [ ] Test user created
- [ ] Roles assigned
- [ ] Can get JWT token
- [ ] Token includes roles

---

## Success Checklist

After completing all steps, you should have:

- ✅ Keycloak realm imported with all roles
- ✅ Backend server running on http://localhost:8000
- ✅ Frontend server running on http://localhost:3000
- ✅ Test user created in Keycloak
- ✅ Can login to frontend
- ✅ Can see workflow dashboard
- ✅ APIs are protected by Keycloak

---

## Next Steps After Testing

1. **Create more users** with different roles (team_lead, admin)
2. **Test approval workflow** (analyst requests, team_lead approves)
3. **Test work item creation** and assignment
4. **Test query history** tracking
5. **Deploy to production** when ready

---

**Need Help?**

Check these files:
- `TROUBLESHOOTING_FRONTEND.md` - Frontend issues
- `WORKFLOW_API_DOCUMENTATION.md` - API reference
- `COMPLETE_WORKFLOW_IMPLEMENTATION.md` - Full system overview

---

**You're almost there! Just start both servers and test! 🎉**
