#!/bin/bash
# Quick Test Script for Date Range + Status Filter
# Usage: ./QUICK_TEST.sh <username> <password> <practice_id>

set -e

USERNAME=$1
PASSWORD=$2
PRACTICE_ID=$3

if [ -z "$USERNAME" ] || [ -z "$PASSWORD" ] || [ -z "$PRACTICE_ID" ]; then
    echo "Usage: $0 <username> <password> <practice_id>"
    echo "Example: $0 admin@example.com mypassword 1"
    exit 1
fi

echo "=========================================="
echo "Quick Test: Date Range + Status Filter"
echo "=========================================="
echo "Username: $USERNAME"
echo "Practice ID: $PRACTICE_ID"
echo ""

# Run automated test
python3 test_status_filter.py \
    --username "$USERNAME" \
    --password "$PASSWORD" \
    --practice-id "$PRACTICE_ID" \
    --month1 "2024-07" \
    --month2 "2024-08" \
    --status "DENIED"

# Check exit code
if [ $? -eq 0 ]; then
    echo ""
    echo "=========================================="
    echo "✅ ALL TESTS PASSED!"
    echo "=========================================="
    exit 0
else
    echo ""
    echo "=========================================="
    echo "❌ TESTS FAILED - Check output above"
    echo "=========================================="
    echo ""
    echo "Next steps:"
    echo "1. Check backend logs:"
    echo "   ssh connectme@169.59.163.43 'journalctl -u connectme-preprod-backend -n 200 --no-pager | grep \"Claim status breakdown\"'"
    echo ""
    echo "2. Run manual tests using MANUAL_TEST_CHECKLIST.md"
    echo ""
    echo "3. Review README.md for detailed analysis"
    exit 1
fi

