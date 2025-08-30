#!/usr/bin/env python3
"""
Demo Data Generator for AMAN Testing
Creates realistic synthetic data for testing and demonstrations
"""
import json
import random
import uuid
from datetime import datetime, timedelta
from faker import Faker
import pandas as pd
import os

class DemoDataGenerator:
    def __init__(self):
        self.fake = Faker()
        self.industries = [
            'Technology', 'Healthcare', 'Financial Services', 'Manufacturing',
            'Retail', 'Energy', 'Telecommunications', 'Automotive', 'Aerospace',
            'Biotechnology', 'Real Estate', 'Media & Entertainment', 'Consumer Goods',
            'Industrial Equipment', 'Software', 'Pharmaceuticals', 'Fintech'
        ]
        self.company_sizes = ['startup', 'small', 'medium', 'large', 'enterprise']
        
        # Predefined realistic company profiles for consistent demos
        self.demo_companies = [
            {
                'name': 'TechGiant Corp',
                'ticker': 'TGNT',
                'industry': 'Technology',
                'size': 'enterprise',
                'employees': 150000,
                'revenue': 100000000000,
                'founded': 1995,
                'description': 'Leading global technology company specializing in cloud computing, AI, and enterprise software solutions.'
            },
            {
                'name': 'AI Innovations Ltd',
                'ticker': None,
                'industry': 'Artificial Intelligence',
                'size': 'medium',
                'employees': 800,
                'revenue': 150000000,
                'founded': 2018,
                'description': 'Cutting-edge AI startup focused on machine learning platforms and autonomous systems.'
            },
            {
                'name': 'HealthTech Solutions Inc',
                'ticker': 'HLTH',
                'industry': 'Healthcare',
                'size': 'large',
                'employees': 25000,
                'revenue': 5000000000,
                'founded': 2005,
                'description': 'Digital health platform providing telemedicine and health analytics solutions.'
            },
            {
                'name': 'GreenEnergy Dynamics',
                'ticker': None,
                'industry': 'Energy',
                'size': 'medium',
                'employees': 1200,
                'revenue': 300000000,
                'founded': 2015,
                'description': 'Renewable energy company specializing in solar and wind power solutions.'
            },
            {
                'name': 'FinanceFlow Corp',
                'ticker': 'FINF',
                'industry': 'Financial Services',
                'size': 'large',
                'employees': 45000,
                'revenue': 8000000000,
                'founded': 1987,
                'description': 'Global financial services provider offering banking, investment, and insurance products.'
            },
            {
                'name': 'CyberSecure Systems',
                'ticker': None,
                'industry': 'Cybersecurity',
                'size': 'small',
                'employees': 350,
                'revenue': 75000000,
                'founded': 2020,
                'description': 'Cybersecurity startup providing advanced threat detection and response solutions.'
            }
        ]
    
    def generate_company_profile(self, company_type='target', use_predefined=False):
        """Generate realistic company profile"""
        if use_predefined and self.demo_companies:
            # Use predefined company and remove from list
            company_data = self.demo_companies.pop(0)
            return {
                'id': str(uuid.uuid4()),
                'name': company_data['name'],
                'ticker_symbol': company_data['ticker'],
                'industry': company_data['industry'],
                'company_size': company_data['size'],
                'employee_count': company_data['employees'],
                'annual_revenue': company_data['revenue'],
                'founded_year': company_data['founded'],
                'headquarters_location': f"{self.fake.city()}, {self.fake.state_abbr()}",
                'market_cap': int(company_data['revenue'] * random.uniform(2, 8)) if company_data['ticker'] else None,
                'description': company_data['description'],
                'website_url': f"https://www.{company_data['name'].lower().replace(' ', '').replace('corp', '').replace('inc', '').replace('ltd', '')}.com"
            }
        
        # Generate random company
        industry = random.choice(self.industries)
        size = random.choice(self.company_sizes)
        
        # Size-based parameters
        size_params = {
            'startup': {'employees': (10, 100), 'revenue': (1e6, 50e6)},
            'small': {'employees': (100, 500), 'revenue': (50e6, 200e6)},
            'medium': {'employees': (500, 2000), 'revenue': (200e6, 1e9)},
            'large': {'employees': (2000, 10000), 'revenue': (1e9, 10e9)},
            'enterprise': {'employees': (10000, 100000), 'revenue': (10e9, 100e9)}
        }
        
        params = size_params[size]
        employees = random.randint(*params['employees'])
        revenue = random.uniform(*params['revenue'])
        
        company_name = f"{self.fake.company()} {random.choice(['Corp', 'Inc', 'Ltd', 'LLC'])}"
        
        return {
            'id': str(uuid.uuid4()),
            'name': company_name,
            'ticker_symbol': self.fake.lexify('????').upper() if size in ['large', 'enterprise'] else None,
            'industry': industry,
            'sector': self._get_sector_for_industry(industry),
            'company_size': size,
            'employee_count': employees,
            'annual_revenue': int(revenue),
            'founded_year': random.randint(1980, 2020),
            'headquarters_location': f"{self.fake.city()}, {self.fake.state_abbr()}",
            'market_cap': int(revenue * random.uniform(2, 8)) if size in ['large', 'enterprise'] else None,
            'description': self.fake.text(max_nb_chars=200),
            'website_url': f"https://www.{company_name.lower().replace(' ', '').replace('corp', '').replace('inc', '').replace('ltd', '').replace('llc', '')}.com"
        }
    
    def _get_sector_for_industry(self, industry):
        """Map industry to sector"""
        sector_mapping = {
            'Technology': 'Information Technology',
            'Healthcare': 'Healthcare',
            'Financial Services': 'Financials',
            'Manufacturing': 'Industrials',
            'Retail': 'Consumer Discretionary',
            'Energy': 'Energy',
            'Telecommunications': 'Communication Services',
            'Automotive': 'Consumer Discretionary',
            'Aerospace': 'Industrials',
            'Biotechnology': 'Healthcare',
            'Real Estate': 'Real Estate',
            'Media & Entertainment': 'Communication Services',
            'Consumer Goods': 'Consumer Staples',
            'Industrial Equipment': 'Industrials',
            'Software': 'Information Technology',
            'Pharmaceuticals': 'Healthcare',
            'Fintech': 'Financials'
        }
        return sector_mapping.get(industry, 'Miscellaneous')
    
    def generate_financial_data(self, company_profile, years=3):
        """Generate financial statements for multiple years"""
        base_revenue = company_profile['revenue']
        financial_data = []
        
        for i in range(years):
            year = 2024 - (years - 1 - i)
            
            # Add some growth/decline variation
            growth_rate = random.uniform(-0.1, 0.3)  # -10% to +30%
            revenue = base_revenue * (1 + growth_rate * i)
            
            # Calculate other financial metrics
            gross_margin = random.uniform(0.2, 0.7)
            operating_margin = random.uniform(0.05, gross_margin - 0.1)
            net_margin = random.uniform(0.02, operating_margin - 0.02)
            
            financial_data.append({
                'year': year,
                'revenue': int(revenue),
                'gross_profit': int(revenue * gross_margin),
                'operating_income': int(revenue * operating_margin),
                'net_income': int(revenue * net_margin),
                'total_assets': int(revenue * random.uniform(1.5, 3.0)),
                'total_debt': int(revenue * random.uniform(0.2, 1.0)),
                'cash': int(revenue * random.uniform(0.1, 0.5)),
                'shares_outstanding': random.randint(10000000, 1000000000)
            })
        
        return financial_data
    
    d 
   
    def generate_deal_scenario(self, deal_type='acquisition', use_predefined=False):
        """Generate complete M&A deal scenario"""
        acquirer = self.generate_company_profile('acquirer', use_predefined)
        target = self.generate_company_profile('target', use_predefined)
        
        # Ensure acquirer is larger than target
        if acquirer['annual_revenue'] < target['annual_revenue']:
            acquirer, target = target, acquirer
        
        deal_value = int(target['annual_revenue'] * random.uniform(2, 6))
        
        return {
            'id': str(uuid.uuid4()),
            'name': f"{acquirer['name']} Acquires {target['name']}",
            'description': f"Strategic acquisition of {target['name']} by {acquirer['name']} to expand market presence and capabilities in {target['industry']}.",
            'acquirer_id': acquirer['id'],
            'target_id': target['id'],
            'acquirer': acquirer,
            'target': target,
            'deal_value': deal_value,
            'currency': 'USD',
            'status': random.choice(['draft', 'active', 'completed']),
            'created_by': f"{self.fake.first_name()} {self.fake.last_name()}",
            'estimated_completion_date': (datetime.now() + timedelta(days=random.randint(90, 365))).isoformat(),
            'priority': random.randint(1, 10),
            'metadata': {
                'deal_structure': random.choice(['cash', 'stock', 'cash_and_stock']),
                'announcement_date': (datetime.now() - timedelta(days=random.randint(1, 90))).isoformat(),
                'analysis_scope': ['financial', 'legal', 'synergy', 'reputation', 'operations'],
                'expected_synergies': random.randint(50000000, 500000000),
                'regulatory_approval_required': random.choice([True, False])
            }
        }
    
    def generate_test_dataset(self, num_deals=10):
        """Generate complete test dataset"""
        dataset = {
            'deals': [],
            'companies': [],
            'financial_data': {},
            'generated_at': datetime.now().isoformat()
        }
        
        for _ in range(num_deals):
            deal = self.generate_deal_scenario()
            dataset['deals'].append(deal)
            
            # Add companies if not already present
            for company in [deal['acquirer'], deal['target']]:
                if not any(c['id'] == company['id'] for c in dataset['companies']):
                    dataset['companies'].append(company)
                    dataset['financial_data'][company['id']] = self.generate_financial_data(company)
        
        return dataset
    
    def save_dataset(self, dataset, filename='demo_dataset.json'):
        """Save dataset to file"""
        with open(f'tests/data/{filename}', 'w') as f:
            json.dump(dataset, f, indent=2)
        
        print(f"📊 Demo dataset saved to tests/data/{filename}")
        print(f"   Deals: {len(dataset['deals'])}")
        print(f"   Companies: {len(dataset['companies'])}")

def main():
    """Generate demo datasets for testing"""
    generator = DemoDataGenerator()
    
    # Generate different sized datasets
    datasets = {
        'small_dataset.json': 5,
        'medium_dataset.json': 15,
        'large_dataset.json': 50
    }
    
    for filename, num_deals in datasets.items():
        print(f"🔄 Generating {filename} with {num_deals} deals...")
        dataset = generator.generate_test_dataset(num_deals)
        generator.save_dataset(dataset, filename)
    
    print("✅ All demo datasets generated successfully!")

if __name__ == '__main__':
    main()