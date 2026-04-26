import os
from datetime import timedelta
from pathlib import Path

# Base Configuration
BASE_DIR = Path(__file__).resolve().parent
DB_PATH = os.path.join(BASE_DIR, 'database', 'demo.db')

# Database
DATABASE_URL = f"sqlite:///{DB_PATH}"
SQLALCHEMY_ECHO = False

# OTP Configuration
OTP_LENGTH = 6
OTP_EXPIRY_MINUTES = 10
MAX_OTP_ATTEMPTS = 3
OTP_TYPE = "numeric"  # numeric, alphanumeric

# Rate Limiting
RATE_LIMIT_WINDOW = 60  # seconds
RATE_LIMIT_MAX_REQUESTS = 5  # requests per window per identifier
COOLDOWN_PERIOD = 300  # 5 minutes after rate limit

# Processing
BATCH_SIZE = 10
PROCESSING_DELAY = 0.5  # seconds between requests (simulate processing)
CONCURRENT_PROCESSING = False  # Set True for async processing

# Logging
LOG_DIR = os.path.join(BASE_DIR, 'logs')
LOG_FILE = os.path.join(LOG_DIR, 'audit.log')
REPORT_DIR = os.path.join(BASE_DIR, 'reports')

# Create directories if they don't exist
os.makedirs(LOG_DIR, exist_ok=True)
os.makedirs(REPORT_DIR, exist_ok=True)

# Security
GENERIC_ERROR_RESPONSE = False  # If True, don't reveal if account exists
ENABLE_ABUSE_DETECTION = True
ABUSE_THRESHOLD = 20  # attempts before flagging

# Color Configuration
COLORS = {
    "PROCESSING_ON": "cyan",
    "ACCOUNT_FOUND": "yellow",
    "ACCOUNT_NOT_FOUND": "red",
    "CODE_GENERATED": "green",
    "CODE_SENT": "green",
    "RATE_LIMITED": "magenta",
    "ERROR": "red",
    "SUCCESS": "green",
}
