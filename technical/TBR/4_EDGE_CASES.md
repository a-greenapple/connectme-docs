# Edge Cases & Error Scenarios

## Overview
This document outlines common edge cases, error scenarios, and how the system handles them.

---

## 1. Date Range Edge Cases

### 1.1 Future Dates
**Scenario:** User selects dates in the future  
**System Behavior:**
- Frontend: Date picker prevents selection (max=today)
- Backend: Returns 400 error if bypassed
- UHC API: Returns error code LCLM_PS_107

**Expected Error Message:**
```
[LCLM_PS_107] First Service Date and Last Service Date should be within last 24 months.
```

**Test Cases:**
```bash
# Test 1: Future date
firstServiceDate: 2025-11-01
lastServiceDate: 2025-11-30
Expected: Frontend blocks, or backend returns error

# Test 2: Partially future
firstServiceDate: 2025-10-01
lastServiceDate: 2025-11-30
Expected: Frontend blocks dates > today
```

---

### 1.2 Dates Older Than 24 Months
**Scenario:** User selects dates older than 24 months  
**System Behavior:**
- Frontend: Date picker prevents selection (min=24 months ago)
- Backend: Passes to UHC, which returns error
- UHC API: Returns error code LCLM_PS_107

**Test Cases:**
```bash
# Test: 25 months ago
firstServiceDate: 2023-09-01
lastServiceDate: 2023-09-30
Expected: Frontend blocks or UHC returns error
```

---

### 1.3 Date Range Too Large
**Scenario:** User selects >90 days without patient filter  
**System Behavior:**
- Frontend: Shows warning banner
- Backend: Allows but may return many results
- UHC API: May timeout or return partial results

**Test Cases:**
```bash
# Test 1: 91 days without filter
firstServiceDate: 2024-07-01
lastServiceDate: 2024-09-30
Expected: Warning shown, search allowed

# Test 2: 366 days with patient filter
firstServiceDate: 2024-01-01
lastServiceDate: 2024-12-31
patientFirstName: John
Expected: Warning shown, search allowed

# Test 3: 366 days without filter
firstServiceDate: 2024-01-01
lastServiceDate: 2024-12-31
Expected: Warning shown, recommend adding filter
```

---

## 2. API Response Edge Cases

### 2.1 Empty Results
**Scenario:** No claims found for date range  
**System Behavior:**
- Backend: Returns empty array
- Frontend: Shows "No claims found" message

**Test Cases:**
```bash
# Test: Date range with no activity
firstServiceDate: 2024-12-25
lastServiceDate: 2024-12-26
Expected: "No claims found" message
```

---

### 2.2 Partial API Failures
**Scenario:** Summary API succeeds, but Details or Payment API fails  
**System Behavior:**
- Backend: Returns summary data with flags
- Frontend: Shows summary, marks details as unavailable

**Response Structure:**
```json
{
  "claimNumber": "12345",
  "hasDetailedData": false,
  "hasPaymentData": false,
  "detailsError": "Failed to fetch details",
  "paymentError": "Failed to fetch payment"
}
```

**Test Cases:**
```bash
# Simulate by temporarily breaking Detail API URL
Expected: Claims show but with "Details unavailable" message
```

---

### 2.3 Missing Fields in API Response
**Scenario:** UHC API doesn't return expected fields  
**System Behavior:**
- Backend: Uses `.get()` with defaults
- Frontend: Displays "N/A" for missing fields

**Common Missing Fields:**
- `totalAllowdAmt` → defaults to '0.00'
- `providerName` → defaults to 'N/A'
- `checkNbr` → defaults to None
- `claimCodes` → defaults to []

**Test Cases:**
```bash
# Check claims with various statuses
Status: Pending → May not have payment data
Status: Denied → May not have allowed amount
Status: Submitted → May not have any financial data
```

---

## 3. Payment Reconciliation Edge Cases

