import os
from dotenv import load_dotenv
from pathlib import Path

# Get the project root directory
project_root = Path(__file__).parent.parent

# Load environment variables from .env file
env_path = project_root / '.env'
print(f"\n[DEBUG] Loading .env from: {env_path}")
load_dotenv(env_path, override=True)  # Force override existing env vars

# Configuration - Force using values from .env
API_URL = os.environ.get('API_URL')  # Use environ instead of getenv
USERNAME = os.environ.get('USERNAME')
PASSWORD = os.environ.get('PASSWORD')

# Print loaded values for debugging
print(f"[DEBUG] Loaded configuration:")
print(f"[DEBUG] API_URL: {API_URL}")
print(f"[DEBUG] USERNAME: {USERNAME}")
print(f"[DEBUG] PASSWORD: {PASSWORD}")

# Default timeout for requests
TIMEOUT = 30

# API endpoints - Updated to match actual API
ENDPOINTS = {
    'login': '/login',  # Changed from /api/login
    'logout': '/logout',  # Changed from /api/logout
    'ping': '/ping',  # Changed from /api/ping
    'ssid': '/ssid',  # Changed from /api/ssid
    'mesh': '/mesh'   # Changed from /api/mesh
} 