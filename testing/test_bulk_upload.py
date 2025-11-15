#!/opt/homebrew/bin/python3
"""
Test CSV Bulk Upload Functionality

Usage:
    /opt/homebrew/bin/python3 test_bulk_upload.py <username> <password>
    /opt/homebrew/bin/python3 test_bulk_upload.py vigneshr mypassword
"""
import requests
import json
import sys
import time
import os
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

def create_test_csv(filename, scenario):
    """Create a test CSV file"""
    print_header(f"Step 2: Creating Test CSV - {scenario['name']}")
    
    with open(filename, 'w') as f:
        f.write(scenario['content'])
    
    print_success(f"Created: {filename}")
    print_info(f"Rows: {len(scenario['content'].strip().split(chr(10))) - 1}")
    print_info("Content preview:")
    for line in scenario['content'].strip().split('\n')[:5]:
        print_info(f"  {line}")
    
    return filename

def upload_csv(token, filename, provider='uhc', use_batch_query=True):
    """Upload CSV file for bulk processing"""
    print_header("Step 3: Uploading CSV File")
    
    try:
        with open(filename, 'rb') as f:
            files = {'file': (os.path.basename(filename), f, 'text/csv')}
            data = {
                'provider': provider,
                'use_batch_query': str(use_batch_query).lower(),
            }
            
            print_info(f"Uploading: {filename}")
            print_info(f"Provider: {provider}")
            print_info(f"Batch Query: {use_batch_query}")
            
            response = session.post(
                f"{BACKEND_URL}/api/v1/claims/bulk/upload/",
                files=files,
                data=data,
                headers={'Authorization': f'Bearer {token}'},
                timeout=30
            )
        
        print_info(f"Status Code: {response.status_code}")
        
        if response.status_code in [200, 201]:
            job_data = response.json()
            print_success("Upload successful!")
            print_info(f"Job ID: {job_data.get('id')}")
            print_info(f"Status: {job_data.get('status')}")
            print_info(f"Filename: {job_data.get('filename')}")
            print_info(f"Total Rows: {job_data.get('total_rows')}")
            return True, job_data
        else:
            print_error(f"Upload failed: {response.status_code}")
            try:
                error_data = response.json()
                print_error(f"Error: {json.dumps(error_data, indent=2)}")
            except:
                print_error(f"Response: {response.text[:500]}")
            return False, None
    except Exception as e:
        print_error(f"Error during upload: {e}")
        import traceback
        traceback.print_exc()
        return False, None

def monitor_job_progress(token, job_id, max_wait=60):
    """Monitor job processing progress"""
    print_header("Step 4: Monitoring Job Progress")
    
    start_time = time.time()
    check_count = 0
    
    while time.time() - start_time < max_wait:
        check_count += 1
        
        try:
            response = session.get(
                f"{BACKEND_URL}/api/v1/claims/csv-jobs/{job_id}/",
                headers={'Authorization': f'Bearer {token}'},
                timeout=10
            )
            
            if response.status_code == 200:
                job_data = response.json()
                status = job_data.get('status')
                processed = job_data.get('processed_rows', 0)
                total = job_data.get('total_rows', 0)
                success_count = job_data.get('success_count', 0)
                failure_count = job_data.get('failure_count', 0)
                
                progress = (processed / total * 100) if total > 0 else 0
                
                print_info(f"[Check {check_count}] Status: {status} | Progress: {progress:.1f}% ({processed}/{total}) | Success: {success_count} | Failed: {failure_count}")
                
                if status in ['COMPLETED', 'FAILED', 'CANCELLED']:
                    print_success(f"Job finished with status: {status}")
                    return True, job_data
                
                time.sleep(3)
            else:
                print_error(f"Failed to check job status: {response.status_code}")
                return False, None
        except Exception as e:
            print_error(f"Error checking job status: {e}")
            return False, None
    
    print_error(f"Job did not complete within {max_wait} seconds")
    return False, None

def download_results(token, job_id, output_filename):
    """Download job results"""
    print_header("Step 5: Downloading Results")
    
    try:
        response = session.get(
            f"{BACKEND_URL}/api/v1/claims/csv-jobs/{job_id}/download_results/",
            headers={'Authorization': f'Bearer {token}'},
            timeout=30
        )
        
        if response.status_code == 200:
            with open(output_filename, 'wb') as f:
                f.write(response.content)
            
            print_success(f"Results downloaded: {output_filename}")
            
            # Show preview
            with open(output_filename, 'r') as f:
                lines = f.readlines()[:10]
                print_info("Results preview (first 10 lines):")
                for line in lines:
                    print_info(f"  {line.strip()}")
            
            return True
        else:
            print_error(f"Failed to download results: {response.status_code}")
            return False
    except Exception as e:
        print_error(f"Error downloading results: {e}")
        return False

