# ConnectMe Testing Suite

Comprehensive testing scripts for ConnectMe Pre-Prod environment.

## 📋 Test Scripts

### 1. **test_practice_api.py**
Tests the Practice API functionality:
- Practice API without authentication
- Practice API with authentication
- Practice data retrieval
- Bulk upload endpoint accessibility

### 2. **test_claims_search.py**
Tests claims search functionality:
- Date range only search
- Search with patient name
- Search with patient name + DOB
- Different date ranges
- Practice selection

### 3. **test_bulk_upload.py**
Tests CSV bulk upload functionality:
- Upload CSV with patient info (no claim numbers)
- Upload CSV with claim numbers
- Job monitoring and progress tracking
- Results download

## 🚀 Quick Start

### Prerequisites
```bash
# Use Homebrew Python (required for SSL support)
/opt/homebrew/bin/python3 -m pip install requests urllib3
```

### ⚠️ Important: Use Homebrew Python
The system Python 3.9.6 has SSL issues. **Always use `/opt/homebrew/bin/python3`**:

```bash
# Check Homebrew Python version
/opt/homebrew/bin/python3 --version
# Should show: Python 3.13.7 or newer
```

### Run Individual Tests
Pass username and password as arguments:

```bash
# Test Practice API
/opt/homebrew/bin/python3 testing/test_practice_api.py <username> <password>
/opt/homebrew/bin/python3 testing/test_practice_api.py vigneshr mypassword

# Test Claims Search
/opt/homebrew/bin/python3 testing/test_claims_search.py <username> <password>
/opt/homebrew/bin/python3 testing/test_claims_search.py vigneshr mypassword

# Test Bulk Upload
/opt/homebrew/bin/python3 testing/test_bulk_upload.py <username> <password>
/opt/homebrew/bin/python3 testing/test_bulk_upload.py vigneshr mypassword
```

### Run All Tests
Pass username and password as arguments:

```bash
chmod +x testing/run_all_tests.sh
./testing/run_all_tests.sh <username> <password>
./testing/run_all_tests.sh vigneshr mypassword
```

### 🔧 SSL Troubleshooting
If you see SSL errors, see `testing/SSL_FIX_README.md` for details.

## 📊 Test Scenarios

### Claims Search Scenarios
1. **Date Range Only** - Search last 30 days
2. **Date Range + Patient Name** - Search with CHANTAL KISA
3. **Date Range + Patient + DOB** - Full patient info search
4. **Shorter Date Range** - Search last 7 days

### Bulk Upload Scenarios
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

## 🔧 Troubleshooting

### Authentication Fails
```bash
# Check Keycloak status
curl -s "https://auth.totesoft.com/realms/connectme-preprod/.well-known/openid-configuration" | python3 -m json.tool
```

### Practice API Returns Empty
```bash
# Check if practices exist in database
ssh connectme@169.59.163.43 'cd /var/www/connectme-preprod-backend && source venv/bin/activate && python manage.py shell -c "from apps.providers.models import Practice; print(Practice.objects.all())"'
```

### Claims Search Fails
```bash
# Check backend logs
ssh connectme@169.59.163.43 'sudo journalctl -u connectme-preprod-backend -n 100 --no-pager'

# Check UHC API configuration
ssh connectme@169.59.163.43 'cd /var/www/connectme-preprod-backend && source venv/bin/activate && python manage.py shell -c "from apps.providers.models import ProviderCredential; print(ProviderCredential.objects.filter(provider__code=\"UHC\").first().__dict__)"'
```

### Bulk Upload Fails
```bash
# Check Celery worker status
ssh connectme@169.59.163.43 'sudo systemctl status connectme-preprod-celery'

# Check Celery logs
ssh connectme@169.59.163.43 'sudo tail -100 /var/www/connectme-preprod-backend/logs/celery.log'

# Restart Celery if needed
ssh connectme@169.59.163.43 'sudo systemctl restart connectme-preprod-celery'
```

## 📝 Test Output

Each test script provides detailed output:
- ✅ Success messages (green)
- ❌ Error messages (red)
- ℹ️  Info messages (blue)
- Test summaries with pass/fail counts
- Troubleshooting tips for failures

## 🎯 Expected Results

### All Tests Passing
```
📊 TEST SUMMARY
================================================================================
Total Tests: 4
✅ Passed: 4
❌ Failed: 0
Success Rate: 100.0%
```

### Some Tests Failing
The scripts will provide specific error messages and troubleshooting steps.

## 🔐 Security Notes

- **Never commit credentials** to version control
- Use environment variables for sensitive data:
  ```bash
  export CONNECTME_USERNAME="your_username"
  export CONNECTME_PASSWORD="your_password"
  ```
- Update scripts to read from environment:
  ```python
  import os
  TEST_USERNAME = os.environ.get('CONNECTME_USERNAME', 'vigneshr')
  TEST_PASSWORD = os.environ.get('CONNECTME_PASSWORD', 'your_password_here')
  ```

## 📚 Additional Resources

- **Backend API Docs**: https://pre-prod.connectme.be.totessoft.com/api/docs/
- **Frontend**: https://pre-prod.connectme.apps.totessoft.com
- **Keycloak Admin**: https://auth.totesoft.com/admin/

## 🐛 Reporting Issues

When reporting test failures, include:
1. Test script name and scenario
2. Full error output
3. Backend logs (if available)
4. Environment details (OS, Python version)

## 📅 Test Maintenance

- Update test data regularly (dates, patient names)
- Review and update expected results
- Add new test scenarios as features are added
- Keep credentials secure and up-to-date
