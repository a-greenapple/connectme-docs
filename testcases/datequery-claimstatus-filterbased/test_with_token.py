#!/usr/bin/env python3
"""
Test script that uses an existing access token from the browser
Usage: python3 test_with_token.py <access_token> <practice_id>
"""

import requests
import json
import sys
from collections import defaultdict

API_BASE_URL = "https://pre-prod.connectme.be.totessoft.com/api/v1"

def search_claims(access_token, first_date, last_date, practice_id, status_filter=None):
    """Search claims with given parameters"""
    url = f"{API_BASE_URL}/claims/search/"
    headers = {
        "Authorization": f"Bearer {access_token}",
        "Content-Type": "application/json"
    }
    
    payload = {
        "firstServiceDate": first_date,
        "lastServiceDate": last_date,
        "practiceId": str(practice_id)
    }
    
    if status_filter:
        payload["statusFilter"] = status_filter
    
    print(f"\n{'='*70}")
    print(f"Date Range: {first_date} to {last_date}")
    print(f"Status Filter: {status_filter or 'None (All statuses)'}")
    print(f"{'='*70}")
    
    try:
        response = requests.post(url, headers=headers, json=payload, timeout=120)
        
        if response.status_code == 200:
            data = response.json()
            claims = data.get('claims', [])
            
            # Analyze results
            claim_numbers = [c.get('claimNumber') for c in claims]
            statuses = [c.get('status') for c in claims]
            status_counts = defaultdict(int)
            for status in statuses:
                status_counts[status] += 1
            
            print(f"✅ SUCCESS: {len(claims)} claims returned")
            print(f"   Claim Numbers: {', '.join(claim_numbers)}")
            print(f"   Status Breakdown: {dict(status_counts)}")
            
            return {
                'success': True,
                'count': len(claims),
                'claim_numbers': claim_numbers,
                'status_counts': dict(status_counts),
                'claims': claims
            }
        else:
            print(f"❌ FAILED: HTTP {response.status_code}")
            print(f"   Error: {response.text}")
            return {
                'success': False,
                'error': response.text,
                'status_code': response.status_code
            }
            
    except Exception as e:
        print(f"❌ EXCEPTION: {str(e)}")
        return {
            'success': False,
            'error': str(e)
        }

def main():
    if len(sys.argv) < 3:
        print("Usage: python3 test_with_token.py <access_token> <practice_id>")
        print("\nTo get your access token:")
        print("1. Login to https://pre-prod.connectme.apps.totessoft.com")
        print("2. Open browser DevTools (F12)")
        print("3. Go to Console tab")
        print("4. Run: localStorage.getItem('kc_access_token')")
        print("5. Copy the token (without quotes)")
        sys.exit(1)
    
    access_token = sys.argv[1]
    practice_id = sys.argv[2]
    
    print("\n" + "="*70)
    print("CLAIM STATUS FILTER TEST SUITE")
    print("="*70)
    print(f"Practice ID: {practice_id}")
    print(f"Status Filter: DENIED")
    print("="*70)
    
    # TC001: July with DENIED filter
    print("\n🧪 TC001: July 2024 with DENIED filter")
    tc001 = search_claims(access_token, "2024-07-01", "2024-07-30", practice_id, "DENIED")
    
    # TC002: August with DENIED filter
    print("\n🧪 TC002: August 2024 with DENIED filter")
    tc002 = search_claims(access_token, "2024-08-01", "2024-08-30", practice_id, "DENIED")
    
    # TC003: July-August with DENIED filter
    print("\n🧪 TC003: July-August 2024 with DENIED filter")
    tc003 = search_claims(access_token, "2024-07-01", "2024-08-31", practice_id, "DENIED")
    
    # TC004: July-August WITHOUT filter
    print("\n🧪 TC004: July-August 2024 WITHOUT filter (baseline)")
    tc004 = search_claims(access_token, "2024-07-01", "2024-08-31", practice_id, None)
    
    # Analysis
    print("\n" + "="*70)
    print("TEST RESULTS ANALYSIS")
    print("="*70)
    
    if not all([tc001.get('success'), tc002.get('success'), tc003.get('success'), tc004.get('success')]):
        print("❌ CRITICAL: Some tests failed to execute")
        sys.exit(1)
    
    count1 = tc001.get('count', 0)
    count2 = tc002.get('count', 0)
    count3 = tc003.get('count', 0)
    count4 = tc004.get('count', 0)
    
    print(f"\n📊 Claim Counts:")
    print(f"  TC001 (July DENIED):     {count1}")
    print(f"  TC002 (Aug DENIED):      {count2}")
    print(f"  TC003 (Jul-Aug DENIED):  {count3}")
    print(f"  TC004 (Jul-Aug ALL):     {count4}")
    
    # Critical Check
    expected_count = count1 + count2
    print(f"\n🔍 Critical Check:")
    print(f"   Expected (TC001 + TC002): {expected_count}")
    print(f"   Actual (TC003):           {count3}")
    
    if count3 != expected_count:
        print(f"   ❌ MISMATCH! Missing {expected_count - count3} claims")
        
        # Detailed analysis
        claims1 = set(tc001.get('claim_numbers', []))
        claims2 = set(tc002.get('claim_numbers', []))
        claims3 = set(tc003.get('claim_numbers', []))
        
        print(f"\n   📋 Claim Number Analysis:")
        print(f"   - TC001 claims: {claims1}")
        print(f"   - TC002 claims: {claims2}")
        print(f"   - TC003 claims: {claims3}")
        
        missing = claims1.union(claims2) - claims3
        if missing:
            print(f"   ❌ Missing from TC003: {missing}")
        
        extra = claims3 - claims1.union(claims2)
        if extra:
            print(f"   ⚠️  Extra in TC003: {extra}")
    else:
        print(f"   ✅ PASS: Counts match!")
    
    # Baseline check
    tc004_status_counts = tc004.get('status_counts', {})
    expected_denied = tc004_status_counts.get('DENIED', 0)
    
    print(f"\n🔍 Baseline Check (TC004):")
    print(f"   Total claims (unfiltered):  {count4}")
    print(f"   Status breakdown:           {tc004_status_counts}")
    print(f"   Expected DENIED claims:     {expected_denied}")
    print(f"   Actual DENIED claims (TC003): {count3}")
    
    if expected_denied != count3:
        print(f"   ❌ MISMATCH! Filter may be losing claims")
    else:
        print(f"   ✅ PASS: Filter working correctly!")
    
    # Final verdict
    print("\n" + "="*70)
    print("FINAL VERDICT")
    print("="*70)
    
    if count3 == expected_count and count3 == expected_denied:
        print("✅ ALL TESTS PASSED!")
        print("   - Date range filtering works correctly")
        print("   - Status filtering works correctly")
        print("   - No claims are lost")
        sys.exit(0)
    else:
        print("❌ TESTS FAILED!")
        print("\n🔧 Recommended Actions:")
        print("   1. Check backend logs:")
        print("      ssh connectme@169.59.163.43 'journalctl -u connectme-preprod-backend -n 200 --no-pager | grep \"Claim status breakdown\"'")
        print("   2. Verify UHC API is returning all claims for the combined date range")
        print("   3. Check for pagination or limits in UHC API response")
        sys.exit(1)

if __name__ == '__main__':
    main()

