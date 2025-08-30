"""
Unit tests for Legal Agent
"""
import pytest
from unittest.mock import Mock, patch, MagicMock
import sys
import os

# Add agents to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..', 'agents'))

from legal.legal_agent import LegalAgent
from legal.sec_edgar_client import SECEdgarClient
from legal.opencorporates_client import OpenCorporatesClient

class TestLegalAgent:
    
    @pytest.fixture
    def legal_agent(self, mock_env_vars):
        """Create a Legal Agent instance for testing"""
        return LegalAgent()
    
    @pytest.fixture
    def sample_legal_document(self):
        """Sample legal document text for testing"""
        return """
        MERGER AGREEMENT
        
        This Agreement is entered into between Company A and Company B.
        
        REPRESENTATIONS AND WARRANTIES
        Each party represents that it has full corporate power and authority.
        
        LITIGATION
        There are no pending or threatened legal proceedings against the Company.
        
        COMPLIANCE
        The Company is in compliance with all applicable laws and regulations.
        """
    
    @pytest.mark.unit
    def test_legal_agent_initialization(self, legal_agent):
        """Test Legal Agent initialization"""
        assert legal_agent is not None
        assert hasattr(legal_agent, 'analyze')
    
    @pytest.mark.unit
    def test_extract_legal_entities(self, legal_agent, sample_legal_document):
        """Test legal entity extraction from documents"""
        entities = legal_agent.extract_entities(sample_legal_document)
        
        assert 'companies' in entities
        assert 'legal_terms' in entities
        assert len(entities['companies']) > 0
    
    @pytest.mark.unit
    def test_compliance_analysis(self, legal_agent, sample_legal_document):
        """Test compliance gap analysis"""
        compliance_report = legal_agent.analyze_compliance(sample_legal_document)
        
        assert 'compliance_score' in compliance_report
        assert 'gaps' in compliance_report
        assert 'recommendations' in compliance_report
        assert 0 <= compliance_report['compliance_score'] <= 100
    
    @pytest.mark.unit
    def test_contract_risk_assessment(self, legal_agent, sample_legal_document):
        """Test contract risk assessment"""
        risk_assessment = legal_agent.assess_contract_risks(sample_legal_document)
        
        assert 'risk_score' in risk_assessment
        assert 'risk_factors' in risk_assessment
        assert 'severity_levels' in risk_assessment
    
    @pytest.mark.unit
    def test_litigation_analysis(self, legal_agent):
        """Test litigation history analysis"""
        company_name = "Test Corporation"
        
        with patch.object(legal_agent, 'fetch_litigation_data') as mock_fetch:
            mock_fetch.return_value = {
                'cases': [
                    {'case_id': '1', 'status': 'settled', 'amount': 1000000},
                    {'case_id': '2', 'status': 'ongoing', 'amount': 500000}
                ]
            }
            
            litigation_report = legal_agent.analyze_litigation(company_name)
            
            assert 'total_cases' in litigation_report
            assert 'ongoing_cases' in litigation_report
            assert 'financial_exposure' in litigation_report
    
    @pytest.mark.unit
    @patch('legal.legal_agent.requests.get')
    def test_sec_filing_analysis(self, mock_get, legal_agent):
        """Test SEC filing analysis"""
        # Mock SEC API response
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.json.return_value = {
            'filings': [
                {
                    'form': '10-K',
                    'date': '2023-12-31',
                    'url': 'https://example.com/filing.html'
                }
            ]
        }
        mock_get.return_value = mock_response
        
        filings = legal_agent.fetch_sec_filings('TEST')
        
        assert len(filings) > 0
        assert filings[0]['form'] == '10-K'
    
    @pytest.mark.unit
    def test_regulatory_compliance_check(self, legal_agent):
        """Test regulatory compliance checking"""
        company_data = {
            'industry': 'Financial Services',
            'locations': ['New York', 'London'],
            'business_type': 'Investment Banking'
        }
        
        compliance_check = legal_agent.check_regulatory_compliance(company_data)
        
        assert 'applicable_regulations' in compliance_check
        assert 'compliance_status' in compliance_check
        assert 'required_licenses' in compliance_check

class TestSECEdgarClient:
    
    @pytest.fixture
    def sec_client(self):
        """Create SEC Edgar client for testing"""
        return SECEdgarClient()
    
    @pytest.mark.unit
    @patch('legal.sec_edgar_client.requests.get')
    def test_fetch_company_filings(self, mock_get, sec_client):
        """Test fetching company filings from SEC"""
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.json.return_value = {
            'filings': {
                'recent': {
                    'form': ['10-K', '10-Q'],
                    'filingDate': ['2023-12-31', '2023-09-30'],
                    'accessionNumber': ['0001234567-23-000001', '0001234567-23-000002']
                }
            }
        }
        mock_get.return_value = mock_response
        
        filings = sec_client.get_company_filings('AAPL')
        
        assert len(filings) > 0
        assert 'form' in filings[0]
        assert 'filingDate' in filings[0]
    
    @pytest.mark.unit
    def test_parse_filing_content(self, sec_client):
        """Test parsing SEC filing content"""
        sample_html = """
        <html>
        <body>
        <div>Risk Factors: Market volatility may affect our business.</div>
        <div>Legal Proceedings: No material legal proceedings.</div>
        </body>
        </html>
        """
        
        parsed_content = sec_client.parse_filing_content(sample_html)
        
        assert 'risk_factors' in parsed_content
        assert 'legal_proceedings' in parsed_content

class TestOpenCorporatesClient:
    
    @pytest.fixture
    def opencorp_client(self):
        """Create OpenCorporates client for testing"""
        return OpenCorporatesClient()
    
    @pytest.mark.unit
    @patch('legal.opencorporates_client.requests.get')
    def test_search_company(self, mock_get, opencorp_client):
        """Test company search in OpenCorporates"""
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.json.return_value = {
            'results': {
                'companies': [
                    {
                        'company': {
                            'name': 'Test Corporation',
                            'jurisdiction_code': 'us_de',
                            'incorporation_date': '2010-01-01',
                            'company_type': 'Corporation'
                        }
                    }
                ]
            }
        }
        mock_get.return_value = mock_response
        
        companies = opencorp_client.search_company('Test Corporation')
        
        assert len(companies) > 0
        assert companies[0]['name'] == 'Test Corporation'
    
    @pytest.mark.unit
    def test_get_company_officers(self, opencorp_client):
        """Test fetching company officers"""
        with patch.object(opencorp_client, '_make_request') as mock_request:
            mock_request.return_value = {
                'officers': [
                    {
                        'officer': {
                            'name': 'John Doe',
                            'position': 'CEO',
                            'start_date': '2020-01-01'
                        }
                    }
                ]
            }
            
            officers = opencorp_client.get_company_officers('12345')
            
            assert len(officers) > 0
            assert officers[0]['name'] == 'John Doe'
            assert officers[0]['position'] == 'CEO'