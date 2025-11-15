#!/usr/bin/env python3
"""
Automated Test Script for Date Range + Claim Status Filter

Tests the claim search functionality with status filters across different date ranges
to verify that results are consistent and no claims are lost.

Usage:
    python test_status_filter.py --practice-id 1 --month1 2024-07 --month2 2024-08
"""

import requests
import json
import argparse
from datetime import datetime, timedelta
from collections import defaultdict
import sys

# Configuration
API_BASE_URL = "https://pre-prod.connectme.be.totessoft.com/api/v1"
KEYCLOAK_URL = "https://auth.totesoft.com/realms/connectme-preprod/protocol/openid-connect/token"


class ClaimStatusFilterTester:
    def __init__(self, access_token, practice_id):
        self.access_token = access_token
        self.practice_id = practice_id
        self.results = {}
        
    def search_claims(self, first_date, last_date, status_filter=None, test_name=""):
        """Search claims with given parameters"""
        url = f"{API_BASE_URL}/claims/search/"
        headers = {
            "Authorization": f"Bearer {self.access_token}",
            "Content-Type": "application/json"
        }
        
        payload = {
            "firstServiceDate": first_date,
            "lastServiceDate": last_date,
            "practiceId": str(self.practice_id)
        }
        
        if status_filter:
            payload["statusFilter"] = status_filter
        
        print(f"\n{'='*60}")
        print(f"Test: {test_name}")
        print(f"Date Range: {first_date} to {last_date}")
        print(f"Status Filter: {status_filter or 'None (All statuses)'}")
        print(f"{'='*60}")
        
        try:
            response = requests.post(url, headers=headers, json=payload, timeout=120)
            
            if response.status_code == 200:
                data = response.json()
                claims = data.get('claims', [])
                
                # Analyze results
                claim_numbers = [c.get('claimNumber') for c in claims]
                statuses = [c.get('status') for c in claims]
                status_counts = defaultdict(int)
                for status in statuses:
                    status_counts[status] += 1
                
                result = {
                    'success': True,
                    'count': len(claims),
                    'claim_numbers': claim_numbers,
                    'status_counts': dict(status_counts),
                    'claims': claims
                }
                
                print(f"✅ SUCCESS: {len(claims)} claims returned")
                print(f"   Claim Numbers: {', '.join(claim_numbers[:5])}{'...' if len(claim_numbers) > 5 else ''}")
                print(f"   Status Breakdown: {dict(status_counts)}")
                
                return result
            else:
                print(f"❌ FAILED: HTTP {response.status_code}")
                print(f"   Error: {response.text}")
                return {
                    'success': False,
                    'error': response.text,
                    'status_code': response.status_code
                }
                
        except Exception as e:
            print(f"❌ EXCEPTION: {str(e)}")
            return {
                'success': False,
                'error': str(e)
            }
    
    def run_test_suite(self, month1, month2, status_to_test="DENIED"):
        """Run complete test suite"""
        
        # Parse months (format: YYYY-MM)
        year1, mon1 = month1.split('-')
        year2, mon2 = month2.split('-')
        
        # Calculate date ranges
        first_date_month1 = f"{month1}-01"
        last_date_month1 = f"{month1}-30"  # Simplified, adjust for actual month end
        
        first_date_month2 = f"{month2}-01"
        last_date_month2 = f"{month2}-30"
        
        first_date_combined = first_date_month1
        last_date_combined = last_date_month2
        
        print("\n" + "="*60)
        print("CLAIM STATUS FILTER TEST SUITE")
        print("="*60)
        print(f"Practice ID: {self.practice_id}")
        print(f"Status Filter: {status_to_test}")
        print(f"Month 1: {month1}")
        print(f"Month 2: {month2}")
        print("="*60)
        
        # TC001: First month with filter
        tc001 = self.search_claims(
            first_date_month1, last_date_month1, 
            status_filter=status_to_test,
            test_name=f"TC001: {month1} with {status_to_test} filter"
        )
        self.results['TC001'] = tc001
        
        # TC002: Second month with filter
        tc002 = self.search_claims(
            first_date_month2, last_date_month2,
            status_filter=status_to_test,
            test_name=f"TC002: {month2} with {status_to_test} filter"
        )
        self.results['TC002'] = tc002
        
        # TC003: Combined months with filter
        tc003 = self.search_claims(
            first_date_combined, last_date_combined,
            status_filter=status_to_test,
            test_name=f"TC003: {month1} to {month2} with {status_to_test} filter"
        )
        self.results['TC003'] = tc003
        
        # TC004: Combined months WITHOUT filter (baseline)
        tc004 = self.search_claims(
            first_date_combined, last_date_combined,
            status_filter=None,
            test_name=f"TC004: {month1} to {month2} WITHOUT filter (baseline)"
        )
        self.results['TC004'] = tc004
        
        # Analysis
        self.analyze_results(status_to_test)
    
    def analyze_results(self, status_filter):
        """Analyze test results and identify issues"""
        
        print("\n" + "="*60)
        print("TEST RESULTS ANALYSIS")
        print("="*60)
        
        tc001 = self.results.get('TC001', {})
        tc002 = self.results.get('TC002', {})
        tc003 = self.results.get('TC003', {})
        tc004 = self.results.get('TC004', {})
        
        issues = []
        
        # Check if all tests succeeded
        if not all([tc001.get('success'), tc002.get('success'), tc003.get('success'), tc004.get('success')]):
            print("❌ CRITICAL: Some tests failed to execute")
            return
        
        count1 = tc001.get('count', 0)
        count2 = tc002.get('count', 0)
        count3 = tc003.get('count', 0)
        count4 = tc004.get('count', 0)
        
        print(f"\nClaim Counts:")
        print(f"  TC001 (Month 1 filtered): {count1}")
        print(f"  TC002 (Month 2 filtered): {count2}")
        print(f"  TC003 (Combined filtered): {count3}")
        print(f"  TC004 (Combined unfiltered): {count4}")
        
        # Critical Check: TC003 should equal TC001 + TC002
        expected_count = count1 + count2
        print(f"\n🔍 Critical Check:")
        print(f"   Expected (TC001 + TC002): {expected_count}")
        print(f"   Actual (TC003): {count3}")
        
        if count3 != expected_count:
            print(f"   ❌ MISMATCH! Missing {expected_count - count3} claims")
            issues.append(f"TC003 count ({count3}) != TC001 ({count1}) + TC002 ({count2})")
            
            # Check for duplicates
            claims1 = set(tc001.get('claim_numbers', []))
            claims2 = set(tc002.get('claim_numbers', []))
            claims3 = set(tc003.get('claim_numbers', []))
            
            print(f"\n   Claim Number Analysis:")
            print(f"   - TC001 unique claims: {len(claims1)}")
            print(f"   - TC002 unique claims: {len(claims2)}")
            print(f"   - TC003 unique claims: {len(claims3)}")
            print(f"   - Expected unique: {len(claims1.union(claims2))}")
            
            missing_from_tc003 = claims1.union(claims2) - claims3
            if missing_from_tc003:
                print(f"   ❌ Missing claims in TC003: {missing_from_tc003}")
                issues.append(f"Missing claims: {missing_from_tc003}")
            
            extra_in_tc003 = claims3 - claims1.union(claims2)
            if extra_in_tc003:
                print(f"   ⚠️  Extra claims in TC003: {extra_in_tc003}")
        else:
            print(f"   ✅ PASS: Counts match!")
        
        # Check TC004 baseline
        tc004_status_counts = tc004.get('status_counts', {})
        expected_filtered_count = tc004_status_counts.get(status_filter, 0)
        
        print(f"\n🔍 Baseline Check (TC004):")
        print(f"   Total claims (unfiltered): {count4}")
        print(f"   Status breakdown: {tc004_status_counts}")
        print(f"   Expected {status_filter} claims: {expected_filtered_count}")
        print(f"   Actual {status_filter} claims (TC003): {count3}")
        
        if expected_filtered_count != count3:
            print(f"   ❌ MISMATCH! Filter may be losing claims")
            issues.append(f"Baseline {status_filter} count ({expected_filtered_count}) != TC003 count ({count3})")
        else:
            print(f"   ✅ PASS: Filter working correctly!")
        
        # Summary
        print("\n" + "="*60)
        print("FINAL VERDICT")
        print("="*60)
        
        if not issues:
            print("✅ ALL TESTS PASSED!")
            print("   - Date range filtering works correctly")
            print("   - Status filtering works correctly")
            print("   - No claims are lost")
            return True
        else:
            print("❌ TESTS FAILED!")
            print("\nIssues Found:")
            for i, issue in enumerate(issues, 1):
                print(f"   {i}. {issue}")
            
            print("\n🔧 Recommended Actions:")
            print("   1. Check backend logs for UHC API responses")
            print("   2. Verify UHC API pagination settings")
            print("   3. Check for duplicate claim handling")
            print("   4. Review status filter implementation")
            return False


