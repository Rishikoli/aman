"""
ML-Powered Financial Analysis Engine
Provides advanced financial analysis capabilities including ratio calculations,
anomaly detection, and forecasting using pandas/NumPy and scikit-learn.
"""

import pandas as pd
import numpy as np
from sklearn.ensemble import IsolationForest
from sklearn.preprocessing import StandardScaler
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_absolute_error, mean_squared_error
import warnings
from typing import Dict, List, Tuple, Optional, Any
import logging
from datetime import datetime, timedelta
import json

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Suppress sklearn warnings
warnings.filterwarnings('ignore', category=UserWarning)

class FinancialAnalysisEngine:
    """
    Advanced financial analysis engine with ML capabilities
    """
    
    def __init__(self):
        """Initialize the financial analysis engine"""
        self.scaler = StandardScaler()
        self.anomaly_detector = IsolationForest(
            contamination=0.1,  # Expect 10% anomalies
            random_state=42,
            n_estimators=100
        )
        self.forecasting_models = {}
        
    def calculate_financial_ratios(self, financial_data: Dict) -> Dict[str, Any]:
        """
        Calculate comprehensive financial ratios from financial statements
        
        Args:
            financial_data: Dictionary containing financial statements
            
        Returns:
            Dictionary containing calculated ratios and analysis
        """
        try:
            logger.info("Calculating financial ratios...")
            
            # Convert to DataFrame for easier manipulation
            df = self._prepare_financial_dataframe(financial_data)
            
            if df.empty:
                raise ValueError("No financial data available for ratio calculations")
            
            ratios = {}
            
            # Liquidity Ratios
            ratios['liquidity'] = self._calculate_liquidity_ratios(df)
            
            # Profitability Ratios
            ratios['profitability'] = self._calculate_profitability_ratios(df)
            
            # Leverage/Debt Ratios
            ratios['leverage'] = self._calculate_leverage_ratios(df)
            
            # Efficiency Ratios
            ratios['efficiency'] = self._calculate_efficiency_ratios(df)
            
            # Market Ratios (if market data available)
            ratios['market'] = self._calculate_market_ratios(df, financial_data.get('profile', {}))
            
            # Growth Ratios
            ratios['growth'] = self._calculate_growth_ratios(df)
            
            # Add metadata
            ratios['metadata'] = {
                'calculation_date': datetime.now().isoformat(),
                'periods_analyzed': len(df),
                'latest_period': df.index[0] if not df.empty else None,
                'data_quality_score': self._assess_data_quality(df)
            }
            
            logger.info(f"Successfully calculated ratios for {len(df)} periods")
            return ratios
            
        except Exception as e:
            logger.error(f"Error calculating financial ratios: {str(e)}")
            raise
    
    def detect_financial_anomalies(self, financial_data: Dict) -> Dict[str, Any]:
        """
        Detect financial anomalies using machine learning
        
        Args:
            financial_data: Dictionary containing financial statements
            
        Returns:
            Dictionary containing anomaly detection results
        """
        try:
            logger.info("Detecting financial anomalies...")
            
            df = self._prepare_financial_dataframe(financial_data)
            
            if len(df) < 3:
                return {
                    'anomalies': [],
                    'warning': 'Insufficient data for anomaly detection (minimum 3 periods required)',
                    'data_points': len(df)
                }
            
            # Select key financial metrics for anomaly detection
            anomaly_features = [
                'revenue', 'net_income', 'total_assets', 'total_liabilities',
                'cash_and_equivalents', 'operating_cash_flow', 'free_cash_flow'
            ]
            
            # Filter available features
            available_features = [f for f in anomaly_features if f in df.columns and not df[f].isna().all()]
            
            if len(available_features) < 3:
                return {
                    'anomalies': [],
                    'warning': 'Insufficient financial metrics for anomaly detection',
                    'available_features': available_features
                }
            
            # Prepare data for anomaly detection
            feature_data = df[available_features].fillna(df[available_features].median())
            
            # Normalize the data
            normalized_data = self.scaler.fit_transform(feature_data)
            
            # Detect anomalies
            anomaly_scores = self.anomaly_detector.fit_predict(normalized_data)
            anomaly_probabilities = self.anomaly_detector.score_samples(normalized_data)
            
            # Identify anomalous periods
            anomalies = []
            for i, (period, score, prob) in enumerate(zip(df.index, anomaly_scores, anomaly_probabilities)):
                if score == -1:  # Anomaly detected
                    anomaly_details = self._analyze_anomaly(df.loc[period], available_features, prob)
                    anomalies.append({
                        'period': period,
                        'anomaly_score': float(prob),
                        'severity': self._classify_anomaly_severity(prob),
                        'affected_metrics': anomaly_details['affected_metrics'],
                        'description': anomaly_details['description'],
                        'potential_causes': anomaly_details['potential_causes']
                    })
            
            # Sort by severity (most severe first)
            anomalies.sort(key=lambda x: x['anomaly_score'])
            
            result = {
                'anomalies': anomalies,
                'total_anomalies': len(anomalies),
                'anomaly_rate': len(anomalies) / len(df),
                'features_analyzed': available_features,
                'periods_analyzed': len(df),
                'metadata': {
                    'detection_date': datetime.now().isoformat(),
                    'model_type': 'Isolation Forest',
                    'contamination_rate': 0.1
                }
            }
            
            logger.info(f"Detected {len(anomalies)} anomalies in {len(df)} periods")
            return result
            
        except Exception as e:
            logger.error(f"Error detecting financial anomalies: {str(e)}")
            raise
    
    def create_financial_forecasts(self, financial_data: Dict, forecast_years: int = 3) -> Dict[str, Any]:
        """
        Create 3-year financial forecasts with confidence intervals
        
        Args:
            financial_data: Dictionary containing financial statements
            forecast_years: Number of years to forecast (default: 3)
            
        Returns:
            Dictionary containing forecasts and confidence intervals
        """
        try:
            logger.info(f"Creating {forecast_years}-year financial forecasts...")
            
            df = self._prepare_financial_dataframe(financial_data)
            
            if len(df) < 3:
                return {
                    'forecasts': {},
                    'warning': 'Insufficient historical data for forecasting (minimum 3 periods required)',
                    'data_points': len(df)
                }
            
            # Key metrics to forecast
            forecast_metrics = [
                'revenue', 'net_income', 'total_assets', 'total_liabilities',
                'operating_cash_flow', 'free_cash_flow'
            ]
            
            forecasts = {}
            
            for metric in forecast_metrics:
                if metric in df.columns and not df[metric].isna().all():
                    try:
                        forecast_result = self._forecast_metric(df, metric, forecast_years)
                        forecasts[metric] = forecast_result
                    except Exception as e:
                        logger.warning(f"Failed to forecast {metric}: {str(e)}")
                        forecasts[metric] = {
                            'error': f"Forecasting failed: {str(e)}",
                            'values': [],
                            'confidence_intervals': []
                        }
            
            # Calculate derived forecasts
            if 'revenue' in forecasts and 'net_income' in forecasts:
                forecasts['net_margin_forecast'] = self._calculate_margin_forecast(
                    forecasts['revenue'], forecasts['net_income']
                )
            
            # Add summary statistics
            summary = self._generate_forecast_summary(forecasts, df)
            
            result = {
                'forecasts': forecasts,
                'summary': summary,
                'metadata': {
                    'forecast_date': datetime.now().isoformat(),
                    'forecast_years': forecast_years,
                    'historical_periods': len(df),
                    'forecasted_metrics': len([f for f in forecasts if 'error' not in forecasts[f]])
                }
            }
            
            logger.info(f"Successfully created forecasts for {len(forecasts)} metrics")
            return result
            
        except Exception as e:
            logger.error(f"Error creating financial forecasts: {str(e)}")
            raise
    
    def _prepare_financial_dataframe(self, financial_data: Dict) -> pd.DataFrame:
        """
        Convert financial data to a standardized DataFrame
        
        Args:
            financial_data: Raw financial data dictionary
            
        Returns:
            Standardized pandas DataFrame
        """
        try:
            statements = financial_data.get('statements', {})
            
            # Combine all statement types
            all_data = []
            
            # Process income statements
            income_statements = statements.get('incomeStatement', [])
            for stmt in income_statements:
                period_data = {
                    'period': stmt.get('date', stmt.get('calendarYear')),
                    'revenue': self._safe_float(stmt.get('revenue')),
                    'net_income': self._safe_float(stmt.get('netIncome')),
                    'gross_profit': self._safe_float(stmt.get('grossProfit')),
                    'operating_income': self._safe_float(stmt.get('operatingIncome')),
                    'ebitda': self._safe_float(stmt.get('ebitda')),
                }
                all_data.append(period_data)
            
            # Process balance sheets
            balance_sheets = statements.get('balanceSheet', [])
            for i, stmt in enumerate(balance_sheets):
                if i < len(all_data):
                    all_data[i].update({
                        'total_assets': self._safe_float(stmt.get('totalAssets')),
                        'total_liabilities': self._safe_float(stmt.get('totalLiabilities')),
                        'shareholders_equity': self._safe_float(stmt.get('totalStockholdersEquity')),
                        'cash_and_equivalents': self._safe_float(stmt.get('cashAndCashEquivalents')),
                        'total_debt': self._safe_float(stmt.get('totalDebt')),
                        'current_assets': self._safe_float(stmt.get('totalCurrentAssets')),
                        'current_liabilities': self._safe_float(stmt.get('totalCurrentLiabilities')),
                    })
            
            # Process cash flow statements
            cash_flows = statements.get('cashFlow', [])
            for i, stmt in enumerate(cash_flows):
                if i < len(all_data):
                    all_data[i].update({
                        'operating_cash_flow': self._safe_float(stmt.get('operatingCashFlow')),
                        'free_cash_flow': self._safe_float(stmt.get('freeCashFlow')),
                        'capital_expenditures': self._safe_float(stmt.get('capitalExpenditure')),
                    })
            
            # Create DataFrame
            if not all_data:
                return pd.DataFrame()
            
            df = pd.DataFrame(all_data)
            
            # Set period as index and sort by most recent first
            if 'period' in df.columns:
                df['period'] = pd.to_datetime(df['period'], errors='coerce')
                df = df.set_index('period').sort_index(ascending=False)
            
            return df
            
        except Exception as e:
            logger.error(f"Error preparing financial dataframe: {str(e)}")
            return pd.DataFrame()
    
    def _safe_float(self, value) -> Optional[float]:
        """Safely convert value to float"""
        if value is None or value == '':
            return None
        try:
            return float(value)
        except (ValueError, TypeError):
            return None
    
    def _calculate_liquidity_ratios(self, df: pd.DataFrame) -> Dict[str, List[float]]:
        """Calculate liquidity ratios"""
        ratios = {}
        
        # Current Ratio
        if 'current_assets' in df.columns and 'current_liabilities' in df.columns:
            ratios['current_ratio'] = (df['current_assets'] / df['current_liabilities']).fillna(0).tolist()
        
        # Quick Ratio (assuming 75% of current assets are liquid)
        if 'current_assets' in df.columns and 'current_liabilities' in df.columns:
            ratios['quick_ratio'] = ((df['current_assets'] * 0.75) / df['current_liabilities']).fillna(0).tolist()
        
        # Cash Ratio
        if 'cash_and_equivalents' in df.columns and 'current_liabilities' in df.columns:
            ratios['cash_ratio'] = (df['cash_and_equivalents'] / df['current_liabilities']).fillna(0).tolist()
        
        return ratios
    
    def _calculate_profitability_ratios(self, df: pd.DataFrame) -> Dict[str, List[float]]:
        """Calculate profitability ratios"""
        ratios = {}
        
        # Gross Margin
        if 'gross_profit' in df.columns and 'revenue' in df.columns:
            ratios['gross_margin'] = (df['gross_profit'] / df['revenue'] * 100).fillna(0).tolist()
        
        # Net Margin
        if 'net_income' in df.columns and 'revenue' in df.columns:
            ratios['net_margin'] = (df['net_income'] / df['revenue'] * 100).fillna(0).tolist()
        
        # Operating Margin
        if 'operating_income' in df.columns and 'revenue' in df.columns:
            ratios['operating_margin'] = (df['operating_income'] / df['revenue'] * 100).fillna(0).tolist()
        
        # Return on Assets (ROA)
        if 'net_income' in df.columns and 'total_assets' in df.columns:
            ratios['roa'] = (df['net_income'] / df['total_assets'] * 100).fillna(0).tolist()
        
        # Return on Equity (ROE)
        if 'net_income' in df.columns and 'shareholders_equity' in df.columns:
            ratios['roe'] = (df['net_income'] / df['shareholders_equity'] * 100).fillna(0).tolist()
        
        return ratios
    
    def _calculate_leverage_ratios(self, df: pd.DataFrame) -> Dict[str, List[float]]:
        """Calculate leverage/debt ratios"""
        ratios = {}
        
        # Debt-to-Equity Ratio
        if 'total_debt' in df.columns and 'shareholders_equity' in df.columns:
            ratios['debt_to_equity'] = (df['total_debt'] / df['shareholders_equity']).fillna(0).tolist()
        
        # Debt-to-Assets Ratio
        if 'total_debt' in df.columns and 'total_assets' in df.columns:
            ratios['debt_to_assets'] = (df['total_debt'] / df['total_assets']).fillna(0).tolist()
        
        # Equity Ratio
        if 'shareholders_equity' in df.columns and 'total_assets' in df.columns:
            ratios['equity_ratio'] = (df['shareholders_equity'] / df['total_assets']).fillna(0).tolist()
        
        return ratios
    
    def _calculate_efficiency_ratios(self, df: pd.DataFrame) -> Dict[str, List[float]]:
        """Calculate efficiency ratios"""
        ratios = {}
        
        # Asset Turnover
        if 'revenue' in df.columns and 'total_assets' in df.columns:
            ratios['asset_turnover'] = (df['revenue'] / df['total_assets']).fillna(0).tolist()
        
        # Free Cash Flow Margin
        if 'free_cash_flow' in df.columns and 'revenue' in df.columns:
            ratios['fcf_margin'] = (df['free_cash_flow'] / df['revenue'] * 100).fillna(0).tolist()
        
        return ratios
    
    def _calculate_market_ratios(self, df: pd.DataFrame, profile: Dict) -> Dict[str, Any]:
        """Calculate market ratios (if market data available)"""
        ratios = {}
        
        market_cap = profile.get('marketCap')
        if market_cap and 'net_income' in df.columns:
            # P/E Ratio (using most recent net income)
            recent_net_income = df['net_income'].iloc[0] if not df.empty else 0
            if recent_net_income > 0:
                ratios['pe_ratio'] = market_cap / (recent_net_income * 1000000)  # Convert to millions
        
        return ratios
    
    def _calculate_growth_ratios(self, df: pd.DataFrame) -> Dict[str, List[float]]:
        """Calculate growth ratios"""
        ratios = {}
        
        if len(df) < 2:
            return ratios
        
        # Revenue Growth
        if 'revenue' in df.columns:
            revenue_growth = df['revenue'].pct_change(periods=-1) * 100  # Negative because data is sorted desc
            ratios['revenue_growth'] = revenue_growth.fillna(0).tolist()
        
        # Net Income Growth
        if 'net_income' in df.columns:
            ni_growth = df['net_income'].pct_change(periods=-1) * 100
            ratios['net_income_growth'] = ni_growth.fillna(0).tolist()
        
        # Asset Growth
        if 'total_assets' in df.columns:
            asset_growth = df['total_assets'].pct_change(periods=-1) * 100
            ratios['asset_growth'] = asset_growth.fillna(0).tolist()
        
        return ratios
    
    def _assess_data_quality(self, df: pd.DataFrame) -> float:
        """Assess the quality of financial data"""
        if df.empty:
            return 0.0
        
        # Calculate completeness score
        total_cells = df.size
        non_null_cells = df.count().sum()
        completeness = non_null_cells / total_cells if total_cells > 0 else 0
        
        # Calculate consistency score (basic check for reasonable values)
        consistency_score = 1.0
        
        # Check for negative values where they shouldn't be
        if 'revenue' in df.columns:
            negative_revenue = (df['revenue'] < 0).sum()
            consistency_score -= (negative_revenue / len(df)) * 0.2
        
        if 'total_assets' in df.columns:
            negative_assets = (df['total_assets'] < 0).sum()
            consistency_score -= (negative_assets / len(df)) * 0.3
        
        # Overall quality score
        quality_score = (completeness * 0.7 + max(0, consistency_score) * 0.3)
        return round(quality_score, 2)
    
    def _analyze_anomaly(self, period_data: pd.Series, features: List[str], anomaly_score: float) -> Dict[str, Any]:
        """Analyze a specific anomaly to provide insights"""
        affected_metrics = []
        
        # Find metrics that are significantly different from median
        for feature in features:
            value = period_data.get(feature, 0)
            if abs(value) > 1e9:  # Very large values
                affected_metrics.append(f"{feature}: unusually large value ({value:,.0f})")
            elif value < 0 and feature in ['revenue', 'total_assets']:  # Negative values where positive expected
                affected_metrics.append(f"{feature}: unexpected negative value ({value:,.0f})")
        
        # Generate description
        severity = self._classify_anomaly_severity(anomaly_score)
        description = f"{severity} anomaly detected in financial metrics"
        
        # Suggest potential causes
        potential_causes = [
            "Accounting restatements or corrections",
            "Merger, acquisition, or divestiture activity",
            "One-time charges or extraordinary items",
            "Data entry errors or reporting inconsistencies",
            "Significant business model changes"
        ]
        
        return {
            'affected_metrics': affected_metrics,
            'description': description,
            'potential_causes': potential_causes
        }
    
    def _classify_anomaly_severity(self, anomaly_score: float) -> str:
        """Classify anomaly severity based on score"""
        if anomaly_score < -0.5:
            return "Critical"
        elif anomaly_score < -0.3:
            return "High"
        elif anomaly_score < -0.1:
            return "Medium"
        else:
            return "Low"
    
    def _forecast_metric(self, df: pd.DataFrame, metric: str, forecast_years: int) -> Dict[str, Any]:
        """Forecast a specific financial metric"""
        # Get historical data
        historical_data = df[metric].dropna()
        
        if len(historical_data) < 3:
            raise ValueError(f"Insufficient data for {metric} forecasting")
        
        # Prepare time series data
        X = np.arange(len(historical_data)).reshape(-1, 1)
        y = historical_data.values
        
        # Fit linear regression model
        model = LinearRegression()
        model.fit(X, y)
        
        # Generate forecasts
        future_X = np.arange(len(historical_data), len(historical_data) + forecast_years).reshape(-1, 1)
        forecasts = model.predict(future_X)
        
        # Calculate prediction intervals (simple approach using historical volatility)
        residuals = y - model.predict(X)
        std_error = np.std(residuals)
        
        # 95% confidence intervals
        confidence_intervals = []
        for i, forecast in enumerate(forecasts):
            # Increase uncertainty for longer forecasts
            uncertainty_factor = 1 + (i * 0.2)
            margin = 1.96 * std_error * uncertainty_factor
            confidence_intervals.append({
                'lower': forecast - margin,
                'upper': forecast + margin
            })
        
        # Calculate model performance metrics
        train_predictions = model.predict(X)
        mae = mean_absolute_error(y, train_predictions)
        rmse = np.sqrt(mean_squared_error(y, train_predictions))
        
        return {
            'values': forecasts.tolist(),
            'confidence_intervals': confidence_intervals,
            'model_performance': {
                'mae': mae,
                'rmse': rmse,
                'r_squared': model.score(X, y)
            },
            'trend': 'increasing' if model.coef_[0] > 0 else 'decreasing',
            'annual_growth_rate': (model.coef_[0] / np.mean(y)) * 100 if np.mean(y) != 0 else 0
        }
    
    def _calculate_margin_forecast(self, revenue_forecast: Dict, income_forecast: Dict) -> Dict[str, Any]:
        """Calculate forecasted profit margins"""
        if not revenue_forecast.get('values') or not income_forecast.get('values'):
            return {'error': 'Missing revenue or income forecasts'}
        
        margins = []
        for rev, inc in zip(revenue_forecast['values'], income_forecast['values']):
            if rev != 0:
                margins.append((inc / rev) * 100)
            else:
                margins.append(0)
        
        return {
            'values': margins,
            'description': 'Forecasted net profit margins (%)'
        }
    
    def _generate_forecast_summary(self, forecasts: Dict, historical_df: pd.DataFrame) -> Dict[str, Any]:
        """Generate summary statistics for forecasts"""
        summary = {
            'total_metrics_forecasted': len([f for f in forecasts if 'error' not in forecasts[f]]),
            'forecast_reliability': 'Medium',  # Default
            'key_insights': []
        }
        
        # Analyze revenue forecast if available
        if 'revenue' in forecasts and 'values' in forecasts['revenue']:
            revenue_values = forecasts['revenue']['values']
            if len(revenue_values) > 0:
                avg_growth = forecasts['revenue'].get('annual_growth_rate', 0)
                if avg_growth > 10:
                    summary['key_insights'].append("Strong revenue growth projected")
                elif avg_growth < -5:
                    summary['key_insights'].append("Revenue decline projected")
                else:
                    summary['key_insights'].append("Stable revenue growth projected")
        
        # Analyze profitability trends
        if 'net_income' in forecasts and 'values' in forecasts['net_income']:
            ni_growth = forecasts['net_income'].get('annual_growth_rate', 0)
            if ni_growth > 15:
                summary['key_insights'].append("Strong profitability improvement expected")
            elif ni_growth < -10:
                summary['key_insights'].append("Profitability challenges projected")
        
        return summary