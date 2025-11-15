/**
 * Browser Console Test for Date Range + Status Filter
 * 
 * HOW TO RUN:
 * 1. Login to https://pre-prod.connectme.apps.totessoft.com
 * 2. Navigate to Claims Search page
 * 3. Open Browser DevTools (F12)
 * 4. Go to Console tab
 * 5. Copy and paste this entire script
 * 6. Press Enter
 * 7. Wait for results (will take 2-3 minutes)
 */

(async function runClaimStatusFilterTests() {
    console.log('%c='.repeat(70), 'color: blue; font-weight: bold');
    console.log('%cCLAIM STATUS FILTER TEST SUITE', 'color: blue; font-size: 16px; font-weight: bold');
    console.log('%c='.repeat(70), 'color: blue; font-weight: bold');
    
    // Configuration
    const API_BASE_URL = 'https://pre-prod.connectme.be.totessoft.com/api/v1';
    const PRACTICE_ID = '1'; // Change if needed
    const STATUS_FILTER = 'DENIED';
    
    // Get token from localStorage (same as frontend)
    const token = localStorage.getItem('kc_access_token');
    if (!token) {
        console.error('%c❌ ERROR: Not authenticated. Please login first.', 'color: red; font-weight: bold');
        return;
    }
    
    console.log('%c✅ Using authentication token from localStorage', 'color: green');
    console.log(`%cPractice ID: ${PRACTICE_ID}`, 'color: gray');
    console.log(`%cStatus Filter: ${STATUS_FILTER}`, 'color: gray');
    console.log('');
    
    // Helper function to search claims (exactly like frontend)
    async function searchClaims(firstDate, lastDate, statusFilter, testName) {
        console.log(`%c🧪 ${testName}`, 'color: cyan; font-weight: bold');
        console.log(`   Date Range: ${firstDate} to ${lastDate}`);
        console.log(`   Status Filter: ${statusFilter || 'None (All statuses)'}`);
        
        const payload = {
            firstServiceDate: firstDate,
            lastServiceDate: lastDate,
            practiceId: PRACTICE_ID
        };
        
        if (statusFilter) {
            payload.statusFilter = statusFilter;
        }
        
        try {
            const response = await fetch(`${API_BASE_URL}/claims/search/`, {
                method: 'POST',
                headers: {
                    'Authorization': `Bearer ${token}`,
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify(payload)
            });
            
            if (response.ok) {
                const data = await response.json();
                const claims = data.claims || [];
                
                // Analyze statuses
                const statusCounts = {};
                claims.forEach(claim => {
                    const status = claim.status || 'UNKNOWN';
                    statusCounts[status] = (statusCounts[status] || 0) + 1;
                });
                
                const claimNumbers = claims.map(c => c.claimNumber);
                
                console.log(`%c   ✅ SUCCESS: ${claims.length} claims returned`, 'color: green');
                console.log(`   Claim Numbers: ${claimNumbers.join(', ')}`);
                console.log(`   Status Breakdown:`, statusCounts);
                console.log('');
                
                return {
                    success: true,
                    count: claims.length,
                    claimNumbers: claimNumbers,
                    statusCounts: statusCounts,
                    claims: claims
                };
            } else {
                const error = await response.text();
                console.error(`%c   ❌ FAILED: HTTP ${response.status}`, 'color: red');
                console.error(`   Error:`, error);
                console.log('');
                return {
                    success: false,
                    error: error,
                    statusCode: response.status
                };
            }
        } catch (error) {
            console.error(`%c   ❌ EXCEPTION: ${error.message}`, 'color: red');
            console.log('');
            return {
                success: false,
                error: error.message
            };
        }
    }
    
    // Run tests
    console.log('%c' + '='.repeat(70), 'color: blue');
    console.log('%cRUNNING TESTS...', 'color: blue; font-weight: bold');
    console.log('%c' + '='.repeat(70), 'color: blue');
    console.log('');
    
    // TC001: July with DENIED filter
    const tc001 = await searchClaims('2024-07-01', '2024-07-30', STATUS_FILTER, 'TC001: July 2024 with DENIED filter');
    
    // TC002: August with DENIED filter
    const tc002 = await searchClaims('2024-08-01', '2024-08-30', STATUS_FILTER, 'TC002: August 2024 with DENIED filter');
    
    // TC003: July-August with DENIED filter (CRITICAL TEST)
    const tc003 = await searchClaims('2024-07-01', '2024-08-31', STATUS_FILTER, 'TC003: July-August 2024 with DENIED filter');
    
    // TC004: July-August WITHOUT filter (baseline)
    const tc004 = await searchClaims('2024-07-01', '2024-08-31', null, 'TC004: July-August 2024 WITHOUT filter (baseline)');
    
    // Analysis
    console.log('%c' + '='.repeat(70), 'color: blue; font-weight: bold');
    console.log('%cTEST RESULTS ANALYSIS', 'color: blue; font-size: 16px; font-weight: bold');
    console.log('%c' + '='.repeat(70), 'color: blue; font-weight: bold');
    console.log('');
    
    if (!tc001.success || !tc002.success || !tc003.success || !tc004.success) {
        console.error('%c❌ CRITICAL: Some tests failed to execute', 'color: red; font-weight: bold');
        return;
    }
    
    const count1 = tc001.count;
    const count2 = tc002.count;
    const count3 = tc003.count;
    const count4 = tc004.count;
    
    console.log('%c📊 Claim Counts:', 'color: blue; font-weight: bold');
    console.log(`   TC001 (July DENIED):     ${count1}`);
    console.log(`   TC002 (Aug DENIED):      ${count2}`);
    console.log(`   TC003 (Jul-Aug DENIED):  ${count3}`);
    console.log(`   TC004 (Jul-Aug ALL):     ${count4}`);
    console.log('');
    
    // Critical Check: TC003 should equal TC001 + TC002
    const expectedCount = count1 + count2;
    console.log('%c🔍 Critical Check:', 'color: orange; font-weight: bold');
    console.log(`   Expected (TC001 + TC002): ${expectedCount}`);
    console.log(`   Actual (TC003):           ${count3}`);
    
    let hasCriticalIssue = false;
    
    if (count3 !== expectedCount) {
        console.error(`%c   ❌ MISMATCH! Missing ${expectedCount - count3} claims`, 'color: red; font-weight: bold');
        hasCriticalIssue = true;
        
        // Detailed analysis
        const claims1 = new Set(tc001.claimNumbers);
        const claims2 = new Set(tc002.claimNumbers);
        const claims3 = new Set(tc003.claimNumbers);
        
        console.log('');
        console.log('%c   📋 Detailed Claim Analysis:', 'color: orange; font-weight: bold');
        console.log('   TC001 claims:', Array.from(claims1));
        console.log('   TC002 claims:', Array.from(claims2));
        console.log('   TC003 claims:', Array.from(claims3));
        console.log('');
        
        const allExpected = new Set([...claims1, ...claims2]);
        const missing = new Set([...allExpected].filter(x => !claims3.has(x)));
        const extra = new Set([...claims3].filter(x => !allExpected.has(x)));
        
        if (missing.size > 0) {
            console.error('%c   ❌ Missing from TC003:', 'color: red; font-weight: bold', Array.from(missing));
        }
        if (extra.size > 0) {
            console.warn('%c   ⚠️  Extra in TC003:', 'color: orange; font-weight: bold', Array.from(extra));
        }
    } else {
        console.log('%c   ✅ PASS: Counts match!', 'color: green; font-weight: bold');
    }
    console.log('');
    
    // Baseline check
    const expectedDenied = tc004.statusCounts[STATUS_FILTER] || 0;
    console.log('%c🔍 Baseline Check (TC004):', 'color: orange; font-weight: bold');
    console.log(`   Total claims (unfiltered):    ${count4}`);
    console.log('   Status breakdown:', tc004.statusCounts);
    console.log(`   Expected DENIED claims:       ${expectedDenied}`);
    console.log(`   Actual DENIED claims (TC003): ${count3}`);
    
    if (expectedDenied !== count3) {
        console.error('%c   ❌ MISMATCH! Filter may be losing claims', 'color: red; font-weight: bold');
        hasCriticalIssue = true;
    } else {
        console.log('%c   ✅ PASS: Filter working correctly!', 'color: green; font-weight: bold');
    }
    console.log('');
    
    // Final Verdict
    console.log('%c' + '='.repeat(70), 'color: blue; font-weight: bold');
    console.log('%cFINAL VERDICT', 'color: blue; font-size: 16px; font-weight: bold');
    console.log('%c' + '='.repeat(70), 'color: blue; font-weight: bold');
    console.log('');
    
    if (!hasCriticalIssue) {
        console.log('%c✅ ALL TESTS PASSED!', 'color: green; font-size: 18px; font-weight: bold');
        console.log('%c   - Date range filtering works correctly', 'color: green');
        console.log('%c   - Status filtering works correctly', 'color: green');
        console.log('%c   - No claims are lost', 'color: green');
    } else {
        console.error('%c❌ TESTS FAILED!', 'color: red; font-size: 18px; font-weight: bold');
        console.log('');
        console.log('%c🔧 Recommended Actions:', 'color: orange; font-weight: bold');
        console.log('   1. Check backend logs for UHC API responses');
        console.log('   2. Verify UHC API is returning all claims for combined date range');
        console.log('   3. Check for pagination or limits in UHC API');
        console.log('   4. Review backend filtering logic');
        console.log('');
        console.log('%c📝 To check backend logs:', 'color: cyan; font-weight: bold');
        console.log('   ssh connectme@169.59.163.43 \'journalctl -u connectme-preprod-backend -n 200 --no-pager | grep "Claim status breakdown"\'');
    }
    console.log('');
    console.log('%c' + '='.repeat(70), 'color: blue; font-weight: bold');
    
    // Return results for programmatic access
    return {
        tc001, tc002, tc003, tc004,
        passed: !hasCriticalIssue,
        summary: {
            julyCount: count1,
            augustCount: count2,
            combinedCount: count3,
            baselineCount: count4,
            expectedCombined: expectedCount,
            mismatch: count3 !== expectedCount
        }
    };
})();

