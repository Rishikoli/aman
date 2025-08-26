#!/usr/bin/env python3
"""
AMAN Superset Dashboard Setup Script
Automatically configures Superset with AMAN-specific datasets and dashboards
"""

import os
import json
import requests
import time
from typing import Dict, List, Any

class SupersetSetup:
    def __init__(self, base_url: str = "http://localhost:8088"):
        self.base_url = base_url
        self.session = requests.Session()
        self.csrf_token = None
        self.access_token = None
        
    def login(self, username: str = "admin", password: str = "admin123") -> bool:
        """Login to Superset and get authentication tokens"""
        try:
            # Get CSRF token
            response = self.session.get(f"{self.base_url}/login/")
            if response.status_code != 200:
                print(f"Failed to get login page: {response.status_code}")
                return False
                
            # Login
            login_data = {
                "username": username,
                "password": password
            }
            
            response = self.session.post(
                f"{self.base_url}/api/v1/security/login",
                json=login_data
            )
            
            if response.status_code == 200:
                result = response.json()
                self.access_token = result.get("access_token")
                self.session.headers.update({
                    "Authorization": f"Bearer {self.access_token}"
                })
                print("Successfully logged in to Superset")
                return True
            else:
                print(f"Login failed: {response.status_code} - {response.text}")
                return False
                
        except Exception as e:
            print(f"Login error: {e}")
            return False
    
    def get_csrf_token(self) -> str:
        """Get CSRF token for form submissions"""
        try:
            response = self.session.get(f"{self.base_url}/api/v1/security/csrf_token/")
            if response.status_code == 200:
                return response.json()["result"]
            return None
        except Exception as e:
            print(f"CSRF token error: {e}")
            return None
    
    def create_database_connection(self) -> bool:
        """Create AMAN PostgreSQL database connection"""
        try:
            csrf_token = self.get_csrf_token()
            if not csrf_token:
                print("Failed to get CSRF token")
                return False
                
            database_config = {
                "database_name": "AMAN PostgreSQL",
                "sqlalchemy_uri": "postgresql://aman_user:aman_password@postgres:5432/aman_db",
                "expose_in_sqllab": True,
                "allow_ctas": True,
                "allow_cvas": True,
                "allow_dml": False,
                "force_ctas_schema": None,
                "cache_timeout": 0,
                "extra": json.dumps({
                    "metadata_params": {},
                    "engine_params": {
                        "pool_size": 10,
                        "max_overflow": 20
                    }
                })
            }
            
            headers = {
                "X-CSRFToken": csrf_token,
                "Content-Type": "application/json"
            }
            
            response = self.session.post(
                f"{self.base_url}/api/v1/database/",
                json=database_config,
                headers=headers
            )
            
            if response.status_code in [200, 201]:
                print("Successfully created AMAN database connection")
                return True
            else:
                print(f"Failed to create database connection: {response.status_code} - {response.text}")
                return False
                
        except Exception as e:
            print(f"Database connection error: {e}")
            return False
    
    def create_datasets(self) -> List[int]:
        """Create datasets for AMAN tables and views"""
        datasets = [
            {"table_name": "deals_overview", "schema": "public"},
            {"table_name": "agent_performance", "schema": "public"},
            {"table_name": "risk_assessment_summary", "schema": "public"},
            {"table_name": "financial_metrics_comparison", "schema": "public"},
            {"table_name": "deal_timeline_analysis", "schema": "public"},
            {"table_name": "industry_benchmarks", "schema": "public"},
            {"table_name": "executive_summary", "schema": "public"},
            {"table_name": "deals", "schema": "public"},
            {"table_name": "companies", "schema": "public"},
            {"table_name": "agent_executions", "schema": "public"},
            {"table_name": "findings", "schema": "public"},
            {"table_name": "financial_data", "schema": "public"}
        ]
        
        created_datasets = []
        csrf_token = self.get_csrf_token()
        
        for dataset in datasets:
            try:
                dataset_config = {
                    "table_name": dataset["table_name"],
                    "schema": dataset["schema"],
                    "database": 1,  # Assuming AMAN database is ID 1
                    "sql": None,
                    "is_sqllab_view": False,
                    "template_params": None,
                    "cache_timeout": 0
                }
                
                headers = {
                    "X-CSRFToken": csrf_token,
                    "Content-Type": "application/json"
                }
                
                response = self.session.post(
                    f"{self.base_url}/api/v1/dataset/",
                    json=dataset_config,
                    headers=headers
                )
                
                if response.status_code in [200, 201]:
                    dataset_id = response.json()["id"]
                    created_datasets.append(dataset_id)
                    print(f"Created dataset: {dataset['table_name']} (ID: {dataset_id})")
                else:
                    print(f"Failed to create dataset {dataset['table_name']}: {response.status_code}")
                    
            except Exception as e:
                print(f"Dataset creation error for {dataset['table_name']}: {e}")
        
        return created_datasets
    
    def create_charts(self, dataset_ids: List[int]) -> List[int]:
        """Create charts for AMAN dashboards"""
        charts_config = [
            {
                "slice_name": "Deal Status Distribution",
                "viz_type": "pie",
                "params": {
                    "groupby": ["status"],
                    "metric": "count",
                    "pie_label_type": "key_value",
                    "donut": True,
                    "show_legend": True,
                    "color_scheme": "bnbColors"
                }
            },
            {
                "slice_name": "Deal Value by Industry",
                "viz_type": "bar",
                "params": {
                    "groupby": ["acquirer_industry"],
                    "metric": "sum__deal_value",
                    "order_desc": True,
                    "show_legend": False,
                    "color_scheme": "supersetColors"
                }
            },
            {
                "slice_name": "Agent Success Rate",
                "viz_type": "bar",
                "params": {
                    "groupby": ["agent_type"],
                    "metric": "avg__success_rate",
                    "order_desc": True,
                    "show_legend": False,
                    "color_scheme": "googleCategory20c"
                }
            },
            {
                "slice_name": "Risk Findings by Category",
                "viz_type": "bar",
                "params": {
                    "groupby": ["risk_category"],
                    "metric": "sum__finding_count",
                    "order_desc": True,
                    "show_legend": False,
                    "color_scheme": "d3Category20"
                }
            },
            {
                "slice_name": "Deal Timeline Progress",
                "viz_type": "line",
                "params": {
                    "groupby": ["deal_name"],
                    "metric": "completion_percentage",
                    "granularity_sqla": "deal_start_date",
                    "time_grain_sqla": "P1W",
                    "show_legend": True,
                    "line_interpolation": "linear"
                }
            }
        ]
        
        created_charts = []
        csrf_token = self.get_csrf_token()
        
        for i, chart_config in enumerate(charts_config):
            try:
                # Use appropriate dataset ID based on chart type
                dataset_id = dataset_ids[min(i, len(dataset_ids) - 1)]
                
                chart_data = {
                    "slice_name": chart_config["slice_name"],
                    "viz_type": chart_config["viz_type"],
                    "datasource_id": dataset_id,
                    "datasource_type": "table",
                    "params": json.dumps(chart_config["params"]),
                    "cache_timeout": 0
                }
                
                headers = {
                    "X-CSRFToken": csrf_token,
                    "Content-Type": "application/json"
                }
                
                response = self.session.post(
                    f"{self.base_url}/api/v1/chart/",
                    json=chart_data,
                    headers=headers
                )
                
                if response.status_code in [200, 201]:
                    chart_id = response.json()["id"]
                    created_charts.append(chart_id)
                    print(f"Created chart: {chart_config['slice_name']} (ID: {chart_id})")
                else:
                    print(f"Failed to create chart {chart_config['slice_name']}: {response.status_code}")
                    
            except Exception as e:
                print(f"Chart creation error for {chart_config['slice_name']}: {e}")
        
        return created_charts
    
    def create_dashboards(self, chart_ids: List[int]) -> List[int]:
        """Create multiple AMAN dashboards"""
        dashboards_config = [
            {
                "dashboard_title": "AMAN Executive Dashboard",
                "slug": "aman-executive-dashboard",
                "description": "High-level executive overview of M&A activities and performance",
                "charts": chart_ids[:5]  # First 5 charts
            },
            {
                "dashboard_title": "Comprehensive M&A Analysis",
                "slug": "comprehensive-ma-analysis",
                "description": "Detailed M&A analytics with advanced visualizations",
                "charts": chart_ids  # All charts
            },
            {
                "dashboard_title": "M&A Scenario Modeling",
                "slug": "ma-scenario-modeling",
                "description": "Interactive scenario modeling and what-if analysis",
                "charts": chart_ids[2:]  # Subset for scenario analysis
            }
        ]
        
        created_dashboards = []
        csrf_token = self.get_csrf_token()
        
        for dashboard_config in dashboards_config:
            try:
                dashboard_data = {
                    "dashboard_title": dashboard_config["dashboard_title"],
                    "slug": dashboard_config["slug"],
                    "published": True,
                    "json_metadata": json.dumps({
                        "color_scheme": "supersetColors",
                        "refresh_frequency": 300,
                        "timed_refresh_immune_slices": [],
                        "expanded_slices": {},
                        "label_colors": {},
                        "shared_label_colors": {},
                        "color_scheme_domain": [],
                        "cross_filters_enabled": True,
                        "native_filter_configuration": [
                            {
                                "id": "deal_status_filter",
                                "filterType": "filter_select",
                                "targets": [{"datasetId": 1, "column": {"name": "status"}}],
                                "name": "Deal Status",
                                "description": "Filter by deal status"
                            },
                            {
                                "id": "industry_filter", 
                                "filterType": "filter_select",
                                "targets": [{"datasetId": 1, "column": {"name": "acquirer_industry"}}],
                                "name": "Industry",
                                "description": "Filter by industry sector"
                            }
                        ]
                    }),
                    "position_json": json.dumps({
                        f"CHART-{i+1}": {
                            "children": [],
                            "id": f"CHART-{i+1}",
                            "meta": {
                                "chartId": chart_id,
                                "height": 50,
                                "width": 6 if i % 2 == 0 else 6
                            },
                            "type": "CHART"
                        } for i, chart_id in enumerate(dashboard_config["charts"])
                    }),
                    "slices": dashboard_config["charts"]
                }
                
                headers = {
                    "X-CSRFToken": csrf_token,
                    "Content-Type": "application/json"
                }
                
                response = self.session.post(
                    f"{self.base_url}/api/v1/dashboard/",
                    json=dashboard_data,
                    headers=headers
                )
                
                if response.status_code in [200, 201]:
                    dashboard_id = response.json()["id"]
                    created_dashboards.append(dashboard_id)
                    print(f"Created dashboard: {dashboard_config['dashboard_title']} (ID: {dashboard_id})")
                else:
                    print(f"Failed to create dashboard {dashboard_config['dashboard_title']}: {response.status_code}")
                    
            except Exception as e:
                print(f"Dashboard creation error for {dashboard_config['dashboard_title']}: {e}")
        
        return created_dashboards
    
    def setup_complete_aman_integration(self) -> bool:
        """Complete AMAN Superset setup"""
        print("Starting AMAN Superset integration setup...")
        
        # Wait for Superset to be ready
        print("Waiting for Superset to be ready...")
        max_retries = 30
        for i in range(max_retries):
            try:
                response = requests.get(f"{self.base_url}/health")
                if response.status_code == 200:
                    break
            except:
                pass
            time.sleep(10)
            print(f"Waiting... ({i+1}/{max_retries})")
        
        # Login
        if not self.login():
            return False
        
        # Create database connection
        if not self.create_database_connection():
            print("Warning: Database connection creation failed, continuing...")
        
        # Create datasets
        dataset_ids = self.create_datasets()
        if not dataset_ids:
            print("Failed to create datasets")
            return False
        
        # Create charts
        chart_ids = self.create_charts(dataset_ids)
        if not chart_ids:
            print("Failed to create charts")
            return False
        
        # Create dashboards
        dashboard_ids = self.create_dashboards(chart_ids)
        if not dashboard_ids:
            print("Failed to create dashboards")
            return False
        
        print("AMAN Superset integration setup completed successfully!")
        print(f"Access your dashboard at: {self.base_url}/superset/dashboard/aman-executive-dashboard/")
        return True

def main():
    """Main setup function"""
    setup = SupersetSetup()
    success = setup.setup_complete_aman_integration()
    
    if success:
        print("\n" + "="*50)
        print("AMAN SUPERSET SETUP COMPLETE")
        print("="*50)
        print("Access Superset at: http://localhost:8088")
        print("Username: admin")
        print("Password: admin123")
        print("Dashboard: AMAN Executive Dashboard")
        print("="*50)
    else:
        print("Setup failed. Please check the logs above.")
        exit(1)

if __name__ == "__main__":
    main()