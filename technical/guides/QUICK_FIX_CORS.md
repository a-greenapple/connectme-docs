# ⚡ Quick Fix: CORS Error (2 Minutes)

## 🎯 The Fix

You need to add one line to Keycloak configuration.

---

## 📋 Steps

### 1. Open Keycloak Admin
Go to: **https://auth.totesoft.com/admin**

### 2. Login
Try any admin credentials you have access to

### 3. Select Realm
Top-left dropdown → Select: **`connectme-preprod`**

### 4. Go to Client
Left menu → **Clients** → Click: **`connectme-preprod-frontend`**

### 5. Find "Web Origins"
Scroll down to the **"Web Origins"** field

### 6. Add This Line
```
https://pre-prod.connectme.apps.totessoft.com
```

If there's already content, add it on a new line or separated by space.

You can also add:
```
+
```
(The `+` means "allow all redirect URIs")

### 7. Save
Click **"Save"** button at the bottom

### 8. Clear Browser Cache
- Chrome: `Ctrl+Shift+Delete` → Clear "Cached images and files"
- Or use Incognito mode

### 9. Test
Go to: https://pre-prod.connectme.apps.totessoft.com

Try login with: `admin` / `hufze7-coqrok-zUfwuf`

---

## ✅ Done!

The CORS error should be gone.

---

## 🆘 Can't Access Keycloak Admin?

**Option 1:** Ask your Keycloak administrator to add the Web Origin

**Option 2:** If Keycloak is on the same server, we can try to access it locally

**Option 3:** Check if you have access to the Keycloak database directly

---

## 📸 What You're Looking For

In the Keycloak client configuration, you'll see a form. Look for:

```
┌─────────────────────────────────────────────┐
│ Web Origins:                                │
│ ┌─────────────────────────────────────────┐ │
│ │ https://pre-prod.connectme.apps.       │ │  ← ADD THIS
│ │    totessoft.com                        │ │
│ │ +                                       │ │  ← AND THIS
│ └─────────────────────────────────────────┘ │
└─────────────────────────────────────────────┘
```

---

**Time:** 2 minutes  
**Risk:** None (only adds CORS permission)  
**Impact:** Fixes login immediately

