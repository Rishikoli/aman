#!/usr/bin/env python3
"""
Comprehensive test runner for AMAN system
Executes all test suites and generates coverage reports
"""
import subprocess
import sys
import os
import json
import time
from datetime import datetime
import argparse

class ComprehensiveTestRunner:
    def __init__(self):
        self.test_results = {}
        self.start_time = None
        self.end_time = None
    
    def run_unit_tests(self):
        """Run all unit tests"""
        print("🧪 Running Unit Tests...")
        cmd = [
            sys.executable, '-m', 'pytest', 
            'tests/unit/', 
            '-v', '--tb=short',
            '--cov=agents',
            '--cov-report=html:tests/coverage/unit',
            '--cov-report=term-missing',
            '--junit-xml=tests/results/unit_tests.xml'
        ]
        
        result = subprocess.run(cmd, capture_output=True, text=True)
        self.test_results['unit_tests'] = {
            'exit_code': result.returncode,
            'stdout': result.stdout,
            'stderr': result.stderr
        }
        
        if result.returncode == 0:
            print("✅ Unit tests passed")
        else:
            print("❌ Unit tests failed")
            print(result.stdout)
            print(result.stderr)
        
        return result.returncode == 0
    
    def run_integration_tests(self):
        """Run integration tests"""
        print("🔗 Running Integration Tests...")
        cmd = [
            sys.executable, '-m', 'pytest',
            'tests/integration/',
            '-v', '--tb=short',
            '--junit-xml=tests/results/integration_tests.xml'
        ]
        
        result = subprocess.run(cmd, capture_output=True, text=True)
        self.test_results['integration_tests'] = {
            'exit_code': result.returncode,
            'stdout': result.stdout,
            'stderr': result.stderr
        }
        
        if result.returncode == 0:
            print("✅ Integration tests passed")
        else:
            print("❌ Integration tests failed")
        
        return result.returncode == 0    

    def run_e2e_tests(self):
        """Run end-to-end tests"""
        print("🎯 Running End-to-End Tests...")
        cmd = [
            sys.executable, '-m', 'pytest',
            'tests/e2e/',
            '-v', '--tb=short',
            '-m', 'not slow',  # Skip slow tests by default
            '--junit-xml=tests/results/e2e_tests.xml'
        ]
        
        result = subprocess.run(cmd, capture_output=True, text=True)
        self.test_results['e2e_tests'] = {
            'exit_code': result.returncode,
            'stdout': result.stdout,
            'stderr': result.stderr
        }
        
        if result.returncode == 0:
            print("✅ End-to-end tests passed")
        else:
            print("❌ End-to-end tests failed")
        
        return result.returncode == 0
    
    def run_performance_tests(self):
        """Run performance tests"""
        print("⚡ Running Performance Tests...")
        cmd = [
            sys.executable, '-m', 'pytest',
            'tests/performance/',
            '-v', '--tb=short',
            '--junit-xml=tests/results/performance_tests.xml'
        ]
        
        result = subprocess.run(cmd, capture_output=True, text=True)
        self.test_results['performance_tests'] = {
            'exit_code': result.returncode,
            'stdout': result.stdout,
            'stderr': result.stderr
        }
        
        if result.returncode == 0:
            print("✅ Performance tests passed")
        else:
            print("❌ Performance tests failed")
        
        return result.returncode == 0
    
    def generate_test_report(self):
        """Generate comprehensive test report"""
        print("📊 Generating Test Report...")
        
        report = {
            'test_run_info': {
                'start_time': self.start_time.isoformat(),
                'end_time': self.end_time.isoformat(),
                'duration_seconds': (self.end_time - self.start_time).total_seconds()
            },
            'test_results': self.test_results,
            'summary': {
                'total_suites': len(self.test_results),
                'passed_suites': sum(1 for r in self.test_results.values() if r['exit_code'] == 0),
                'failed_suites': sum(1 for r in self.test_results.values() if r['exit_code'] != 0)
            }
        }
        
        # Save report
        os.makedirs('tests/results', exist_ok=True)
        with open('tests/results/comprehensive_test_report.json', 'w') as f:
            json.dump(report, f, indent=2)
        
        # Print summary
        print(f"\n📋 Test Summary:")
        print(f"   Total test suites: {report['summary']['total_suites']}")
        print(f"   Passed: {report['summary']['passed_suites']}")
        print(f"   Failed: {report['summary']['failed_suites']}")
        print(f"   Duration: {report['test_run_info']['duration_seconds']:.2f} seconds")
        
        return report['summary']['failed_suites'] == 0

def main():
    parser = argparse.ArgumentParser(description='Run comprehensive AMAN test suite')
    parser.add_argument('--unit', action='store_true', help='Run unit tests only')
    parser.add_argument('--integration', action='store_true', help='Run integration tests only')
    parser.add_argument('--e2e', action='store_true', help='Run e2e tests only')
    parser.add_argument('--performance', action='store_true', help='Run performance tests only')
    parser.add_argument('--all', action='store_true', help='Run all tests (default)')
    
    args = parser.parse_args()
    
    # Default to all tests if no specific test type specified
    if not any([args.unit, args.integration, args.e2e, args.performance]):
        args.all = True
    
    runner = ComprehensiveTestRunner()
    runner.start_time = datetime.now()
    
    print("🚀 Starting Comprehensive Test Suite for AMAN")
    print(f"   Start time: {runner.start_time}")
    
    # Create results directory
    os.makedirs('tests/results', exist_ok=True)
    
    success = True
    
    if args.all or args.unit:
        success &= runner.run_unit_tests()
    
    if args.all or args.integration:
        success &= runner.run_integration_tests()
    
    if args.all or args.e2e:
        success &= runner.run_e2e_tests()
    
    if args.all or args.performance:
        success &= runner.run_performance_tests()
    
    runner.end_time = datetime.now()
    
    # Generate final report
    report_success = runner.generate_test_report()
    
    if success and report_success:
        print("\n🎉 All tests passed successfully!")
        sys.exit(0)
    else:
        print("\n💥 Some tests failed. Check the results for details.")
        sys.exit(1)

if __name__ == '__main__':
    main()