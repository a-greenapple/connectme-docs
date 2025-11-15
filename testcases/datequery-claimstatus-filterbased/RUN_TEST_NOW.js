// ========================================
// PAGINATION FIX TEST - November 15, 2025
// ========================================
// 
// INSTRUCTIONS:
// 1. Go to: https://pre-prod.connectme.apps.totessoft.com/claims
// 2. Log in if needed
// 3. Open browser console (F12 or Cmd+Option+J)
// 4. Copy and paste this ENTIRE file into the console
// 5. Press Enter
// 
// The test will run automatically and show results
// ========================================

async function testPaginationFix() {
  const token = localStorage.getItem('kc_access_token');
  const API_URL = 'https://pre-prod.connectme.be.totessoft.com/api/v1';
  
  if (!token) {
    console.error('❌ Not logged in! Please log in first.');
    return;
  }
  
  console.log('╔════════════════════════════════════════════════════════════╗');
  console.log('║       🧪 TESTING PAGINATION FIX - November 15, 2025       ║');
  console.log('╚════════════════════════════════════════════════════════════╝\n');
  
  console.log('📋 Testing Scenario:');
  console.log('   Practice: 854203105 (RSM)');
  console.log('   Status Filter: DENIED');
  console.log('   Expected: All DENIED claims across date ranges\n');
  
  // Test 1: July only
  console.log('━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━');
  console.log('📅 TEST 1: July 1-31, 2025 (DENIED only)');
  console.log('━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━');
  
  let response = await fetch(`${API_URL}/claims/search/`, {
    method: 'POST',
    headers: {
      'Authorization': `Bearer ${token}`,
      'Content-Type': 'application/json',
    },
    body: JSON.stringify({
      firstServiceDate: '2025-07-01',
      lastServiceDate: '2025-07-31',
      practiceId: '1',
      statusFilter: 'DENIED'
    })
  });
  
  if (!response.ok) {
    console.error(`❌ API Error: ${response.status} ${response.statusText}`);
    return;
  }
  
  let data = await response.json();
  const julyCount = data.claims?.length || 0;
  console.log(`   ✅ Found ${julyCount} DENIED claims in July`);
  if (julyCount > 0) {
    console.log(`   📄 Claim Numbers:`, data.claims.map(c => c.claimNumber).join(', '));
  }
  console.log('');
  
  // Test 2: August only
  console.log('━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━');
  console.log('📅 TEST 2: August 1-31, 2025 (DENIED only)');
  console.log('━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━');
  
  response = await fetch(`${API_URL}/claims/search/`, {
    method: 'POST',
    headers: {
      'Authorization': `Bearer ${token}`,
      'Content-Type': 'application/json',
    },
    body: JSON.stringify({
      firstServiceDate: '2025-08-01',
      lastServiceDate: '2025-08-31',
      practiceId: '1',
      statusFilter: 'DENIED'
    })
  });
  
  if (!response.ok) {
    console.error(`❌ API Error: ${response.status} ${response.statusText}`);
    return;
  }
  
  data = await response.json();
  const augustCount = data.claims?.length || 0;
  console.log(`   ✅ Found ${augustCount} DENIED claims in August`);
  if (augustCount > 0) {
    console.log(`   📄 Claim Numbers:`, data.claims.map(c => c.claimNumber).join(', '));
  }
  console.log('');
  
  // Test 3: Combined (THE PAGINATION FIX TEST)
  console.log('━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━');
  console.log('📅 TEST 3: July 1 - August 31, 2025 (DENIED only)');
  console.log('           ⭐ THIS TESTS THE PAGINATION FIX ⭐');
  console.log('━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━');
  
  console.log('   ⏳ Searching... (this may take a moment due to pagination)');
  
  response = await fetch(`${API_URL}/claims/search/`, {
    method: 'POST',
    headers: {
      'Authorization': `Bearer ${token}`,
      'Content-Type': 'application/json',
    },
    body: JSON.stringify({
      firstServiceDate: '2025-07-01',
      lastServiceDate: '2025-08-31',
      practiceId: '1',
      statusFilter: 'DENIED'
    })
  });
  
  if (!response.ok) {
    console.error(`❌ API Error: ${response.status} ${response.statusText}`);
    return;
  }
  
  data = await response.json();
  const combinedCount = data.claims?.length || 0;
  const expectedCount = julyCount + augustCount;
  
  console.log(`   ✅ Found ${combinedCount} DENIED claims in July+August`);
  if (combinedCount > 0) {
    console.log(`   📄 Claim Numbers:`, data.claims.map(c => c.claimNumber).join(', '));
  }
  console.log('');
  
  // Results Analysis
  console.log('╔════════════════════════════════════════════════════════════╗');
  console.log('║                      📊 TEST RESULTS                       ║');
  console.log('╚════════════════════════════════════════════════════════════╝\n');
  
  console.log(`   July DENIED claims:        ${julyCount}`);
  console.log(`   August DENIED claims:      ${augustCount}`);
  console.log(`   ─────────────────────────────────────`);
  console.log(`   Expected Total:            ${expectedCount}`);
  console.log(`   Actual Total (Combined):   ${combinedCount}`);
  console.log('');
  
  if (combinedCount === expectedCount && combinedCount > 0) {
    console.log('   ✅ ✅ ✅  PAGINATION FIX WORKING!  ✅ ✅ ✅');
    console.log('   All DENIED claims found across date ranges.');
    console.log('   The pagination is correctly fetching all pages.');
  } else if (combinedCount === 0) {
    console.log('   ⚠️  No DENIED claims found in this date range.');
    console.log('   This might be expected if there are no denied claims.');
  } else if (combinedCount < expectedCount) {
    console.log(`   ❌  ISSUE DETECTED: Missing ${expectedCount - combinedCount} claims`);
    console.log('   The pagination might not be working correctly.');
    console.log('   Check backend logs for pagination details.');
  } else {
    console.log(`   ⚠️  Unexpected: Found MORE claims than expected (+${combinedCount - expectedCount})`);
    console.log('   This could indicate duplicate claims or data changes.');
  }
  
  console.log('\n━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━');
  console.log('📋 Next Steps:');
  console.log('   1. Check backend logs for pagination details:');
  console.log('      Look for: "Retrieved X claims from page Y"');
  console.log('   2. If test failed, review backend logs on server');
  console.log('   3. Report results to development team');
  console.log('━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━\n');
}

// Run the test
console.log('Starting pagination test...\n');
testPaginationFix().catch(error => {
  console.error('❌ Test failed with error:', error);
});

