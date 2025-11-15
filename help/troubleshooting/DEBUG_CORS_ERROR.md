# Debug CORS Error - Step by Step

## Current Status

✅ **Backend CORS:** Working correctly
✅ **Keycloak CORS:** Working correctly

Both are returning proper CORS headers:
```
access-control-allow-origin: https://pre-prod.connectme.apps.totessoft.com
access-control-allow-credentials: true
```

## Debugging Steps

### Step 1: Identify the Failing Request

1. Open browser (Chrome/Firefox)
2. Open Developer Tools (F12)
3. Go to **Network** tab
4. Check "Preserve log"
5. Go to: https://pre-prod.connectme.apps.totessoft.com
6. Look for requests with red status or CORS errors
7. Click on the failed request
8. Check:
   - Request URL
   - Request Method
   - Status Code
   - Response Headers

**Take a screenshot and share:**
- The Network tab showing the failed request
- The Headers tab of that request
- The Console tab showing the error

### Step 2: Common CORS Error Patterns

#### Pattern 1: Missing CORS Headers
**Error:** "No 'Access-Control-Allow-Origin' header is present"
**Cause:** Server not sending CORS headers
**Solution:** Already fixed ✅

#### Pattern 2: Credentials with Wildcard
**Error:** "The value of the 'Access-Control-Allow-Origin' header in the response must not be the wildcard '*' when the request's credentials mode is 'include'"
**Cause:** Using `credentials: 'include'` with wildcard origin
**Solution:** Use specific origin (already done ✅)

#### Pattern 3: Preflight Failure
**Error:** "Response to preflight request doesn't pass access control check"
**Cause:** OPTIONS request failing
**Solution:** Check if OPTIONS method is allowed

#### Pattern 4: Multiple CORS Headers
**Error:** "The 'Access-Control-Allow-Origin' header contains multiple values"
**Cause:** Both nginx and Django adding CORS headers
**Solution:** Remove from one (nginx already doesn't have them ✅)

#### Pattern 5: Protocol Mismatch
**Error:** "Origin https://... is not allowed"
**Cause:** Mixing HTTP and HTTPS
**Solution:** Ensure all URLs use HTTPS

### Step 3: Check Frontend Code

Look for fetch/axios calls in the frontend:

```javascript
// Check if credentials are being sent
fetch(url, {
  credentials: 'include',  // This requires specific origin, not wildcard
  headers: {
    'Content-Type': 'application/json',
  }
})
```

### Step 4: Test Specific Endpoints

```bash
# Test backend health
curl -I "https://pre-prod.connectme.be.totessoft.com/api/v1/health/" \
  -H "Origin: https://pre-prod.connectme.apps.totessoft.com"

# Test auth endpoint
curl -I "https://pre-prod.connectme.be.totessoft.com/api/v1/auth/keycloak/validate/" \
  -H "Origin: https://pre-prod.connectme.apps.totessoft.com"

# Test Keycloak
curl -I "https://auth.totesoft.com/realms/connectme-preprod/protocol/openid-connect/token" \
  -H "Origin: https://pre-prod.connectme.apps.totessoft.com"
```

### Step 5: Check for Cached Responses

CORS errors can be cached by the browser:

1. **Clear browser cache:**
   - Chrome: Settings → Privacy → Clear browsing data
   - Or use Incognito mode

2. **Hard refresh:**
   - Chrome/Firefox: Ctrl+Shift+R (Cmd+Shift+R on Mac)

3. **Disable cache in DevTools:**
   - Network tab → Check "Disable cache"

### Step 6: Check SSL/TLS

Mixed content can cause CORS-like errors:

```bash
# Check SSL certificate
curl -v https://pre-prod.connectme.apps.totessoft.com 2>&1 | grep -i "ssl\|tls\|certificate"
curl -v https://pre-prod.connectme.be.totessoft.com 2>&1 | grep -i "ssl\|tls\|certificate"
curl -v https://auth.totesoft.com 2>&1 | grep -i "ssl\|tls\|certificate"
```

### Step 7: Check Nginx Configuration

```bash
# Check nginx config for backend
ssh connectme@169.59.163.43 'cat /etc/nginx/sites-available/connectme-preprod-backend'

# Look for:
# - proxy_pass directives
# - add_header directives (should NOT have CORS headers)
# - proxy_set_header directives
```

### Step 8: Check Backend Logs

```bash
# Watch backend logs in real-time
ssh connectme@169.59.163.43 'sudo journalctl -u connectme-preprod-backend -f'

# Or check recent logs
ssh connectme@169.59.163.43 'sudo journalctl -u connectme-preprod-backend -n 100'

# Look for:
# - CORS-related errors
# - 403 Forbidden
# - Authentication errors
```

## Quick Fixes to Try

### Fix 1: Restart Backend
```bash
ssh connectme@169.59.163.43 'sudo systemctl restart connectme-preprod-backend'
```

### Fix 2: Restart Nginx
```bash
ssh connectme@169.59.163.43 'sudo systemctl restart nginx'
```

### Fix 3: Clear Browser Data
- Chrome: Settings → Privacy → Clear browsing data
- Select: Cached images and files, Cookies
- Time range: All time
- Click "Clear data"

### Fix 4: Try Different Browser
- Test in Firefox, Safari, or Edge
- Or use Incognito/Private mode

### Fix 5: Check Frontend Environment
```bash
ssh connectme@169.59.163.43 'cat /var/www/connectme-preprod-frontend/.env'

# Verify:
# NEXT_PUBLIC_API_URL=https://pre-prod.connectme.be.totessoft.com
# NEXT_PUBLIC_KEYCLOAK_URL=https://auth.totesoft.com
```

## Information Needed

To help debug further, please provide:

1. **Exact error message** from browser console
2. **Network tab screenshot** showing the failed request
3. **Request URL** that's failing
4. **Request headers** from the failed request
5. **Response headers** from the failed request
6. **What action** triggers the error (page load, button click, etc.)
7. **Browser** and version you're using

## Possible Scenarios

### Scenario A: Frontend Not Loading
**Symptom:** Blank page, CORS error on initial load
**Cause:** Frontend trying to fetch data before user is authenticated
**Solution:** Add loading state, handle unauthenticated state

### Scenario B: Login Redirect Failing
**Symptom:** CORS error during Keycloak redirect
**Cause:** Keycloak client configuration
**Solution:** Update Keycloak client redirect URIs

### Scenario C: API Calls Failing
**Symptom:** CORS error on specific API calls
**Cause:** Missing authentication token or wrong endpoint
**Solution:** Check token is being sent in Authorization header

### Scenario D: WebSocket Connection
**Symptom:** CORS error on WebSocket connection
**Cause:** WebSocket CORS is different from HTTP CORS
**Solution:** Configure WebSocket CORS separately

## Testing Commands

```bash
# Test from command line (should all return 200 with CORS headers)
curl -I -H "Origin: https://pre-prod.connectme.apps.totessoft.com" \
  https://pre-prod.connectme.be.totessoft.com/api/v1/health/

curl -I -H "Origin: https://pre-prod.connectme.apps.totessoft.com" \
  https://pre-prod.connectme.be.totessoft.com/api/v1/auth/keycloak/validate/

curl -I -H "Origin: https://pre-prod.connectme.apps.totessoft.com" \
  https://auth.totesoft.com/realms/connectme-preprod/.well-known/openid-configuration
```

## Next Steps

1. **Gather information** using the debugging steps above
2. **Share the details** (error message, screenshots, etc.)
3. **Try quick fixes** (restart services, clear cache)
4. **Check specific endpoint** that's failing

---

**Status:** Awaiting more information about the specific failing request

