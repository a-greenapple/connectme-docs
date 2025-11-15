#!/opt/homebrew/bin/python3
"""
Test Practice API and Claims Search with Practice Selector

Usage:
    /opt/homebrew/bin/python3 test_practice_api.py <username> <password>
    /opt/homebrew/bin/python3 test_practice_api.py vigneshr mypassword
"""
import requests
import json
import sys
import urllib3
import ssl
from datetime import datetime
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
FRONTEND_URL = "https://pre-prod.connectme.apps.totessoft.com"
KEYCLOAK_URL = "https://auth.totesoft.com/realms/connectme-preprod/protocol/openid-connect/token"

# Get credentials from command line or use defaults
TEST_USERNAME = sys.argv[1] if len(sys.argv) > 1 else "vigneshr"
TEST_PASSWORD = sys.argv[2] if len(sys.argv) > 2 else None

def print_header(title):
    """Print a formatted header"""
    print("\n" + "="*80)
    print(f"🧪 {title}")
    print("="*80)

def print_success(message):
    """Print success message"""
    print(f"✅ {message}")

def print_error(message):
    """Print error message"""
    print(f"❌ {message}")

def print_info(message):
    """Print info message"""
    print(f"ℹ️  {message}")

def get_auth_token(username, password):
    """Get Keycloak authentication token"""
    print_header("Step 1: Authentication")
    
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

def test_practice_api_without_auth():
    """Test Practice API without authentication"""
    print_header("Step 2: Test Practice API (No Auth)")
    
    try:
        response = session.get(
            f"{BACKEND_URL}/api/v1/providers/practices/",
            timeout=10
        )
        
        print_info(f"Status Code: {response.status_code}")
        
        if response.status_code == 200:
            data = response.json()
            print_success("Practice API accessible without auth (AllowAny is working)")
            print_info(f"Response: {json.dumps(data, indent=2)}")
            
            # Check if we got practices
            practices = data.get('results', data)
            if isinstance(practices, list) and len(practices) > 0:
                print_success(f"Found {len(practices)} practice(s)")
                for practice in practices:
                    print_info(f"  - {practice['name']} (TIN: {practice['tin']})")
                return True, practices
            else:
                print_error("No practices found in response")
                return False, []
        else:
            print_error(f"Failed to fetch practices: {response.status_code}")
            print_error(f"Response: {response.text}")
            return False, []
    except Exception as e:
        print_error(f"Error testing Practice API: {e}")
        return False, []

def test_practice_api_with_auth(token):
    """Test Practice API with authentication"""
    print_header("Step 3: Test Practice API (With Auth)")
    
    try:
        response = session.get(
            f"{BACKEND_URL}/api/v1/providers/practices/",
            headers={'Authorization': f'Bearer {token}'},
            timeout=10
        )
        
        print_info(f"Status Code: {response.status_code}")
        
        if response.status_code == 200:
            data = response.json()
            print_success("Practice API works with authentication")
            
            # Check if we got practices
            practices = data.get('results', data)
            if isinstance(practices, list) and len(practices) > 0:
                print_success(f"Found {len(practices)} practice(s)")
                for practice in practices:
                    print_info(f"  - {practice['name']} (TIN: {practice['tin']})")
                return True, practices
            else:
                print_error("No practices found in response")
                return False, []
        else:
            print_error(f"Failed to fetch practices: {response.status_code}")
            print_error(f"Response: {response.text}")
            return False, []
    except Exception as e:
        print_error(f"Error testing Practice API: {e}")
        return False, []

