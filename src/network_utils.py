import requests
from .config import API_URL, USERNAME, PASSWORD, TIMEOUT, ENDPOINTS

class NetworkAPI:
    def __init__(self):
        self.session = requests.Session()
        self.base_url = API_URL
        self.token = None

    def login(self):
        """Login to the network device"""
        try:
            response = self.session.post(
                f"{self.base_url}{ENDPOINTS['login']}",
                json={"username": USERNAME, "password": PASSWORD},
                timeout=TIMEOUT
            )
            response.raise_for_status()
            self.token = response.json().get('token')
            return True
        except requests.exceptions.RequestException as e:
            print(f"Login failed: {str(e)}")
            return False

    def logout(self):
        """Logout from the network device"""
        try:
            response = self.session.post(
                f"{self.base_url}{ENDPOINTS['logout']}",
                headers={"Authorization": f"Bearer {self.token}"},
                timeout=TIMEOUT
            )
            response.raise_for_status()
            self.token = None
            return True
        except requests.exceptions.RequestException as e:
            print(f"Logout failed: {str(e)}")
            return False

    def ping(self, host):
        """Ping a host"""
        try:
            response = self.session.get(
                f"{self.base_url}{ENDPOINTS['ping']}",
                params={"host": host},
                headers={"Authorization": f"Bearer {self.token}"},
                timeout=TIMEOUT
            )
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            print(f"Ping failed: {str(e)}")
            return None

    def change_ssid(self, new_ssid):
        """Change the SSID of the network"""
        try:
            response = self.session.put(
                f"{self.base_url}{ENDPOINTS['ssid']}",
                json={"ssid": new_ssid},
                headers={"Authorization": f"Bearer {self.token}"},
                timeout=TIMEOUT
            )
            response.raise_for_status()
            return True
        except requests.exceptions.RequestException as e:
            print(f"SSID change failed: {str(e)}")
            return False

    def enable_mesh(self):
        """Enable mesh networking"""
        try:
            response = self.session.post(
                f"{self.base_url}{ENDPOINTS['mesh']}",
                json={"enabled": True},
                headers={"Authorization": f"Bearer {self.token}"},
                timeout=TIMEOUT
            )
            response.raise_for_status()
            return True
        except requests.exceptions.RequestException as e:
            print(f"Mesh enable failed: {str(e)}")
            return False 