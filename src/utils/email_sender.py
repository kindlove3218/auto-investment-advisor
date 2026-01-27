import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.application import MIMEApplication
import logging
from typing import Optional, List
import os

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class EmailSender:
    def __init__(self, smtp_server: str, smtp_port: int, sender: str, password: str):
        self.smtp_server = smtp_server
        self.smtp_port = smtp_port
        self.sender = sender
        self.password = password

    def send_email(self, receiver: str, subject: str, body: str, 
                   html: bool = False, attachments: Optional[List[str]] = None) -> bool:
        try:
            msg = MIMEMultipart()
            msg['From'] = self.sender
            msg['To'] = receiver
            msg['Subject'] = subject
            
            msg.attach(MIMEText(body, 'html' if html else 'plain', 'utf-8'))
            
            if attachments:
                for attachment in attachments:
                    if os.path.exists(attachment):
                        with open(attachment, 'rb') as f:
                            part = MIMEApplication(f.read(), Name=os.path.basename(attachment))
                        part['Content-Disposition'] = f'attachment; filename="{os.path.basename(attachment)}"'
                        msg.attach(part)
            
            with smtplib.SMTP(self.smtp_server, self.smtp_port) as server:
                server.starttls()
                server.login(self.sender, self.password)
                server.send_message(msg)
            
            logger.info(f"邮件发送成功: {receiver}")
            return True
        except Exception as e:
            logger.error(f"邮件发送失败: {e}")
            return False

    def send_investment_report(self, receiver: str, report_content: str, 
                               html: bool = True, attachments: Optional[List[str]] = None) -> bool:
        from datetime import datetime
        
        today = datetime.now().strftime('%Y-%m-%d')
        subject = f"【投资日报】{today} - 股市投资机会分析报告"
        
        return self.send_email(receiver, subject, report_content, html, attachments)
