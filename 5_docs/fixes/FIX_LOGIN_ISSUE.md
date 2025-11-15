# 🔧 Fix Login Issue - Step by Step

## Problem

Login page appears, but after entering credentials and clicking "Sign in", it refreshes and returns to the login page.

## Root Cause

The Keycloak client `connectme-frontend` likely doesn't have **Direct Access Grants** enabled, which is required for password-based (Resource Owner Password Credentials) login flow.

---

## ✅ Solution: Enable Direct Access Grants

### Step 1: Go to Keycloak Admin Console

1. Open: **https://auth.totesoft.com/admin/**
2. Login with your admin credentials
3. Select realm: **connectme** (top-left dropdown)

### Step 2: Configure the Frontend Client

1. Click **Clients** in the left sidebar
2. Find and click **connectme-frontend**
3. Go to the **Settings** tab (should be selected by default)

### Step 3: Enable Direct Access Grants

Scroll down to find **Authentication flow** section:

**Enable these options:**
- ✅ **Standard flow** (should already be enabled)
- ✅ **Direct access grants** ← **THIS IS THE KEY ONE!**

**Optional (for better security in production):**
- ✅ **Implicit flow** (if you want)
- ❌ **Service accounts roles** (not needed for frontend)

### Step 4: Save Changes

1. Scroll to the bottom
2. Click **Save**
3. You should see a success message

---

## 🧪 Test the Fix

### Option 1: Use the Test Page

I just created a test page for you:

1. Go to: **http://localhost:3000/test-login**
2. Enter your credentials:
   - Username: `test.analyst`
   - Password: `test123`
3. Click **Test Login**

**Expected Results:**
- ✅ **Success**: You'll see "Success! Token received" with token details
- ❌ **Error**: You'll see the exact error message from Keycloak

### Option 2: Use the Regular Login Page

1. Go to: **http://localhost:3000/login**
2. Enter credentials
3. Click **Sign in**
4. Should redirect to dashboard!

---

## 📋 Common Error Messages

### Error: "unauthorized_client"

**Full message:**
```json
{
  "error": "unauthorized_client",
  "error_description": "Client not enabled to retrieve service account"
}
```

**Solution:**
- Enable **Direct access grants** in Keycloak client settings (see above)

### Error: "invalid_grant"

**Full message:**
```json
{
  "error": "invalid_grant",
  "error_description": "Invalid user credentials"
}
```

**Solution:**
- Check username and password are correct
- Verify user exists in Keycloak
- Check user's password is set (Credentials tab in user settings)
- Make sure "Temporary" is OFF for the password

### Error: "invalid_client"

**Full message:**
```json
{
  "error": "invalid_client",
  "error_description": "Invalid client or Invalid client credentials"
}
```

**Solution:**
- Check client ID matches: `connectme-frontend`
- Check realm name matches: `connectme`
- Verify client exists in Keycloak

### Error: Connection refused or CORS error

**Solution:**
- Check Keycloak is accessible: `curl https://auth.totesoft.com`
- Check `.env.local` has correct URL
- Check browser console for CORS errors

---

## 🔍 Debug Checklist

Use the test page (http://localhost:3000/test-login) and check:

- [ ] Environment variables are loaded correctly
- [ ] Keycloak URL is accessible
- [ ] Client ID matches
- [ ] Username exists in Keycloak
- [ ] Password is correct
- [ ] Direct access grants is enabled
- [ ] User has required roles assigned

---

## 📸 Screenshots of Keycloak Settings

### Where to Find "Direct Access Grants"

In Keycloak Admin Console:
```
Clients → connectme-frontend → Settings tab

Scroll down to "Authentication flow" section:

┌─────────────────────────────────────────┐
│ Authentication flow                      │
│                                          │
│ ☑ Standard flow                         │
│ ☑ Direct access grants  ← ENABLE THIS! │
│ ☐ Implicit flow                         │
│ ☐ Service accounts roles                │
│ ☐ OAuth 2.0 Device Authorization Grant  │
└─────────────────────────────────────────┘

[Save] button at bottom
```

---

## 🎯 After Fixing

Once you enable Direct Access Grants:

1. **Test immediately** - No need to restart servers
2. **Try test page first** - http://localhost:3000/test-login
3. **Then try regular login** - http://localhost:3000/login
4. **Check browser console** - Look for any errors (F12 → Console)

---

## 🚀 Alternative: Use Authorization Code Flow (More Secure)

If you want to use the more secure Authorization Code flow instead of Direct Access Grants:

### Update Keycloak Client Settings:
- ✅ Standard flow: **Enabled**
- ❌ Direct access grants: **Disabled**
- ✅ Valid redirect URIs: Add `http://localhost:3000/*`

### Update Frontend Code:
This would require implementing the OAuth 2.0 Authorization Code flow with PKCE, which is more complex but more secure for production.

**For now, Direct Access Grants is fine for development and testing.**

---

## 📞 Still Not Working?

If you still have issues after enabling Direct Access Grants:

1. **Check browser console** (F12 → Console tab)
2. **Check network tab** (F12 → Network tab)
3. **Look for the POST request** to `/protocol/openid-connect/token`
4. **Check the response** - what error code and message?

Share the error message and I can help further!

---

**Next: Go enable Direct Access Grants in Keycloak now!** 🎯