### 3.1 Single Check, Multiple Claims
**Scenario:** One check covers multiple claims  
**System Behavior:**
- Frontend: Shows warning in payment modal
- Displays: This claim amount vs. total check amount
- Suggests: Search by payment date to find related claims

**Example:**
```
Check #36001529: $1,113.47 total
  - Claim A: $260.82
  - Claim B: $400.00
  - Claim C: $452.65
```

**Test Cases:**
```bash
# Search for claims with same payment date
paymentDate: 2024-09-18
Expected: Multiple claims with same check number
```

---

### 3.2 Multiple Drafts, Same Check
**Scenario:** One check has multiple draft numbers  
**System Behavior:**
- Frontend: Groups by check number
- Shows: Total check amount + individual drafts
- Displays: Badge with draft count

**Example:**
```
Check #36001529 (3 drafts)
  - Draft 0140095788: $1,113.47
  - Draft 0140095789: $1,113.47
  - Draft 0140095790: $1,113.47
```

**Test Cases:**
```bash
# Look for claims with multiple payment records
Expected: Smart grouping by check number
```

---

### 3.3 Zero Dollar Payments
**Scenario:** Claim paid $0.00  
**System Behavior:**
- Frontend: Shows $0.00 in green (not an error)
- Reason: Could be denied, or patient responsibility only

**Test Cases:**
```bash
# Check denied claims
Status: Denied
paidAmount: $0.00
patientBalance: $0.00 or full amount
Expected: Green display, not red (it's correct)
```

---

## 4. Financial Calculation Edge Cases

### 4.1 Charged < Allowed
**Scenario:** Allowed amount exceeds charged amount  
**System Behavior:**
- Backend: Calculates negative adjustment
- Frontend: Shows negative adjustment (unusual but valid)

**Example:**
```
Charged: $100.00
Allowed: $120.00
Adjustment: -$20.00 (provider gets more than charged)
```

**Test Cases:**
```bash
# Rare but possible with certain contracts
Expected: Negative adjustment displayed correctly
```

---

### 4.2 Missing Allowed Amount
**Scenario:** UHC doesn't provide `totalAllowdAmt`  
**System Behavior:**
- Backend: Defaults to '0.00'
- Frontend: Doesn't show financial breakdown section

**Test Cases:**
```bash
# Check claims with status "Pending" or "Submitted"
Expected: No financial breakdown section shown
```

---

### 4.3 Patient Balance > Allowed Amount
**Scenario:** Patient owes more than allowed (error in data)  
**System Behavior:**
- Frontend: Displays as-is (red color)
- Note: This indicates a data issue, not a system bug

**Test Cases:**
```bash
# Data validation
Allowed: $100.00
Paid: $80.00
Patient Balance: $150.00  # ERROR - should be ≤ $20
Expected: Display but flag for review
```

---

## 5. Authentication & Authorization Edge Cases

### 5.1 Token Expiration During Search
**Scenario:** JWT token expires mid-search  
**System Behavior:**
- Backend: Returns 401 Unauthorized
- Frontend: Redirects to login
- User: Must log in again

**Test Cases:**
```bash
# Simulate by waiting for token expiration
Expected: Graceful redirect to login
```

---

### 5.2 Insufficient Permissions
**Scenario:** User lacks required role  
**System Behavior:**
- Backend: Returns 403 Forbidden
- Frontend: Shows "Access Denied" message

**Test Cases:**
```bash
# User without claims:read role
Expected: 403 error with clear message
```

---

### 5.3 Invalid TIN Configuration
**Scenario:** User's TIN not configured in system  
**System Behavior:**
- Backend: Returns 404 or 400 error
- Frontend: Shows "Configuration error" message

**Test Cases:**
```bash
# User with no Practice mapping
Expected: Clear error about missing configuration
```

---

## 6. Network & Performance Edge Cases

