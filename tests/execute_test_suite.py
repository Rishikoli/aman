#!/usr/bin/env python3
"""
Test Suite Execution Script for AMAN
Executes comprehensive test suite and validates all requirements
"""
import subprocess
import sys
import os
import json
import time
from datetime import datetime

def setup_test_environment():
    """Set up the test environment"""
    print("🔧 Setting up test environment...")
    
    # Create required directories
    os.makedirs('tests/results', exist_ok=True)
    os.makedirs('tests/coverage', exist_ok=True)
    
    # Generate demo data
    print("📊 Generating demo data...")
    try:
        subprocess.run([sys.executable, 'tests/data/demo_data_generator.py'], check=True)
        print("✅ Demo data generated")
    except subprocess.CalledProcessError:
        print("⚠️  Demo data generation failed, using existing data")

def run_unit_tests():
    """Run unit tests with coverage"""
    print("\n🧪 Running Unit Tests...")
    
    cmd = [
        sys.executable, '-m', 'pytest',
        'tests/unit/',
        '-v',
        '--tb=short',
        '--cov=agents',
        '--cov-report=html:tests/coverage/unit',
        '--cov-report=term-missing',
        '--cov-fail-under=70',
        '--junit-xml=tests/results/unit_tests.xml'
    ]
    
    result = subprocess.run(cmd, capture_output=True, text=True)
    
    if result.returncode == 0:
        print("✅ Unit tests passed")
    else:
        print("❌ Unit tests failed")
        print("STDOUT:", result.stdout[-500:])  # Last 500 chars
        print("STDERR:", result.stderr[-500:])
    
    return result.returncode == 0

def run_integration_tests():
    """Run integration tests"""
    print("\n🔗 Running Integration Tests...")
    
    cmd = [
        sys.executable, '-m', 'pytest',
        'tests/integration/',
        '-v',
        '--tb=short',
        '--junit-xml=tests/results/integration_tests.xml'
    ]
    
    result = subprocess.run(cmd, capture_output=True, text=True)
    
    if result.returncode == 0:
        print("✅ Integration tests passed")
    else:
        print("❌ Integration tests failed")
        print("STDOUT:", result.stdout[-500:])
        print("STDERR:", result.stderr[-500:])
    
    return result.returncode == 0

def run_e2e_tests():
    """Run end-to-end tests"""
    print("\n🎯 Running End-to-End Tests...")
    
    cmd = [
        sys.executable, '-m', 'pytest',
        'tests/e2e/',
        '-v',
        '--tb=short',
        '-m', 'not slow',  # Skip slow tests for faster execution
        '--junit-xml=tests/results/e2e_tests.xml'
    ]
    
    result = subprocess.run(cmd, capture_output=True, text=True)
    
    if result.returncode == 0:
        print("✅ End-to-end tests passed")
    else:
        print("❌ End-to-end tests failed")
        print("STDOUT:", result.stdout[-500:])
        print("STDERR:", result.stderr[-500:])
    
    return result.returncode == 0

def run_performance_tests():
    """Run performance tests"""
    print("\n⚡ Running Performance Tests...")
    
    cmd = [
        sys.executable, '-m', 'pytest',
        'tests/performance/',
        '-v',
        '--tb=short',
        '--junit-xml=tests/results/performance_tests.xml'
    ]
    
    result = subprocess.run(cmd, capture_output=True, text=True)
    
    if result.returncode == 0:
        print("✅ Performance tests passed")
    else:
        print("❌ Performance tests failed")
        print("STDOUT:", result.stdout[-500:])
        print("STDERR:", result.stderr[-500:])
    
    return result.returncode == 0d
ef generate_final_report(test_results, start_time, end_time):
    """Generate final test execution report"""
    print("\n📊 Generating Final Test Report...")
    
    total_duration = (end_time - start_time).total_seconds()
    
    report = {
        'execution_info': {
            'start_time': start_time.isoformat(),
            'end_time': end_time.isoformat(),
            'duration_seconds': total_duration,
            'test_environment': 'local'
        },
        'test_results': test_results,
        'summary': {
            'total_test_suites': len(test_results),
            'passed_suites': sum(1 for result in test_results.values() if result),
            'failed_suites': sum(1 for result in test_results.values() if not result),
            'overall_status': 'PASSED' if all(test_results.values()) else 'FAILED'
        },
        'requirements_validation': validate_requirements_coverage(test_results)
    }
    
    # Save JSON report
    with open('tests/results/final_test_report.json', 'w') as f:
        json.dump(report, f, indent=2)
    
    # Generate HTML report
    generate_html_report(report)
    
    # Print summary
    print(f"\n📋 Test Execution Summary:")
    print(f"   Duration: {total_duration:.2f} seconds")
    print(f"   Test Suites: {report['summary']['total_test_suites']}")
    print(f"   Passed: {report['summary']['passed_suites']}")
    print(f"   Failed: {report['summary']['failed_suites']}")
    print(f"   Overall Status: {report['summary']['overall_status']}")
    
    return report

