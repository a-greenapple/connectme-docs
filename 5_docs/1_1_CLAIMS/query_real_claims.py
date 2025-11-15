#!/usr/bin/env python3
"""
Query UHC API to find real working claims and create a test CSV
"""
import requests
import csv
import json
from datetime import datetime, timedelta

# API Configuration
API_BASE_URL = "https://connectme.be.totesoft.com"
AUTH_URL = f"{API_BASE_URL}/api/v1/auth/mock/login/"
SEARCH_URL = f"{API_BASE_URL}/api/v1/claims/search/"

def get_auth_token():
    """Get authentication token"""
    print("🔐 Authenticating...")
    try:
        response = requests.post(AUTH_URL, json={}, timeout=10)
        if response.status_code == 200:
            data = response.json()
            token = data.get('access_token')
            print(f"✅ Authentication successful!")
            return token
        else:
            print(f"❌ Auth failed: {response.status_code}")
            return None
    except Exception as e:
        print(f"❌ Auth error: {e}")
        return None

def search_claims(token, start_date, end_date):
    """Search for claims in date range"""
    print(f"\n🔍 Searching claims from {start_date} to {end_date}...")
    
    headers = {
        'Authorization': f'Bearer {token}',
        'Content-Type': 'application/json'
    }
    
    payload = {
        'firstServiceDate': start_date,
        'lastServiceDate': end_date
    }
    
    try:
        response = requests.post(SEARCH_URL, headers=headers, json=payload, timeout=30)
        print(f"   Response status: {response.status_code}")
        
        if response.status_code == 200:
            data = response.json()
            claims = data.get('claims', [])
            print(f"✅ Found {len(claims)} claims!")
            return claims
        else:
            print(f"❌ Search failed: {response.text[:200]}")
            return []
    except Exception as e:
        print(f"❌ Search error: {e}")
        return []

def create_csv_from_claims(claims, filename):
    """Create CSV file from claims data"""
    if not claims:
        print("\n❌ No claims to write to CSV")
        return False
    
    print(f"\n📝 Creating CSV: {filename}")
    
    csv_data = []
    for i, claim in enumerate(claims[:10]):  # Limit to first 10 claims
        try:
            # Extract data from claim
            claim_number = claim.get('claimNumber', '')
            
            # Try to get patient info
            patient = claim.get('patient', {})
            first_name = patient.get('firstName', 'UNKNOWN')
            last_name = patient.get('lastName', 'UNKNOWN')
            dob = patient.get('dateOfBirth', '01/01/1970')
            
            # Try to get subscriber info
            subscriber = claim.get('subscriber', {})
            subscriber_id = subscriber.get('memberId', '') or subscriber.get('subscriberId', '')
            
            # Try to get service dates
            service_lines = claim.get('serviceLines', [])
            service_date = ''
            if service_lines:
                service_date = service_lines[0].get('serviceDate', '')
            
            # If no service date, try claim level
            if not service_date:
                service_date = claim.get('serviceDate', '') or claim.get('firstServiceDate', '')
            
            if claim_number:
                csv_data.append({
                    'claim_number': claim_number,
                    'first_name': first_name,
                    'last_name': last_name,
                    'date_of_birth': dob,
                    'subscriber_id': subscriber_id,
                    'first_service_date': service_date,
                    'last_service_date': service_date
                })
                print(f"   ✅ Added: {claim_number}")
        except Exception as e:
            print(f"   ⚠️  Skipped claim {i+1}: {e}")
            continue
    
    if not csv_data:
        print("❌ No valid claims to write")
        return False
    
    # Write CSV
    with open(filename, 'w', newline='') as f:
        fieldnames = ['claim_number', 'first_name', 'last_name', 'date_of_birth', 
                     'subscriber_id', 'first_service_date', 'last_service_date']
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(csv_data)
    
    print(f"✅ Created {filename} with {len(csv_data)} claims")
    return True

def main():
    print("""
╔═══════════════════════════════════════════════════════════════════════════╗
║                                                                           ║
║         🔍 QUERYING REAL CLAIMS FROM UHC API                             ║
║                                                                           ║
╚═══════════════════════════════════════════════════════════════════════════╝
    """)
    
    # Get auth token
    token = get_auth_token()
    if not token:
        print("\n❌ Cannot proceed without authentication")
        return
    
    # Try multiple date ranges
    date_ranges = [
        ('2024-01-01', '2024-12-31', 'working-claims-2024.csv'),
        ('2023-01-01', '2023-12-31', 'working-claims-2023.csv'),
        ('2022-01-01', '2022-12-31', 'working-claims-2022.csv'),
    ]
    
    found_any = False
    for start, end, filename in date_ranges:
        claims = search_claims(token, start, end)
        if claims:
            if create_csv_from_claims(claims, f'csv-templates/{filename}'):
                found_any = True
                break  # Stop after finding claims in one range
    
    if found_any:
        print("""
╔═══════════════════════════════════════════════════════════════════════════╗
║                                                                           ║
║         ✅ SUCCESS! CSV CREATED WITH REAL CLAIMS                         ║
║                                                                           ║
╚═══════════════════════════════════════════════════════════════════════════╝

🎯 NEXT STEPS:

1. Upload the CSV via bulk upload page
2. Leave date fields EMPTY (auto-detection)
3. Enable "Use batch query optimization"
4. Click Upload
5. Should show SUCCESS!

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
        """)
    else:
        print("""
╔═══════════════════════════════════════════════════════════════════════════╗
║                                                                           ║
║         ⚠️  NO CLAIMS FOUND                                              ║
║                                                                           ║
╚═══════════════════════════════════════════════════════════════════════════╝

This means:
  1. Your UHC practice has no claims in 2022-2024
  2. Practice/Payer mapping needs configuration
  3. Using UHC test/sandbox environment with no data

🔍 TO DEBUG:

1. Check practice configuration:
   ssh user@server
   cd /var/www/connectme-backend
   source venv/bin/activate
   python manage.py shell
   
   >>> from apps.providers.models import Practice, PracticePayerMapping
   >>> Practice.objects.all()
   >>> PracticePayerMapping.objects.all()

2. Try Claims Search manually in the web UI with different dates

3. Contact UHC to verify your practice TIN has claim data

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
        """)

if __name__ == "__main__":
    main()
