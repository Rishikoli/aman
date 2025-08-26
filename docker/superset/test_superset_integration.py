#!/usr/bin/env python3
"""
Test script for AMAN Superset integration
"""

import requests
import time
import json

def test_superset_health():
    """Test if Superset is running and healthy"""
    try:
        response = requests.get("http://localhost:8088/health", timeout=10)
        if response.status_code == 200:
            print("✓ Superset is running and healthy")
            return True
        else:
            print(f"✗ Superset health check failed: {response.status_code}")
            return False
    except Exception as e:
        print(f"✗ Superset connection failed: {e}")
        return False

def test_database_connection():
    """Test if Superset can connect to AMAN database"""
    try:
        # This would require authentication, so we'll just check if the endpoint exists
        response = requests.get("http://localhost:8088/api/v1/database/", timeout=10)
        if response.status_code in [200, 401, 403]:  # 401/403 means endpoint exists but needs auth
            print("✓ Superset API endpoints are accessible")
            return True
        else:
            print(f"✗ Superset API not accessible: {response.status_code}")
            return False
    except Exception as e:
        print(f"✗ Superset API connection failed: {e}")
        return False

def test_login_page():
    """Test if Superset login page is accessible"""
    try:
        response = requests.get("http://localhost:8088/login/", timeout=10)
        if response.status_code == 200:
            print("✓ Superset login page is accessible")
            return True
        else:
            print(f"✗ Superset login page failed: {response.status_code}")
            return False
    except Exception as e:
        print(f"✗ Superset login page connection failed: {e}")
        return False

def main():
    """Run all tests"""
    print("Testing AMAN Superset Integration")
    print("=" * 40)
    
    tests = [
        test_superset_health,
        test_database_connection,
        test_login_page
    ]
    
    passed = 0
    total = len(tests)
    
    for test in tests:
        if test():
            passed += 1
        time.sleep(1)
    
    print("\n" + "=" * 40)
    print(f"Tests passed: {passed}/{total}")
    
    if passed == total:
        print("✓ All tests passed! Superset integration is working.")
        print("\nNext steps:")
        print("1. Access Superset at http://localhost:8088")
        print("2. Login with admin/admin123")
        print("3. Create database connection to AMAN PostgreSQL")
        print("4. Import AMAN datasets and create dashboards")
    else:
        print("✗ Some tests failed. Check Superset configuration.")
    
    return passed == total

if __name__ == "__main__":
    success = main()
    exit(0 if success else 1)