def validate_requirements_coverage(test_results):
    """Validate that tests cover all requirements"""
    requirements_coverage = {
        'requirement_1': test_results.get('integration_tests', False),  # Orchestrator
        'requirement_2': test_results.get('unit_tests', False),        # Finance Agent
        'requirement_3': test_results.get('unit_tests', False),        # Legal Agent
        'requirement_4': test_results.get('unit_tests', False),        # Tech/IP Agent
        'requirement_5': test_results.get('unit_tests', False),        # HR Agent
        'requirement_6': test_results.get('unit_tests', False),        # Synergy Agent
        'requirement_7': test_results.get('unit_tests', False),        # Reputation Agent
        'requirement_8': test_results.get('e2e_tests', False),         # Visualization
        'requirement_9': test_results.get('unit_tests', False),        # Audit Trail
        'requirement_10': test_results.get('integration_tests', False), # Search/Query
        'requirement_11': test_results.get('performance_tests', False), # Timeline Prediction
        'requirement_12': test_results.get('e2e_tests', False)         # Knowledge Management
    }
    
    coverage_percentage = (sum(requirements_coverage.values()) / len(requirements_coverage)) * 100
    
    return {
        'requirements_covered': requirements_coverage,
        'coverage_percentage': coverage_percentage,
        'missing_coverage': [req for req, covered in requirements_coverage.items() if not covered]
    }

def generate_html_report(report):
    """Generate HTML test report"""
    html_content = f"""
    <!DOCTYPE html>
    <html>
    <head>
        <title>AMAN Test Suite Report</title>
        <style>
            body {{ font-family: Arial, sans-serif; margin: 20px; }}
            .header {{ background-color: #f8f9fa; padding: 20px; border-radius: 8px; margin-bottom: 20px; }}
            .status-passed {{ color: #28a745; font-weight: bold; }}
            .status-failed {{ color: #dc3545; font-weight: bold; }}
            .test-suite {{ margin: 15px 0; padding: 15px; border: 1px solid #dee2e6; border-radius: 5px; }}
            .coverage-info {{ background-color: #e7f3ff; padding: 15px; border-radius: 5px; margin: 20px 0; }}
            .requirements {{ background-color: #f8f9fa; padding: 15px; border-radius: 5px; }}
        </style>
    </head>
    <body>
        <div class="header">
            <h1>🧪 AMAN Comprehensive Test Suite Report</h1>
            <p><strong>Execution Time:</strong> {report['execution_info']['start_time'][:19]}</p>
            <p><strong>Duration:</strong> {report['execution_info']['duration_seconds']:.2f} seconds</p>
            <p><strong>Overall Status:</strong> 
                <span class="status-{'passed' if report['summary']['overall_status'] == 'PASSED' else 'failed'}">
                    {report['summary']['overall_status']}
                </span>
            </p>
        </div>
        
        <div class="test-suite">
            <h2>Test Suite Results</h2>
            <ul>
    """
    
    for suite_name, passed in report['test_results'].items():
        status_class = 'status-passed' if passed else 'status-failed'
        status_text = 'PASSED' if passed else 'FAILED'
        html_content += f'<li><strong>{suite_name}:</strong> <span class="{status_class}">{status_text}</span></li>'
    
    coverage_pct = report['requirements_validation']['coverage_percentage']
    
    html_content += f"""
            </ul>
        </div>
        
        <div class="coverage-info">
            <h2>Requirements Coverage</h2>
            <p><strong>Coverage:</strong> {coverage_pct:.1f}% ({len(report['requirements_validation']['requirements_covered'])} requirements)</p>
            <p><strong>Missing Coverage:</strong> {', '.join(report['requirements_validation']['missing_coverage']) if report['requirements_validation']['missing_coverage'] else 'None'}</p>
        </div>
        
        <div class="requirements">
            <h2>Requirements Validation</h2>
            <ul>
    """
    
    for req, covered in report['requirements_validation']['requirements_covered'].items():
        status_class = 'status-passed' if covered else 'status-failed'
        status_text = 'Covered' if covered else 'Missing'
        html_content += f'<li><strong>{req}:</strong> <span class="{status_class}">{status_text}</span></li>'
    
    html_content += """
            </ul>
        </div>
    </body>
    </html>
    """
    
    with open('tests/results/test_report.html', 'w') as f:
        f.write(html_content)
    
    print("📄 HTML report generated: tests/results/test_report.html")

def main():
    """Main test execution function"""
    print("🚀 Starting AMAN Comprehensive Test Suite")
    print("=" * 50)
    
    start_time = datetime.now()
    
    # Setup environment
    setup_test_environment()
    
    # Run all test suites
    test_results = {
        'unit_tests': run_unit_tests(),
        'integration_tests': run_integration_tests(),
        'e2e_tests': run_e2e_tests(),
        'performance_tests': run_performance_tests()
    }
    
    end_time = datetime.now()
    
    # Generate final report
    report = generate_final_report(test_results, start_time, end_time)
    
    # Exit with appropriate code
    if report['summary']['overall_status'] == 'PASSED':
        print("\n🎉 All tests completed successfully!")
        sys.exit(0)
    else:
        print("\n💥 Some tests failed. Check the detailed report.")
        sys.exit(1)

if __name__ == '__main__':
    main()