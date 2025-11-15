# 🧪 Testing Workflow API - Step by Step Guide

## Prerequisites

✅ Django server running
✅ Test data created (from test_workflow_setup.py)
✅ Admin user available

---

## Step 1: Start Django Server

```bash
cd backend
./venv/bin/python3 manage.py runserver
```

Server will start at: `http://localhost:8000`

---

## Step 2: Get Admin Token (Temporary for Testing)

Since we're testing without full Keycloak integration, we'll use Django admin session.

### Option A: Use Django Admin Session

1. Go to: `http://localhost:8000/admin/`
2. Login with: `admin` / `admin123`
3. Open browser console and get session cookie

### Option B: Create Mock Authentication (For Testing)

We'll create a simple token endpoint for testing.

---

## Step 3: Test Endpoints with cURL

### Test 1: List Teams

```bash
curl -X GET http://localhost:8000/api/v1/workflow/teams/ \
  -H "Content-Type: application/json"
```

**Expected Response:**
```json
[
  {
    "id": "uuid",
    "name": "RCM East Team",
    "code": "RCM-East",
    "member_count": 2,
    "active_work_count": 2
  }
]
```

### Test 2: List Work Items

```bash
curl -X GET http://localhost:8000/api/v1/workflow/work-items/ \
  -H "Content-Type: application/json"
```

### Test 3: Get Dashboard Stats

```bash
curl -X GET http://localhost:8000/api/v1/workflow/dashboard/ \
  -H "Content-Type: application/json"
```

### Test 4: Get Query Limits

```bash
curl -X GET http://localhost:8000/api/v1/workflow/query-limits/ \
  -H "Content-Type: application/json"
```

### Test 5: Check Re-Query Permission

```bash
curl -X POST http://localhost:8000/api/v1/workflow/check-requery/ \
  -H "Content-Type: application/json" \
  -d '{
    "resource_type": "claim",
    "resource_id": "CLM123456"
  }'
```

### Test 6: Create Work Item

```bash
curl -X POST http://localhost:8000/api/v1/workflow/work-items/ \
  -H "Content-Type: application/json" \
  -d '{
    "title": "Test Work Item",
    "description": "Testing API creation",
    "work_type": "callback",
    "status": "new",
    "priority": "medium",
    "patient_name": "Test Patient",
    "patient_dob": "1980-01-01",
    "payer": "UHC"
  }'
```

### Test 7: Get Query History

```bash
curl -X GET http://localhost:8000/api/v1/workflow/query-history/ \
  -H "Content-Type: application/json"
```

### Test 8: Get Query History Stats

```bash
curl -X GET http://localhost:8000/api/v1/workflow/query-history/stats/ \
  -H "Content-Type: application/json"
```

---

## Step 4: Test with Python

Create a test script:

```python
import requests

BASE_URL = "http://localhost:8000/api/v1/workflow"

# Test 1: Dashboard
response = requests.get(f"{BASE_URL}/dashboard/")
print(f"Dashboard: {response.status_code}")
if response.status_code == 200:
    print(response.json())

# Test 2: Teams
response = requests.get(f"{BASE_URL}/teams/")
print(f"\nTeams: {response.status_code}")
if response.status_code == 200:
    print(f"Found {len(response.json())} teams")

# Test 3: Work Items
response = requests.get(f"{BASE_URL}/work-items/")
print(f"\nWork Items: {response.status_code}")
if response.status_code == 200:
    print(f"Found {len(response.json())} work items")

# Test 4: Query Limits
response = requests.get(f"{BASE_URL}/query-limits/")
print(f"\nQuery Limits: {response.status_code}")
if response.status_code == 200:
    print(response.json())
```

---

## Step 5: Test in Browser

Open these URLs in your browser:

1. **Django Admin:**
   - URL: `http://localhost:8000/admin/`
   - Check: Workflow → Teams, Work Items, Query History

2. **API Endpoints (will show JSON):**
   - `http://localhost:8000/api/v1/workflow/teams/`
   - `http://localhost:8000/api/v1/workflow/work-items/`
   - `http://localhost:8000/api/v1/workflow/query-history/`

---

## Step 6: Test with Postman/Insomnia

### Import Collection

Create a new collection with these requests:

**1. Get Teams**
- Method: GET
- URL: `http://localhost:8000/api/v1/workflow/teams/`

**2. Get Work Items**
- Method: GET
- URL: `http://localhost:8000/api/v1/workflow/work-items/`
- Query Params:
  - `status`: new
  - `assigned_to`: me

**3. Get Dashboard**
- Method: GET
- URL: `http://localhost:8000/api/v1/workflow/dashboard/`

**4. Create Work Item**
- Method: POST
- URL: `http://localhost:8000/api/v1/workflow/work-items/`
- Body (JSON):
```json
{
  "title": "Postman Test",
  "description": "Testing from Postman",
  "work_type": "callback",
  "status": "new",
  "priority": "medium",
  "patient_name": "John Doe",
  "patient_dob": "1980-01-01",
  "payer": "UHC"
}
```

**5. Check Re-Query**
- Method: POST
- URL: `http://localhost:8000/api/v1/workflow/check-requery/`
- Body (JSON):
```json
{
  "resource_type": "claim",
  "resource_id": "CLM123456"
}
```

---

## Expected Issues & Solutions

### Issue 1: 403 Forbidden

**Cause:** Authentication required

**Solution:** 
- For now, we'll temporarily disable authentication for testing
- Or use Django session authentication from admin login

### Issue 2: 401 Unauthorized

**Cause:** No authentication token

**Solution:**
- Login to Django admin first
- Use session cookie from browser

### Issue 3: CORS Errors

**Cause:** Frontend calling from different origin

**Solution:**
- Already configured in settings.py
- CORS_ALLOW_ALL_ORIGINS = True (development only)

---

## Verification Checklist

After testing, verify:

- ✅ Django server starts without errors
- ✅ Admin panel accessible
- ✅ Teams endpoint returns data
- ✅ Work items endpoint returns data
- ✅ Dashboard endpoint returns stats
- ✅ Query limits endpoint returns limits
- ✅ Can create work items via API
- ✅ Can check re-query permissions
- ✅ Query history is tracked

---

## Next: Enable Full Authentication

Once basic testing works, we'll:

1. Connect Keycloak authentication
2. Test with JWT tokens
3. Verify role-based permissions
4. Test approval workflow
5. Integrate with frontend

---

**Ready to start testing!**
