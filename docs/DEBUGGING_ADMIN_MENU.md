# Debugging Admin Menu Visibility

## 🎯 **Issue**
Admin menu not visible in navigation despite being configured correctly.

---

## 🔍 **Debug Logging Added**

I've added comprehensive console logging to help diagnose the issue. When you visit the site, the browser console will show:

### **Keycloak Service Logs:**
```
[Keycloak] Token payload: {...}
[Keycloak] Realm access roles: [...]
[Keycloak] Extracted role: ...
[Keycloak] All roles: [...]
[Keycloak] Final userInfo: {...}
```

### **Auth Context Logs:**
```
[Auth] Initializing auth...
[Auth] User is authenticated
[Auth] User info from storage: {...}
[Auth] Fetching fresh user info...
[Auth] Fresh user info fetched: {...}
[Auth] User state set: {...}
[Auth] Auth initialization complete
```

### **Navbar Logs:**
```
[Navbar] User: {...}
[Navbar] isAuthenticated: true/false
[Navbar] User role: admin/user/undefined
```

---

## 📋 **Testing Steps**

### 1. **Open Browser Console**
1. Visit: https://connectme.apps.totesoft.com
2. Press `F12` (or `Cmd+Option+I` on Mac)
3. Go to **Console** tab
4. Clear existing logs (click 🚫 icon)

### 2. **Login**
1. Login with your Keycloak credentials:
   - Email: `admin@connectme.com`
   - Password: Your password
2. Watch the console for logs

### 3. **Check the Logs**
Look for these specific patterns:

#### ✅ **Expected (Working):**
```
[Auth] User is authenticated
[Keycloak] Extracted role: admin
[Navbar] User role: admin
[Navbar] isAuthenticated: true
```

#### ❌ **Problem Patterns:**

**Pattern 1: No Role in Token**
```
[Keycloak] Realm access roles: undefined
[Keycloak] Extracted role: user
[Navbar] User role: user
```
→ **Issue**: Keycloak not including roles in JWT token

**Pattern 2: User Not Set**
```
[Auth] User is authenticated
[Auth] User state set: null
[Navbar] User: null
```
→ **Issue**: Auth context not setting user properly

**Pattern 3: Not Authenticated**
```
[Auth] User not authenticated
[Navbar] isAuthenticated: false
```
→ **Issue**: Login not working or token expired

---

## 🛠️ **Troubleshooting Based on Logs**

### **Issue: No Roles in Token**

**Symptoms:**
- `[Keycloak] Realm access roles: undefined`
- `[Keycloak] Extracted role: user`

**Fix:**
1. Login to Keycloak Admin: https://api.connectme.totesoft.com
2. Go to **Realm Settings** → **Tokens**
3. Ensure "Add to token" is enabled for roles
4. Go to **Users** → Find your user
5. Go to **Role Mappings** tab
6. Assign appropriate roles (admin, manager, etc.)

### **Issue: User Info Not Fetched**

**Symptoms:**
- `[Auth] Fresh user info fetched: null`
- Network errors in console

**Fix:**
1. Check if Keycloak is running
2. Verify `NEXT_PUBLIC_KEYCLOAK_URL` environment variable
3. Check CORS settings on Keycloak

### **Issue: Token Expired**

**Symptoms:**
- `[Auth] Token expired, attempting refresh...`
- Redirect to login page

**Fix:**
- Login again
- Token refresh should work automatically

---

## 🔧 **Manual Inspection**

### **Check LocalStorage:**

1. In browser console, run:
```javascript
// Check if user is authenticated
console.log('Token:', localStorage.getItem('kc_access_token'));

// Check user info
console.log('User:', JSON.parse(localStorage.getItem('kc_user_info') || '{}'));
```

2. Verify the output:
   - Token should be a long JWT string
   - User info should include `role` and `roles` fields

### **Decode JWT Token:**

1. Copy the token from localStorage
2. Visit: https://jwt.io
3. Paste the token
4. Check the payload section for:
```json
{
  "realm_access": {
    "roles": ["admin", "user", ...]
  }
}
```

---

## 🎯 **Expected Admin Menu Behavior**

### **Configuration:**
```typescript
// In Navbar.tsx
{
  name: '⚙️ Admin', 
  href: '/admin',
  submenu: [
    { name: '👥 User Management', href: '/users' },
    { name: '⚙️ Settings', href: '/settings' },
  ],
  adminOnly: false  // Currently accessible to ALL authenticated users
}
```

### **Visibility Logic:**
```typescript
// Skip admin menu for non-admin users
if (item.adminOnly && user?.role !== 'admin' && user?.role !== 'manager') {
  return null;
}
```

**Current State:**
- `adminOnly: false` → Menu shows for ALL authenticated users
- Should be visible regardless of role

**If Not Visible:**
- User is not authenticated
- `isAuthenticated` is false
- Check console logs

---

## 📊 **Common Scenarios**

### **Scenario 1: Fresh Login**
```
[Auth] Initializing auth...
[Auth] User not authenticated
[Auth] Auth initialization complete
→ User clicks login
[Auth] User is authenticated
[Keycloak] Fetching user info...
[Keycloak] Extracted role: admin
[Navbar] User role: admin
```
✅ Admin menu should appear

### **Scenario 2: Page Refresh (Authenticated)**
```
[Auth] Initializing auth...
[Auth] User is authenticated
[Auth] User info from storage: {...}
[Navbar] User: {...}
[Navbar] User role: admin
```
✅ Admin menu should persist

### **Scenario 3: Token Expired**
```
[Auth] Initializing auth...
[Auth] User is authenticated
[Auth] Fetching fresh user info...
[Keycloak] Token expired
[Auth] Token refresh failed, logging out
```
❌ Redirected to login page

---

## 🐛 **Known Issues**

1. **Static Build Logs**: During build (seen in deployment), Navbar logs show `User: null` - This is normal for static site generation

2. **Console Spam**: Debug logging is verbose - will be removed once issue is resolved

3. **Role Mapping**: If Keycloak admin hasn't assigned roles, user will have default `user` role

---

## 📝 **Next Steps**

After testing, please provide:

1. **Console Logs**: Copy/paste the relevant console output
2. **Screenshot**: If possible, screenshot of the navigation bar
3. **LocalStorage**: Output of the manual inspection commands

This will help pinpoint the exact issue!

---

## 🔄 **Temporary Workaround**

If Admin menu is still not visible, you can:

1. **Direct URL**: Navigate directly to https://connectme.apps.totesoft.com/users
2. **Should work** even if menu is hidden (authentication is the only requirement)

---

**Last Updated**: October 16, 2025  
**Status**: 🔍 Debugging in Progress

