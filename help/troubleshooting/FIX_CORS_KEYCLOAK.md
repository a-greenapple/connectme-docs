# CORS Error Fix - Keycloak Configuration

## Error
```
Failed to load resource: Origin https://pre-prod.connectme.apps.totessoft.com is not allowed by Access-Control-Allow-Origin. Status code: 200
```

## Root Cause
The CORS error is likely coming from **Keycloak**, not the Django backend. 

The backend CORS is configured correctly ✅:
- `access-control-allow-origin: https://pre-prod.connectme.apps.totessoft.com`
- `access-control-allow-credentials: true`

The issue is that the **Keycloak client** needs to have the frontend URL in its allowed origins.

## Solution: Update Keycloak Client Configuration

### Method 1: Via Keycloak Admin Console (RECOMMENDED)

1. **Login to Keycloak Admin**
   - URL: https://auth.totesoft.com/admin
   - Realm: `master`
   - Try credentials: `admin` / `hufze7-coqrok-zUfwuf` or `connectme` / `Qojsyb-fynwa1-johsyj`

2. **Select the Realm**
   - Click on realm dropdown (top left)
   - Select: `connectme-preprod`

3. **Go to Clients**
   - Left menu → Clients
   - Find and click: `connectme-preprod-frontend`

4. **Update Client Settings**
   
   Scroll down to find these fields and update:

   **Valid Redirect URIs:**
   ```
   https://pre-prod.connectme.apps.totessoft.com/*
   http://localhost:3000/*
   http://localhost:3001/*
   ```

   **Valid Post Logout Redirect URIs:**
   ```
   https://pre-prod.connectme.apps.totessoft.com/*
   http://localhost:3000/*
   ```

   **Web Origins:** (This is the critical one for CORS!)
   ```
   https://pre-prod.connectme.apps.totessoft.com
   http://localhost:3000
   http://localhost:3001
   +
   ```
   
   **Note:** The `+` means "allow all origins from Valid Redirect URIs"

5. **Save**
   - Click "Save" at the bottom

6. **Test**
   - Clear browser cache
   - Try logging in again

### Method 2: Via Keycloak REST API

If you have admin access token, you can update via API:

```bash
# Get admin token
TOKEN=$(curl -s -X POST "https://auth.totesoft.com/realms/master/protocol/openid-connect/token" \
  -d "username=admin" \
  -d "password=hufze7-coqrok-zUfwuf" \
  -d "grant_type=password" \
  -d "client_id=admin-cli" | jq -r '.access_token')

# Get client ID
CLIENT_UUID=$(curl -s -X GET "https://auth.totesoft.com/admin/realms/connectme-preprod/clients?clientId=connectme-preprod-frontend" \
  -H "Authorization: Bearer $TOKEN" | jq -r '.[0].id')

# Update client
curl -X PUT "https://auth.totesoft.com/admin/realms/connectme-preprod/clients/$CLIENT_UUID" \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "webOrigins": [
      "https://pre-prod.connectme.apps.totessoft.com",
      "http://localhost:3000",
      "http://localhost:3001",
      "+"
    ],
    "redirectUris": [
      "https://pre-prod.connectme.apps.totessoft.com/*",
      "http://localhost:3000/*",
      "http://localhost:3001/*"
    ]
  }'
```

## Verification

### 1. Check Keycloak CORS Headers

```bash
curl -I -X OPTIONS "https://auth.totesoft.com/realms/connectme-preprod/protocol/openid-connect/token" \
  -H "Origin: https://pre-prod.connectme.apps.totessoft.com" \
  -H "Access-Control-Request-Method: POST"
```

**Expected Response:**
```
HTTP/1.1 200 OK
access-control-allow-origin: https://pre-prod.connectme.apps.totessoft.com
access-control-allow-credentials: true
access-control-allow-methods: POST, OPTIONS
```

### 2. Test Login Flow

1. Open browser console (F12)
2. Go to: https://pre-prod.connectme.apps.totessoft.com
3. Click login
4. Watch the Network tab
5. Look for requests to `auth.totesoft.com`
6. Check response headers for `access-control-allow-origin`

## Alternative: Temporary Workaround

If you can't access Keycloak admin console, you can temporarily disable CORS checking in your browser for testing:

### Chrome
```bash
# macOS
open -na "Google Chrome" --args --disable-web-security --user-data-dir="/tmp/chrome-cors-disabled"

# Linux
google-chrome --disable-web-security --user-data-dir="/tmp/chrome-cors-disabled"
```

### Firefox
1. Open `about:config`
2. Search for `security.fileuri.strict_origin_policy`
3. Set to `false`

**⚠️ WARNING:** Only use this for testing! Re-enable security after testing.

## Backend CORS Configuration (Already Correct ✅)

For reference, the backend is already configured correctly:

**`.env`:**
```env
CORS_ALLOWED_ORIGINS=https://pre-prod.connectme.apps.totessoft.com,http://localhost:3000,http://localhost:3001
```

**`settings.py`:**
```python
CORS_ALLOWED_ORIGINS = os.environ.get('CORS_ALLOWED_ORIGINS', '').split(',')
CORS_ALLOW_CREDENTIALS = True
CORS_ALLOW_HEADERS = [
    'accept', 'accept-encoding', 'authorization', 'content-type',
    'dnt', 'origin', 'user-agent', 'x-csrftoken', 'x-requested-with',
]
CORS_ALLOW_METHODS = ['DELETE', 'GET', 'OPTIONS', 'PATCH', 'POST', 'PUT']
```

## Common Issues

### Issue 1: Multiple CORS Headers
**Symptom:** Multiple `Access-Control-Allow-Origin` headers in response

**Solution:** Make sure nginx is NOT adding CORS headers. Only Django should add them.

Check nginx config:
```bash
ssh connectme@169.59.163.43 'grep -i "add_header.*Access-Control" /etc/nginx/sites-available/connectme-preprod-backend'
```

If found, remove them and reload nginx:
```bash
sudo systemctl reload nginx
```

### Issue 2: Credentials with Wildcard
**Symptom:** CORS error even though origin is allowed

**Solution:** When using `credentials: true`, you cannot use wildcard `*` for origins. Must specify exact origins.

### Issue 3: Missing OPTIONS Method
**Symptom:** Preflight requests fail

**Solution:** Ensure OPTIONS method is allowed in both Django and nginx.

## Summary

**The issue is most likely:**
1. ❌ Keycloak client `connectme-preprod-frontend` doesn't have `https://pre-prod.connectme.apps.totessoft.com` in Web Origins
2. ✅ Backend CORS is configured correctly
3. ✅ CORS middleware is installed and working

**Action Required:**
- Update Keycloak client configuration to add the frontend URL to Web Origins

**Quick Test:**
```bash
# Test backend CORS (should work ✅)
curl -I "https://pre-prod.connectme.be.totessoft.com/api/v1/auth/keycloak/validate/" \
  -H "Origin: https://pre-prod.connectme.apps.totessoft.com"

# Test Keycloak CORS (might fail ❌)
curl -I "https://auth.totesoft.com/realms/connectme-preprod/protocol/openid-connect/token" \
  -H "Origin: https://pre-prod.connectme.apps.totessoft.com"
```

---

**Last Updated:** November 11, 2025  
**Status:** Diagnosis complete - Keycloak client configuration update required

