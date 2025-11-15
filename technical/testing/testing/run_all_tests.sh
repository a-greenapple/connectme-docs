#!/bin/bash
#
# Master Test Runner for ConnectMe Pre-Prod
# Runs all test scripts and generates a summary report
#
# Usage:
#   ./run_all_tests.sh <username> <password>
#   ./run_all_tests.sh vigneshr mypassword
#

# Check if credentials provided
if [ $# -lt 2 ]; then
    echo "❌ Error: Username and password required"
    echo ""
    echo "Usage: ./run_all_tests.sh <username> <password>"
    echo "Example: ./run_all_tests.sh vigneshr mypassword"
    exit 1
fi

USERNAME=$1
PASSWORD=$2

echo "================================================================================"
echo "🚀 ConnectMe Pre-Prod - Master Test Suite"
echo "================================================================================"
echo "Test Time: $(date '+%Y-%m-%d %H:%M:%S')"
echo "Username: $USERNAME"
echo "================================================================================"
echo ""

# Colors
GREEN='\033[0;32m'
RED='\033[0;31m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Counters
TOTAL_TESTS=0
PASSED_TESTS=0
FAILED_TESTS=0

# Function to run a test
run_test() {
    local test_name=$1
    local test_script=$2
    
    echo ""
    echo "================================================================================"
    echo "Running: $test_name"
    echo "================================================================================"
    
    TOTAL_TESTS=$((TOTAL_TESTS + 1))
    
    if python3 "$test_script"; then
        echo -e "${GREEN}✅ $test_name - PASSED${NC}"
        PASSED_TESTS=$((PASSED_TESTS + 1))
        return 0
    else
        echo -e "${RED}❌ $test_name - FAILED${NC}"
        FAILED_TESTS=$((FAILED_TESTS + 1))
        return 1
    fi
}

# Change to testing directory
cd "$(dirname "$0")"

# Run tests with credentials
run_test "Practice API Tests" "test_practice_api.py $USERNAME $PASSWORD"
run_test "Claims Search Tests" "test_claims_search.py $USERNAME $PASSWORD"
run_test "Bulk Upload Tests" "test_bulk_upload.py $USERNAME $PASSWORD"

# Print summary
echo ""
echo "================================================================================"
echo "📊 FINAL TEST SUMMARY"
echo "================================================================================"
echo "Total Test Suites: $TOTAL_TESTS"
echo -e "${GREEN}✅ Passed: $PASSED_TESTS${NC}"
echo -e "${RED}❌ Failed: $FAILED_TESTS${NC}"

if [ $FAILED_TESTS -eq 0 ]; then
    echo -e "${GREEN}🎉 All tests passed!${NC}"
    SUCCESS_RATE=100
else
    SUCCESS_RATE=$((PASSED_TESTS * 100 / TOTAL_TESTS))
    echo -e "${YELLOW}⚠️  Some tests failed${NC}"
fi

echo "Success Rate: ${SUCCESS_RATE}%"
echo "================================================================================"

# Exit with appropriate code
if [ $FAILED_TESTS -eq 0 ]; then
    exit 0
else
    exit 1
fi
