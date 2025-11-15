# 🔍 Debug Authentication Issue

## The Problem
You're getting a 403 error, which means the Authorization header is either:
1. Not being sent
2. Sent with an invalid/expired token
3. Sent but Django can't validate it

## Quick Debug Steps

### Step 1: Check if Token Exists in Browser
Open browser console (F12) and run:
```javascript
console.log('Access Token:', localStorage.getItem('keycloak_access_token'));
console.log('Refresh Token:', localStorage.getItem('keycloak_refresh_token'));
console.log('User Info:', localStorage.getItem('keycloak_user_info'));
```

**Expected:** You should see tokens and user info
**If empty:** You're not logged in properly

---

### Step 2: Check Network Request Headers
1. Open DevTools (F12)
2. Go to **Network** tab
3. Search for claims again
4. Click on the `search/` request
5. Go to **Headers** section
6. Look for **Request Headers**

**Expected to see:**
```
Authorization: Bearer eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCJ9...
```

**If missing:** The token is not being added to the request

---

### Step 3: Manual Token Test
1. Copy your access token from localStorage
2. Test it directly with curl:

```bash
# Get your token from browser console first
TOKEN="YOUR_TOKEN_HERE"

# Test the API
curl -X POST http://localhost:8000/api/v1/claims/search/ \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "firstServiceDate": "2025-05-01",
    "lastServiceDate": "2025-05-02"
  }'
```

**Expected:** Should return claims data or a specific error
**If 403:** Token is invalid or Django can't validate it

---

### Step 4: Check Django Keycloak Authentication

The Django logs should show more details. Look for:

**Good:**
```
INFO KeycloakAuthentication: Validating token
INFO User test.analyst authenticated successfully
```

**Bad:**
```
ERROR KeycloakAuthentication: Failed to validate token
ERROR Invalid token signature
ERROR Token expired
```

---

## Most Likely Issues

### Issue 1: User Not Logged In Properly
**Solution:**
1. Go to http://localhost:3000/login
2. Clear browser cache (Ctrl+Shift+Delete)
3. Login again: test.analyst / test123
4. Check localStorage for tokens (Step 1 above)

### Issue 2: Token Not Being Sent
**Solution:**
Check if the axios interceptor is running:
```javascript
// Add this to frontend/src/lib/api.ts temporarily
apiClient.interceptors.request.use(
  async (config) => {
    const token = await keycloakService.ensureValidToken();
    console.log('🔑 Token being sent:', token ? 'YES' : 'NO'); // ADD THIS
    console.log('🔑 Token value:', token?.substring(0, 50) + '...'); // ADD THIS
    
    if (token) {
      config.headers.Authorization = `Bearer ${token}`;
    }
    
    return config;
  },
  // ...
);
```

### Issue 3: Django Can't Validate Keycloak Token
**Solution:**
Check Django Keycloak settings in `config/settings.py`:
```python
KEYCLOAK_SERVER_URL = 'https://auth.totesoft.com'
KEYCLOAK_REALM = 'connectme'
KEYCLOAK_CLIENT_ID = 'connectme-frontend'
```

Make sure these match your Keycloak configuration!

---

## Quick Test Sequence

1. **Logout completely:**
   - Clear browser cache
   - Clear localStorage
   - Close all tabs

2. **Fresh login:**
   - Go to http://localhost:3000/login
   - Login: test.analyst / test123
   - Open console and check for tokens

3. **Test search:**
   - Go to Claims page
   - Open Network tab
   - Search for claims
   - Check if Authorization header is present

4. **Share results:**
   - Screenshot of Network tab (Headers section)
   - Console output showing tokens
   - Django terminal logs

---

## What to Share

Please share:
1. **Browser Console Output:**
   ```javascript
   localStorage.getItem('keycloak_access_token')?.substring(0, 100)
   ```

2. **Network Tab - Request Headers:**
   - Screenshot or copy the Authorization header

3. **Django Terminal Logs:**
   - The lines around the 403 error
   - Any KeycloakAuthentication messages

This will help me identify the exact issue!
