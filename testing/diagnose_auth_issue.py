#!/usr/bin/env python3
"""
Diagnose Authentication Issues
"""
import requests
import json

BACKEND_URL = "https://pre-prod.connectme.be.totessoft.com"
KEYCLOAK_URL = "https://auth.totesoft.com/realms/connectme-preprod/protocol/openid-connect/token"

def print_header(title):
    print("\n" + "="*80)
    print(f"🔍 {title}")
    print("="*80)

def test_keycloak_token():
    """Test getting a Keycloak token"""
    print_header("Step 1: Testing Keycloak Token Generation")
    
    print("⚠️  Please enter your credentials:")
    username = input("Username: ")
    password = input("Password: ")
    
    try:
        response = requests.post(
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
            print(f"✅ Token obtained successfully")
            print(f"   Token (first 50 chars): {access_token[:50]}...")
            print(f"   Token length: {len(access_token)} characters")
            print(f"   Expires in: {token_data.get('expires_in')} seconds")
            return access_token
        else:
            print(f"❌ Failed to get token: {response.status_code}")
            print(f"   Response: {response.text}")
            return None
    except Exception as e:
        print(f"❌ Error: {e}")
        return None

def test_claims_search_with_token(token):
    """Test claims search with token"""
    print_header("Step 2: Testing Claims Search API")
    
    from datetime import date, timedelta
    end_date = date.today()
    start_date = end_date - timedelta(days=7)
    
    payload = {
        'firstServiceDate': start_date.strftime('%Y-%m-%d'),
        'lastServiceDate': end_date.strftime('%Y-%m-%d'),
        'practiceId': '1',
    }
    
    print(f"📤 Sending request to: {BACKEND_URL}/api/v1/claims/search/")
    print(f"   Payload: {json.dumps(payload, indent=2)}")
    print(f"   Token (first 30 chars): {token[:30]}...")
    
    try:
        response = requests.post(
            f"{BACKEND_URL}/api/v1/claims/search/",
            json=payload,
            headers={
                'Authorization': f'Bearer {token}',
                'Content-Type': 'application/json',
            },
            timeout=60
        )
        
        print(f"\n📥 Response:")
        print(f"   Status Code: {response.status_code}")
        print(f"   Headers: {dict(response.headers)}")
        
        if response.status_code == 200:
            print(f"✅ Search successful!")
            data = response.json()
            print(f"   Claims found: {data.get('count', 0)}")
        else:
            print(f"❌ Search failed!")
            try:
                error_data = response.json()
                print(f"   Error: {json.dumps(error_data, indent=2)}")
            except:
                print(f"   Response text: {response.text[:500]}")
        
        return response.status_code == 200
    except Exception as e:
        print(f"❌ Error: {e}")
        import traceback
        traceback.print_exc()
        return False

def test_practice_api_with_token(token):
    """Test practice API with token"""
    print_header("Step 3: Testing Practice API")
    
    print(f"📤 Sending request to: {BACKEND_URL}/api/v1/providers/practices/")
    print(f"   Token (first 30 chars): {token[:30]}...")
    
    try:
        response = requests.get(
            f"{BACKEND_URL}/api/v1/providers/practices/",
            headers={'Authorization': f'Bearer {token}'},
            timeout=10
        )
        
        print(f"\n📥 Response:")
        print(f"   Status Code: {response.status_code}")
        
        if response.status_code == 200:
            print(f"✅ Practice API works!")
            data = response.json()
            practices = data.get('results', data)
            print(f"   Practices found: {len(practices) if isinstance(practices, list) else 0}")
        else:
            print(f"❌ Practice API failed!")
            print(f"   Response: {response.text[:500]}")
        
        return response.status_code == 200
    except Exception as e:
        print(f"❌ Error: {e}")
        return False

def check_backend_logs():
    """Provide commands to check backend logs"""
    print_header("Step 4: Backend Log Commands")
    
    print("Run these commands to check backend logs:")
    print()
    print("1. Check recent backend logs:")
    print("   ssh connectme@169.59.163.43 'sudo journalctl -u connectme-preprod-backend -n 100 --no-pager'")
    print()
    print("2. Monitor backend logs in real-time:")
    print("   ssh connectme@169.59.163.43 'sudo journalctl -u connectme-preprod-backend -f'")
    print()
    print("3. Check for authentication errors:")
    print("   ssh connectme@169.59.163.43 'sudo journalctl -u connectme-preprod-backend -n 100 --no-pager | grep -i \"auth\\|403\\|401\"'")
    print()
    print("4. Check gunicorn error logs:")
    print("   ssh connectme@169.59.163.43 'sudo tail -100 /var/www/connectme-preprod-backend/logs/gunicorn-error.log'")

def main():
    print("\n" + "🔍 " + "="*76)
    print("🔍 ConnectMe Authentication Diagnostic Tool")
    print("🔍 " + "="*76)
    
    # Get token
    token = test_keycloak_token()
    
    if not token:
        print("\n❌ Cannot proceed without a valid token")
        return False
    
    # Test APIs
    practice_ok = test_practice_api_with_token(token)
    claims_ok = test_claims_search_with_token(token)
    
    # Show log commands
    check_backend_logs()
    
    # Summary
    print("\n" + "="*80)
    print("📊 DIAGNOSTIC SUMMARY")
    print("="*80)
    print(f"Token Generation: {'✅ OK' if token else '❌ FAILED'}")
    print(f"Practice API: {'✅ OK' if practice_ok else '❌ FAILED'}")
    print(f"Claims Search: {'✅ OK' if claims_ok else '❌ FAILED'}")
    print("="*80)
    
    if not claims_ok:
        print("\n🔧 TROUBLESHOOTING STEPS:")
        print("1. Check if backend is running")
        print("2. Verify Keycloak authentication is configured")
        print("3. Check backend logs for errors")
        print("4. Verify CORS settings")
        print("5. Check if practice exists and has payer mapping")
    
    return token and practice_ok and claims_ok

if __name__ == '__main__':
    import sys
    success = main()
    sys.exit(0 if success else 1)