def run_bulk_upload_tests():
    """Run all bulk upload tests"""
    print("\n" + "🚀 " + "="*76)
    print("🚀 ConnectMe Bulk Upload Test Suite")
    print("🚀 " + "="*76)
    print(f"🚀 Test Time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print(f"🚀 Username: {TEST_USERNAME}")
    print("🚀 " + "="*76)
    
    # Check if credentials are set
    if not TEST_PASSWORD:
        print_error("\n❌ Please provide password!")
        print_info("Usage: python3 test_bulk_upload.py <username> <password>")
        print_info("Example: python3 test_bulk_upload.py vigneshr mypassword")
        return False
    
    # Get auth token
    token = get_auth_token(TEST_USERNAME, TEST_PASSWORD)
    if not token:
        print_error("Failed to authenticate. Cannot proceed with tests.")
        return False
    
    # Define test scenarios
    end_date = date.today()
    start_date = end_date - timedelta(days=30)
    
    scenarios = [
        {
            'name': 'Scenario 1: Patient Info (No Claim Numbers)',
            'filename': 'test_patients.csv',
            'content': f"""first_name,last_name,date_of_birth,first_service_date,last_service_date
CHANTAL,KISA,05/10/1975,{start_date.strftime('%m/%d/%Y')},{end_date.strftime('%m/%d/%Y')}
JOHN,DOE,01/15/1980,{start_date.strftime('%m/%d/%Y')},{end_date.strftime('%m/%d/%Y')}
JANE,SMITH,05/20/1975,{start_date.strftime('%m/%d/%Y')},{end_date.strftime('%m/%d/%Y')}
"""
        },
        {
            'name': 'Scenario 2: With Claim Numbers',
            'filename': 'test_claims.csv',
            'content': """claim_number,first_name,last_name,date_of_birth
FH65850583,CHANTAL,KISA,05/10/1975
FH73828971,JOHN,DOE,01/15/1980
FH73828973,JANE,SMITH,05/20/1975
"""
        },
    ]
    
    # Run tests
    results = {'passed': 0, 'failed': 0, 'total': len(scenarios)}
    
    for scenario in scenarios:
        print("\n" + "="*80)
        print(f"🧪 Testing: {scenario['name']}")
        print("="*80)
        
        # Create CSV
        csv_filename = create_test_csv(scenario['filename'], scenario)
        
        # Upload CSV
        success, job_data = upload_csv(token, csv_filename)
        
        if success and job_data:
            job_id = job_data.get('id')
            
            # Monitor progress
            success, final_job_data = monitor_job_progress(token, job_id)
            
            if success and final_job_data:
                # Download results
                results_filename = f"results_{job_id}.csv"
                download_results(token, job_id, results_filename)
                
                # Check if job completed successfully
                if final_job_data.get('status') == 'COMPLETED':
                    results['passed'] += 1
                    print_success(f"✅ {scenario['name']} - PASSED")
                else:
                    results['failed'] += 1
                    print_error(f"❌ {scenario['name']} - FAILED (Status: {final_job_data.get('status')})")
            else:
                results['failed'] += 1
                print_error(f"❌ {scenario['name']} - FAILED (Monitoring failed)")
        else:
            results['failed'] += 1
            print_error(f"❌ {scenario['name']} - FAILED (Upload failed)")
        
        # Cleanup
        if os.path.exists(csv_filename):
            os.remove(csv_filename)
            print_info(f"Cleaned up: {csv_filename}")
    
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
        print("1. Check Celery worker status:")
        print("   ssh connectme@169.59.163.43 'sudo systemctl status connectme-preprod-celery'")
        print("\n2. Check Celery logs:")
        print("   ssh connectme@169.59.163.43 'sudo tail -100 /var/www/connectme-preprod-backend/logs/celery.log'")
        print("\n3. Check backend logs:")
        print("   ssh connectme@169.59.163.43 'sudo journalctl -u connectme-preprod-backend -f'")
        print("\n4. Verify token is being sent:")
        print("   - Check browser console for 'kc_access_token'")
        print("   - Verify Authorization header is present")
        print("="*80)
    
    return results['failed'] == 0

if __name__ == '__main__':
    success = run_bulk_upload_tests()
    sys.exit(0 if success else 1)
