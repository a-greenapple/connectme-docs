# ConnectMe Testing Suite - Complete Summary
**Date:** November 7, 2025  
**Status:** ✅ READY TO USE

---

## 📁 Testing Files Structure

```
connectme/
└── testing/
    ├── README.md                      # Complete testing documentation
    ├── run_all_tests.sh               # Master test runner
    ├── test_practice_api.py           # Practice API tests
    ├── test_claims_search.py          # Claims search tests
    ├── test_bulk_upload.py            # Bulk upload tests
    └── test_bulk_upload_by_patient.py # Legacy test (kept for reference)
```

---

## 🚀 Quick Start Guide

### 1. **Update Credentials**

Edit each test script and update these lines:
```python
TEST_USERNAME = "your_username"  # e.g., "vigneshr"
TEST_PASSWORD = "your_password"  # Your actual password
```

Files to update:
- `testing/test_practice_api.py`
- `testing/test_claims_search.py`
- `testing/test_bulk_upload.py`

### 2. **Run Tests**

**Option A: Run All Tests**
```bash
cd /Users/ssiva/Documents/1_Data/AI/abce/connectme
./testing/run_all_tests.sh
```

**Option B: Run Individual Tests**
```bash
# Test Practice API
python3 testing/test_practice_api.py

# Test Claims Search
python3 testing/test_claims_search.py

# Test Bulk Upload
python3 testing/test_bulk_upload.py
```

---

## 🧪 Test Coverage

### 1. **Practice API Tests** (`test_practice_api.py`)

Tests:
- ✅ Practice API without authentication
- ✅ Practice API with authentication
- ✅ Practice data retrieval
- ✅ Bulk upload endpoint accessibility

**What it validates:**
- Practice API returns data
- Pagination works correctly
- Authentication is optional (AllowAny)
- Practice data includes TIN and name

### 2. **Claims Search Tests** (`test_claims_search.py`)

Scenarios:
1. **Date Range Only** - Last 30 days
2. **Date Range + Patient Name** - With CHANTAL KISA
3. **Date Range + Patient + DOB** - Full patient info
4. **Shorter Date Range** - Last 7 days

**What it validates:**
- Claims search API works
- Practice ID is passed correctly
- Different search parameters work
- Results are returned in correct format
- UHC API integration works

### 3. **Bulk Upload Tests** (`test_bulk_upload.py`)

Scenarios:
1. **Patient Info Only** - CSV without claim numbers
   ```csv
   first_name,last_name,date_of_birth,first_service_date,last_service_date
   CHANTAL,KISA,05/10/1975,10/01/2025,10/31/2025
   ```

2. **With Claim Numbers** - CSV with specific claims
   ```csv
   claim_number,first_name,last_name,date_of_birth
   FH65850583,CHANTAL,KISA,05/10/1975
   ```

**What it validates:**
- CSV upload works
- Authentication with kc_access_token
- Celery job processing
- Job status monitoring
- Results download

---

## 📊 Expected Output

### Successful Test Run

```
================================================================================
🚀 ConnectMe Pre-Prod - Master Test Suite
================================================================================
Test Time: 2025-11-07 12:30:00
================================================================================

================================================================================
Running: Practice API Tests
================================================================================
✅ Practice API accessible without auth
✅ Found 1 practice(s)
  - RSM (TIN: 854203105)
✅ Practice API Tests - PASSED

================================================================================
Running: Claims Search Tests
================================================================================
✅ Authenticated as: vigneshr
✅ Found practice: RSM (ID: 1, TIN: 854203105)
✅ Search successful! Found 12 claim(s)
✅ Claims Search Tests - PASSED

================================================================================
Running: Bulk Upload Tests
================================================================================
✅ Authenticated as: vigneshr
✅ Created: test_patients.csv
✅ Upload successful!
✅ Job finished with status: COMPLETED
✅ Bulk Upload Tests - PASSED

================================================================================
📊 FINAL TEST SUMMARY
================================================================================
Total Test Suites: 3
✅ Passed: 3
❌ Failed: 0
Success Rate: 100%
🎉 All tests passed!
================================================================================
```

---

## 🔧 Troubleshooting

### Issue: Authentication Fails

**Symptoms:**
```
❌ Authentication failed: 401
Error: Invalid user credentials
```

**Solutions:**
1. Verify username and password are correct
2. Check if user exists in Keycloak
3. Try logging in via frontend first

### Issue: Practice API Returns Empty

**Symptoms:**
```
❌ No practices found in response
```

**Solutions:**
1. Check if practices exist in database:
   ```bash
   ssh connectme@169.59.163.43 'cd /var/www/connectme-preprod-backend && source venv/bin/activate && python manage.py shell -c "from apps.providers.models import Practice; print(list(Practice.objects.all()))"'
   ```

