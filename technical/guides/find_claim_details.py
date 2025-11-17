#!/usr/bin/env python3
"""
Search for a specific claim to find its actual service dates and patient details
"""
import requests
import json
from datetime import datetime, timedelta

API_BASE_URL = "https://connectme.be.totesoft.com"

def get_auth_token():
    """Get authentication token"""
    print("🔐 Authenticating...")
    try:
        response = requests.post(f"{API_BASE_URL}/api/v1/auth/mock/login/", json={}, timeout=10)
        if response.status_code == 200:
            token = response.json().get('access_token')
            print(f"✅ Authenticated\n")
            return token
        return None
    except Exception as e:
        print(f"❌ Auth error: {e}")
        return None

def search_claim_by_date_ranges(token, claim_number):
    """Search for a claim across multiple date ranges"""
    print(f"🔍 Searching for claim: {claim_number}\n")
    
    headers = {'Authorization': f'Bearer {token}', 'Content-Type': 'application/json'}
    
    # Try different 90-day windows going back 24 months
    today = datetime.now()
    
    date_ranges = []
    for i in range(8):  # 8 quarters = 2 years
        end = today - timedelta(days=i*90)
        start = end - timedelta(days=89)
        date_ranges.append((start.strftime('%Y-%m-%d'), end.strftime('%Y-%m-%d')))
    
    for start, end in date_ranges:
        print(f"   Trying: {start} to {end}...", end='')
        
        payload = {
            'firstServiceDate': start,
            'lastServiceDate': end
        }
        
        try:
            response = requests.post(f"{API_BASE_URL}/api/v1/claims/search/", 
                                   headers=headers, json=payload, timeout=60)
            
            if response.status_code == 200:
                data = response.json()
                claims = data.get('claims', [])
                
                # Search for our claim number in the results
                for claim in claims:
                    if str(claim.get('claimNumber', '')).strip() == str(claim_number).strip():
                        print(f" ✅ FOUND!\n")
                        return claim, start, end
                
                print(f" ({len(claims)} claims, not found)")
            else:
                print(f" ❌ Error: {response.status_code}")
        except Exception as e:
            print(f" ❌ Timeout/Error")
            continue
    
    return None, None, None

def create_csv_from_claim(claim, claim_number, start_date, end_date):
    """Create CSV with the found claim details"""
    filename = f'csv-templates/real-claim-{claim_number}.csv'
    
    print(f"\n📝 Creating CSV: {filename}")
    print("\nClaim Details:")
    print("="*70)
    
    # Extract details
    claim_num = claim.get('claimNumber', claim_number)
    
    patient = claim.get('patient', {})
    first_name = patient.get('firstName', 'UNKNOWN')
    last_name = patient.get('lastName', 'UNKNOWN')
    dob = patient.get('dateOfBirth', '01/01/1970')
    
    subscriber = claim.get('subscriber', {})
    subscriber_id = subscriber.get('memberId', '') or subscriber.get('subscriberId', 'UNKNOWN')
    
    # Service dates
    service_date = claim.get('serviceDate', '') or claim.get('firstServiceDate', start_date)
    
    print(f"Claim Number:    {claim_num}")
    print(f"Patient Name:    {first_name} {last_name}")
    print(f"Date of Birth:   {dob}")
    print(f"Subscriber ID:   {subscriber_id}")
    print(f"Service Date:    {service_date}")
    print(f"Found in Range:  {start_date} to {end_date}")
    print("="*70)
    
    # Create CSV
    import csv
    with open(filename, 'w', newline='') as f:
        writer = csv.writer(f)
        writer.writerow(['claim_number', 'first_name', 'last_name', 'date_of_birth', 
                        'subscriber_id', 'first_service_date', 'last_service_date'])
        writer.writerow([claim_num, first_name, last_name, dob, subscriber_id, 
                        service_date, service_date])
    
    print(f"\n✅ Created: {filename}")
    print("\nNow upload this CSV to test bulk upload!")
    return filename

def main():
    print("""
╔═══════════════════════════════════════════════════════════════════════════╗
║                                                                           ║
║         🔍 FINDING REAL CLAIM DETAILS                                    ║
║                                                                           ║
╚═══════════════════════════════════════════════════════════════════════════╝
    """)
    
    claim_number = "51598988"
    
    token = get_auth_token()
    if not token:
        print("❌ Cannot proceed without authentication")
        return
    
    claim, start_date, end_date = search_claim_by_date_ranges(token, claim_number)
    
    if claim:
        print("\n" + "="*70)
        print("  ✅ SUCCESS! FOUND CLAIM DETAILS")
        print("="*70)
        create_csv_from_claim(claim, claim_number, start_date, end_date)
    else:
        print(f"""
╔═══════════════════════════════════════════════════════════════════════════╗
║                                                                           ║
║         ❌ CLAIM {claim_number} NOT FOUND IN LAST 24 MONTHS              ║
║                                                                           ║
╚═══════════════════════════════════════════════════════════════════════════╝

Possible reasons:
1. Claim is older than 24 months (UHC limit)
2. Claim belongs to a different practice/TIN
3. Claim was never submitted to UHC
4. Incorrect claim number

🔍 What to do:

1. Verify the claim number is correct: 51598988
2. Check when this claim was submitted to UHC
3. Verify your practice TIN matches this claim
4. Try using Claims Search in the web UI manually:
   https://connectme.apps.totesoft.com/claims
5. Search different date ranges to find it

💡 Tip: If you know the approximate service date, manually set:
   - Start date: [service_date - 7 days]
   - End date: [service_date + 7 days]
   
Then upload with manual date override in the UI.
        """)

if __name__ == "__main__":
    main()
