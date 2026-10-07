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
SENDER_LOCATION = os.getenv('SENDER_LOCATION', 'Surat, Gujarat, India')

# Rate Limiting
EMAILS_PER_HOUR = int(os.getenv('EMAILS_PER_HOUR', '60'))
DELAY_BETWEEN_EMAILS = int(os.getenv('DELAY_BETWEEN_EMAILS', '25')) # in seconds
MAX_DAILY_EMAILS = int(os.getenv('MAX_DAILY_EMAILS', '100'))

# Target Regions & International Commercial Hubs
TARGET_REGIONS = {
    'US': [
        'New York', 'Los Angeles', 'Chicago', 'Houston', 'Miami', 
        'Dallas', 'Atlanta', 'Austin', 'Phoenix', 'San Diego'
    ],
    'UK': [
        'London', 'Manchester', 'Birmingham', 'Leeds', 'Glasgow', 'Bristol'
    ],
    'UAE': [
        'Dubai', 'Abu Dhabi', 'Sharjah'
    ],
    'Canada': [
        'Toronto', 'Vancouver', 'Montreal', 'Calgary'
    ],
    'Australia': [
        'Sydney', 'Melbourne', 'Brisbane', 'Perth'
    ],
    'India': [
        'Surat', 'Ahmedabad', 'Mumbai', 'Pune', 'Jaipur', 'Delhi', 'Bangalore', 'Rajkot'
    ]
}

# Flattened list of default cities for quick scanning
TARGET_CITIES = [
    # Top International Hubs
    'Dubai', 'London', 'New York', 'Manchester', 'Miami', 'Toronto', 'Sydney', 'Los Angeles', 'Chicago', 'Birmingham',
    # Top Indian Hubs
    'Surat', 'Ahmedabad', 'Mumbai', 'Jaipur'
]

# High-Converting International B2B & Offline Service Niches
TARGET_INDUSTRIES = [
    # High-Ticket Home & Trade Services (Major pain point for missing online booking/portals)
    'roofing contractor', 'custom home builder', 'hvac repair', 'plumbing contractor', 'commercial cleaning',
    'landscaping service', 'auto repair shop', 'cabinet maker',
    # Professional & Healthcare Practices
    'dental clinic', 'chiropractic clinic', 'dermatology clinic', 'physiotherapy clinic', 'med spa',
    # Retail & Wholesale Hubs
    'furniture showroom', 'wholesale fabric supplier', 'textile distributor', 'jewellery showroom', 'boutique fashion brand',
    # B2B Manufacturing & Industrial
    'precision manufacturing', 'custom metal fabrication', 'packaging manufacturer'
]

SEARCH_QUERIES_TEMPLATE = '{industry} in {city} without website contact'
