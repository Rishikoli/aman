#!/usr/bin/env python3
"""
Automated Report Generation for AMAN Superset
Generates and exports reports automatically based on schedules and triggers
"""

import os
import json
import requests
import schedule
import time
import smtplib
from datetime import datetime, timedelta
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders
from typing import Dict, List, Any, Optional
import logging

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('/app/superset_home/automated_reports.log'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

class SupersetReportGenerator:
    def __init__(self, base_url: str = "http://localhost:8088"):
        self.base_url = base_url
        self.session = requests.Session()
        self.access_token = None
        
    def login(self, username: str = "admin", password: str = "admin123") -> bool:
        """Login to Superset"""
        try:
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
                logger.info("Successfully logged in to Superset")
                return True
            else:
                logger.error(f"Login failed: {response.status_code}")
                return False
                
        except Exception as e:
            logger.error(f"Login error: {e}")
            return False
    
    def export_dashboard(self, dashboard_id: int, format: str = "pdf") -> Optional[bytes]:
        """Export dashboard to specified format"""
        try:
            # Get dashboard export
            response = self.session.get(
                f"{self.base_url}/api/v1/dashboard/{dashboard_id}/export/{format}/"
            )
            
            if response.status_code == 200:
                logger.info(f"Successfully exported dashboard {dashboard_id} as {format}")
                return response.content
            else:
                logger.error(f"Dashboard export failed: {response.status_code}")
                return None
                
        except Exception as e:
            logger.error(f"Dashboard export error: {e}")
            return None
    
    def export_chart(self, chart_id: int, format: str = "png") -> Optional[bytes]:
        """Export chart to specified format"""
        try:
            # Get chart export
            response = self.session.get(
                f"{self.base_url}/api/v1/chart/{chart_id}/export/{format}/"
            )
            
            if response.status_code == 200:
                logger.info(f"Successfully exported chart {chart_id} as {format}")
                return response.content
            else:
                logger.error(f"Chart export failed: {response.status_code}")
                return None
                
        except Exception as e:
            logger.error(f"Chart export error: {e}")
            return None
    
    def get_dashboard_data(self, dashboard_id: int) -> Optional[Dict]:
        """Get dashboard metadata and chart data"""
        try:
            response = self.session.get(
                f"{self.base_url}/api/v1/dashboard/{dashboard_id}"
            )
            
            if response.status_code == 200:
                return response.json()
            else:
                logger.error(f"Failed to get dashboard data: {response.status_code}")
                return None
                
        except Exception as e:
            logger.error(f"Dashboard data error: {e}")
            return None
    
    def generate_executive_summary(self) -> str:
        """Generate executive summary from dashboard data"""
        try:
            # Get executive summary data
            response = self.session.post(
                f"{self.base_url}/api/v1/chart/data",
                json={
                    "datasource": {"type": "table", "id": 1},
                    "queries": [{
                        "columns": [],
                        "metrics": ["total_deals", "active_deals", "completed_deals", "total_deal_value"],
                        "row_limit": 1
                    }]
                }
            )
            
            if response.status_code == 200:
                data = response.json()
                if data.get("result") and len(data["result"]) > 0:
                    result = data["result"][0]["data"][0] if data["result"][0]["data"] else {}
                    
                    summary = f"""
                    AMAN Executive Summary - {datetime.now().strftime('%Y-%m-%d')}
                    
                    Key Metrics:
                    - Total Deals: {result.get('total_deals', 'N/A')}
                    - Active Deals: {result.get('active_deals', 'N/A')}
                    - Completed Deals: {result.get('completed_deals', 'N/A')}
                    - Total Deal Value: ${result.get('total_deal_value', 0):,.0f}
                    
                    Generated automatically by AMAN Reporting System
                    """
                    return summary
            
            return "Executive summary data not available"
            
        except Exception as e:
            logger.error(f"Executive summary generation error: {e}")
            return "Error generating executive summary"

class ReportScheduler:
    def __init__(self, report_generator: SupersetReportGenerator):
        self.generator = report_generator
        self.email_config = {
            "smtp_server": os.getenv("SMTP_SERVER", "localhost"),
            "smtp_port": int(os.getenv("SMTP_PORT", "587")),
            "smtp_username": os.getenv("SMTP_USERNAME", ""),
            "smtp_password": os.getenv("SMTP_PASSWORD", ""),
            "from_email": os.getenv("FROM_EMAIL", "aman@company.com")
        }
        
    def send_email_report(self, to_emails: List[str], subject: str, body: str, attachments: List[Dict] = None):
        """Send email report with attachments"""
        try:
            msg = MIMEMultipart()
            msg['From'] = self.email_config["from_email"]
            msg['To'] = ", ".join(to_emails)
            msg['Subject'] = subject
            
            # Add body
            msg.attach(MIMEText(body, 'plain'))
            
            # Add attachments
            if attachments:
                for attachment in attachments:
                    part = MIMEBase('application', 'octet-stream')
                    part.set_payload(attachment['content'])
                    encoders.encode_base64(part)
                    part.add_header(
                        'Content-Disposition',
                        f'attachment; filename= {attachment["filename"]}'
                    )
                    msg.attach(part)
            
            # Send email
            server = smtplib.SMTP(self.email_config["smtp_server"], self.email_config["smtp_port"])
            server.starttls()
            if self.email_config["smtp_username"]:
                server.login(self.email_config["smtp_username"], self.email_config["smtp_password"])
            
            text = msg.as_string()
            server.sendmail(self.email_config["from_email"], to_emails, text)
            server.quit()
            
            logger.info(f"Email report sent to {to_emails}")
            
        except Exception as e:
            logger.error(f"Email sending error: {e}")
    
    def generate_daily_report(self):
        """Generate and send daily executive report"""
        logger.info("Generating daily report...")
        
        if not self.generator.login():
            logger.error("Failed to login for daily report")
            return
        
        try:
            # Generate executive summary
            summary = self.generator.generate_executive_summary()
            
            # Export main dashboard
            dashboard_pdf = self.generator.export_dashboard(1, "pdf")
            
            attachments = []
            if dashboard_pdf:
                attachments.append({
                    "filename": f"AMAN_Daily_Report_{datetime.now().strftime('%Y%m%d')}.pdf",
                    "content": dashboard_pdf
                })
            
            # Send email
            self.send_email_report(
                to_emails=["executives@company.com"],
                subject=f"AMAN Daily Report - {datetime.now().strftime('%Y-%m-%d')}",
                body=summary,
                attachments=attachments
            )
            
        except Exception as e:
            logger.error(f"Daily report generation error: {e}")
    
    def generate_weekly_report(self):
        """Generate and send weekly comprehensive report"""
        logger.info("Generating weekly report...")
        
        if not self.generator.login():
            logger.error("Failed to login for weekly report")
            return
        
        try:
            # Generate comprehensive summary
            summary = self.generator.generate_executive_summary()
            summary += "\n\nWeekly Analysis:\n"
            summary += "- Deal pipeline analysis\n"
            summary += "- Risk assessment trends\n"
            summary += "- Agent performance metrics\n"
            summary += "- Financial metrics comparison\n"
            
            # Export multiple dashboards
            attachments = []
            
            # Main executive dashboard
            exec_dashboard = self.generator.export_dashboard(1, "pdf")
            if exec_dashboard:
                attachments.append({
                    "filename": f"Executive_Dashboard_{datetime.now().strftime('%Y%m%d')}.pdf",
                    "content": exec_dashboard
                })
            
            # Scenario modeling dashboard
            scenario_dashboard = self.generator.export_dashboard(2, "pdf")
            if scenario_dashboard:
                attachments.append({
                    "filename": f"Scenario_Analysis_{datetime.now().strftime('%Y%m%d')}.pdf",
                    "content": scenario_dashboard
                })
            
            # Send email
            self.send_email_report(
                to_emails=["executives@company.com", "analysts@company.com"],
                subject=f"AMAN Weekly Report - Week of {datetime.now().strftime('%Y-%m-%d')}",
                body=summary,
                attachments=attachments
            )
            
        except Exception as e:
            logger.error(f"Weekly report generation error: {e}")
    
    def generate_monthly_report(self):
        """Generate and send monthly comprehensive report"""
        logger.info("Generating monthly report...")
        
        if not self.generator.login():
            logger.error("Failed to login for monthly report")
            return
        
        try:
            # Generate comprehensive monthly summary
            summary = self.generator.generate_executive_summary()
            summary += "\n\nMonthly Analysis:\n"
            summary += "- Deal completion trends\n"
            summary += "- Industry benchmarking\n"
            summary += "- Risk pattern analysis\n"
            summary += "- ROI and performance metrics\n"
            summary += "- Recommendations for next month\n"
            
            # Export all dashboards
            attachments = []
            dashboard_ids = [1, 2, 3]  # Executive, Scenario, Comprehensive
            dashboard_names = ["Executive", "Scenario_Modeling", "Comprehensive_Analysis"]
            
            for dashboard_id, name in zip(dashboard_ids, dashboard_names):
                dashboard_pdf = self.generator.export_dashboard(dashboard_id, "pdf")
                if dashboard_pdf:
                    attachments.append({
                        "filename": f"{name}_Dashboard_{datetime.now().strftime('%Y%m')}.pdf",
                        "content": dashboard_pdf
                    })
            
            # Send email
            self.send_email_report(
                to_emails=["executives@company.com", "analysts@company.com", "board@company.com"],
                subject=f"AMAN Monthly Report - {datetime.now().strftime('%B %Y')}",
                body=summary,
                attachments=attachments
            )
            
        except Exception as e:
            logger.error(f"Monthly report generation error: {e}")
    
    def setup_schedules(self):
        """Setup automated report schedules"""
        # Daily reports at 8 AM
        schedule.every().day.at("08:00").do(self.generate_daily_report)
        
        # Weekly reports on Monday at 9 AM
        schedule.every().monday.at("09:00").do(self.generate_weekly_report)
        
        # Monthly reports on the 1st at 10 AM
        schedule.every().month.do(self.generate_monthly_report)
        
        logger.info("Report schedules configured")
    
    def run_scheduler(self):
        """Run the report scheduler"""
        logger.info("Starting automated report scheduler...")
        
        while True:
            schedule.run_pending()
            time.sleep(60)  # Check every minute

def main():
    """Main function to run automated reporting"""
    logger.info("Starting AMAN Automated Reporting System")
    
    # Initialize components
    report_generator = SupersetReportGenerator()
    scheduler = ReportScheduler(report_generator)
    
    # Setup schedules
    scheduler.setup_schedules()
    
    # Test login
    if report_generator.login():
        logger.info("Successfully connected to Superset")
        
        # Generate initial test report
        logger.info("Generating test report...")
        scheduler.generate_daily_report()
        
        # Start scheduler
        scheduler.run_scheduler()
    else:
        logger.error("Failed to connect to Superset")
        exit(1)

if __name__ == "__main__":
    main()