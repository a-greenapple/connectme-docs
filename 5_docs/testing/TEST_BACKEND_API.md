# 🧪 Backend API Testing Guide

## Current Status

✅ Backend is running on port 8000
✅ Claims search endpoint exists: `/api/v1/claims/search/`
✅ Frontend is making correct API calls
⚠️  Getting "Failed to search claims" error

## Test the Backend API

### Step 1: Get a Token from Frontend

1. Open browser DevTools (F12)
2. Go to **Console** tab
3. Run this command:
   ```javascript
   localStorage.getItem('kc_access_token')
   ```
4. Copy the token (long string starting with `eyJ...`)

### Step 2: Test API with Token

Replace `YOUR_TOKEN_HERE` with the token from step 1:

```bash
curl -X POST http://localhost:8000/api/v1/claims/search/ \
  -H "Authorization: Bearer YOUR_TOKEN_HERE" \
  -H "Content-Type: application/json" \
  -d '{
    "firstServiceDate": "2025-05-01",
    "lastServiceDate": "2025-05-02"
  }'
```

### Step 3: Check Backend Logs

Look at the terminal where Django is running (ttys093) for any error messages.

## Common Issues & Solutions

### Issue 1: "User is not associated with a practice"

**Error:**
```json
{
  "error": "User is not associated with a practice"
}
```

**Solution:**
The Keycloak user needs to be linked to a Django user with an organization.

**Fix:**
1. Go to Django admin: http://localhost:8000/admin/
2. Login with admin credentials
3. Go to **Users** → Find your test user (`test.analyst`)
4. If user doesn't exist, create it
5. Set **Organization** field
6. Save

### Issue 2: "Provider not found" or "Practice not found"

**Error:**
```json
{
  "error": "Provider matching query does not exist"
}
```

**Solution:**
Need to set up UHC provider and practice configuration.

**Fix:**
Run the setup script:
```bash
cd backend
python setup_uhc_rsm.py
```

### Issue 3: OAuth Token Error

**Error:**
```json
{
  "error": "Failed to get OAuth token"
}
```

**Solution:**
UHC credentials need to be configured in Django admin.

**Fix:**
1. Go to: http://localhost:8000/admin/providers/providercredential/
2. Update UHC credentials with valid client_id and client_secret
3. Make sure `is_active` is checked

### Issue 4: CORS Error

**Error in browser console:**
```
Access to XMLHttpRequest at 'http://localhost:8000/api/v1/claims/search/' 
from origin 'http://localhost:3000' has been blocked by CORS policy
```

**Solution:**
Already configured in settings.py, but verify:
```python
CORS_ALLOW_ALL_ORIGINS = True  # Development only
```

## Quick Debug Script

Save this as `test_claims_api.py` in backend folder:

```python
import requests
import json

# Get token from your browser localStorage
TOKEN = "YOUR_TOKEN_HERE"

url = "http://localhost:8000/api/v1/claims/search/"
headers = {
    "Authorization": f"Bearer {TOKEN}",
    "Content-Type": "application/json"
}
data = {
    "firstServiceDate": "2025-05-01",
    "lastServiceDate": "2025-05-02"
}

response = requests.post(url, headers=headers, json=data)
print(f"Status Code: {response.status_code}")
print(f"Response: {json.dumps(response.json(), indent=2)}")
```

Run it:
```bash
cd backend
python test_claims_api.py
```

## Expected Flow

1. Frontend calls `/api/v1/claims/search/` with JWT token
2. Backend validates token with Keycloak
3. Backend looks up user's organization and practice
4. Backend gets UHC OAuth token
5. Backend calls UHC API
6. Backend returns claims data to frontend

## Next Steps

1. **Get the token** from browser localStorage
2. **Test the API** with curl command above
3. **Check backend logs** for the actual error
4. **Share the error message** so I can help fix it

---

**The frontend is working perfectly!** 
**We just need to debug the backend API call.**
