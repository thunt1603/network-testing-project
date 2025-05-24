import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Configuration
API_URL = os.getenv('API_URL')
USERNAME = os.getenv('USERNAME')
PASSWORD = os.getenv('PASSWORD')

# Default timeout for requests
TIMEOUT = 30

# API endpoints
ENDPOINTS = {
    'login': '/api/login',
    'logout': '/api/logout',
    'ping': '/api/ping',
    'ssid': '/api/ssid',
    'mesh': '/api/mesh'
} 