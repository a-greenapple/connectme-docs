# Testing Scripts - Quick Usage Guide

## ✅ All Scripts Now Accept Command-Line Arguments!

No need to edit files - just pass username and password as arguments.

---

## 🚀 Usage

### Run Individual Tests

```bash
# Test Practice API
python3 testing/test_practice_api.py vigneshr yourpassword

# Test Claims Search
python3 testing/test_claims_search.py vigneshr yourpassword

# Test Bulk Upload
python3 testing/test_bulk_upload.py vigneshr yourpassword

# Diagnose Auth Issues
python3 testing/diagnose_auth_issue.py
```

### Run All Tests

```bash
./testing/run_all_tests.sh vigneshr yourpassword
```

---

## 📋 Examples

### Example 1: Test Claims Search
```bash
cd /Users/ssiva/Documents/1_Data/AI/abce/connectme
python3 testing/test_claims_search.py vigneshr mypassword
```

**Output:**
```
================================================================================
🚀 ConnectMe Claims Search Test Suite
================================================================================
🚀 Test Time: 2025-11-07 12:30:00
🚀 Username: vigneshr
================================================================================

✅ Authenticated as: vigneshr
✅ Found practice: RSM (ID: 1, TIN: 854203105)
✅ Search successful! Found 12 claim(s)
```

### Example 2: Run All Tests
```bash
cd /Users/ssiva/Documents/1_Data/AI/abce/connectme
./testing/run_all_tests.sh vigneshr mypassword
```

**Output:**
```
================================================================================
🚀 ConnectMe Pre-Prod - Master Test Suite
================================================================================
Username: vigneshr
================================================================================

✅ Practice API Tests - PASSED
✅ Claims Search Tests - PASSED
✅ Bulk Upload Tests - PASSED

📊 FINAL TEST SUMMARY
Total Test Suites: 3
✅ Passed: 3
❌ Failed: 0
Success Rate: 100%
🎉 All tests passed!
```

---

## 🔧 Troubleshooting

### Error: "Please provide password!"

**Problem:** No password provided as argument

**Solution:**
```bash
# ❌ Wrong
python3 testing/test_claims_search.py

# ✅ Correct
python3 testing/test_claims_search.py vigneshr mypassword
```

### Error: "Authentication failed: 401"

**Problem:** Wrong username or password

**Solution:**
- Verify credentials are correct
- Try logging in via frontend first
- Check if user exists in Keycloak

### Error: "Failed to get practices"

**Problem:** No practices in database or permission issue

**Solution:**
```bash
# Check if practices exist
ssh connectme@169.59.163.43 'cd /var/www/connectme-preprod-backend && source venv/bin/activate && python manage.py shell -c "from apps.providers.models import Practice; print(list(Practice.objects.all()))"'
```

---

## 📝 Script Details

### test_practice_api.py
- Tests Practice API without auth
- Tests Practice API with auth
- Tests bulk upload endpoint
- **Usage:** `python3 test_practice_api.py <username> <password>`

### test_claims_search.py
- Tests 4 different search scenarios
- Validates practice selection
- Tests UHC API integration
- **Usage:** `python3 test_claims_search.py <username> <password>`

### test_bulk_upload.py
- Tests CSV upload with patient info
- Tests CSV upload with claim numbers
- Monitors job processing
- Downloads results
- **Usage:** `python3 test_bulk_upload.py <username> <password>`

### diagnose_auth_issue.py
- Interactive diagnostic tool
- Tests token generation
- Tests API endpoints
- **Usage:** `python3 diagnose_auth_issue.py` (prompts for credentials)

### run_all_tests.sh
- Runs all test scripts
- Generates summary report
- **Usage:** `./run_all_tests.sh <username> <password>`

---

## 🎯 Quick Test Commands

```bash
# Navigate to project
cd /Users/ssiva/Documents/1_Data/AI/abce/connectme

# Test everything
./testing/run_all_tests.sh vigneshr mypassword

# Test just claims search
python3 testing/test_claims_search.py vigneshr mypassword

# Test just bulk upload
python3 testing/test_bulk_upload.py vigneshr mypassword

# Diagnose auth issues
python3 testing/diagnose_auth_issue.py
```

---

## 🔐 Security Note

**Never commit passwords to git!**

For CI/CD, use environment variables:
```bash
export TEST_USERNAME="vigneshr"
export TEST_PASSWORD="mypassword"

# Then modify scripts to read from env:
python3 testing/test_claims_search.py $TEST_USERNAME $TEST_PASSWORD
```

---

**All scripts are ready to use! Just provide your credentials as arguments.** 🎉

