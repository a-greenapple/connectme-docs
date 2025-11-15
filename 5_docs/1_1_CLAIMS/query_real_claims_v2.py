#!/usr/bin/env python3
"""
Query UHC API with proper constraints (90 days, last 24 months)
"""
import requests
import csv
from datetime import datetime, timedelta

API_BASE_URL = "https://connectme.be.totesoft.com"

def get_auth_token():
    """Get authentication token"""
    print("🔐 Authenticating...")
    try:
        response = requests.post(f"{API_BASE_URL}/api/v1/auth/mock/login/", json={}, timeout=10)
        if response.status_code == 200:
            token = response.json().get('access_token')
            print(f"✅ Authenticated")
            return token
        return None
    except Exception as e:
        print(f"❌ Auth error: {e}")
        return None

def search_claims(token, start_date, end_date):
    """Search for claims"""
    print(f"🔍 Searching {start_date} to {end_date}...")
    
    headers = {'Authorization': f'Bearer {token}', 'Content-Type': 'application/json'}
    payload = {'firstServiceDate': start_date, 'lastServiceDate': end_date}
    
    try:
        response = requests.post(f"{API_BASE_URL}/api/v1/claims/search/", 
                               headers=headers, json=payload, timeout=30)
        
        if response.status_code == 200:
            data = response.json()
            claims = data.get('claims', [])
            print(f"✅ Found {len(claims)} claims")
            return claims
        else:
            print(f"❌ Error: {response.text[:150]}")
            return []
    except Exception as e:
        print(f"❌ Search error: {e}")
        return []

def main():
    print("\n" + "="*70)
    print("  QUERYING UHC API FOR REAL CLAIMS")
    print("  (with proper constraints: 90 days max, last 24 months)")
    print("="*70 + "\n")
    
    token = get_auth_token()
    if not token:
        return
    
    # Generate 90-day windows within last 24 months
    today = datetime.now()
    date_windows = []
    
    # Try last 6 quarters (90-day windows)
    for i in range(6):
        end = today - timedelta(days=i*90)
        start = end - timedelta(days=89)  # 90 days total
        
        # Only if within 24 months
        if (today - start).days <= 730:
            date_windows.append((
                start.strftime('%Y-%m-%d'),
                end.strftime('%Y-%m-%d'),
                f"Q{i+1}"
            ))
    
    print(f"Will try {len(date_windows)} date windows:\n")
    
    all_claims = []
    for start, end, label in date_windows:
        print(f"\n[{label}] {start} to {end}")
        claims = search_claims(token, start, end)
        if claims:
            all_claims.extend(claims)
            print(f"   📊 Total claims collected: {len(all_claims)}")
            if len(all_claims) >= 10:
                print(f"   ✅ Got enough claims, stopping search")
                break
    
    if all_claims:
        # Create CSV
        filename = 'csv-templates/working-claims-real.csv'
        print(f"\n📝 Creating CSV: {filename}")
        
        csv_data = []
        for claim in all_claims[:10]:  # First 10
            claim_number = claim.get('claimNumber', '')
            if claim_number:
                csv_data.append({
                    'claim_number': claim_number,
                    'first_name': claim.get('patient', {}).get('firstName', 'UNKNOWN'),
                    'last_name': claim.get('patient', {}).get('lastName', 'UNKNOWN'),
                    'date_of_birth': claim.get('patient', {}).get('dateOfBirth', '01/01/1970'),
                    'subscriber_id': claim.get('subscriber', {}).get('memberId', ''),
                    'first_service_date': claim.get('firstServiceDate', ''),
                    'last_service_date': claim.get('lastServiceDate', '')
                })
        
        with open(filename, 'w', newline='') as f:
            fieldnames = ['claim_number', 'first_name', 'last_name', 'date_of_birth',
                         'subscriber_id', 'first_service_date', 'last_service_date']
            writer = csv.DictWriter(f, fieldnames=fieldnames)
            writer.writeheader()
            writer.writerows(csv_data)
        
        print(f"✅ Created {filename} with {len(csv_data)} claims\n")
        print("="*70)
        print("  SUCCESS! Upload this CSV to test bulk upload")
        print("="*70 + "\n")
    else:
        print("\n" + "="*70)
        print("  NO CLAIMS FOUND IN ANY WINDOW")
        print("="*70)
        print("""
Possible reasons:
1. UHC sandbox/test environment has no data
2. Practice TIN not configured correctly
3. No claims submitted in last 24 months
4. API credentials don't have access to claim data

Try using your enhanced-template-real.csv with the correct date range
(90 days max, within last 24 months).
        """)

if __name__ == "__main__":
    main()
