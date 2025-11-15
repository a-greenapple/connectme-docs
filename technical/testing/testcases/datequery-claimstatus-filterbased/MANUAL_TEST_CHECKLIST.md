# Manual Test Checklist - Date Range + Status Filter

## Pre-Test Setup

- [ ] Login to pre-prod: https://pre-prod.connectme.apps.totessoft.com
- [ ] Navigate to Claims Search page
- [ ] Select Practice: ________________
- [ ] Note current date: ________________

## Test Execution

### Test 1: July 2024 with DENIED Filter

**Steps:**
1. [ ] Set First Service Date: `2024-07-01`
2. [ ] Set Last Service Date: `2024-07-30`
3. [ ] Set Status Filter: `DENIED`
4. [ ] Click "Search Claims"
5. [ ] Wait for results

**Results:**
- [ ] Search completed successfully
- [ ] Number of claims returned: ________
- [ ] Claim numbers: ________________________________
- [ ] All claims show status "DENIED": YES / NO
- [ ] All service dates within July 1-30: YES / NO

**Screenshot:** `test1_july_denied.png`

---

### Test 2: August 2024 with DENIED Filter

**Steps:**
1. [ ] Set First Service Date: `2024-08-01`
2. [ ] Set Last Service Date: `2024-08-30`
3. [ ] Set Status Filter: `DENIED`
4. [ ] Click "Search Claims"
5. [ ] Wait for results

**Results:**
- [ ] Search completed successfully
- [ ] Number of claims returned: ________
- [ ] Claim numbers: ________________________________
- [ ] All claims show status "DENIED": YES / NO
- [ ] All service dates within Aug 1-30: YES / NO

**Screenshot:** `test2_aug_denied.png`

---

### Test 3: July-August 2024 with DENIED Filter (CRITICAL)

**Steps:**
1. [ ] Set First Service Date: `2024-07-01`
2. [ ] Set Last Service Date: `2024-08-31`
3. [ ] Set Status Filter: `DENIED`
4. [ ] Click "Search Claims"
5. [ ] Wait for results

**Results:**
- [ ] Search completed successfully
- [ ] Number of claims returned: ________
- [ ] Claim numbers: ________________________________
- [ ] All claims show status "DENIED": YES / NO
- [ ] All service dates within July 1 - Aug 31: YES / NO

**Critical Verification:**
```
Expected Count = Test 1 Count + Test 2 Count
Expected: ________ (from Test 1) + ________ (from Test 2) = ________
Actual: ________

PASS / FAIL: ________
```

**Screenshot:** `test3_july_aug_denied.png`

---

### Test 4: July-August 2024 WITHOUT Filter (Baseline)

**Steps:**
1. [ ] Set First Service Date: `2024-07-01`
2. [ ] Set Last Service Date: `2024-08-31`
3. [ ] Set Status Filter: `All Statuses`
4. [ ] Click "Search Claims"
5. [ ] Wait for results

**Results:**
- [ ] Search completed successfully
- [ ] Total claims returned: ________
- [ ] Status breakdown (count each):
  - DENIED: ________
  - PAID: ________
  - PENDING: ________
  - FINALIZED: ________
  - PARTIAL: ________
  - Other: ________

**Verification:**
```
DENIED count from Test 4: ________
DENIED count from Test 3: ________

Match: YES / NO
```

**Screenshot:** `test4_july_aug_all.png`

---

### Test 5: Claim Number Cross-Check

**Steps:**
1. [ ] List all claim numbers from Test 1: ________________________________
2. [ ] List all claim numbers from Test 2: ________________________________
3. [ ] List all claim numbers from Test 3: ________________________________

**Verification:**
- [ ] All claims from Test 1 appear in Test 3: YES / NO
- [ ] All claims from Test 2 appear in Test 3: YES / NO
- [ ] No duplicate claims in Test 3: YES / NO
- [ ] No extra claims in Test 3: YES / NO

