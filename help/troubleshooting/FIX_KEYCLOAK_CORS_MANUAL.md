# Fix Keycloak CORS Error - Manual Steps

## 🔴 Error
```
Origin https://pre-prod.connectme.apps.totessoft.com is not allowed by Access-Control-Allow-Origin
Fetch API cannot load https://auth.totesoft.com/realms/connectme-preprod/protocol/openid-connect/token
```

## 🎯 Root Cause
The Keycloak client `connectme-preprod-frontend` doesn't have the frontend URL in its **Web Origins** configuration.

## ✅ Solution: Update Keycloak Client (5 minutes)

### Step 1: Access Keycloak Admin Console

1. Open browser and go to: **https://auth.totesoft.com/admin**

2. You'll see the Keycloak login page

3. **Try these credentials** (one should work):
   - Username: `admin` / Password: `hufze7-coqrok-zUfwuf`
   - Username: `connectme` / Password: `Qojsyb-fynwa1-johsyj`
   - Or any other Keycloak admin credentials you have

---

### Step 2: Select the Realm

1. After login, you'll see the Keycloak admin console

2. Look at the **top-left corner** - you'll see a dropdown showing the current realm (probably "master")

3. Click on the realm dropdown

4. Select: **`connectme-preprod`**

---

### Step 3: Navigate to Clients

1. In the **left sidebar menu**, find and click: **Clients**

2. You'll see a list of clients

3. Find and click on: **`connectme-preprod-frontend`**

4. You're now in the client configuration page

---

### Step 4: Update Web Origins (CRITICAL!)

Scroll down until you find the **"Web Origins"** field. This is the key setting!

**Current value** (probably):
```
(empty or missing the frontend URL)
```

**Change to:**
```
https://pre-prod.connectme.apps.totessoft.com
http://localhost:3000
http://localhost:3001
+
```

**Important Notes:**
- Add each URL on a **new line** or separated by spaces
- The `+` symbol means "allow all origins from Valid Redirect URIs"
- Make sure there are **no trailing slashes** on the URLs
- Use **HTTPS** for the production URL

---

### Step 5: Update Valid Redirect URIs

While you're here, also verify the **"Valid Redirect URIs"** field:

**Should contain:**
```
https://pre-prod.connectme.apps.totessoft.com/*
http://localhost:3000/*
http://localhost:3001/*
```

**Important Notes:**
- Each URL should end with `/*` (wildcard)
- This allows redirects to any path under that domain

---

### Step 6: Update Valid Post Logout Redirect URIs

Also check **"Valid Post Logout Redirect URIs"**:

**Should contain:**
```
https://pre-prod.connectme.apps.totessoft.com/*
http://localhost:3000/*
```

---

### Step 7: Verify Other Settings

While you're in the client configuration, verify these settings:

| Setting | Value |
|---------|-------|
| **Client Protocol** | openid-connect |
| **Access Type** | public |
| **Standard Flow Enabled** | ON |
| **Direct Access Grants Enabled** | ON |
| **Valid Redirect URIs** | https://pre-prod.connectme.apps.totessoft.com/* |
| **Web Origins** | https://pre-prod.connectme.apps.totessoft.com |
| **Admin URL** | (can be empty) |

---

### Step 8: Save Configuration

1. Scroll to the **bottom** of the page

2. Click the **"Save"** button

3. You should see a success message: "Client successfully updated"

---

### Step 9: Test the Fix

1. **Clear your browser cache:**
   - Chrome: `Ctrl+Shift+Delete` (Mac: `Cmd+Shift+Delete`)
   - Select: "Cached images and files" + "Cookies"
   - Time range: "All time"
   - Click "Clear data"

2. **Close and reopen your browser** (or use Incognito mode)

3. **Go to the login page:**
   - https://pre-prod.connectme.apps.totessoft.com

4. **Click login** - you should be redirected to Keycloak

5. **Enter credentials:**
   - Username: `admin`
   - Password: `hufze7-coqrok-zUfwuf`

6. **Check for errors** in browser console (F12)

7. **You should be logged in!** ✅

---

## 🔍 Visual Guide

### What You're Looking For

When you open the client configuration, you'll see a form with many fields. The key fields are:

