#!/usr/bin/env python3
"""
Automated Test: Practice Selector Feature
Tests the complete practice selector functionality
"""
import requests
import json
import sys
from datetime import datetime

# Configuration
BASE_URL = "https://pre-prod.connectme.be.totessoft.com"
KEYCLOAK_URL = "https://auth.totesoft.com/realms/connectme-preprod"
CLIENT_ID = "connectme-preprod-frontend"

# Test credentials (update as needed)
TEST_USERNAME = "vigneshr"
TEST_PASSWORD = "your_password_here"  # Update this

class Colors:
    GREEN = '\033[92m'
    RED = '\033[91m'
    YELLOW = '\033[93m'
    BLUE = '\033[94m'
    RESET = '\033[0m'

def print_header(text):
    print(f"\n{'='*80}")
    print(f"{Colors.BLUE}{text}{Colors.RESET}")
    print(f"{'='*80}\n")

def print_success(text):
    print(f"{Colors.GREEN}✅ {text}{Colors.RESET}")

def print_error(text):
    print(f"{Colors.RED}❌ {text}{Colors.RESET}")

def print_warning(text):
    print(f"{Colors.YELLOW}⚠️  {text}{Colors.RESET}")

def print_info(text):
    print(f"ℹ️  {text}")

def get_token():
    """Get Keycloak access token"""
    print_info("Attempting to get Keycloak token...")
    
    try:
        response = requests.post(
            f"{KEYCLOAK_URL}/protocol/openid-connect/token",
            data={
                'client_id': CLIENT_ID,
                'username': TEST_USERNAME,
                'password': TEST_PASSWORD,
                'grant_type': 'password',
                'scope': 'openid profile email',
            },
            headers={'Content-Type': 'application/x-www-form-urlencoded'},
            timeout=10
        )
        
        if response.status_code == 200:
            token = response.json()['access_token']
            print_success(f"Token obtained: {token[:30]}...")
            return token
        else:
            print_error(f"Failed to get token: {response.status_code}")
            print_error(f"Response: {response.text}")
            return None
    except Exception as e:
        print_error(f"Error getting token: {e}")
        return None

def test_practice_api_without_auth():
    """Test 1: Practice API without authentication (should work with AllowAny)"""
    print_header("Test 1: Practice API Without Authentication")
    
    try:
        response = requests.get(
            f"{BASE_URL}/api/v1/providers/practices/",
            timeout=10
        )
        
        print_info(f"Status Code: {response.status_code}")
        
        if response.status_code == 200:
            data = response.json()
            print_success("Practice API is accessible")
            print_info(f"Response format: {type(data)}")
            
            if 'results' in data:
                practices = data['results']
                print_success(f"Paginated response with {len(practices)} practices")
            elif isinstance(data, list):
                practices = data
                print_success(f"Array response with {len(practices)} practices")
            else:
                print_error("Unexpected response format")
                return False
            
            if len(practices) > 0:
                print_success(f"Found practice: {practices[0]['name']} (TIN: {practices[0]['tin']})")
                return True
            else:
                print_warning("No practices found in response")
                return False
        else:
            print_error(f"Failed: {response.status_code}")
            print_error(f"Response: {response.text[:200]}")
            return False
            
    except Exception as e:
        print_error(f"Exception: {e}")
        return False

def test_practice_api_with_auth(token):
    """Test 2: Practice API with authentication"""
    print_header("Test 2: Practice API With Authentication")
    
    if not token:
        print_warning("Skipping - no token available")
        return False
    
    try:
        response = requests.get(
            f"{BASE_URL}/api/v1/providers/practices/",
            headers={'Authorization': f'Bearer {token}'},
            timeout=10
        )
        
        print_info(f"Status Code: {response.status_code}")
        
        if response.status_code == 200:
            data = response.json()
            practices = data.get('results', data)
            print_success(f"Authenticated request successful")
            print_success(f"Found {len(practices)} practices")
            
            for practice in practices:
                print_info(f"  - {practice['name']} (ID: {practice['id']}, TIN: {practice['tin']})")
            
            return True
        else:
            print_error(f"Failed: {response.status_code}")
            return False
            
    except Exception as e:
        print_error(f"Exception: {e}")
        return False