### 6.1 UHC API Timeout
**Scenario:** UHC API takes >30 seconds  
**System Behavior:**
- Backend: Timeout after 30s (configurable)
- Frontend: Shows timeout error
- Retry: User can try again

**Test Cases:**
```bash
# Simulate with very large date range
firstServiceDate: 2023-10-01
lastServiceDate: 2024-10-01
Expected: May timeout, show retry option
```

---

### 6.2 Slow Network
**Scenario:** User has slow internet connection  
**System Behavior:**
- Frontend: Shows loading spinner
- Timeout: After 60 seconds
- Message: "Request taking longer than expected"

**Test Cases:**
```bash
# Throttle network in browser DevTools
Expected: Loading indicator, eventual timeout
```

---

### 6.3 Large Result Sets
**Scenario:** Query returns 1000+ claims  
**System Behavior:**
- Backend: Returns all (no pagination on UHC side)
- Frontend: Renders all, may be slow
- CSV Export: Works fine

**Test Cases:**
```bash
# Large date range with no filters
firstServiceDate: 2024-01-01
lastServiceDate: 2024-12-31
Expected: All claims returned, may take time to render
```

---

## 7. Data Quality Edge Cases

### 7.1 Duplicate Claims
**Scenario:** Same claim appears multiple times  
**System Behavior:**
- Backend: Returns as-is from UHC
- Frontend: Displays all (not de-duped)
- Note: This is UHC data, not a system bug

**Test Cases:**
```bash
# Check for duplicate claim numbers
Expected: Display all, user can sort/filter
```

---

### 7.2 Inconsistent Dates
**Scenario:** Payment date before service date  
**System Behavior:**
- Backend: Returns as-is
- Frontend: Displays as-is
- Timeline: Shows in chronological order

**Test Cases:**
```bash
# Data validation
serviceDate: 2024-09-01
paymentDate: 2024-08-01  # Before service!
Expected: Display both, timeline shows correctly
```

---

### 7.3 Special Characters in Names
**Scenario:** Patient name has special characters  
**System Behavior:**
- Backend: Handles UTF-8 encoding
- Frontend: Displays correctly
- CSV Export: Properly escaped

**Test Cases:**
```bash
# Test names
patientName: "O'Brien"
patientName: "José García"
patientName: "Smith-Jones"
Expected: Display and export correctly
```

---

## 8. Browser Compatibility Edge Cases

### 8.1 Old Browsers
**Scenario:** User on IE11 or old Safari  
**System Behavior:**
- May not work (Next.js requires modern browser)
- Shows: "Please upgrade your browser" message

**Supported Browsers:**
- Chrome 90+
- Firefox 88+
- Safari 14+
- Edge 90+

---

### 8.2 JavaScript Disabled
**Scenario:** User has JS disabled  
**System Behavior:**
- App won't load (React requires JS)
- Shows: Fallback message

---

### 8.3 Small Screens / Mobile
**Scenario:** User on mobile device  
**System Behavior:**
- Responsive design adapts
- Tables scroll horizontally
- Modals adjust to screen size

**Test Cases:**
```bash
# Test on various screen sizes
320px (iPhone SE)
768px (iPad)
1024px (Desktop)
Expected: Responsive layout
```

---

## 9. CSV Export Edge Cases

### 9.1 Large Exports
**Scenario:** Exporting 1000+ claims  
**System Behavior:**
- Frontend: Generates CSV client-side
- Browser: May pause briefly
- File: Downloads successfully

**Test Cases:**
```bash
# Export large result set
Expected: File downloads, may take 5-10 seconds
```

---

### 9.2 Special Characters in Data
**Scenario:** Claim data contains commas, quotes  
**System Behavior:**
- CSV: Properly escapes with quotes
- Excel: Opens correctly

**Test Cases:**
```bash
# Data with special chars
providerName: "Smith, Jones & Associates"
Expected: CSV escapes: "Smith, Jones & Associates"
```

---