```
┌─────────────────────────────────────────────────────┐
│ Client ID: connectme-preprod-frontend              │
├─────────────────────────────────────────────────────┤
│ Name: ConnectMe Pre-Prod Frontend                  │
├─────────────────────────────────────────────────────┤
│ ...                                                 │
├─────────────────────────────────────────────────────┤
│ Valid Redirect URIs:                                │
│ ┌─────────────────────────────────────────────────┐ │
│ │ https://pre-prod.connectme.apps.totessoft.com/* │ │
│ │ http://localhost:3000/*                         │ │
│ └─────────────────────────────────────────────────┘ │
├─────────────────────────────────────────────────────┤
│ Web Origins: ⚠️ THIS IS THE KEY FIELD!             │
│ ┌─────────────────────────────────────────────────┐ │
│ │ https://pre-prod.connectme.apps.totessoft.com   │ │
│ │ http://localhost:3000                           │ │
│ │ +                                               │ │
│ └─────────────────────────────────────────────────┘ │
├─────────────────────────────────────────────────────┤
│ ...                                                 │
└─────────────────────────────────────────────────────┘
```

---

## 🚨 Troubleshooting

### Issue 1: Can't Login to Keycloak Admin
**Try these credentials:**
1. `admin` / `hufze7-coqrok-zUfwuf`
2. `connectme` / `Qojsyb-fynwa1-johsyj`
3. Contact your Keycloak administrator
4. Check if you have access to the Keycloak server directly

### Issue 2: Can't Find the Client
**Steps:**
1. Make sure you selected the correct realm: `connectme-preprod`
2. In the Clients list, use the search box to find: `connectme-preprod-frontend`
3. If not found, the client might need to be created

### Issue 3: Still Getting CORS Error After Update
**Try:**
1. Clear browser cache completely
2. Use Incognito/Private mode
3. Try a different browser
4. Wait 1-2 minutes for Keycloak to update
5. Restart Keycloak (if you have server access)

### Issue 4: Save Button Doesn't Work
**Check:**
1. Make sure all required fields are filled
2. Check browser console for JavaScript errors
3. Try refreshing the Keycloak admin page
4. Try a different browser

---

## 📋 Alternative: Create Client if Missing

If the client doesn't exist, create it:

1. Go to: Clients → Create
2. Fill in:
   - **Client ID:** `connectme-preprod-frontend`
   - **Client Protocol:** openid-connect
   - **Root URL:** `https://pre-prod.connectme.apps.totessoft.com`
3. Click "Save"
4. Then follow Steps 4-8 above to configure it

---

## 🧪 Verification Commands

After making changes, test from command line:

```bash
# Test Keycloak CORS (should return CORS headers)
curl -I -X OPTIONS "https://auth.totesoft.com/realms/connectme-preprod/protocol/openid-connect/token" \
  -H "Origin: https://pre-prod.connectme.apps.totessoft.com" \
  -H "Access-Control-Request-Method: POST"

# Expected output should include:
# access-control-allow-origin: https://pre-prod.connectme.apps.totessoft.com
```

---

## 📞 Need Help?

If you're still stuck:

1. **Take screenshots** of:
   - The Keycloak client configuration page
   - The Web Origins field
   - The browser console errors

2. **Check these:**
   - Can you access Keycloak admin console?
   - Can you see the `connectme-preprod` realm?
   - Can you see the `connectme-preprod-frontend` client?

3. **Alternative:** If you can't access Keycloak admin, contact your system administrator to make these changes

---

## ✅ Success Checklist

- [ ] Logged into Keycloak admin console
- [ ] Selected `connectme-preprod` realm
- [ ] Found `connectme-preprod-frontend` client
- [ ] Updated Web Origins to include frontend URL
- [ ] Updated Valid Redirect URIs
- [ ] Clicked Save
- [ ] Cleared browser cache
- [ ] Tested login - no CORS error!

---

**Estimated Time:** 5 minutes  
**Difficulty:** Easy  
**Risk:** Low (only affects frontend authentication)

---

## 🎯 Quick Reference

**What to change:**
```
Web Origins: https://pre-prod.connectme.apps.totessoft.com
```

**Where:**
```
Keycloak Admin → connectme-preprod realm → Clients → connectme-preprod-frontend → Web Origins
```

**Why:**
```
Keycloak needs to know which origins are allowed to make requests to its token endpoint
```

---

**Last Updated:** November 11, 2025  
**Status:** Manual configuration required - awaiting Keycloak admin access

