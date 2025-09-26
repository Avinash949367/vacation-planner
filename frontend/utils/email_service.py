import smtplib
import random
import string
import time
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from kivy.storage.jsonstore import JsonStore
import json

class EmailVerificationService:
    def __init__(self):
        self.store = JsonStore('user_data.json')
        self.smtp_server = "smtp.gmail.com"  # Change to your SMTP server
        self.smtp_port = 587
        self.sender_email = "your-email@gmail.com"  # Change to your email
        self.sender_password = "your-app-password"  # Change to your app password
        
    def generate_verification_code(self):
        """Generate a 6-digit verification code"""
        return ''.join(random.choices(string.digits, k=6))
    
    def send_verification_email(self, email, code):
        """Send verification code to email"""
        try:
            # Create message
            msg = MIMEMultipart()
            msg['From'] = self.sender_email
            msg['To'] = email
            msg['Subject'] = "TravelMate - Email Verification Code"
            
            # Email body
            body = f"""
            <html>
            <body>
                <h2>TravelMate Email Verification</h2>
                <p>Your verification code is:</p>
                <h1 style="color: #1976d2; font-size: 32px; letter-spacing: 5px;">{code}</h1>
                <p>This code will expire in 10 minutes.</p>
                <p>If you didn't request this code, please ignore this email.</p>
                <br>
                <p>Best regards,<br>TravelMate Team</p>
            </body>
            </html>
            """
            
            msg.attach(MIMEText(body, 'html'))
            
            # Send email
            server = smtplib.SMTP(self.smtp_server, self.smtp_port)
            server.starttls()
            server.login(self.sender_email, self.sender_password)
            text = msg.as_string()
            server.sendmail(self.sender_email, email, text)
            server.quit()
            
            return True, None
        except Exception as e:
            return False, str(e)
    
    def store_verification_code(self, email, code):
        """Store verification code with timestamp"""
        verification_data = {
            'email': email,
            'code': code,
            'timestamp': str(int(time.time())),
            'expires_in': 600  # 10 minutes
        }
        self.store.put('verification_code', **verification_data)
    
    def verify_code(self, email, code):
        """Verify the entered code"""
        try:
            if not self.store.exists('verification_code'):
                return False, "No verification code found"
            
            stored_data = self.store.get('verification_code')
            current_time = int(time.time())
            stored_time = int(stored_data['timestamp'])
            
            # Check if code is expired (10 minutes)
            if current_time - stored_time > stored_data['expires_in']:
                return False, "Verification code has expired"
            
            # Check if email and code match
            if stored_data['email'] == email and stored_data['code'] == code:
                # Clear verification code after successful verification
                self.store.delete('verification_code')
                return True, "Email verified successfully"
            else:
                return False, "Invalid verification code"
                
        except Exception as e:
            return False, f"Verification error: {str(e)}"
    
    def is_email_verified(self, email):
        """Check if email is verified (simplified for demo)"""
        # In a real app, this would check against your backend
        return True  # For demo purposes, always return True

# For demo purposes, we'll use a mock email service
class MockEmailVerificationService:
    def __init__(self):
        self.store = JsonStore('user_data.json')
        self.verification_codes = {}  # Store codes in memory for demo
    
    def generate_verification_code(self):
        """Generate a 6-digit verification code"""
        return ''.join(random.choices(string.digits, k=6))
    
    def send_verification_email(self, email, code):
        """Mock email sending - just store the code"""
        try:
            self.verification_codes[email] = {
                'code': code,
                'timestamp': int(time.time()),
                'expires_in': 600  # 10 minutes
            }
            print(f"Mock Email sent to {email} with code: {code}")
            return True, None
        except Exception as e:
            return False, str(e)
    
    def verify_code(self, email, code):
        """Verify the entered code"""
        try:
            if email not in self.verification_codes:
                return False, "No verification code found for this email"
            
            stored_data = self.verification_codes[email]
            current_time = int(time.time())
            
            # Check if code is expired (10 minutes)
            if current_time - stored_data['timestamp'] > stored_data['expires_in']:
                del self.verification_codes[email]
                return False, "Verification code has expired"
            
            # Check if code matches
            if stored_data['code'] == code:
                del self.verification_codes[email]
                return True, "Email verified successfully"
            else:
                return False, "Invalid verification code"
                
        except Exception as e:
            return False, f"Verification error: {str(e)}"
    
    def is_email_verified(self, email):
        """Check if email is verified"""
        return email not in self.verification_codes

# Use mock service for demo
EmailService = MockEmailVerificationService
