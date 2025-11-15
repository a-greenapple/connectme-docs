# ConnectMe Test Cases

## 📁 Test Suites

### 1. Date Range + Claim Status Filter Tests
**Directory:** [`datequery-claimstatus-filterbased/`](datequery-claimstatus-filterbased/)

**Purpose:** Test claim search functionality with status filters across different date ranges

**Issue Being Tested:**
- When searching July 1-30 with DENIED filter → Returns 2 claims
- When searching Aug 1-30 with DENIED filter → Returns 3 claims
- When searching July 1-Aug 31 with DENIED filter → Should return 5 claims (but might return only 2)

**Quick Start:**
1. Open [`datequery-claimstatus-filterbased/HOW_TO_RUN_TESTS.md`](datequery-claimstatus-filterbased/HOW_TO_RUN_TESTS.md)
2. Use [`datequery-claimstatus-filterbased/BROWSER_CONSOLE_TEST.js`](datequery-claimstatus-filterbased/BROWSER_CONSOLE_TEST.js) (EASIEST)

**Files:**
- `BROWSER_CONSOLE_TEST.js` - Browser console test (recommended)
- `HOW_TO_RUN_TESTS.md` - Complete instructions
- `README.md` - Detailed test case documentation
- `MANUAL_TEST_CHECKLIST.md` - Manual testing guide
- `test_status_filter.py` - Python automated test
- `test_with_token.py` - Python test with browser token
- `QUICK_TEST.sh` - Shell script runner

---

## 🚀 Quick Access

### Run Tests Immediately
```bash
# Browser Console (EASIEST - NO SETUP)
# 1. Login to https://pre-prod.connectme.apps.totessoft.com
# 2. Press F12
# 3. Open: datequery-claimstatus-filterbased/BROWSER_CONSOLE_TEST.js
# 4. Copy & paste in console
# 5. Press Enter

# Python with token
cd datequery-claimstatus-filterbased
python3 test_with_token.py YOUR_TOKEN 1
```

### View Documentation
```bash
# Test instructions
open datequery-claimstatus-filterbased/HOW_TO_RUN_TESTS.md

# Test cases
open datequery-claimstatus-filterbased/README.md

# Manual checklist
open datequery-claimstatus-filterbased/MANUAL_TEST_CHECKLIST.md
```

---

## 📊 Test Coverage

### Current Test Suites
- ✅ Date Range + Status Filter Tests

### Planned Test Suites
- ⏳ Bulk Upload Tests
- ⏳ User Management Tests
- ⏳ Workflow Tests
- ⏳ API Integration Tests

---

## 📝 Adding New Test Suites

When adding a new test suite, create a directory with:

```
testcases/
└── your-test-suite-name/
    ├── README.md                  ← Test case documentation
    ├── HOW_TO_RUN_TESTS.md       ← Instructions
    ├── BROWSER_CONSOLE_TEST.js   ← Browser test (if applicable)
    ├── test_*.py                  ← Python tests
    ├── MANUAL_TEST_CHECKLIST.md  ← Manual testing guide
    └── *.sh                       ← Shell scripts
```

---

## 🔗 Related Documentation

- **Main Testing Index:** [`../TESTING_INDEX.md`](../TESTING_INDEX.md)
- **API Documentation:** [`../API_DOCUMENTATION.md`](../API_DOCUMENTATION.md)
- **Admin Documentation:** [`../help/admin/index.html`](../help/admin/index.html)
- **Documentation Index:** [`../help/md/DOCUMENTATION_INDEX.md`](../help/md/DOCUMENTATION_INDEX.md)

---

**Project:** ConnectMe  
**Environment:** Pre-Prod  
**URL:** https://pre-prod.connectme.apps.totessoft.com

