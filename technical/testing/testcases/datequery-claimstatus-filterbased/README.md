# Date Range Query with Claim Status Filter - Test Cases

## Overview
Test cases to verify that claim status filtering works correctly across different date ranges and returns consistent results.

## Test Scenario
**Issue**: When searching with status filter across different date ranges, the results are inconsistent.
- July 1-30 with DENIED filter: Returns 2 claims
- Aug 1-30 with DENIED filter: Returns 3 claims
- July 1-Aug 31 with DENIED filter: Returns only 2 claims (expected 5)

## Test Environment
- **Backend**: Django REST Framework with UHC API integration
- **Frontend**: Next.js React application
- **API Endpoint**: `POST /api/v1/claims/search/`
- **Filter Parameter**: `statusFilter` (DENIED, PAID, PENDING, PARTIAL, FINALIZED)

## Test Cases

### TC001: Single Month - July with DENIED Filter
**Objective**: Verify DENIED claims are returned for July date range

**Prerequisites**:
- User is authenticated
- Practice has active UHC credentials
- Known DENIED claims exist in July

**Test Data**:
```json
{
  "firstServiceDate": "2024-07-01",
  "lastServiceDate": "2024-07-30",
  "practiceId": "1",
  "statusFilter": "DENIED"
}
```

**Expected Results**:
- Status: 200 OK
- Response contains only claims with `claimStatus: "DENIED"`
- All claims have service dates between July 1-30
- Count matches actual DENIED claims in that period

**Verification**:
1. Check backend logs for: `Claim status breakdown: {...}`
2. Verify: `Status filter 'DENIED' applied: X claims → Y claims`
3. Confirm all returned claims have `status: "DENIED"`

---

### TC002: Single Month - August with DENIED Filter
**Objective**: Verify DENIED claims are returned for August date range

**Test Data**:
```json
{
  "firstServiceDate": "2024-08-01",
  "lastServiceDate": "2024-08-30",
  "practiceId": "1",
  "statusFilter": "DENIED"
}
```

**Expected Results**:
- Status: 200 OK
- Response contains only claims with `claimStatus: "DENIED"`
- All claims have service dates between Aug 1-30
- Count matches actual DENIED claims in that period

---

### TC003: Two Months - July to August with DENIED Filter
**Objective**: Verify DENIED claims from both months are returned

**Test Data**:
```json
{
  "firstServiceDate": "2024-07-01",
  "lastServiceDate": "2024-08-31",
  "practiceId": "1",
  "statusFilter": "DENIED"
}
```

**Expected Results**:
- Status: 200 OK
- Response contains DENIED claims from BOTH July AND August
- **Total count = TC001 count + TC002 count**
- All claims have service dates between July 1 - Aug 31
- No duplicate claims

**Critical Check**:
```
If TC001 returns 2 claims and TC002 returns 3 claims,
then TC003 MUST return 5 claims (not 2 or 3)
```

---

### TC004: Verify UHC API Returns All Claims (No Filter)
**Objective**: Confirm UHC API returns all claims before filtering

**Test Data**:
```json
{
  "firstServiceDate": "2024-07-01",
  "lastServiceDate": "2024-08-31",
  "practiceId": "1"
  // NO statusFilter
}
```

**Expected Results**:
- Status: 200 OK
- Response contains ALL claims (DENIED, PAID, PENDING, etc.)
- Backend logs show: `Retrieved X claims from Summary API`
- Backend logs show: `Claim status breakdown: {DENIED: Y, PAID: Z, ...}`

**Verification**:
- Check if total claims = sum of all statuses
- Verify no claims are missing

---

### TC005: Compare Filtered vs Unfiltered Results
**Objective**: Verify filter doesn't lose claims

**Steps**:
1. Search July 1 - Aug 31 WITHOUT filter (get all claims)
2. Search July 1 - Aug 31 WITH DENIED filter
3. Manually count DENIED claims from step 1
4. Compare with count from step 2

**Expected Results**:
- Count from step 3 = Count from step 2
- No claims are lost during filtering

---

### TC006: Multiple Status Filters - Sequential Tests
**Objective**: Verify each status filter works independently

**Test Data** (run separately):
```json
// Test 1: PAID
{
  "firstServiceDate": "2024-07-01",
  "lastServiceDate": "2024-08-31",
  "practiceId": "1",
  "statusFilter": "PAID"
}

// Test 2: PENDING
{
  "firstServiceDate": "2024-07-01",
  "lastServiceDate": "2024-08-31",
  "practiceId": "1",
  "statusFilter": "PENDING"
}

// Test 3: DENIED
{
  "firstServiceDate": "2024-07-01",
  "lastServiceDate": "2024-08-31",
  "practiceId": "1",
  "statusFilter": "DENIED"
}
```

**Expected Results**:
- Each filter returns only claims matching that status
- Sum of all filtered results ≤ total unfiltered results
- No overlap between different status results

