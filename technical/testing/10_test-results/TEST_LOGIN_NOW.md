# 🧪 Test Login Flow - Quick Guide

## ✅ Current Status

- ✅ Backend running on http://localhost:8000
- ✅ Frontend running on http://localhost:3000
- ✅ Keycloak realm imported
- ✅ Test user created
- ✅ Root page now redirects to login

---

## 🔄 What Just Changed

I updated the root page (`/`) to properly check authentication:
- **If logged in** → Redirects to `/dashboard`
- **If NOT logged in** → Redirects to `/login`

This means you should now see the login page!

---

## 🧪 Test the Login Flow

### Step 1: Clear Browser Cache (Important!)

Since you already visited the site, clear your browser cache:

**Option A - Hard Refresh:**
- **Mac**: `Cmd + Shift + R`
- **Windows/Linux**: `Ctrl + Shift + R`

**Option B - Clear localStorage:**
1. Open browser DevTools (F12)
2. Go to **Application** tab (Chrome) or **Storage** tab (Firefox)
3. Click **Local Storage** → `http://localhost:3000`
4. Click **Clear All**
5. Refresh page

### Step 2: Visit the Site

Go to: **http://localhost:3000**

You should now see the **Login Page**!

### Step 3: Login with Test User

Use the credentials for the user you created in Keycloak:

**Example:**
- Username: `test.analyst`
- Password: `test123`

### Step 4: After Login

You should be redirected to `/dashboard` and see:
- ✅ Welcome message with your name
- ✅ Quick action cards
- ✅ System status
- ✅ Your account info

---

## 🎯 Test All Pages

After logging in, test these URLs:

1. **Dashboard**: http://localhost:3000/dashboard
2. **Claims**: http://localhost:3000/claims
3. **Workflow**: http://localhost:3000/workflow
4. **Approvals**: http://localhost:3000/workflow/approvals

---

## 🐛 Troubleshooting

### Issue: Still seeing old dashboard without login

**Solution:**
```bash
# Clear browser cache completely
# Then visit in incognito/private mode
```

### Issue: Login page shows but can't login

**Check Keycloak URL in .env.local:**
```bash
cat frontend/.env.local
```

Should show:
```
NEXT_PUBLIC_KEYCLOAK_URL=https://auth.totesoft.com
NEXT_PUBLIC_KEYCLOAK_REALM=connectme
NEXT_PUBLIC_KEYCLOAK_CLIENT_ID=connectme-frontend
```

**Test Keycloak connection:**
```bash
curl https://auth.totesoft.com/realms/connectme
```

Should return JSON with realm info.

### Issue: "Login failed" error

**Possible causes:**
1. Wrong username/password
2. User not created in Keycloak
3. Keycloak client not configured correctly

**Verify user exists:**
1. Go to: https://auth.totesoft.com/admin/
2. Login as admin
3. Select realm: **connectme**
4. Go to **Users**
5. Find your test user
6. Check **Credentials** tab - password should be set

### Issue: Can login but get errors on other pages

**Check backend is running:**
```bash
curl http://localhost:8000/api/v1/workflow/dashboard/
```

If you get 401 Unauthorized, that's expected (need auth token).
If you get connection refused, backend is not running.

---

## 📋 Complete Test Checklist

- [ ] Clear browser cache/localStorage
- [ ] Visit http://localhost:3000
- [ ] See login page (not dashboard)
- [ ] Enter username and password
- [ ] Click "Login"
- [ ] Redirected to dashboard
- [ ] See welcome message with your name
- [ ] Navigate to Claims page
- [ ] Navigate to Workflow page
- [ ] Navigate to Approvals page
- [ ] Click Logout
- [ ] Redirected back to login page

---

## 🎉 Success Criteria

You've successfully tested the login flow when:

1. ✅ Root page (`/`) redirects to login
2. ✅ Can login with Keycloak credentials
3. ✅ Dashboard shows after login
4. ✅ Navbar shows user info
5. ✅ Can navigate to all pages
6. ✅ Logout works and redirects to login

---

## 🔐 Create More Test Users

### In Keycloak Admin Console:

**Analyst User:**
```
Username: analyst1
Email: analyst1@test.com
Password: test123
Realm Role: analyst
Client Roles: claims:read, workflow:view_own, history:view_own
Group: team:RCM-East
```

**Team Lead User:**
```
Username: teamlead1
Email: teamlead1@test.com
Password: test123
Realm Role: team_lead
Client Roles: (all analyst roles + requery:approve, workflow:view_team, team:manage)
Group: team:RCM-East
```

**Admin User:**
```
Username: admin1
Email: admin1@test.com
Password: test123
Realm Role: admin
Client Roles: (all roles)
```

---

## 📊 What to Test Next

After login works:

1. **Test Workflow Dashboard**
   - Should show 0 work items (empty state)
   - Should show query limits
   - Should show stats

2. **Test Approvals Page**
   - Should show "No pending approvals"
   - Filter tabs should work

3. **Test API Integration**
   - Open browser DevTools → Network tab
   - Navigate to workflow page
   - Check API calls to backend
   - Should see Authorization header with JWT token

4. **Test Logout**
   - Click logout button
   - Should redirect to login
   - Try accessing /dashboard directly
   - Should redirect back to login

---

## 🚀 Next Steps After Testing

1. **Test with different roles** (analyst vs team_lead vs admin)
2. **Create work items** via Django admin
3. **Test approval workflow**
4. **Test query history tracking**
5. **Deploy to production**

---

**Ready to test! Clear your browser cache and visit http://localhost:3000** 🎉
