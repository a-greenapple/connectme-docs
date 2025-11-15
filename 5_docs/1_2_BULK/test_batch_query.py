#!/usr/bin/env python3
"""
Test if batch query returns the claims
"""
import requests
import json

API_BASE_URL = "https://connectme.be.totesoft.com"

def get_auth_token():
    """Get authentication token"""
    print("🔐 Authenticating...")
    response = requests.post(f"{API_BASE_URL}/api/v1/auth/mock/login/", json={}, timeout=10)
    if response.status_code == 200:
        token = response.json().get('access_token')
        print("✅ Authenticated\n")
        return token
    return None

def test_batch_query(token, start_date, end_date):
    """Test batch query with date range"""
    print(f"🔍 Testing batch query: {start_date} to {end_date}")
    
    headers = {'Authorization': f'Bearer {token}', 'Content-Type': 'application/json'}
    
    payload = {
        'firstServiceDate': start_date,
        'lastServiceDate': end_date
    }
    
    response = requests.post(
        f"{API_BASE_URL}/api/v1/claims/search/",
        headers=headers,
        json=payload,
        timeout=60
    )
    
    if response.status_code == 200:
        data = response.json()
        claims = data.get('claims', [])
        print(f"✅ Query successful: {len(claims)} claims found")
        
        # Check if our specific claims are in the results
        target_claims = ['FE23924647', '51545088', '51598988', '51611599', 'FE98163821']
        found_claims = [c.get('claimNumber') for c in claims]
        
        print("\n📋 Checking for target claims:")
        for target in target_claims:
            if target in found_claims:
                print(f"   ✅ {target} - FOUND")
            else:
                print(f"   ❌ {target} - NOT FOUND")
        
        return claims
    else:
        print(f"❌ Query failed: {response.status_code}")
        print(response.text)
        return []

def main():
    token = get_auth_token()
    if not token:
        return
    
    print("="*80)
    print("TEST 1: Query with buffer (June 24 - July 10)")
    print("="*80)
    claims1 = test_batch_query(token, '2025-06-24', '2025-07-10')
    
    print("\n" + "="*80)
    print("TEST 2: Query exact dates (July 1 - July 3)")
    print("="*80)
    claims2 = test_batch_query(token, '2025-07-01', '2025-07-03')
    
    print("\n" + "="*80)
    print("CONCLUSION:")
    print("="*80)
    if len(claims1) >= 5 and len(claims2) >= 5:
        print("✅ Both queries work - issue is in claim matching logic")
    elif len(claims2) >= 5:
        print("⚠️  Exact date query works, buffered query doesn't")
        print("    → Solution: Remove the 7-day buffer completely")
    else:
        print("❌ Neither query returns our claims")
        print("    → Need to investigate further")

if __name__ == "__main__":
    main()
