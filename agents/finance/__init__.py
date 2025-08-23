"""
Finance Agent Module
ML-powered financial analysis capabilities for M&A due diligence
"""

from .finance_agent import FinanceAgent
from .financial_analysis_engine import FinancialAnalysisEngine
from .gemini_financial_analyzer import GeminiFinancialAnalyzer

__all__ = [
    'FinanceAgent',
    'FinancialAnalysisEngine', 
    'GeminiFinancialAnalyzer'
]

__version__ = '2.0.0'