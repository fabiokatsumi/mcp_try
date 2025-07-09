#!/bin/bash

# Dokploy MCP Server Health Check Script
# Use this script to verify your deployment is working correctly

set -e

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m'

# Configuration - Update these values
SERVER_URL="https://mcp.yourdomain.com"
API_KEY="your-api-key-here"
TIMEOUT=30

# Function to print colored output
print_status() { echo -e "${BLUE}[INFO]${NC} $1"; }
print_success() { echo -e "${GREEN}[PASS]${NC} $1"; }
print_warning() { echo -e "${YELLOW}[WARN]${NC} $1"; }
print_error() { echo -e "${RED}[FAIL]${NC} $1"; }

# Function to test endpoint
test_endpoint() {
    local url="$1"
    local expected_status="$2"
    local description="$3"
    local headers="$4"
    
    print_status "Testing: $description"
    
    if [ -n "$headers" ]; then
        response=$(curl -s -w "%{http_code}" -m $TIMEOUT -H "$headers" "$url" 2>/dev/null || echo "000")
    else
        response=$(curl -s -w "%{http_code}" -m $TIMEOUT "$url" 2>/dev/null || echo "000")
    fi
    
    status_code="${response: -3}"
    response_body="${response%???}"
    
    if [ "$status_code" = "$expected_status" ]; then
        print_success "$description (HTTP $status_code)"
        return 0
    else
        print_error "$description (Expected: $expected_status, Got: $status_code)"
        if [ "$status_code" = "000" ]; then
            print_error "Connection failed or timeout"
        elif [ -n "$response_body" ]; then
            echo "Response: $response_body" | head -c 200
            echo
        fi
        return 1
    fi
}

# Main health check function
main() {
    echo "========================================"
    echo "🏥 MCP Server Health Check"
    echo "========================================"
    echo "Server URL: $SERVER_URL"
    echo "Timeout: ${TIMEOUT}s"
    echo "========================================"
    
    local failures=0
    
    # Test 1: Health endpoint (no auth required)
    test_endpoint "$SERVER_URL/health" "200" "Health Check Endpoint" || ((failures++))
    
    # Test 2: API without authentication (should fail)
    test_endpoint "$SERVER_URL/api/tools" "401" "API Endpoint (No Auth)" || ((failures++))
    
    # Test 3: API with authentication (should succeed)
    test_endpoint "$SERVER_URL/api/tools" "200" "API Endpoint (With Auth)" "Authorization: Bearer $API_KEY" || ((failures++))
    
    # Test 4: Invalid API key (should fail)
    test_endpoint "$SERVER_URL/api/tools" "401" "API Endpoint (Invalid Auth)" "Authorization: Bearer invalid-key" || ((failures++))
    
    # Test 5: Rate limiting test
    print_status "Testing rate limiting..."
    local rate_limit_hits=0
    for i in {1..20}; do
        status=$(curl -s -w "%{http_code}" -m 5 -H "Authorization: Bearer $API_KEY" "$SERVER_URL/api/tools" 2>/dev/null | tail -c 3)
        if [ "$status" = "429" ]; then
            ((rate_limit_hits++))
            break
        fi
        sleep 0.1
    done
    
    if [ $rate_limit_hits -gt 0 ]; then
        print_success "Rate Limiting (Triggered after multiple requests)"
    else
        print_warning "Rate Limiting (Not triggered - may need tuning)"
    fi
    
    # Test 6: SSL Certificate
    print_status "Testing SSL certificate..."
    if curl -s --max-time $TIMEOUT "$SERVER_URL/health" > /dev/null 2>&1; then
        cert_info=$(curl -s --max-time $TIMEOUT -I "$SERVER_URL/health" 2>&1 | grep -i "subject\|issuer\|expire" || echo "")
        if [ -n "$cert_info" ]; then
            print_success "SSL Certificate (Valid)"
        else
            print_warning "SSL Certificate (Could not verify details)"
        fi
    else
        print_error "SSL Certificate (Connection failed)"
        ((failures++))
    fi
    
    # Test 7: Response time
    print_status "Testing response time..."
    response_time=$(curl -w "%{time_total}" -s -o /dev/null -m $TIMEOUT "$SERVER_URL/health" 2>/dev/null || echo "timeout")
    
    if [ "$response_time" != "timeout" ]; then
        response_ms=$(echo "$response_time * 1000" | bc -l 2>/dev/null | cut -d. -f1)
        if [ "$response_ms" -lt 1000 ]; then
            print_success "Response Time (${response_ms}ms)"
        elif [ "$response_ms" -lt 3000 ]; then
            print_warning "Response Time (${response_ms}ms - Consider optimization)"
        else
            print_error "Response Time (${response_ms}ms - Too slow)"
            ((failures++))
        fi
    else
        print_error "Response Time (Timeout after ${TIMEOUT}s)"
        ((failures++))
    fi
    
    # Summary
    echo "========================================"
    if [ $failures -eq 0 ]; then
        print_success "🎉 All health checks passed!"
        echo "Your MCP server is running correctly."
    else
        print_error "❌ $failures health check(s) failed."
        echo "Please review the issues above and check your deployment."
        exit 1
    fi
    echo "========================================"
}

# Check if required tools are installed
check_dependencies() {
    for cmd in curl bc; do
        if ! command -v $cmd >/dev/null 2>&1; then
            print_error "Required command '$cmd' is not installed."
            echo "Please install it and try again."
            exit 1
        fi
    done
}

# Usage information
usage() {
    echo "Usage: $0 [OPTIONS]"
    echo ""
    echo "Options:"
    echo "  -u, --url URL      Server URL (default: $SERVER_URL)"
    echo "  -k, --key KEY      API key for authentication"
    echo "  -t, --timeout SEC  Request timeout in seconds (default: $TIMEOUT)"
    echo "  -h, --help         Show this help message"
    echo ""
    echo "Example:"
    echo "  $0 -u https://mcp.example.com -k your-api-key"
}

# Parse command line arguments
while [[ $# -gt 0 ]]; do
    case $1 in
        -u|--url)
            SERVER_URL="$2"
            shift 2
            ;;
        -k|--key)
            API_KEY="$2"
            shift 2
            ;;
        -t|--timeout)
            TIMEOUT="$2"
            shift 2
            ;;
        -h|--help)
            usage
            exit 0
            ;;
        *)
            echo "Unknown option: $1"
            usage
            exit 1
            ;;
    esac
done

# Validate configuration
if [ -z "$SERVER_URL" ]; then
    print_error "Server URL is required. Use -u option or update the script."
    exit 1
fi

if [ -z "$API_KEY" ] || [ "$API_KEY" = "your-api-key-here" ]; then
    print_error "Valid API key is required. Use -k option or update the script."
    exit 1
fi

# Run health checks
check_dependencies
main
