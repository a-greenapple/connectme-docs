#!/usr/bin/env python3
"""
Extract patient details from the claim search export to create bulk upload CSV
"""
import csv
import json

# Read the export file
with open('claims_detailed_export_2025-10-15.csv', 'r') as f:
    reader = csv.DictReader(f)
    claims = list(reader)

print("📋 Found Claims from Manual Search:")
print("="*80)
for i, claim in enumerate(claims, 1):
    print(f"\n{i}. Claim: {claim['Claim Number']}")
    print(f"   Patient: {claim['Patient']}")
    print(f"   Service Date: {claim['Service Date']}")
    print(f"   Status: {claim['Status']}")
    print(f"   Provider: {claim['Provider']}")

print("\n" + "="*80)
print("\n⚠️  PROBLEM IDENTIFIED:")
print("The export doesn't include:")
print("   - Patient Date of Birth")
print("   - Subscriber ID (Member ID)")
print("\nThese are REQUIRED for bulk upload CSV!")
print("\n💡 Solution: We need to query each claim individually to get full patient details")
