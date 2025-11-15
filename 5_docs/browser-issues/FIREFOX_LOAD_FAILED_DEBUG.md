# Firefox "load failed" Debug Guide

## Issue
- Safari: Works perfectly ✅
- Firefox: Shows "load failed" ❌

## What "load failed" Means
The page component renders, but the API call to fetch jobs is failing.

## Possible Causes

### 1. CORS Issue (Most Likely)
Firefox has stricter CORS enforcement than Safari.

**Symptoms:**
- Console shows: "CORS policy blocked"
- Network tab shows: Failed CORS preflight
- Status: (failed) or 0

**Solution:**
```python
# In backend settings.py, ensure:
CORS_ALLOWED_ORIGINS = [
    'https://connectme.apps.totesoft.com',
    'http://localhost:3000',  # for development
]

CORS_ALLOW_CREDENTIALS = True
CORS_ALLOW_HEADERS = ['*']
CORS_ALLOW_METHODS = ['GET', 'POST', 'PUT', 'DELETE', 'OPTIONS']
```

### 2. Authentication Token Issue
Firefox might handle localStorage differently.

**Symptoms:**
- Console shows: 403 Forbidden
- Network tab shows: 403 status
- Response: "Authentication credentials were not provided"

**Check:**
```javascript
// In Firefox console, type:
localStorage.getItem('access_token')
// Does it return a token?
```

### 3. Network Request Failure
Actual network connectivity issue.

**Symptoms:**
- Console shows: "Failed to fetch"
- Network tab shows: Network error
- No status code shown

**Test:**
Open this URL directly in Firefox:
https://connectme.be.totesoft.com/api/v1/claims/csv-jobs/

If you see JSON → Backend works, frontend issue
If you see error → Backend issue

### 4. Different Cache Behavior
Firefox didn't clear the cache properly.

**Solution:**
```
Firefox → Settings → Privacy & Security → Cookies and Site Data
→ Clear Data → Check both boxes → Clear

OR

Ctrl+Shift+Delete → Check everything → Clear Now
```

## Debug Steps

### Step 1: Check Network Tab
```
F12 → Network → Refresh page

Look for:
- csv-jobs request
- Status code (if any)
- Type (XHR, fetch)
- Headers
```

### Step 2: Check Console
```
F12 → Console

Look for:
- Red error messages (not warnings)
- "CORS" in the message
- "403" or "401"
- "Failed to fetch"
```

### Step 3: Check Authentication
```
F12 → Console → Type:
localStorage.getItem('access_token')

Should show: "mock_access_token_..."
If null → Not logged in!
```

### Step 4: Test Backend Directly
```
Open in Firefox:
https://connectme.be.totesoft.com/api/v1/claims/csv-jobs/

Expected: JSON with count and results
If error: Backend issue
```

## Quick Fixes to Try

### Fix 1: Hard Refresh
```
Ctrl+Shift+R (or Cmd+Shift+R on Mac)
```

### Fix 2: Clear All Data
```
Settings → Privacy → Clear Data → Everything
```

### Fix 3: Disable Extensions
```
Try Firefox in Private/Incognito mode
(Extensions are usually disabled)
```

### Fix 4: Check if logged in
```
Go to login page first
Log in with Keycloak
Then try bulk upload page
```

## Common Error Messages

### "CORS policy: No 'Access-Control-Allow-Origin'"
**Cause:** Backend not allowing frontend origin
**Fix:** Update CORS_ALLOWED_ORIGINS in backend

### "403 Forbidden"
**Cause:** Authentication failing
**Fix:** Check if logged in, verify token

### "Failed to fetch"
**Cause:** Network or CORS issue
**Fix:** Check network connectivity, CORS headers

### "TypeError: NetworkError when attempting to fetch resource"
**Cause:** CORS or SSL issue
**Fix:** Check backend CORS, SSL certificates

## Information Needed

To debug further, please provide:

1. **Network tab screenshot** showing the failed request
2. **Console tab** - any RED error messages
3. **What happens when you open:**
   `https://connectme.be.totesoft.com/api/v1/claims/csv-jobs/`
   directly in Firefox?
4. **In Console, type:** `localStorage.getItem('access_token')`
   and share what it shows

## Expected Behavior

**Working (like Safari):**
1. Page loads
2. API call to csv-jobs succeeds
3. Job history displays
4. No "load failed" message

**Current (Firefox):**
1. Page loads
2. API call to csv-jobs fails
3. Shows "load failed"
4. No job history

## Next Step

**Please check the Network tab** and tell me:
- What's the status code of the failed request?
- Is there a CORS error in console?
- Are you logged in? (check localStorage.getItem('access_token'))

This will help me pinpoint the exact issue!