def test_claims_search_with_practice(token, practice_id):
    """Test claims search with practice selection"""
    print_header("Step 4: Test Claims Search with Practice")
    
    try:
        # Use recent dates for testing
        from datetime import date, timedelta
        end_date = date.today()
        start_date = end_date - timedelta(days=30)
        
        payload = {
            'firstServiceDate': start_date.strftime('%Y-%m-%d'),
            'lastServiceDate': end_date.strftime('%Y-%m-%d'),
            'practiceId': str(practice_id),
            'patientFirstName': 'CHANTAL',
            'patientLastName': 'KISA',
        }
        
        print_info(f"Searching claims with:")
        print_info(f"  Practice ID: {practice_id}")
        print_info(f"  Date Range: {start_date} to {end_date}")
        print_info(f"  Patient: CHANTAL KISA")
        
        response = session.post(
            f"{BACKEND_URL}/api/v1/claims/search/",
            json=payload,
            headers={
                'Authorization': f'Bearer {token}',
                'Content-Type': 'application/json',
            },
            timeout=30
        )
        
        print_info(f"Status Code: {response.status_code}")
        
        if response.status_code == 200:
            data = response.json()
            claims_count = data.get('count', len(data.get('claims', [])))
            print_success(f"Claims search successful!")
            print_info(f"Found {claims_count} claim(s)")
            
            if claims_count > 0:
                print_info("Sample claims:")
                for claim in data.get('claims', [])[:3]:
                    print_info(f"  - {claim.get('claimNumber')} - {claim.get('patient')}")
            
            return True
        else:
            print_error(f"Claims search failed: {response.status_code}")
            print_error(f"Response: {response.text[:500]}")
            return False
    except Exception as e:
        print_error(f"Error testing claims search: {e}")
        return False

def test_bulk_upload_token():
    """Test that bulk upload endpoint is accessible"""
    print_header("Step 5: Test Bulk Upload Endpoint")
    
    try:
        # Just test that the endpoint exists (will return 400 without file)
        response = session.post(
            f"{BACKEND_URL}/api/v1/claims/bulk/upload/",
            timeout=10
        )
        
        print_info(f"Status Code: {response.status_code}")
        
        # 400 is expected (no file), 401 would be auth error
        if response.status_code in [400, 401]:
            if response.status_code == 400:
                print_success("Bulk upload endpoint accessible (400 = missing file, as expected)")
                return True
            else:
                print_error("Bulk upload requires authentication (401)")
                return False
        else:
            print_info(f"Unexpected status: {response.status_code}")
            return False
    except Exception as e:
        print_error(f"Error testing bulk upload: {e}")
        return False

def run_all_tests():
    """Run all tests"""
    print("\n" + "🚀 " + "="*76)
    print("🚀 ConnectMe Practice API & Claims Search Test Suite")
    print("🚀 " + "="*76)
    print(f"🚀 Test Time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print(f"🚀 Username: {TEST_USERNAME}")
    print("🚀 " + "="*76)
    
    results = {
        'passed': 0,
        'failed': 0,
        'total': 0
    }
    
    # Test 1: Practice API without auth
    success, practices = test_practice_api_without_auth()
    results['total'] += 1
    if success:
        results['passed'] += 1
    else:
        results['failed'] += 1
    
    # Get auth token (optional for remaining tests)
    token = None
    if TEST_PASSWORD:
        token = get_auth_token(TEST_USERNAME, TEST_PASSWORD)
        
        if token:
            # Test 2: Practice API with auth
            success, auth_practices = test_practice_api_with_auth(token)
            results['total'] += 1
            if success:
                results['passed'] += 1
                practices = auth_practices  # Use authenticated practices
            else:
                results['failed'] += 1
            
            # Test 3: Claims search with practice
            if practices and len(practices) > 0:
                practice_id = practices[0]['id']
                success = test_claims_search_with_practice(token, practice_id)
                results['total'] += 1
                if success:
                    results['passed'] += 1
                else:
                    results['failed'] += 1
    else:
        print_info("\nSkipping authenticated tests (provide password as argument)")
        print_info("Usage: python3 test_practice_api.py <username> <password>")
    
    # Test 4: Bulk upload endpoint
    success = test_bulk_upload_token()
    results['total'] += 1
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
    
    # Frontend test instructions
    print("\n" + "="*80)
    print("🌐 MANUAL FRONTEND TESTS")
    print("="*80)
    print(f"1. Open: {FRONTEND_URL}/claims")
    print("2. Check that practice dropdown appears at top")
    print("3. Verify 'RSM (TIN: 854203105)' is shown")
    print("4. Try searching for claims with practice selected")
    print("5. Go to: {}/bulk-upload".format(FRONTEND_URL))
    print("6. Try uploading a CSV file")
    print("="*80)
    
    return results['failed'] == 0

if __name__ == '__main__':
    success = run_all_tests()
    sys.exit(0 if success else 1)