2. Verify practice is active:
   ```python
   Practice.objects.filter(is_active=True)
   ```

### Issue: Claims Search Fails

**Symptoms:**
```
❌ Search failed: 500
Error: Internal Server Error
```

**Solutions:**
1. Check backend logs:
   ```bash
   ssh connectme@169.59.163.43 'sudo journalctl -u connectme-preprod-backend -n 100'
   ```

2. Verify UHC API credentials:
   ```bash
   ssh connectme@169.59.163.43 'cd /var/www/connectme-preprod-backend && source venv/bin/activate && python manage.py shell -c "from apps.providers.models import ProviderCredential; cred = ProviderCredential.objects.filter(provider__code=\"UHC\").first(); print(f\"Auth URL: {cred.auth_url}\"); print(f\"API Base: {cred.api_base_url}\")"'
   ```

3. Check practice has payer mapping:
   ```bash
   ssh connectme@169.59.163.43 'cd /var/www/connectme-preprod-backend && source venv/bin/activate && python manage.py shell -c "from apps.providers.models import PracticePayerMapping; print(list(PracticePayerMapping.objects.filter(is_active=True)))"'
   ```

### Issue: Bulk Upload Fails

**Symptoms:**
```
❌ Upload failed: 401
Error: Unauthorized
```

**Solutions:**
1. Check Celery worker status:
   ```bash
   ssh connectme@169.59.163.43 'sudo systemctl status connectme-preprod-celery'
   ```

2. Restart Celery if needed:
   ```bash
   ssh connectme@169.59.163.43 'sudo systemctl restart connectme-preprod-celery'
   ```

3. Check Celery logs:
   ```bash
   ssh connectme@169.59.163.43 'sudo tail -100 /var/www/connectme-preprod-backend/logs/celery.log'
   ```

4. Verify token is correct:
   - Check browser console for `kc_access_token`
   - Ensure frontend is sending token in Authorization header

---

## 🎯 What Each Test Validates

### Practice API Tests
- ✅ Backend API is accessible
- ✅ Practice data exists in database
- ✅ Pagination works correctly
- ✅ Response format is correct

### Claims Search Tests
- ✅ Authentication works
- ✅ Practice selection works
- ✅ UHC API integration works
- ✅ Different search parameters work
- ✅ Results are returned correctly

### Bulk Upload Tests
- ✅ CSV upload works
- ✅ Celery worker is running
- ✅ Job processing works
- ✅ Job monitoring works
- ✅ Results download works

---

## 📝 Test Data

### Test Patients
- **CHANTAL KISA** - DOB: 05/10/1975
- **JOHN DOE** - DOB: 01/15/1980
- **JANE SMITH** - DOB: 05/20/1975

### Test Claims
- **FH65850583** - CHANTAL KISA
- **FH73828971** - JOHN DOE
- **FH73828973** - JANE SMITH

### Test Practice
- **Name:** RSM
- **TIN:** 854203105
- **Provider:** UnitedHealthcare (UHC)
- **Payer ID:** 87726

---

## 🔐 Security Best Practices

1. **Never commit credentials** to version control
2. Use environment variables:
   ```bash
   export CONNECTME_USERNAME="your_username"
   export CONNECTME_PASSWORD="your_password"
   ```

3. Update scripts to use environment variables:
   ```python
   import os
   TEST_USERNAME = os.environ.get('CONNECTME_USERNAME', 'vigneshr')
   TEST_PASSWORD = os.environ.get('CONNECTME_PASSWORD')
   ```

4. Add `.env` to `.gitignore`

---

## 📚 Additional Resources

- **Backend API Docs:** https://pre-prod.connectme.be.totessoft.com/api/docs/
- **Frontend:** https://pre-prod.connectme.apps.totessoft.com
- **Keycloak Admin:** https://auth.totesoft.com/admin/

---

## ✅ Checklist Before Running Tests

- [ ] Updated `TEST_USERNAME` in all test scripts
- [ ] Updated `TEST_PASSWORD` in all test scripts
- [ ] Verified backend is running
- [ ] Verified Celery worker is running
- [ ] Verified frontend is accessible
- [ ] Have network access to pre-prod environment

---

## 🎉 Success Criteria

All tests pass when:
- ✅ Practice API returns RSM practice
- ✅ Claims search returns results (or empty if no claims)
- ✅ Bulk upload creates job and processes CSV
- ✅ No 401/403/500 errors
- ✅ All services are running correctly

---

**Ready to test! Run `./testing/run_all_tests.sh` to start.** 🚀

