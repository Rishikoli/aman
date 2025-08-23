#!/usr/bin/env python3
"""
ML Analysis Wrapper Script
Provides a command-line interface for the ML-powered Financial Analysis Engine
"""

import sys
import os
import json
import traceback
from datetime import datetime

# Add the agents directory to the Python path
current_dir = os.path.dirname(os.path.abspath(__file__))
backend_dir = os.path.dirname(current_dir)
project_root = os.path.dirname(backend_dir)
agents_dir = os.path.join(project_root, 'agents')
sys.path.append(agents_dir)

print(f"Python path: {sys.path}", file=sys.stderr)
print(f"Agents dir: {agents_dir}", file=sys.stderr)
print(f"Current working directory: {os.getcwd()}", file=sys.stderr)

try:
    from finance.finance_agent import FinanceAgent
except ImportError as e:
    print(f"Error importing FinanceAgent: {e}", file=sys.stderr)
    sys.exit(1)

def load_input_data(input_file):
    """Load input data from JSON file"""
    try:
        with open(input_file, 'r') as f:
            return json.load(f)
    except Exception as e:
        raise Exception(f"Failed to load input data: {str(e)}")

def save_output_data(output_file, data):
    """Save output data to JSON file"""
    try:
        with open(output_file, 'w') as f:
            json.dump(data, f, indent=2, default=str)
    except Exception as e:
        raise Exception(f"Failed to save output data: {str(e)}")

def handle_comprehensive_analysis(agent, financial_data, options):
    """Handle comprehensive financial analysis"""
    try:
        result = agent.analyze_company_financials(financial_data, options)
        return {
            'success': True,
            'data': result,
            'timestamp': datetime.now().isoformat()
        }
    except Exception as e:
        return {
            'success': False,
            'error': str(e),
            'timestamp': datetime.now().isoformat()
        }

def handle_quick_health_check(agent, financial_data):
    """Handle quick financial health check"""
    try:
        result = agent.quick_financial_health_check(financial_data)
        return {
            'success': True,
            'data': result,
            'timestamp': datetime.now().isoformat()
        }
    except Exception as e:
        return {
            'success': False,
            'error': str(e),
            'timestamp': datetime.now().isoformat()
        }

def handle_compare_companies(agent, company_data_list):
    """Handle company comparison"""
    try:
        result = agent.compare_companies(company_data_list)
        return {
            'success': True,
            'data': result,
            'timestamp': datetime.now().isoformat()
        }
    except Exception as e:
        return {
            'success': False,
            'error': str(e),
            'timestamp': datetime.now().isoformat()
        }

def handle_test_capabilities(agent):
    """Handle capability testing"""
    try:
        result = agent.test_agent_capabilities()
        return {
            'success': True,
            'data': result,
            'timestamp': datetime.now().isoformat()
        }
    except Exception as e:
        return {
            'success': False,
            'error': str(e),
            'timestamp': datetime.now().isoformat()
        }

def main():
    """Main execution function"""
    if len(sys.argv) != 3:
        print("Usage: python mlAnalysisWrapper.py <input_file> <output_file>", file=sys.stderr)
        sys.exit(1)
    
    input_file = sys.argv[1]
    output_file = sys.argv[2]
    
    try:
        # Load input data
        input_data = load_input_data(input_file)
        action = input_data.get('action')
        
        if not action:
            raise Exception("No action specified in input data")
        
        # Initialize the Finance Agent
        agent = FinanceAgent()
        
        # Handle different actions
        if action == 'comprehensive_analysis':
            financial_data = input_data.get('financial_data')
            options = input_data.get('options', {})
            
            if not financial_data:
                raise Exception("No financial data provided for comprehensive analysis")
            
            result = handle_comprehensive_analysis(agent, financial_data, options)
            
        elif action == 'quick_health_check':
            financial_data = input_data.get('financial_data')
            
            if not financial_data:
                raise Exception("No financial data provided for health check")
            
            result = handle_quick_health_check(agent, financial_data)
            
        elif action == 'compare_companies':
            company_data_list = input_data.get('company_data_list')
            
            if not company_data_list or len(company_data_list) < 2:
                raise Exception("At least 2 companies required for comparison")
            
            result = handle_compare_companies(agent, company_data_list)
            
        elif action == 'test_capabilities':
            result = handle_test_capabilities(agent)
            
        else:
            raise Exception(f"Unknown action: {action}")
        
        # Save output
        save_output_data(output_file, result)
        
        # Print success message to stdout
        print(f"ML analysis completed successfully: {action}")
        
    except Exception as e:
        # Create error response
        error_result = {
            'success': False,
            'error': str(e),
            'traceback': traceback.format_exc(),
            'timestamp': datetime.now().isoformat()
        }
        
        try:
            save_output_data(output_file, error_result)
        except:
            pass  # If we can't save the error, just exit
        
        print(f"ML analysis failed: {str(e)}", file=sys.stderr)
        sys.exit(1)

if __name__ == "__main__":
    main()