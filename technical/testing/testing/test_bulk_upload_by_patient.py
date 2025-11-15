#!/usr/bin/env python
"""
Test bulk upload by patient information (without claim numbers)
This searches for claims by patient name, DOB, and practice
"""
import requests
import os

# Configuration
BACKEND_URL = "https://pre-prod.connectme.be.totessoft.com"

# Test credentials
USERNAME = "admin"
PASSWORD = "admin123"

print("="*80)
print("🧪 Testing Bulk Upload - Search by Patient Info")
print("="*80)
print()

# Step 1: Login to get token
print("Step 1: Logging in...")
try:
    login_response = requests.post(
        f"https://auth.totesoft.com/realms/connectme-preprod/protocol/openid-connect/token",
        data={
            'client_id': 'connectme-preprod-frontend',
            'username': USERNAME,
            'password': PASSWORD,
            'grant_type': 'password',
            'scope': 'openid profile email',
        },
        headers={'Content-Type': 'application/x-www-form-urlencoded'},
        timeout=10
    )
    
    if login_response.status_code == 200:
        token_data = login_response.json()
        access_token = token_data['access_token']
        print(f"✅ Login successful")
        print(f"   Token: {access_token[:30]}...")
    else:
        print(f"❌ Login failed: {login_response.status_code}")
        print(f"   Response: {login_response.text}")
        exit(1)
except Exception as e:
    print(f"❌ Login error: {e}")
    exit(1)

print()

# Step 2: Create test CSV file with patient info
print("Step 2: Creating test CSV file...")
csv_content = """first_name,last_name,date_of_birth,practice_id,first_service_date,last_service_date
CHANTAL,KISA,05/10/1975,1,10/01/2025,10/31/2025
JOHN,DOE,01/15/1980,1,10/01/2025,10/31/2025
JANE,SMITH,05/20/1975,1,10/01/2025,10/31/2025
ROBERT,JOHNSON,03/12/1968,1,10/01/2025,10/31/2025
MARY,WILLIAMS,08/25/1982,1,10/01/2025,10/31/2025
"""

csv_filename = "test_patients.csv"
with open(csv_filename, 'w') as f:
    f.write(csv_content)

print(f"✅ Created {csv_filename}")
print(f"   Patients: 5")
print(f"   Format: first_name, last_name, date_of_birth, practice_id, service dates")
print()

# Step 3: Upload CSV
print("Step 3: Uploading CSV file...")
try:
    with open(csv_filename, 'rb') as f:
        files = {'file': (csv_filename, f, 'text/csv')}
        data = {
            'provider': 'uhc',
            'use_batch_query': 'true',
            'start_date': '2025-10-01',  # Optional: helps with batch query
            'end_date': '2025-10-31',
        }
        
        upload_response = requests.post(
            f"{BACKEND_URL}/api/v1/claims/bulk/upload/",
            files=files,
            data=data,
            headers={'Authorization': f'Bearer {access_token}'},
            timeout=30
        )
    
    print(f"   Status Code: {upload_response.status_code}")
    
    if upload_response.status_code in [200, 201]:
        result = upload_response.json()
        print(f"✅ Upload successful")
        print(f"   Job ID: {result.get('id')}")
        print(f"   Status: {result.get('status')}")
        print(f"   Filename: {result.get('filename')}")
        print(f"   Total Rows: {result.get('total_rows')}")
        
        job_id = result.get('id')
        
        # Step 4: Check job progress
        print()
        print("Step 4: Monitoring job progress...")
        import time
        
        for i in range(20):  # Check for up to 60 seconds
            time.sleep(3)
            
            try:
                progress_response = requests.get(
                    f"{BACKEND_URL}/api/v1/claims/bulk/jobs/{job_id}/progress/",
                    headers={'Authorization': f'Bearer {access_token}'},
                    timeout=10
                )
                
                if progress_response.status_code == 200:
                    progress = progress_response.json()
                    status_val = progress.get('status')
                    processed = progress.get('processed_rows', 0)
                    total = progress.get('total_rows', 0)
                    success = progress.get('success_count', 0)
                    failed = progress.get('failure_count', 0)
                    
                    print(f"   [{i+1}] Status: {status_val} | Processed: {processed}/{total} | Success: {success} | Failed: {failed}")
                    
                    if status_val in ['COMPLETED', 'FAILED', 'CANCELLED']:
                        break
                else:
                    print(f"   ⚠️  Progress check failed: {progress_response.status_code}")
            except Exception as e:
                print(f"   ⚠️  Progress check error: {e}")
        
        # Step 5: Get results
        print()
        if status_val == 'COMPLETED':
            print("Step 5: Downloading results...")
            
            try:
                results_response = requests.get(
                    f"{BACKEND_URL}/api/v1/claims/bulk/jobs/{job_id}/download_results/",
                    headers={'Authorization': f'Bearer {access_token}'},
                    timeout=30
                )
                
                if results_response.status_code == 200:
                    results_filename = f"results_{job_id}.csv"
                    with open(results_filename, 'wb') as f:
                        f.write(results_response.content)
                    print(f"✅ Results downloaded: {results_filename}")
                    
                    # Show first few lines
                    with open(results_filename, 'r') as f:
                        lines = f.readlines()[:10]
                        print()
                        print("First 10 lines of results:")
                        for line in lines:
                            print(f"   {line.strip()}")
                else:
                    print(f"⚠️  Could not download results: {results_response.status_code}")
            except Exception as e:
                print(f"⚠️  Download error: {e}")
        elif status_val == 'FAILED':
            print("❌ Job failed")
            # Try to get error log
            try:
                job_response = requests.get(
                    f"{BACKEND_URL}/api/v1/claims/bulk/jobs/{job_id}/",
                    headers={'Authorization': f'Bearer {access_token}'},
                    timeout=10
                )
                if job_response.status_code == 200:
                    job_data = job_response.json()
                    error_log = job_data.get('error_log')
                    if error_log:
                        print(f"   Error log: {error_log[:500]}")
            except:
                pass
        
    else:
        print(f"❌ Upload failed: {upload_response.status_code}")
        print(f"   Response: {upload_response.text}")
        
except Exception as e:
    print(f"❌ Upload error: {e}")
    import traceback
    traceback.print_exc()

print()
print("="*80)
print("✅ Test Complete")
print("="*80)

# Cleanup
if os.path.exists(csv_filename):
    os.remove(csv_filename)
    print(f"🧹 Cleaned up {csv_filename}")

