import smtplib
import ssl
import csv
import time
import os
import re
from datetime import datetime
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

class EmailSender:
    def __init__(self):
        try:
            from config import SMTP_HOST, SMTP_PORT, SENDER_EMAIL, SENDER_PASSWORD, SENDER_NAME, DELAY_BETWEEN_EMAILS, EMAILS_PER_HOUR, MAX_DAILY_EMAILS
            self.smtp_server = SMTP_HOST
            self.smtp_port = SMTP_PORT
            self.username = SENDER_EMAIL
            self.password = SENDER_PASSWORD
            self.from_email = SENDER_EMAIL
            self.from_name = SENDER_NAME
            self.delay = DELAY_BETWEEN_EMAILS
            self.emails_per_hour = EMAILS_PER_HOUR
            self.max_daily = MAX_DAILY_EMAILS
        except ImportError:
            self.smtp_server = os.getenv("SMTP_HOST", "smtp.gmail.com")
            self.smtp_port = int(os.getenv("SMTP_PORT", 587))
            self.username = os.getenv("SENDER_EMAIL", "")
            self.password = os.getenv("SENDER_PASSWORD", "")
            self.from_email = self.username
            self.from_name = os.getenv("SENDER_NAME", "Shailesh Singh")
            self.delay = int(os.getenv("DELAY_BETWEEN_EMAILS", 180))
            self.emails_per_hour = int(os.getenv("EMAILS_PER_HOUR", 20))
            self.max_daily = int(os.getenv("MAX_DAILY_EMAILS", 50))
            
        self.server = None
        self.log_file = "send_log.csv"
        self._ensure_log_file()

    def _ensure_log_file(self):
        if not os.path.exists(self.log_file):
            with open(self.log_file, 'w', newline='', encoding='utf-8') as f:
                writer = csv.writer(f)
                writer.writerow(['timestamp', 'recipient', 'subject', 'success', 'error'])

    def connect(self):
        try:
            if self.smtp_port == 465:
                context = ssl.create_default_context()
                self.server = smtplib.SMTP_SSL(self.smtp_server, self.smtp_port, context=context)
            else:
                self.server = smtplib.SMTP(self.smtp_server, self.smtp_port)
                self.server.starttls()
            self.server.login(self.username, self.password)
            return True
        except Exception as e:
            print(f"Connection failed: {e}")
            return False

    def disconnect(self):
        if self.server:
            try:
                self.server.quit()
            except:
                pass
            self.server = None

    def validate_email(self, email):
        if not email or '@' not in email:
            return False
        pattern = r'^[\w\.-]+@[\w\.-]+\.\w+$'
        if not re.match(pattern, email):
            return False
        
        # Check if email domain actually exists in DNS to prevent NXDOMAIN bounces
        domain = email.split('@')[-1].strip().lower()
        import socket
        try:
            socket.gethostbyname(domain)
            return True
        except Exception:
            return False

    def log_send(self, prospect_email, success, subject="", error=None):
        with open(self.log_file, 'a', newline='', encoding='utf-8') as f:
            writer = csv.writer(f)
            writer.writerow([datetime.now().isoformat(), prospect_email, subject, success, error or ""])

    def get_send_stats(self):
        total_sent = 0
        successful = 0
        failed = 0
        today_count = 0
        today_str = datetime.now().date().isoformat()
        
        if os.path.exists(self.log_file):
            with open(self.log_file, 'r', encoding='utf-8') as f:
                reader = csv.DictReader(f)
                for row in reader:
                    total_sent += 1
                    if row['success'] == 'True':
                        successful += 1
                        if row['timestamp'].startswith(today_str):
                            today_count += 1
                    else:
                        failed += 1
        return {
            'total_sent': total_sent,
            'successful': successful,
            'failed': failed,
            'today_count': today_count
        }

    def can_send_more(self):
        stats = self.get_send_stats()
        return stats['today_count'] < self.max_daily

    def send_email(self, to_email, subject, body_text, body_html=None):
        if not self.validate_email(to_email):
            self.log_send(to_email, False, subject, "Invalid email format")
            return False, "Invalid email format"
            
        msg = MIMEMultipart('alternative')
        msg['Subject'] = subject
        msg['From'] = f"{self.from_name} <{self.from_email}>"
        msg['To'] = to_email
        msg['Reply-To'] = self.from_email
        msg['List-Unsubscribe'] = f"<mailto:{self.from_email}?subject=unsubscribe>"
        
        msg.attach(MIMEText(body_text, 'plain'))
        if body_html:
            msg.attach(MIMEText(body_html, 'html'))
            
        try:
            if not self.server:
                if not self.connect():
                    return False, "Failed to connect to SMTP server"
            self.server.send_message(msg)
            self.log_send(to_email, True, subject)
            return True, None
        except smtplib.SMTPRecipientsRefused:
            self.log_send(to_email, False, subject, "Recipient refused")
            return False, "Recipient refused"
        except smtplib.SMTPException as e:
            self.log_send(to_email, False, subject, str(e))
            return False, f"SMTP Error: {e}"
        except Exception as e:
            self.log_send(to_email, False, subject, str(e))
            return False, f"Error: {e}"

    def send_batch(self, prospects_with_emails):
        if not prospects_with_emails:
            print("No prospects to send to.")
            return

        print(f"Summary: You are about to send {len(prospects_with_emails)} emails.")
        confirm = input("Are you sure you want to proceed? (y/n): ")
        if confirm.lower() != 'y':
            print("Aborted.")
            return

        if not self.connect():
            print("Failed to establish SMTP connection. Aborting.")
            return

        total = len(prospects_with_emails)
        for i, prospect in enumerate(prospects_with_emails, 1):
            if not self.can_send_more():
                print("Daily limit reached. Stopping batch.")
                break
                
            email = prospect.get('email')
            subject = prospect.get('subject', 'Introduction')
            body = prospect.get('body', '')
            
            print(f"[{i}/{total}] Sending to {email}...")
            success, err = self.send_email(email, subject, body)
            
            if success:
                print(f"  ✓ Sent successfully.")
            else:
                print(f"  ✗ Failed: {err}")
                
            if i < total:
                print(f"  Waiting {self.delay} seconds before next email (Rate limiting)...")
                time.sleep(self.delay)
                
        self.disconnect()
        print("Batch complete.")

    def test_connection(self):
        print("Testing SMTP connection...")
        if self.connect():
            print("✓ Connection successful.")
            self.disconnect()
            return True
        else:
            print("✗ Connection failed.")
            return False

    def send_test_email(self, to_email):
        print(f"Sending test email to {to_email}...")
        success, err = self.send_email(to_email, "Test Email from Reflecter", "This is a test email.", "<h1>This is a test email.</h1>")
        if success:
            print("✓ Test email sent successfully.")
        else:
            print(f"✗ Failed to send test email: {err}")
            
        self.disconnect()