def test_claims_search_with_practice(token):
    """Test 3: Claims search with practice ID"""
    print_header("Test 3: Claims Search With Practice ID")
    
    if not token:
        print_warning("Skipping - no token available")
        return False
    
    try:
        # First get practices
        practices_response = requests.get(
            f"{BASE_URL}/api/v1/providers/practices/",
            headers={'Authorization': f'Bearer {token}'},
            timeout=10
        )
        
        if practices_response.status_code != 200:
            print_error("Failed to get practices")
            return False
        
        practices_data = practices_response.json()
        practices = practices_data.get('results', practices_data)
        
        if len(practices) == 0:
            print_error("No practices available")
            return False
        
        practice_id = practices[0]['id']
        print_info(f"Using practice ID: {practice_id} ({practices[0]['name']})")
        
        # Now test claims search with practice ID
        search_data = {
            'firstServiceDate': '2025-10-01',
            'lastServiceDate': '2025-10-31',
            'practiceId': str(practice_id),
            'patientFirstName': 'CHANTAL',
            'patientLastName': 'KISA'
        }
        
        print_info(f"Search parameters: {json.dumps(search_data, indent=2)}")
        
        response = requests.post(
            f"{BASE_URL}/api/v1/claims/search/",
            headers={
                'Authorization': f'Bearer {token}',
                'Content-Type': 'application/json'
            },
            json=search_data,
            timeout=30
        )
        
        print_info(f"Status Code: {response.status_code}")
        
        if response.status_code == 200:
            data = response.json()
            print_success("Claims search with practice ID successful")
            print_info(f"Found {data.get('count', 0)} claims")
            return True
        else:
            print_error(f"Failed: {response.status_code}")
            print_error(f"Response: {response.text[:500]}")
            return False
            
    except Exception as e:
        print_error(f"Exception: {e}")
        return False

def test_bulk_upload_endpoint(token):
    """Test 4: Bulk upload endpoint authentication"""
    print_header("Test 4: Bulk Upload Endpoint")
    
    if not token:
        print_warning("Skipping - no token available")
        return False
    
    try:
        # Test with a minimal request (no file, just to check auth)
        response = requests.post(
            f"{BASE_URL}/api/v1/claims/bulk/upload/",
            headers={'Authorization': f'Bearer {token}'},
            timeout=10
        )
        
        print_info(f"Status Code: {response.status_code}")
        
        # 400 is expected (no file), but not 401/403
        if response.status_code == 400:
            data = response.json()
            if 'error' in data and 'file' in data['error'].lower():
                print_success("Bulk upload endpoint is accessible (400 = missing file, as expected)")
                return True
        elif response.status_code in [401, 403]:
            print_error(f"Authentication failed: {response.status_code}")
            return False
        else:
            print_warning(f"Unexpected status: {response.status_code}")
            print_info(f"Response: {response.text[:200]}")
            return False
            
    except Exception as e:
        print_error(f"Exception: {e}")
        return False

def main():
    """Run all tests"""
    print_header("🧪 Practice Selector Feature - Automated Tests")
    print_info(f"Test started at: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print_info(f"Target: {BASE_URL}")
    
    results = {}
    
    # Test 1: Practice API without auth
    results['practice_api_no_auth'] = test_practice_api_without_auth()
    
    # Get token for authenticated tests
    token = None
    if TEST_PASSWORD != "your_password_here":
        token = get_token()
    else:
        print_warning("\n⚠️  No password configured - skipping authenticated tests")
        print_info("Update TEST_PASSWORD in the script to run authenticated tests")
    
    # Test 2: Practice API with auth
    if token:
        results['practice_api_with_auth'] = test_practice_api_with_auth(token)
        
        # Test 3: Claims search with practice
        results['claims_search_with_practice'] = test_claims_search_with_practice(token)
        
        # Test 4: Bulk upload endpoint
        results['bulk_upload_endpoint'] = test_bulk_upload_endpoint(token)
    
    # Summary
    print_header("📊 Test Summary")
    
    total_tests = len(results)
    passed_tests = sum(1 for v in results.values() if v)
    failed_tests = total_tests - passed_tests
    
    for test_name, passed in results.items():
        status = "✅ PASSED" if passed else "❌ FAILED"
        print(f"  {test_name}: {status}")
    
    print(f"\n{'='*80}")
    print(f"Total: {total_tests} | Passed: {passed_tests} | Failed: {failed_tests}")
    
    if failed_tests == 0:
        print_success("\n🎉 All tests passed!")
        return 0
    else:
        print_error(f"\n⚠️  {failed_tests} test(s) failed")
        return 1

if __name__ == '__main__':
    sys.exit(main())

