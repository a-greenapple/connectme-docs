#!/opt/homebrew/bin/python3
"""
Test Claims Search Functionality

Usage:
    python3 test_claims_search.py <username> <password>
    python3 test_claims_search.py vigneshr mypassword
"""
import requests
import json
import sys
import urllib3
import ssl
from datetime import datetime, date, timedelta
from requests.adapters import HTTPAdapter
from urllib3.poolmanager import PoolManager

# Disable SSL warnings (for self-signed certificates)
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

# Create a custom SSL adapter to handle SSL issues
class SSLAdapter(HTTPAdapter):
    def init_poolmanager(self, *args, **kwargs):
        context = ssl.create_default_context()
        context.check_hostname = False
        context.verify_mode = ssl.CERT_NONE
        kwargs['ssl_context'] = context
        return super().init_poolmanager(*args, **kwargs)

# Create a session with the custom adapter
session = requests.Session()
session.mount('https://', SSLAdapter())

# Configuration
BACKEND_URL = "https://pre-prod.connectme.be.totessoft.com"
KEYCLOAK_URL = "https://auth.totesoft.com/realms/connectme-preprod/protocol/openid-connect/token"

# Get credentials from command line or use defaults
TEST_USERNAME = sys.argv[1] if len(sys.argv) > 1 else "vigneshr"
TEST_PASSWORD = sys.argv[2] if len(sys.argv) > 2 else None

def print_header(title):
    print("\n" + "="*80)
    print(f"🧪 {title}")
    print("="*80)

def print_success(message):
    print(f"✅ {message}")

def print_error(message):
    print(f"❌ {message}")

def print_info(message):
    print(f"ℹ️  {message}")

def get_auth_token(username, password):
    """Get Keycloak authentication token"""
    print_header("Step 1: Getting Authentication Token")
    
    try:
        response = session.post(
            KEYCLOAK_URL,
            data={
                'client_id': 'connectme-preprod-frontend',
                'username': username,
                'password': password,
                'grant_type': 'password',
                'scope': 'openid profile email',
            },
            headers={'Content-Type': 'application/x-www-form-urlencoded'},
            timeout=10
        )
        
        if response.status_code == 200:
            token_data = response.json()
            access_token = token_data['access_token']
            print_success(f"Authenticated as: {username}")
            print_info(f"Token: {access_token[:30]}...")
            return access_token
        else:
            print_error(f"Authentication failed: {response.status_code}")
            print_error(f"Response: {response.text}")
            return None
    except Exception as e:
        print_error(f"Authentication error: {e}")
        return None

def get_practice_id(token):
    """Get the first available practice ID"""
    print_header("Step 2: Getting Practice ID")
    
    try:
        response = session.get(
            f"{BACKEND_URL}/api/v1/providers/practices/",
            headers={'Authorization': f'Bearer {token}'} if token else {},
            timeout=10
        )
        
        if response.status_code == 200:
            data = response.json()
            practices = data.get('results', data)
            
            if isinstance(practices, list) and len(practices) > 0:
                practice = practices[0]
                print_success(f"Found practice: {practice['name']} (ID: {practice['id']}, TIN: {practice['tin']})")
                return practice['id']
            else:
                print_error("No practices found")
                return None
        else:
            print_error(f"Failed to get practices: {response.status_code}")
            print_error(f"Response: {response.text}")
            return None
    except Exception as e:
        print_error(f"Error getting practices: {e}")
        return None

def test_claims_search_scenario(token, practice_id, scenario_name, params):
    """Test a specific claims search scenario"""
    print_header(f"Testing: {scenario_name}")
    
    # Add practice_id to params
    params['practiceId'] = str(practice_id)
    
    print_info("Search Parameters:")
    for key, value in params.items():
        print_info(f"  {key}: {value}")
    
    try:
        response = session.post(
            f"{BACKEND_URL}/api/v1/claims/search/",
            json=params,
            headers={
                'Authorization': f'Bearer {token}',
                'Content-Type': 'application/json',
            },
            timeout=60
        )
        
        print_info(f"Status Code: {response.status_code}")
        
        if response.status_code == 200:
            data = response.json()
            
            # Handle different response formats
            claims = data.get('claims', [])
            count = data.get('count', len(claims))
            has_more = data.get('hasMore', False)
            transaction_id = data.get('transactionId')
            
            print_success(f"Search successful!")
            print_info(f"Found: {count} claim(s)")
            if has_more:
                print_info("More results available")
            if transaction_id:
                print_info(f"Transaction ID: {transaction_id}")
            
            # Show sample claims
            if claims and len(claims) > 0:
                print_info("\nSample Claims:")
                for i, claim in enumerate(claims[:5], 1):
                    claim_num = claim.get('claimNumber', 'N/A')
                    patient = claim.get('patient', 'N/A')
                    status = claim.get('status', 'N/A')
                    charged = claim.get('chargedAmount', 'N/A')
                    paid = claim.get('paidAmount', 'N/A')
                    print_info(f"  {i}. {claim_num} - {patient}")
                    print_info(f"     Status: {status}, Charged: ${charged}, Paid: ${paid}")
            
            return True, data
        else:
            print_error(f"Search failed: {response.status_code}")
            try:
                error_data = response.json()
                print_error(f"Error: {json.dumps(error_data, indent=2)}")
            except:
                print_error(f"Response: {response.text[:500]}")
            return False, None
    except Exception as e:
        print_error(f"Error during search: {e}")
        import traceback
        traceback.print_exc()
        return False, None

