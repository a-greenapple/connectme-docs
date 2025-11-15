#!/usr/bin/env python3
"""
Search for claims and extract full details from search results
"""
import requests
import csv
import json
from datetime import datetime

API_BASE_URL = "https://connectme.be.totesoft.com"

def get_auth_token():
    """Get authentication token"""
    print("🔐 Authenticating...")
    try:
        response = requests.post(f"{API_BASE_URL}/api/v1/auth/mock/login/", json={}, timeout=10)
        if response.status_code == 200:
            token = response.json().get('access_token')
            print("✅ Authenticated\n")
            return token
        return None
    except Exception as e:
        print(f"❌ Auth error: {e}")
        return None

def search_claims(token):
    """Search for claims in July 2025 date range"""
    print("🔍 Searching for claims (July 1-3, 2025)...")
    
    headers = {'Authorization': f'Bearer {token}', 'Content-Type': 'application/json'}
    
    payload = {
        'firstServiceDate': '2025-07-01',
        'lastServiceDate': '2025-07-03'
    }
    
    try:
        response = requests.post(
            f"{API_BASE_URL}/api/v1/claims/search/",
            headers=headers,
            json=payload,
            timeout=60
        )
        
        if response.status_code == 200:
            data = response.json()
            claims = data.get('claims', [])
            print(f"✅ Found {len(claims)} claims\n")
            return claims
        else:
            print(f"❌ Error: {response.status_code}")
            print(response.text)
            return []
    except Exception as e:
        print(f"❌ Error: {e}")
        return []

def main():
    print("""
╔═══════════════════════════════════════════════════════════════════════════╗
║                                                                           ║
║      🎯 EXTRACTING REAL CLAIM DETAILS FROM SEARCH                        ║
║                                                                           ║
╚═══════════════════════════════════════════════════════════════════════════╝
    """)
    
    token = get_auth_token()
    if not token:
        return
    
    claims = search_claims(token)
    
    if not claims:
        print("❌ No claims found")
        return
    
    print("📋 Claims found:")
    print("="*80)
    
    # First, let's see what data structure we get
    print(json.dumps(claims[0], indent=2))
    
    print("\n" + "="*80)
    print(f"\n💾 Full data saved to: search_results_july_2025.json")
    
    with open('search_results_july_2025.json', 'w') as f:
        json.dump(claims, f, indent=2)

if __name__ == "__main__":
    main()
