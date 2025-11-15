# ConnectMe Testing Documentation Index

## 📍 Quick Access - Test Files Location

All test files are in: **`./testcases/datequery-claimstatus-filterbased/`**

### 🚀 START HERE: How to Run Tests
**File:** [`testcases/datequery-claimstatus-filterbased/HOW_TO_RUN_TESTS.md`](testcases/datequery-claimstatus-filterbased/HOW_TO_RUN_TESTS.md)

### 🎯 Browser Console Test (RECOMMENDED)
**File:** [`testcases/datequery-claimstatus-filterbased/BROWSER_CONSOLE_TEST.js`](testcases/datequery-claimstatus-filterbased/BROWSER_CONSOLE_TEST.js)

**Quick Steps:**
1. Login to https://pre-prod.connectme.apps.totessoft.com
2. Press F12 (open DevTools)
3. Go to Console tab
4. Open file: `testcases/datequery-claimstatus-filterbased/BROWSER_CONSOLE_TEST.js`
5. Copy entire contents
6. Paste in Console and press Enter
7. Wait 2-3 minutes for results

---

## 📂 Complete File Structure

```
connectme/
├── TESTING_INDEX.md                          ← YOU ARE HERE
├── testcases/
│   └── datequery-claimstatus-filterbased/    ← ALL TEST FILES HERE
│       ├── HOW_TO_RUN_TESTS.md              ← Instructions
│       ├── BROWSER_CONSOLE_TEST.js          ← Browser test (EASIEST)
│       ├── README.md                         ← Test case documentation
│       ├── MANUAL_TEST_CHECKLIST.md         ← Manual testing guide
│       ├── test_status_filter.py            ← Python automated test
│       ├── test_with_token.py               ← Python test with token
│       └── QUICK_TEST.sh                    ← Shell script runner
│
├── help/                                     ← Documentation
│   ├── admin/
│   │   ├── index.html
│   │   ├── permissions.html
│   │   └── setup.html
│   └── md/
│       ├── DOCUMENTATION_INDEX.md
│       ├── admin_permissions.md
│       └── admin_setup.md
│
└── [other project files...]
```

---

## 🧪 Test Suites Available

### 1. Date Range + Status Filter Tests
**Location:** `testcases/datequery-claimstatus-filterbased/`
**Purpose:** Test claim search with status filters across different date ranges
**Issue:** Verify July+August combined search returns all claims (not just from one month)

**Files:**
- `BROWSER_CONSOLE_TEST.js` - Run in browser (EASIEST)
- `test_with_token.py` - Python script with browser token
- `test_status_filter.py` - Full Python automation
- `README.md` - Detailed test cases (TC001-TC010)
- `MANUAL_TEST_CHECKLIST.md` - Manual testing steps
- `HOW_TO_RUN_TESTS.md` - Complete instructions

---

## 📖 Documentation

### Admin Documentation
**Location:** `help/admin/`
- `index.html` - Admin documentation home
- `permissions.html` - Permission system guide
- `setup.html` - Setup instructions

### Markdown Documentation
**Location:** `help/md/`
- `DOCUMENTATION_INDEX.md` - Master documentation index
- `admin_permissions.md` - Permissions (Markdown)
- `admin_setup.md` - Setup (Markdown)

### API Documentation
**Location:** Root directory
- `API_DOCUMENTATION.md` - API endpoints and usage

### Troubleshooting Guides
**Location:** `help/troubleshooting/`
- `FIX_CLAIM_SEARCH_TIMEOUT.md` - Claim search timeout fixes

---

## 🎯 Common Tasks

### Run Status Filter Tests
```bash
# Option 1: Browser Console (EASIEST - NO SETUP NEEDED)
# 1. Open: testcases/datequery-claimstatus-filterbased/BROWSER_CONSOLE_TEST.js
# 2. Copy contents
# 3. Paste in browser console (F12)

# Option 2: Python with token
cd testcases/datequery-claimstatus-filterbased
python3 test_with_token.py YOUR_TOKEN 1

# Option 3: Full automation (requires Keycloak setup)
./QUICK_TEST.sh username password practice_id
```

### View Test Documentation
```bash
# Instructions
open testcases/datequery-claimstatus-filterbased/HOW_TO_RUN_TESTS.md

# Test cases
open testcases/datequery-claimstatus-filterbased/README.md

# Manual checklist
open testcases/datequery-claimstatus-filterbased/MANUAL_TEST_CHECKLIST.md
```

### View Admin Documentation
```bash
# HTML version
open help/admin/index.html

# Markdown version
open help/md/DOCUMENTATION_INDEX.md
```

---

## 🔍 Finding Files

### Using Terminal
```bash
# Find test files
find . -name "*test*.py" -o -name "*test*.js"

# Find documentation
find . -name "*.md" | grep -E "(README|INDEX|HOW_TO)"

# Find all test directories
find . -type d -name "*test*"
```

### Using File Explorer
1. Navigate to: `connectme/testcases/`
2. Open: `datequery-claimstatus-filterbased/`
3. All test files are here

---

## 📝 Quick Reference

| What You Need | File Location |
|---------------|---------------|
| **Run tests NOW** | `testcases/datequery-claimstatus-filterbased/BROWSER_CONSOLE_TEST.js` |
| **Test instructions** | `testcases/datequery-claimstatus-filterbased/HOW_TO_RUN_TESTS.md` |
| **Test cases** | `testcases/datequery-claimstatus-filterbased/README.md` |
| **Manual testing** | `testcases/datequery-claimstatus-filterbased/MANUAL_TEST_CHECKLIST.md` |
| **Admin docs** | `help/admin/index.html` |
| **API docs** | `API_DOCUMENTATION.md` |
| **All docs index** | `help/md/DOCUMENTATION_INDEX.md` |

---

## 🆘 Need Help?

### Can't find test files?
```bash
cd /Users/ssiva/Documents/1_Data/AI/abce/connectme
ls -la testcases/datequery-claimstatus-filterbased/
```

### Can't find documentation?
```bash
cd /Users/ssiva/Documents/1_Data/AI/abce/connectme
ls -la help/
```

### Want to see all markdown files?
```bash
cd /Users/ssiva/Documents/1_Data/AI/abce/connectme
find . -name "*.md" -type f | sort
```

---

## 🎉 Next Steps

1. **Open this file's location:**
   ```bash
   cd /Users/ssiva/Documents/1_Data/AI/abce/connectme
   open .
   ```

2. **Navigate to test files:**
   ```
   testcases/datequery-claimstatus-filterbased/
   ```

3. **Start with:**
   - `HOW_TO_RUN_TESTS.md` - Read instructions
   - `BROWSER_CONSOLE_TEST.js` - Run the test

---

**Last Updated:** 2024-11-15  
**Project:** ConnectMe Pre-Prod  
**Environment:** https://pre-prod.connectme.apps.totessoft.com

