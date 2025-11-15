# How to Run the Tests

## ✅ Recommended: Browser Console Test (Easiest & Most Accurate)

This method tests exactly as the frontend does - using the same authentication and API calls.

### Steps:

1. **Login to the application**
   - Go to: https://pre-prod.connectme.apps.totessoft.com
   - Login with your credentials

2. **Navigate to Claims Search**
   - Click on "Claims" in the navigation menu
   - You should see the Claims Search page

3. **Open Browser DevTools**
   - Press `F12` (Windows/Linux) or `Cmd+Option+I` (Mac)
   - Or right-click anywhere → "Inspect"

4. **Go to Console Tab**
   - Click on the "Console" tab in DevTools

5. **Run the Test Script**
   - Open the file: `BROWSER_CONSOLE_TEST.js`
   - Copy the ENTIRE contents
   - Paste into the Console
   - Press `Enter`

6. **Wait for Results**
   - Tests will run automatically (takes 2-3 minutes)
   - Results will be displayed in the console with color coding:
     - ✅ Green = Success
     - ❌ Red = Failure
     - ⚠️ Orange = Warning

### What the Test Does:

```
TC001: Search July 1-30 with DENIED filter
  ↓
TC002: Search Aug 1-30 with DENIED filter
  ↓
TC003: Search July 1 - Aug 31 with DENIED filter
  ↓
TC004: Search July 1 - Aug 31 WITHOUT filter (baseline)
  ↓
ANALYSIS: Compare results and identify issues
```

### Expected Output:

```
=======================================================================
CLAIM STATUS FILTER TEST SUITE
=======================================================================
✅ Using authentication token from localStorage
Practice ID: 1
Status Filter: DENIED

=======================================================================
RUNNING TESTS...
=======================================================================

🧪 TC001: July 2024 with DENIED filter
   Date Range: 2024-07-01 to 2024-07-30
   Status Filter: DENIED
   ✅ SUCCESS: 2 claims returned
   Claim Numbers: CLAIM001, CLAIM002
   Status Breakdown: {DENIED: 2}

🧪 TC002: August 2024 with DENIED filter
   Date Range: 2024-08-01 to 2024-08-30
   Status Filter: DENIED
   ✅ SUCCESS: 3 claims returned
   Claim Numbers: CLAIM003, CLAIM004, CLAIM005
   Status Breakdown: {DENIED: 3}

🧪 TC003: July-August 2024 with DENIED filter
   Date Range: 2024-07-01 to 2024-08-31
   Status Filter: DENIED
   ✅ SUCCESS: 5 claims returned  ← Should be 5 (2+3)!
   Claim Numbers: CLAIM001, CLAIM002, CLAIM003, CLAIM004, CLAIM005
   Status Breakdown: {DENIED: 5}

🧪 TC004: July-August 2024 WITHOUT filter (baseline)
   Date Range: 2024-07-01 to 2024-08-31
   Status Filter: None (All statuses)
   ✅ SUCCESS: 15 claims returned
   Claim Numbers: ...
   Status Breakdown: {DENIED: 5, PAID: 8, PENDING: 2}

=======================================================================
TEST RESULTS ANALYSIS
=======================================================================

📊 Claim Counts:
   TC001 (July DENIED):     2
   TC002 (Aug DENIED):      3
   TC003 (Jul-Aug DENIED):  5
   TC004 (Jul-Aug ALL):     15

🔍 Critical Check:
   Expected (TC001 + TC002): 5
   Actual (TC003):           5
   ✅ PASS: Counts match!

🔍 Baseline Check (TC004):
   Total claims (unfiltered):    15
   Status breakdown: {DENIED: 5, PAID: 8, PENDING: 2}
   Expected DENIED claims:       5
   Actual DENIED claims (TC003): 5
   ✅ PASS: Filter working correctly!

=======================================================================
FINAL VERDICT
=======================================================================

✅ ALL TESTS PASSED!
   - Date range filtering works correctly
   - Status filtering works correctly
   - No claims are lost
```

---

## Alternative: Python Script with Token

If you prefer command-line testing:

### Steps:

1. **Get your access token**
   - Login to https://pre-prod.connectme.apps.totessoft.com
   - Open DevTools Console (F12)
   - Run: `localStorage.getItem('kc_access_token')`
   - Copy the token (without quotes)

2. **Run the test script**
   ```bash
   cd testcases/datequery-claimstatus-filterbased
   python3 test_with_token.py YOUR_TOKEN_HERE 1
   ```

---

## After Running Tests

### If Tests PASS ✅
- No action needed
- Feature is working correctly
- Document the test results

### If Tests FAIL ❌

1. **Check Backend Logs**
   ```bash
   ssh connectme@169.59.163.43 'journalctl -u connectme-preprod-backend -n 200 --no-pager | grep -A 3 "Claim status breakdown"'
   ```

2. **Look for:**
   - How many claims UHC API returned for each date range
   - Status breakdown before filtering
   - Any error messages

3. **Common Issues:**
   - **UHC API Pagination**: API returns max N claims, larger ranges hit limit
   - **UHC API Behavior**: Different results for different date ranges
   - **Filter Logic Bug**: Backend filter not working correctly
   - **Caching**: Old results cached in browser/backend

4. **Next Steps:**
   - Share backend logs with development team
   - Take screenshots of test results
   - Use `MANUAL_TEST_CHECKLIST.md` for detailed manual testing

---

## Modifying the Tests

### To test different months:
Edit `BROWSER_CONSOLE_TEST.js` lines:
```javascript
const tc001 = await searchClaims('2024-06-01', '2024-06-30', ...);  // June
const tc002 = await searchClaims('2024-07-01', '2024-07-31', ...);  // July
```

### To test different status:
Edit line:
```javascript
const STATUS_FILTER = 'PAID';  // or 'PENDING', 'FINALIZED', etc.
```

### To test different practice:
Edit line:
```javascript
const PRACTICE_ID = '2';  // Change to your practice ID
```

---

## Troubleshooting

### "Not authenticated" error
- Make sure you're logged in
- Refresh the page
- Try logging out and back in

### "Network error"
- Check your internet connection
- Verify backend is running
- Check browser console for CORS errors

### Tests take too long
- This is normal for large date ranges
- Each test makes API calls to UHC
- Wait at least 2-3 minutes for completion

### Inconsistent results
- Clear browser cache
- Hard refresh (Ctrl+Shift+R)
- Run tests multiple times to confirm

---

## Support

For questions or issues:
1. Check `README.md` for detailed test case documentation
2. Review `MANUAL_TEST_CHECKLIST.md` for step-by-step manual testing
3. Contact development team with test results and backend logs

