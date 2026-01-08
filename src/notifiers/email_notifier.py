"""
Email notifier for sending job matches.
"""

import os
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from datetime import datetime
from utils.logger import setup_logger

logger = setup_logger(__name__)


class EmailNotifier:
    """Send email notifications for job matches."""
    
    def __init__(self, config):
        """
        Initialize email notifier.
        
        Args:
            config: Application configuration
        """
        self.config = config
        self.sender = os.getenv('EMAIL_SENDER')
        self.password = os.getenv('EMAIL_PASSWORD')
        self.recipient = os.getenv('EMAIL_RECIPIENT')
        self.smtp_server = os.getenv('SMTP_SERVER', 'smtp.gmail.com')
        self.smtp_port = int(os.getenv('SMTP_PORT', 587))
        
        if not all([self.sender, self.password, self.recipient]):
            raise ValueError("Email credentials not configured in .env file")
    
    def send_notification(self, jobs):
        """
        Send email notification with matched jobs.
        
        Args:
            jobs: List of matched job dictionaries
        """
        if not jobs:
            logger.info("No jobs to notify")
            return
        
        min_jobs = self.config['notifications']['min_jobs']
        if len(jobs) < min_jobs:
            logger.info(f"Only {len(jobs)} jobs found (minimum: {min_jobs}), skipping notification")
            return
        
        # Limit number of jobs in email
        max_jobs = self.config['notifications']['max_jobs_per_email']
        jobs_to_send = jobs[:max_jobs]
        
        # Create email
        subject = self._create_subject(len(jobs))
        body = self._create_body(jobs_to_send, len(jobs))
        
        try:
            self._send_email(subject, body)
            logger.info(f"✓ Email sent successfully to {self.recipient}")
        except Exception as e:
            logger.error(f"Failed to send email: {e}")
            raise
    
    def _create_subject(self, job_count):
        """Create email subject."""
        today = datetime.now().strftime('%Y-%m-%d')
        template = self.config['notifications']['subject_template']
        return template.format(count=job_count, date=today)
    
    def _create_body(self, jobs, total_count):
        """
        Create email body with job details.
        
        Args:
            jobs: List of jobs to include
            total_count: Total number of matches
            
        Returns:
            HTML email body
        """
        html = f"""
        <html>
        <head>
            <style>
                body {{
                    font-family: Arial, sans-serif;
                    line-height: 1.6;
                    color: #333;
                }}
                .header {{
                    background-color: #4CAF50;
                    color: white;
                    padding: 20px;
                    text-align: center;
                }}
                .job-card {{
                    border: 1px solid #ddd;
                    border-radius: 5px;
                    padding: 15px;
                    margin: 15px 0;
                    background-color: #f9f9f9;
                }}
                .job-title {{
                    font-size: 18px;
                    font-weight: bold;
                    color: #2196F3;
                    margin-bottom: 10px;
                }}
                .job-company {{
                    font-size: 16px;
                    color: #555;
                    margin-bottom: 5px;
                }}
                .job-location {{
                    color: #777;
                    margin-bottom: 10px;
                }}
                .job-match {{
                    background-color: #4CAF50;
                    color: white;
                    padding: 5px 10px;
                    border-radius: 3px;
                    display: inline-block;
                    margin: 10px 0;
                }}
                .job-salary {{
                    color: #FF9800;
                    font-weight: bold;
                    margin: 10px 0;
                }}
                .job-description {{
                    color: #666;
                    margin: 10px 0;
                    font-size: 14px;
                }}
                .job-keywords {{
                    color: #9C27B0;
                    font-size: 13px;
                    margin: 10px 0;
                }}
                .apply-button {{
                    background-color: #2196F3;
                    color: white;
                    padding: 10px 20px;
                    text-decoration: none;
                    border-radius: 5px;
                    display: inline-block;
                    margin: 10px 0;
                }}
                .footer {{
                    text-align: center;
                    color: #777;
                    padding: 20px;
                    margin-top: 30px;
                    border-top: 1px solid #ddd;
                }}
            </style>
        </head>
        <body>
            <div class="header">
                <h1>🎯 Your Daily Job Matches</h1>
                <p>Found {total_count} jobs matching your resume at 90%+</p>
            </div>
            
            <div style="padding: 20px;">
        """
        
        for i, job in enumerate(jobs, 1):
            match_score = job.get('match_score', 0) * 100
            
            html += f"""
                <div class="job-card">
                    <div class="job-title">{i}. {job['title']}</div>
                    <div class="job-company">🏢 {job['company']}</div>
                    <div class="job-location">📍 {job.get('location', 'Germany')}</div>
                    <div class="job-match">Match Score: {match_score:.0f}%</div>
            """
            
            if job.get('salary'):
                html += f'<div class="job-salary">💰 {job["salary"]}</div>'
            
            if self.config['notifications']['include_description'] and job.get('description'):
                description = job['description'][:300] + "..." if len(job['description']) > 300 else job['description']
                html += f'<div class="job-description">{description}</div>'
            
            if job.get('keywords_matched'):
                keywords = ', '.join(job['keywords_matched'][:10])
                html += f'<div class="job-keywords">🔑 Matched Keywords: {keywords}</div>'
            
            html += f"""
                    <a href="{job['url']}" class="apply-button">View Job →</a>
                </div>
            """
        
        if total_count > len(jobs):
            html += f"""
                <div style="text-align: center; margin: 20px; color: #666;">
                    <p>... and {total_count - len(jobs)} more matches!</p>
                    <p>Check your database for all results.</p>
                </div>
            """
        
        html += """
            </div>
            
            <div class="footer">
                <p>This is an automated email from your AI Job Matcher.</p>
                <p>Good luck with your applications! 🚀</p>
            </div>
        </body>
        </html>
        """
        
        return html
    
    def _send_email(self, subject, body):
        """
        Send email via SMTP.
        
        Args:
            subject: Email subject
            body: Email body (HTML)
        """
        # Create message
        msg = MIMEMultipart('alternative')
        msg['Subject'] = subject
        msg['From'] = self.sender
        msg['To'] = self.recipient
        
        # Attach HTML body
        html_part = MIMEText(body, 'html')
        msg.attach(html_part)
        
        # Send email
        with smtplib.SMTP(self.smtp_server, self.smtp_port) as server:
            server.starttls()
            server.login(self.sender, self.password)
            server.send_message(msg)
