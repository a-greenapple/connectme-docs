#!/usr/bin/env python3
"""
Query UHC API for full patient details and create bulk upload CSV
"""
import requests
import csv
from datetime import datetime

API_BASE_URL = "https://connectme.be.totesoft.com"

# Claims from manual search
claims = [
    {"claim_number": "51598988", "patient_name": "TOMMY HOWELL", "service_date": "07/03/2025"},
    {"claim_number": "51611599", "patient_name": "MOSTAFA KORDI", "service_date": "07/03/2025"},
    {"claim_number": "FE98163821", "patient_name": "ZOEY WILCOX", "service_date": "07/02/2025"},
    {"claim_number": "FE23924647", "patient_name": "KIMBERLY KURAK", "service_date": "07/01/2025"},
    {"claim_number": "51545088", "patient_name": "RANDALL MOIR", "service_date": "07/01/2025"},
]

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

def get_claim_details(token, claim_number):
    """Get full claim details including patient info"""
    print(f"   Querying claim {claim_number}...", end='')
    
    headers = {'Authorization': f'Bearer {token}', 'Content-Type': 'application/json'}
    
    try:
        response = requests.get(
            f"{API_BASE_URL}/api/v1/claims/{claim_number}/",
            headers=headers,
            timeout=30
        )
        
        if response.status_code == 200:
            print(" ✅")
            return response.json()
        else:
            print(f" ❌ Error: {response.status_code}")
            return None
    except Exception as e:
        print(f" ❌ Error: {e}")
        return None

def main():
    print("""
╔═══════════════════════════════════════════════════════════════════════════╗
║                                                                           ║
║      🎯 BUILDING BULK UPLOAD CSV FROM REAL CLAIMS                        ║
║                                                                           ║
╚═══════════════════════════════════════════════════════════════════════════╝
    """)
    
    token = get_auth_token()
    if not token:
        print("❌ Cannot proceed without authentication")
        return
    
    csv_data = []
    
    print("📊 Fetching full patient details:\n")
    for claim in claims:
        details = get_claim_details(token, claim['claim_number'])
        
        if details:
            patient = details.get('patient', {})
            subscriber = details.get('subscriber', {})
            
            # Parse names
            first_name = patient.get('firstName', '').strip()
            last_name = patient.get('lastName', '').strip()
            
            # Get DOB and subscriber ID
            dob = patient.get('dateOfBirth', 'UNKNOWN')
            subscriber_id = subscriber.get('memberId') or subscriber.get('subscriberId', 'UNKNOWN')
            
            # Parse service date
            service_date = claim['service_date']
            try:
                dt = datetime.strptime(service_date, '%m/%d/%Y')
                service_date_iso = dt.strftime('%Y-%m-%d')
            except:
                service_date_iso = service_date
            
            csv_data.append({
                'claim_number': claim['claim_number'],
                'first_name': first_name,
                'last_name': last_name,
                'date_of_birth': dob,
                'subscriber_id': subscriber_id,
                'first_service_date': service_date_iso,
                'last_service_date': service_date_iso
            })
            
            print(f"      ✓ {first_name} {last_name} | DOB: {dob} | Subscriber: {subscriber_id}")
    
    if not csv_data:
        print("\n❌ No claims retrieved successfully")
        return
    
    # Create CSV
    filename = 'csv-templates/real-claims-july-2025.csv'
    with open(filename, 'w', newline='') as f:
        fieldnames = ['claim_number', 'first_name', 'last_name', 'date_of_birth', 
                     'subscriber_id', 'first_service_date', 'last_service_date']
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(csv_data)
    
    print(f"\n✅ Created: {filename}")
    print(f"   📊 Total claims: {len(csv_data)}")
    print(f"   📅 Date range: July 1-3, 2025 (3 days)")
    print("\n" + "="*80)
    print("\n🎉 SUCCESS! Your bulk upload CSV is ready!")
    print("\n📋 Next Steps:")
    print("   1. Go to: https://connectme.apps.totesoft.com/bulk-upload")
    print("   2. Upload: real-claims-july-2025.csv")
    print("   3. Leave dates EMPTY (auto-detect will use July 1-3)")
    print("   4. Click 'Upload and Process'")
    print("\n✅ Expected Result: All claims should show SUCCESS!")
    print("="*80)

if __name__ == "__main__":
    main()
