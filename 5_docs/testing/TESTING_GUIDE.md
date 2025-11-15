# ConnectMe Testing Guide

## 🧪 How to Run Tests

### 1. Backend API Tests (Pytest)

```bash
# Activate virtual environment
cd connectme-backend
source venv/bin/activate

# Install test dependencies
pip install pytest pytest-django pytest-cov

# Run all tests
pytest

# Run specific test file
pytest apps/claims/tests/test_tasks.py

# Run with coverage
pytest --cov=apps --cov-report=html

# Run verbose
pytest -v
```

### 2. Frontend E2E Tests (Playwright)

```bash
# Go to frontend directory
cd connectme-frontend

# Install Playwright
npm install --save-dev @playwright/test
npx playwright install

# Run all tests
npx playwright test

# Run specific test
npx playwright test tests/bulk-upload.spec.ts

# Run with UI mode (interactive)
npx playwright test --ui

# Run and show browser
npx playwright test --headed

# Generate test report
npx playwright show-report
```

### 3. Manual Testing Checklist

#### Bulk Upload Test:
- [ ] Upload CSV with valid format
- [ ] Upload CSV with service dates (auto-detection)
- [ ] Upload CSV without service dates (manual date entry)
- [ ] Upload large CSV (100+ rows)
- [ ] Cancel in-progress job
- [ ] View results
- [ ] Download results CSV

#### Claim Search Test:
- [ ] Search single claim
- [ ] Search with date range
- [ ] View claim details
- [ ] Test with invalid claim number

## 📋 Test Data

### Valid CSV Format:
```csv
claim_number,first_name,last_name,date_of_birth,subscriber_id,first_service_date,last_service_date
FF39120517,JINWOO,SOK,03/10/2009,0302602155,2025-08-05,2025-08-05
52281881,MARK,HENDERSON,02/09/1966,0990551003,2025-08-04,2025-08-04
```

## 🔍 Monitoring Test Results

### Check Celery Logs:
```bash
ssh user@server "sudo journalctl -u celery.service -n 100 --no-pager"
```

### Check Gunicorn Logs:
```bash
ssh user@server "sudo journalctl -u gunicorn.service -n 100 --no-pager"
```

### Check Frontend Logs:
```bash
ssh user@server "pm2 logs connectme-frontend --lines 50"
```

## 🎯 Test Scenarios

### Scenario 1: Auto-Date Detection
**Goal:** Verify system auto-detects date range from CSV

**Steps:**
1. Create CSV with service dates (Aug 2025)
2. Upload without setting date range
3. Verify logs show: "Auto-detected date range from CSV"
4. Check results

**Expected:** System queries July-Sept 2025

### Scenario 2: Manual Date Override
**Goal:** Verify manual dates take precedence

**Steps:**
1. Create CSV with service dates (Aug 2025)
2. Set date range to Jan-Dec 2024
3. Upload
4. Verify system uses 2024 dates

**Expected:** System queries Jan-Dec 2024

### Scenario 3: Batch Query Performance
**Goal:** Verify batch query is faster

**Steps:**
1. Create CSV with 100 claims
2. Enable batch query
3. Upload and time it
4. Disable batch query
5. Upload same CSV and time it

**Expected:** Batch query is 50-90x faster

