import os
from pathlib import Path
from dotenv import load_dotenv

def load_env():
    """Load environment variables from .env file."""
    load_dotenv()

load_env()

# Base paths
BASE_DIR = Path(__file__).resolve().parent
DATABASE_FILE = os.getenv('DATABASE_FILE', str(BASE_DIR / 'prospects.csv'))
LOG_FILE = os.getenv('LOG_FILE', str(BASE_DIR / 'agent.log'))

# SMTP Settings
SMTP_HOST = os.getenv('SMTP_HOST', 'smtp.gmail.com')
SMTP_PORT = int(os.getenv('SMTP_PORT', '587'))
SENDER_EMAIL = os.getenv('SENDER_EMAIL', '')
SENDER_PASSWORD = os.getenv('SENDER_PASSWORD', '')
SENDER_NAME = os.getenv('SENDER_NAME', 'Shailesh Singh')

# Sender Info
SENDER_COMPANY = os.getenv('SENDER_COMPANY', 'Reflecter Technologies')
SENDER_PHONE = os.getenv('SENDER_PHONE', '+91 91731 08730')
SENDER_WHATSAPP = os.getenv('SENDER_WHATSAPP', '+91 91731 08730')
SENDER_PORTFOLIO = os.getenv('SENDER_PORTFOLIO', 'www.reflecter.in')
SENDER_LOCATION = os.getenv('SENDER_LOCATION', 'Surat, Gujarat')

# Rate Limiting
EMAILS_PER_HOUR = int(os.getenv('EMAILS_PER_HOUR', '60'))
DELAY_BETWEEN_EMAILS = int(os.getenv('DELAY_BETWEEN_EMAILS', '25')) # in seconds (~25s)
MAX_DAILY_EMAILS = int(os.getenv('MAX_DAILY_EMAILS', '100'))

# Search Settings
TARGET_CITIES = [
    'Surat', 'Ahmedabad', 'Mumbai', 'Pune', 'Jaipur', 'Delhi', 'Lucknow', 
    'Indore', 'Ludhiana', 'Coimbatore', 'Hyderabad', 'Bangalore', 'Chennai', 
    'Kolkata', 'Chandigarh', 'Rajkot', 'Vadodara', 'Nagpur', 'Kanpur', 'Bhopal'
]

TARGET_INDUSTRIES = [
    'textile mill', 'fabric trader', 'saree showroom', 'diamond broker', 
    'diamond polishing', 'manufacturing unit', 'retail brand', 'dental clinic', 
    'skin clinic', 'dermatologist', 'eye clinic', 'garment factory', 
    'chemical factory', 'jewellery shop', 'furniture showroom', 'auto parts dealer', 
    'building materials', 'pharma distributor', 'grocery wholesaler', 'sweet shop'
]

SEARCH_QUERIES_TEMPLATE = '{industry} in {city} without website contact number'