def get_access_token(username, password):
    """Get Keycloak access token"""
    print("🔐 Authenticating with Keycloak...")
    
    payload = {
        'grant_type': 'password',
        'client_id': 'connectme-frontend',
        'username': username,
        'password': password
    }
    
    try:
        response = requests.post(KEYCLOAK_URL, data=payload, timeout=10)
        if response.status_code == 200:
            token_data = response.json()
            print("✅ Authentication successful")
            return token_data.get('access_token')
        else:
            print(f"❌ Authentication failed: {response.status_code}")
            print(response.text)
            return None
    except Exception as e:
        print(f"❌ Authentication error: {str(e)}")
        return None


def main():
    parser = argparse.ArgumentParser(description='Test claim status filter across date ranges')
    parser.add_argument('--username', required=True, help='Keycloak username')
    parser.add_argument('--password', required=True, help='Keycloak password')
    parser.add_argument('--practice-id', required=True, help='Practice ID to test')
    parser.add_argument('--month1', required=True, help='First month (YYYY-MM)')
    parser.add_argument('--month2', required=True, help='Second month (YYYY-MM)')
    parser.add_argument('--status', default='DENIED', help='Status to filter (default: DENIED)')
    
    args = parser.parse_args()
    
    # Get access token
    access_token = get_access_token(args.username, args.password)
    if not access_token:
        sys.exit(1)
    
    # Run tests
    tester = ClaimStatusFilterTester(access_token, args.practice_id)
    success = tester.run_test_suite(args.month1, args.month2, args.status)
    
    # Exit with appropriate code
    sys.exit(0 if success else 1)


if __name__ == '__main__':
    main()