**Missing Claims (if any):**
- From Test 1 but not in Test 3: ________________________________
- From Test 2 but not in Test 3: ________________________________

---

## Backend Log Verification

### Check Logs for Test 1 (July)
```bash
ssh connectme@169.59.163.43 'journalctl -u connectme-preprod-backend -n 100 --no-pager | grep -A 3 "Retrieved.*claims from Summary API" | tail -20'
```

**Log Output:**
```
Retrieved X claims from Summary API
Claim status breakdown: {...}
Status filter 'DENIED' applied: X claims → Y claims
```

- [ ] Retrieved count: ________
- [ ] Status breakdown: ________________________________
- [ ] Filtered count: ________

---

### Check Logs for Test 2 (August)

**Log Output:**
```
Retrieved X claims from Summary API
Claim status breakdown: {...}
Status filter 'DENIED' applied: X claims → Y claims
```

- [ ] Retrieved count: ________
- [ ] Status breakdown: ________________________________
- [ ] Filtered count: ________

---

### Check Logs for Test 3 (July-August)

**Log Output:**
```
Retrieved X claims from Summary API
Claim status breakdown: {...}
Status filter 'DENIED' applied: X claims → Y claims
```

- [ ] Retrieved count: ________
- [ ] Status breakdown: ________________________________
- [ ] Filtered count: ________

**Critical Check:**
```
Is Test 3 "Retrieved count" >= Test 1 "Retrieved count" + Test 2 "Retrieved count"?
YES / NO

If NO, this indicates UHC API is not returning all claims for the larger date range!
```

---

## Issue Analysis

### If Test 3 Count < Expected Count:

**Possible Root Causes:**

1. [ ] **UHC API Pagination Issue**
   - UHC returns max N claims per request
   - Larger date range hits this limit
   - Check logs for pagination indicators

2. [ ] **UHC API Date Range Behavior**
   - UHC prioritizes certain claims
   - Check if missing claims are from specific dates

3. [ ] **Backend Filter Logic**
   - Filter applied incorrectly
   - Check logs for filter application

4. [ ] **Response Caching**
   - Browser caching old results
   - Try hard refresh (Ctrl+Shift+R)

5. [ ] **Database Deduplication**
   - Claims being deduplicated incorrectly
   - Check unique constraints

---

## Additional Tests

### Test 6: Different Status Filters

Repeat Test 3 with different statuses:

**PAID Filter:**
- [ ] Claims returned: ________
- [ ] All claims are PAID: YES / NO

**PENDING Filter:**
- [ ] Claims returned: ________
- [ ] All claims are PENDING: YES / NO

**FINALIZED Filter:**
- [ ] Claims returned: ________
- [ ] All claims are FINALIZED: YES / NO

---

### Test 7: Case Sensitivity

Test with lowercase status:

**Steps:**
1. [ ] Manually edit status filter in browser dev tools to `"denied"` (lowercase)
2. [ ] Submit search
3. [ ] Compare results with Test 3

**Results:**
- [ ] Same count as Test 3: YES / NO
- [ ] Same claim numbers: YES / NO

---

## Test Summary

**Date:** ________________
**Tester:** ________________
**Environment:** Pre-Prod
**Practice ID:** ________________

**Overall Result:** PASS / FAIL

**Issues Found:**
1. ________________________________
2. ________________________________
3. ________________________________

**Recommendations:**
1. ________________________________
2. ________________________________
3. ________________________________

**Next Steps:**
- [ ] Report issues to development team
- [ ] Provide screenshots and logs
- [ ] Re-test after fixes
- [ ] Document workarounds if needed

---

## Attachments

- [ ] Screenshot: test1_july_denied.png
- [ ] Screenshot: test2_aug_denied.png
- [ ] Screenshot: test3_july_aug_denied.png
- [ ] Screenshot: test4_july_aug_all.png
- [ ] Backend logs: backend_logs.txt
- [ ] Test results spreadsheet: test_results.xlsx

