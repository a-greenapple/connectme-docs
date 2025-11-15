#!/usr/bin/env python3
"""
Find working claims from UHC API and create a test CSV
"""
import csv
from datetime import datetime, timedelta

# Generate test CSV with various date ranges
def create_test_csvs():
    """Create multiple test CSVs with different date ranges"""
    
    # Test 1: Recent dates (last 30 days)
    print("Creating test CSVs with different date ranges...\n")
    
    today = datetime.now()
    
    # Test scenarios
    scenarios = [
        {
            'name': 'test-recent-30days.csv',
            'start': (today - timedelta(days=30)).strftime('%Y-%m-%d'),
            'end': today.strftime('%Y-%m-%d'),
            'description': 'Last 30 days'
        },
        {
            'name': 'test-recent-90days.csv',
            'start': (today - timedelta(days=90)).strftime('%Y-%m-%d'),
            'end': today.strftime('%Y-%m-%d'),
            'description': 'Last 90 days'
        },
        {
            'name': 'test-year-2024.csv',
            'start': '2024-01-01',
            'end': '2024-12-31',
            'description': 'All of 2024'
        },
        {
            'name': 'test-year-2023.csv',
            'start': '2023-01-01',
            'end': '2023-12-31',
            'description': 'All of 2023'
        }
    ]
    
    # Sample claim data with PLACEHOLDER values
    # You'll need to replace these with actual claims from your system
    sample_claims = [
        {
            'claim_number': 'PLACEHOLDER_CLAIM_1',
            'first_name': 'JOHN',
            'last_name': 'DOE',
            'date_of_birth': '01/15/1980',
            'subscriber_id': 'PLACEHOLDER_SUB_1'
        },
        {
            'claim_number': 'PLACEHOLDER_CLAIM_2',
            'first_name': 'JANE',
            'last_name': 'SMITH',
            'date_of_birth': '05/20/1975',
            'subscriber_id': 'PLACEHOLDER_SUB_2'
        },
        {
            'claim_number': 'PLACEHOLDER_CLAIM_3',
            'first_name': 'BOB',
            'last_name': 'JOHNSON',
            'date_of_birth': '11/30/1990',
            'subscriber_id': 'PLACEHOLDER_SUB_3'
        }
    ]
    
    # Create CSV files for each scenario
    for scenario in scenarios:
        filepath = f"csv-templates/{scenario['name']}"
        
        with open(filepath, 'w', newline='') as f:
            fieldnames = ['claim_number', 'first_name', 'last_name', 'date_of_birth', 
                         'subscriber_id', 'first_service_date', 'last_service_date']
            writer = csv.DictWriter(f, fieldnames=fieldnames)
            writer.writeheader()
            
            for claim in sample_claims:
                row = claim.copy()
                row['first_service_date'] = scenario['start']
                row['last_service_date'] = scenario['end']
                writer.writerow(row)
        
        print(f"✅ Created: {filepath}")
        print(f"   Description: {scenario['description']}")
        print(f"   Date range: {scenario['start']} to {scenario['end']}")
        print()

def print_instructions():
    """Print instructions for finding real claims"""
    
    print("""
╔═══════════════════════════════════════════════════════════════════════════╗
║                                                                           ║
║         📋 HOW TO GET REAL WORKING CLAIMS                                ║
║                                                                           ║
╚═══════════════════════════════════════════════════════════════════════════╝

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
🔍 METHOD 1: Use Claims Search Page
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

1. Go to: https://connectme.apps.totesoft.com/claims

2. Search with date range:
   - Start date: (e.g., 2024-01-01)
   - End date: (e.g., 2024-12-31)
   - Click "Search"

3. If claims are found:
   - Note down 3-5 claim numbers
   - Note the patient details (name, DOB, subscriber ID)
   - Note the service dates

4. Update the CSV files:
   - Replace PLACEHOLDER_CLAIM_X with real claim numbers
   - Replace PLACEHOLDER_SUB_X with real subscriber IDs
   - Use the actual service dates from search results

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
🔍 METHOD 2: Check Your Practice Management System
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

1. Export claims from your practice management system
2. Select claims that were submitted to UHC
3. Include:
   - Claim number
   - Patient first name, last name
   - Date of birth
   - Subscriber ID (insurance member ID)
   - Service dates (from and to)

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
🔍 METHOD 3: Use Database if Available
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

If you have access to the ConnectMe database:

$ ssh user@server
$ cd /var/www/connectme-backend
$ source venv/bin/activate
$ python manage.py shell

>>> from apps.claims.models import Claim
>>> claims = Claim.objects.all()[:5]
>>> for claim in claims:
...     print(f"{claim.claim_number}, {claim.patient_first_name}, {claim.patient_last_name}")

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
📝 CSV FORMAT (After Getting Real Claims):
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

claim_number,first_name,last_name,date_of_birth,subscriber_id,first_service_date,last_service_date
ZE59426195,CHANTAL,KISA,05/10/1975,057896633,2024-03-15,2024-03-15
AB12345678,JOHN,DOE,01/15/1980,123456789,2024-03-20,2024-03-20
CD98765432,JANE,SMITH,05/20/1975,987654321,2024-03-25,2024-03-25

Important:
  - Use REAL claim numbers that exist in UHC
  - Match the service dates with what's in UHC
  - Include patient demographics exactly as in UHC records

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
🧪 TESTING STRATEGY:
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Start Small:
  1. Find ONE working claim via Claims Search
  2. Create CSV with just that one claim
  3. Test bulk upload
  4. If successful → Add more claims
  5. Scale up gradually

This way you can verify the system works with real data step by step!

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
""")

if __name__ == "__main__":
    print("\n" + "="*70)
    print("  CREATING TEST CSV FILES")
    print("="*70 + "\n")
    
    create_test_csvs()
    print_instructions()
    
    print("\n" + "="*70)
    print("  NEXT STEP:")
    print("="*70)
    print("\nUse Claims Search to find working claims, then update the CSV files")
    print("with real claim numbers!\n")