---

### TC007: Edge Case - Single Day with Filter
**Objective**: Verify filter works for single-day date range

**Test Data**:
```json
{
  "firstServiceDate": "2024-07-15",
  "lastServiceDate": "2024-07-15",
  "practiceId": "1",
  "statusFilter": "DENIED"
}
```

**Expected Results**:
- Returns only DENIED claims from July 15
- No claims from other dates

---

### TC008: Edge Case - 90 Day Range with Filter
**Objective**: Verify filter works for maximum date range

**Test Data**:
```json
{
  "firstServiceDate": "2024-06-01",
  "lastServiceDate": "2024-08-30",
  "practiceId": "1",
  "statusFilter": "DENIED"
}
```

**Expected Results**:
- Returns all DENIED claims across 3 months
- No pagination issues
- All claims within date range

---

### TC009: Case Sensitivity - Status Filter
**Objective**: Verify status filter is case-insensitive

**Test Data** (run separately):
```json
// Test 1: Uppercase
{"statusFilter": "DENIED"}

// Test 2: Lowercase
{"statusFilter": "denied"}

// Test 3: Mixed case
{"statusFilter": "Denied"}
```

**Expected Results**:
- All three return identical results
- Backend converts to uppercase before comparison

---

### TC010: Invalid Status Filter
**Objective**: Verify handling of invalid status values

**Test Data**:
```json
{
  "firstServiceDate": "2024-07-01",
  "lastServiceDate": "2024-07-30",
  "practiceId": "1",
  "statusFilter": "INVALID_STATUS"
}
```

**Expected Results**:
- Returns empty results (no claims match)
- OR returns error message
- No server crash

---

## Debugging Checklist

When TC003 fails (combined date range returns fewer claims):

### 1. Check Backend Logs
```bash
ssh connectme@169.59.163.43 'journalctl -u connectme-preprod-backend -n 200 --no-pager | grep -A 5 "Retrieved.*claims from Summary API"'
```

Look for:
- `Retrieved X claims from Summary API`
- `Claim status breakdown: {...}`
- `Status filter 'DENIED' applied: X claims → Y claims`

### 2. Check UHC API Response
```bash
ssh connectme@169.59.163.43 'journalctl -u connectme-preprod-backend -n 200 --no-pager | grep "UHC Response"'
```

Look for:
- Response status codes
- Any error messages
- Pagination indicators

### 3. Verify Claim Numbers
For each test, note the actual claim numbers returned:
- TC001 (July): Claim #1, Claim #2
- TC002 (Aug): Claim #3, Claim #4, Claim #5
- TC003 (July-Aug): Should include ALL of the above

### 4. Check for Duplicates
```python
# In backend, add temporary logging
claim_numbers = [c.get('claimNumber') for c in claims]
logger.info(f"Claim numbers: {claim_numbers}")
if len(claim_numbers) != len(set(claim_numbers)):
    logger.warning("Duplicate claims detected!")
```

---

## Root Cause Analysis

### Possible Issues:

1. **UHC API Pagination**
   - UHC might return max N claims per request
   - Larger date ranges hit this limit
   - Solution: Implement pagination handling

2. **UHC API Date Range Behavior**
   - UHC might process date ranges differently
   - Might prioritize recent claims
   - Solution: Check UHC API documentation

3. **Backend Filtering Logic**
   - Filter might be applied incorrectly
   - Case sensitivity issues
   - Solution: Review filter implementation

4. **Response Caching**
   - Browser or backend might cache responses
   - Solution: Clear cache, add cache-busting headers

5. **Database Deduplication**
   - Claims might be deduplicated incorrectly
   - Solution: Check unique constraints

---

## Test Execution Log Template

```
Date: ___________
Tester: ___________
Environment: Pre-Prod

TC001 - July DENIED:
  - Claims returned: ___
  - Claim numbers: _______________
  - Status: PASS / FAIL

TC002 - Aug DENIED:
  - Claims returned: ___
  - Claim numbers: _______________
  - Status: PASS / FAIL

TC003 - July-Aug DENIED:
  - Claims returned: ___
  - Claim numbers: _______________
  - Expected: ___ (TC001 + TC002)
  - Status: PASS / FAIL
  - Notes: _______________

Backend Logs:
  - July breakdown: _______________
  - Aug breakdown: _______________
  - July-Aug breakdown: _______________
```

---

## Success Criteria

All test cases must pass with:
- ✅ Correct claim counts
- ✅ No duplicate claims
- ✅ No missing claims
- ✅ Consistent results across date ranges
- ✅ TC003 count = TC001 count + TC002 count

---

## Related Files
- Backend: `connectme-backend/apps/claims/api_views.py`
- Frontend: `connectme-frontend/src/components/claims/ClaimsSearchForm.tsx`
- API Docs: `API_DOCUMENTATION.md`