def run_claims_search_tests():
    """Run all claims search tests"""
    print("\n" + "🚀 " + "="*76)
    print("🚀 ConnectMe Claims Search Test Suite")
    print("🚀 " + "="*76)
    print(f"🚀 Test Time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print(f"🚀 Username: {TEST_USERNAME}")
    print("🚀 " + "="*76)
    
    # Check if credentials are set
    if not TEST_PASSWORD:
        print_error("\n❌ Please provide password!")
        print_info("Usage: python3 test_claims_search.py <username> <password>")
        print_info("Example: python3 test_claims_search.py vigneshr mypassword")
        return False
    
    # Get auth token
    token = get_auth_token(TEST_USERNAME, TEST_PASSWORD)
    if not token:
        print_error("Failed to authenticate. Cannot proceed with tests.")
        return False
    
    # Get practice ID
    practice_id = get_practice_id(token)
    if not practice_id:
        print_error("Failed to get practice ID. Cannot proceed with tests.")
        return False
    
    # Define test scenarios
    end_date = date.today()
    start_date = end_date - timedelta(days=30)
    
    scenarios = [
        {
            'name': 'Scenario 1: Date Range Only (Last 30 Days)',
            'params': {
                'firstServiceDate': start_date.strftime('%Y-%m-%d'),
                'lastServiceDate': end_date.strftime('%Y-%m-%d'),
            }
        },
        {
            'name': 'Scenario 2: Date Range + Patient Name',
            'params': {
                'firstServiceDate': start_date.strftime('%Y-%m-%d'),
                'lastServiceDate': end_date.strftime('%Y-%m-%d'),
                'patientFirstName': 'CHANTAL',
                'patientLastName': 'KISA',
            }
        },
        {
            'name': 'Scenario 3: Date Range + Patient Name + DOB',
            'params': {
                'firstServiceDate': start_date.strftime('%Y-%m-%d'),
                'lastServiceDate': end_date.strftime('%Y-%m-%d'),
                'patientFirstName': 'CHANTAL',
                'patientLastName': 'KISA',
                'patientDob': '1975-05-10',
            }
        },
        {
            'name': 'Scenario 4: Shorter Date Range (Last 7 Days)',
            'params': {
                'firstServiceDate': (end_date - timedelta(days=7)).strftime('%Y-%m-%d'),
                'lastServiceDate': end_date.strftime('%Y-%m-%d'),
            }
        },
    ]
    
    # Run tests
    results = {'passed': 0, 'failed': 0, 'total': len(scenarios)}
    
    for scenario in scenarios:
        success, data = test_claims_search_scenario(
            token,
            practice_id,
            scenario['name'],
            scenario['params']
        )
        
        if success:
            results['passed'] += 1
        else:
            results['failed'] += 1
    
    # Print summary
    print("\n" + "="*80)
    print("📊 TEST SUMMARY")
    print("="*80)
    print(f"Total Tests: {results['total']}")
    print(f"✅ Passed: {results['passed']}")
    print(f"❌ Failed: {results['failed']}")
    print(f"Success Rate: {(results['passed']/results['total']*100):.1f}%")
    print("="*80)
    
    # Troubleshooting tips
    if results['failed'] > 0:
        print("\n" + "="*80)
        print("🔧 TROUBLESHOOTING TIPS")
        print("="*80)
        print("1. Check backend logs:")
        print("   ssh connectme@169.59.163.43 'sudo journalctl -u connectme-preprod-backend -f'")
        print("\n2. Verify practice configuration:")
        print("   - Practice exists in database")
        print("   - Practice has payer mapping")
        print("   - User has correct organization TIN")
        print("\n3. Check UHC API credentials:")
        print("   - OAuth URL is correct")
        print("   - Client ID and Secret are valid")
        print("   - Payer ID matches")
        print("="*80)
    
    return results['failed'] == 0

if __name__ == '__main__':
    success = run_claims_search_tests()
    sys.exit(0 if success else 1)