### 9.3 Empty Results Export
**Scenario:** User exports with no results  
**System Behavior:**
- Frontend: Creates CSV with headers only
- File: Downloads with just column names

---

## 10. Concurrent User Edge Cases

### 10.1 Same User, Multiple Tabs
**Scenario:** User opens app in 2+ tabs  
**System Behavior:**
- Each tab: Independent session
- Auth: Shared via localStorage
- Logout: Affects all tabs

**Test Cases:**
```bash
# Open 2 tabs, logout in one
Expected: Both tabs redirect to login
```

---

### 10.2 Multiple Users, Same TIN
**Scenario:** 2+ users query same TIN simultaneously  
**System Behavior:**
- Backend: Independent requests to UHC
- No conflict: Each gets their own results
- Rate Limiting: May apply per TIN

---

## 11. Monitoring & Alerting

### Key Metrics to Monitor:
1. **API Response Times**
   - UHC Summary API: < 5s
   - UHC Details API: < 3s
   - UHC Payment API: < 3s

2. **Error Rates**
   - 4xx errors: < 5%
   - 5xx errors: < 1%
   - UHC API errors: < 2%

3. **Search Patterns**
   - Average date range: 7-30 days
   - Queries >90 days: Flag for review
   - Failed searches: Investigate

4. **User Experience**
   - Time to first result: < 10s
   - CSV export time: < 15s
   - Page load time: < 3s

---

## 12. Recovery Procedures

### 12.1 UHC API Down
**Procedure:**
1. Check UHC status page
2. Notify users via banner
3. Retry with exponential backoff
4. Escalate if down >30 minutes

### 12.2 Database Connection Lost
**Procedure:**
1. Connection pool retries automatically
2. Log error with timestamp
3. Alert admin if persists >5 minutes
4. Check database server status

### 12.3 Keycloak Unavailable
**Procedure:**
1. Users can't log in (existing sessions OK)
2. Check Keycloak server
3. Restart Keycloak if needed
4. Notify users of maintenance

---

## Testing Checklist

### Before Production:
- [ ] Test all date range scenarios
- [ ] Test with 0 results
- [ ] Test with 1000+ results
- [ ] Test with missing API fields
- [ ] Test payment reconciliation
- [ ] Test CSV export (small & large)
- [ ] Test on multiple browsers
- [ ] Test on mobile devices
- [ ] Test token expiration
- [ ] Test concurrent users
- [ ] Load test with 50+ concurrent users
- [ ] Test UHC API timeout scenarios
- [ ] Verify error messages are user-friendly
- [ ] Test with real production data

---

## Common User Mistakes

### 1. Date Range Too Large
**User Error:** Selects 6-month range without filter  
**Solution:** Show warning, recommend adding patient filter

### 2. Wrong Date Format
**User Error:** Types date as MM/DD/YYYY  
**Solution:** Date picker enforces YYYY-MM-DD

### 3. Expecting Real-Time Data
**User Error:** Claim submitted today, not found  
**Solution:** Add note: "Data updated daily by UHC"

### 4. Misunderstanding Contractual Adjustment
**User Error:** Thinks patient owes adjustment amount  
**Solution:** Clear tooltip explaining write-off

---

## Future Enhancements

### 1. Caching
- Cache recent queries for 24 hours
- Reduce UHC API calls
- Faster repeat searches

### 2. Pagination
- Limit frontend display to 100 claims per page
- Improve performance for large result sets
- Still export all to CSV

### 3. Background Jobs
- Queue large date range searches
- Email results when complete
- Reduce timeout issues

### 4. Advanced Filters
- Filter by claim status
- Filter by provider
- Filter by amount range

---

## Contact for Issues

**System Administrator:** [admin@yourorg.com]  
**UHC Support:** 1-800-UHC-SUPPORT  
**Technical Support:** [support@yourorg.com]

---

*Last Updated: October 2025*
*Version: 1.0*
