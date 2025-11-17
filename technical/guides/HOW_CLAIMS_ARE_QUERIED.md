# How Claims Are Queried - Technical Breakdown

## 🔍 Two Different Query Methods

### Method 1: Frontend Claim Search (WORKING on Oct 14)
**Endpoint:** POST `/api/v1/claims/search/`

**Request:**
```json
{
  "firstServiceDate": "2025-07-01",
  "lastServiceDate": "2025-07-03"
}
```

**Backend Process:**
1. Receives request in `apps/claims/api_views.py::search_claims()`
2. Gets UHC OAuth token: `get_oauth_token(credential)`
3. Calls UHC API:
   ```python
   url = "https://apimarketplace.uhc.com/Claims/api/claim/summary/byprovider/v2.0"
   
   headers = {
       'Authorization': f'Bearer {uhc_token}',
       'Content-Type': 'application/json',
       'Accept': 'application/json',
       'tin': '854203105',
       'firstServiceDt': '07/01/2025',  # MM/DD/YYYY format
       'lastServiceDt': '07/03/2025',
       'payerId': '87726'
   }
   
   response = requests.get(url, headers=headers, timeout=60)
   ```
4. Parses response: `response.json().get('claimsSummaryInfo', [])`
5. Returns claims to frontend

**Result on Oct 14:** ✅ Found 5 claims

---

### Method 2: Bulk Upload Batch Query (CURRENTLY TESTING)
**Endpoint:** POST `/api/v1/claims/bulk/upload/`

**Request:**
```
CSV file + use_batch_query=true
```

**Backend Process:**
1. Upload creates job in `apps/claims/views.py::BulkUploadView`
2. Celery task `process_csv_file` starts
3. Detects date range from CSV: June 24 - July 10 (with 7-day buffer)
4. Calls `batch_query_claims()` in `apps/claims/tasks.py`
5. **EXACT SAME UHC API CALL:**
   ```python
   url = "https://apimarketplace.uhc.com/Claims/api/claim/summary/byprovider/v2.0"
   
   headers = {
       'Authorization': f'Bearer {uhc_token}',
       'Content-Type': 'application/json',
       'Accept': 'application/json',
       'tin': '854203105',
       'firstServiceDt': '06/24/2025',  # MM/DD/YYYY format
       'lastServiceDt': '07/10/2025',
       'payerId': '87726'
   }
   
   response = requests.get(url, headers=headers, timeout=60)
   ```
6. Parses response: `response.json().get('claimsSummaryInfo', [])`
7. Builds claims_map: `{claim_number: claim_data}`
8. Matches CSV rows against claims_map

**Result NOW:** ❌ Returns 0 claims

---

## 🤔 WHY THE DIFFERENCE?

### On Oct 14 (Working):
- UHC returned claims for July 1-3, 2025
- Claims had transaction IDs
- Claims were saved to database
- Export was generated

### On Oct 15 (Not Working):
- **EXACT SAME API CALL**
- **EXACT SAME PARAMETERS**
- UHC returns 0 claims
- Claims no longer available

---

## 🔬 WHAT I TESTED

### Test 1: From My Local Machine (Earlier)
```bash
python3 test_batch_query.py
```
**Result:** 
- Query 2025-06-24 to 2025-07-10: ✅ 32 claims found
- Query 2025-07-01 to 2025-07-03: ✅ 5 claims found
- All 5 target claims were IN the results

### Test 2: From Production Server (Just Now)
```bash
ssh connectme@connectme.be.totesoft.com
cd /var/www/connectme-backend
python3 debug_batch_query.py
```
**Result:**
- Query 2025-06-24 to 2025-07-10: ❌ 0 claims found
- Query 2025-07-01 to 2025-07-03: ❌ 0 claims found
- No claims returned

---

## 💡 THE MYSTERY

**Why did MY local machine find 32 claims but the server found 0?**

### Possible Explanations:

#### 1. Mock Authentication
My local test used: `POST /api/v1/auth/mock/login/`

This might return:
- A different token
- Mock/test credentials
- Access to test data

The server uses the REAL production credentials which might:
- Have different access
- See different data
- Have restrictions

#### 2. Time Window
The claims might only be available:
- For a limited time after processing
- Within certain hours
- During specific billing cycles

#### 3. Test vs Production Environment
- My local queries might hit a test endpoint
- Server queries hit production endpoint  
- Test endpoint has sample data
- Production endpoint has real (but different) data

---

## 🎯 THE SOLUTION

### Verify Which Endpoint We're Hitting

Let me check the credential configuration to see if there are different endpoints for test vs production.
