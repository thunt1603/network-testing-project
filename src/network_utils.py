import requests
import json
import time
from .config import API_URL, USERNAME, PASSWORD, TIMEOUT, ENDPOINTS

# ANSI color codes
class Colors:
    HEADER = '\033[95m'
    BLUE = '\033[94m'
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    RED = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'

class NetworkAPI:
    def __init__(self):
        self.session = requests.Session()
        self.base_url = API_URL
        self.token = None
        self.username = USERNAME
        self.password = PASSWORD
        
        print(f"\n{Colors.HEADER}{Colors.BOLD}{'='*70}{Colors.ENDC}")
        print(f"{Colors.HEADER}{Colors.BOLD}🚀 KHỞI TẠO NETWORK API{Colors.ENDC}")
        print(f"{Colors.HEADER}{Colors.BOLD}{'='*70}{Colors.ENDC}")
        print(f"{Colors.BLUE}📡 Base URL:{Colors.ENDC} {self.base_url}")
        print(f"{Colors.BLUE}👤 Username:{Colors.ENDC} {self.username}")
        print(f"{Colors.BLUE}🔑 Password:{Colors.ENDC} {self.password}")
        print(f"{Colors.BLUE}⏱️ Timeout:{Colors.ENDC} {TIMEOUT}s")

    def _print_request_details(self, method, url, headers=None, data=None):
        """Print request details in a formatted way"""
        print(f"\n{Colors.BLUE}{Colors.BOLD}📤 CHI TIẾT REQUEST:{Colors.ENDC}")
        print(f"{Colors.BLUE}🌐 URL:{Colors.ENDC} {url}")
        print(f"{Colors.BLUE}📝 Method:{Colors.ENDC} {method}")
        if headers:
            print(f"{Colors.BLUE}📋 Headers:{Colors.ENDC}")
            # Convert headers to regular dict for JSON serialization
            headers_dict = dict(headers)
            print(json.dumps(headers_dict, indent=2))
        if data:
            print(f"{Colors.BLUE}📦 Data:{Colors.ENDC}")
            print(json.dumps(data, indent=2))

    def _print_response_details(self, response):
        """Print response details in a formatted way"""
        print(f"\n{Colors.BLUE}{Colors.BOLD}📥 CHI TIẾT RESPONSE:{Colors.ENDC}")
        print(f"{Colors.BLUE}📊 Status Code:{Colors.ENDC} {response.status_code}")
        print(f"{Colors.BLUE}📋 Headers:{Colors.ENDC}")
        # Convert response headers to regular dict for JSON serialization
        headers_dict = dict(response.headers)
        print(json.dumps(headers_dict, indent=2))
        print(f"{Colors.BLUE}📄 Content Type:{Colors.ENDC} {response.headers.get('content-type', 'Not specified')}")
        print(f"{Colors.BLUE}📝 Response Text:{Colors.ENDC}")
        print(response.text[:500] + "..." if len(response.text) > 500 else response.text)

    def login(self, username=None, password=None):
        """Login to the network device with detailed debug output"""
        print(f"\n{Colors.HEADER}{Colors.BOLD}{'='*70}{Colors.ENDC}")
        print(f"{Colors.HEADER}{Colors.BOLD}🔐 ĐANG THỰC HIỆN ĐĂNG NHẬP{Colors.ENDC}")
        print(f"{Colors.HEADER}{Colors.BOLD}{'='*70}{Colors.ENDC}")
        
        # Use provided credentials or defaults
        username = username or self.username
        password = password or self.password
        
        # Prepare request
        url = f"{self.base_url}{ENDPOINTS['login']}"
        data = {
            "username": username,
            "password": password
        }
        
        # Convert session headers to regular dict
        headers = dict(self.session.headers)
        self._print_request_details("POST", url, headers, data)
        
        try:
            print(f"\n{Colors.YELLOW}⏳ ĐANG GỬI REQUEST...{Colors.ENDC}")
            start_time = time.time()
            response = self.session.post(
                url,
                json=data,
                timeout=TIMEOUT,
                verify=False  # Disable SSL verification
            )
            end_time = time.time()
            
            self._print_response_details(response)
            print(f"\n{Colors.BLUE}⏱️ Thời gian phản hồi:{Colors.ENDC} {end_time - start_time:.2f}s")
            
            response.raise_for_status()
            
            content_type = response.headers.get('content-type', '')
            if 'text/html' in content_type:
                print(f"\n{Colors.RED}{Colors.BOLD}❌ LỖI: Nhận được response HTML thay vì JSON{Colors.ENDC}")
                print(f"{Colors.RED}Có thể do:{Colors.ENDC}")
                print(f"{Colors.RED}1. Endpoint API không đúng{Colors.ENDC}")
                print(f"{Colors.RED}2. Server trả về trang login thay vì API response{Colors.ENDC}")
                print(f"{Colors.RED}3. Xác thực thất bại và server chuyển hướng về trang login{Colors.ENDC}")
                return False
            
            try:
                resp_json = response.json()
                print(f"\n{Colors.BLUE}{Colors.BOLD}📦 JSON RESPONSE:{Colors.ENDC}")
                print(json.dumps(resp_json, indent=2))
                
                self.token = resp_json.get('token')
                if self.token:
                    print(f"\n{Colors.GREEN}{Colors.BOLD}✅ ĐĂNG NHẬP THÀNH CÔNG!{Colors.ENDC}")
                    print(f"{Colors.GREEN}Token nhận được: {self.token[:20]}...{Colors.ENDC}")
                    return True
                else:
                    print(f"\n{Colors.RED}{Colors.BOLD}❌ LỖI: Không có token trong response{Colors.ENDC}")
                    print(f"{Colors.RED}Các key trong response: {list(resp_json.keys())}{Colors.ENDC}")
                    return False
                    
            except json.JSONDecodeError as e:
                print(f"\n{Colors.RED}{Colors.BOLD}❌ LỖI: Không thể parse JSON response{Colors.ENDC}")
                print(f"{Colors.RED}Chi tiết lỗi: {str(e)}{Colors.ENDC}")
                print(f"{Colors.RED}Server trả về JSON không hợp lệ{Colors.ENDC}")
                return False
                
        except requests.exceptions.RequestException as e:
            print(f"\n{Colors.RED}{Colors.BOLD}❌ LỖI: Request thất bại{Colors.ENDC}")
            print(f"{Colors.RED}Loại lỗi: {type(e).__name__}{Colors.ENDC}")
            print(f"{Colors.RED}Chi tiết: {str(e)}{Colors.ENDC}")
            return False

    def logout(self):
        """Logout from the network device with detailed debug output"""
        print(f"\n{Colors.HEADER}{Colors.BOLD}{'='*70}{Colors.ENDC}")
        print(f"{Colors.HEADER}{Colors.BOLD}🚪 ĐANG THỰC HIỆN ĐĂNG XUẤT{Colors.ENDC}")
        print(f"{Colors.HEADER}{Colors.BOLD}{'='*70}{Colors.ENDC}")
        
        if not self.token:
            print(f"\n{Colors.RED}{Colors.BOLD}❌ LỖI: Không có token để đăng xuất{Colors.ENDC}")
            return False
            
        url = f"{self.base_url}{ENDPOINTS['logout']}"
        headers = {"Authorization": f"Bearer {self.token}"}
        
        self._print_request_details("POST", url, headers)
        
        try:
            print(f"\n{Colors.YELLOW}⏳ ĐANG GỬI REQUEST...{Colors.ENDC}")
            start_time = time.time()
            response = self.session.post(
                url,
                headers=headers,
                timeout=TIMEOUT,
                verify=False  # Disable SSL verification
            )
            end_time = time.time()
            
            self._print_response_details(response)
            print(f"\n{Colors.BLUE}⏱️ Thời gian phản hồi:{Colors.ENDC} {end_time - start_time:.2f}s")
            
            response.raise_for_status()
            self.token = None
            print(f"\n{Colors.GREEN}{Colors.BOLD}✅ ĐĂNG XUẤT THÀNH CÔNG!{Colors.ENDC}")
            return True
            
        except requests.exceptions.RequestException as e:
            print(f"\n{Colors.RED}{Colors.BOLD}❌ LỖI: Đăng xuất thất bại{Colors.ENDC}")
            print(f"{Colors.RED}Loại lỗi: {type(e).__name__}{Colors.ENDC}")
            print(f"{Colors.RED}Chi tiết: {str(e)}{Colors.ENDC}")
            return False

    def ping(self, host):
        """Ping a host with debug output"""
        if not self.token:
            print(f"{Colors.RED}{Colors.BOLD}❌ LỖI: Không có token để thực hiện ping{Colors.ENDC}")
            return None
            
        url = f"{self.base_url}{ENDPOINTS['ping']}"
        params = {"host": host}
        headers = {"Authorization": f"Bearer {self.token}"}
        
        self._print_request_details("GET", url, headers, params)
        
        try:
            print(f"\n{Colors.YELLOW}⏳ ĐANG GỬI REQUEST...{Colors.ENDC}")
            start_time = time.time()
            response = self.session.get(
                url,
                params=params,
                headers=headers,
                timeout=TIMEOUT,
                verify=False  # Disable SSL verification
            )
            end_time = time.time()
            
            self._print_response_details(response)
            print(f"\n{Colors.BLUE}⏱️ Thời gian phản hồi:{Colors.ENDC} {end_time - start_time:.2f}s")
            
            response.raise_for_status()
            return response.json()
            
        except requests.exceptions.RequestException as e:
            print(f"\n{Colors.RED}{Colors.BOLD}❌ LỖI: Ping thất bại{Colors.ENDC}")
            print(f"{Colors.RED}Loại lỗi: {type(e).__name__}{Colors.ENDC}")
            print(f"{Colors.RED}Chi tiết: {str(e)}{Colors.ENDC}")
            return None

    def change_ssid(self, new_ssid):
        """Change the SSID with debug output"""
        if not self.token:
            print(f"{Colors.RED}{Colors.BOLD}❌ LỖI: Không có token để thay đổi SSID{Colors.ENDC}")
            return False
            
        url = f"{self.base_url}{ENDPOINTS['ssid']}"
        data = {"ssid": new_ssid}
        headers = {"Authorization": f"Bearer {self.token}"}
        
        self._print_request_details("PUT", url, headers, data)
        
        try:
            print(f"\n{Colors.YELLOW}⏳ ĐANG GỬI REQUEST...{Colors.ENDC}")
            start_time = time.time()
            response = self.session.put(
                url,
                json=data,
                headers=headers,
                timeout=TIMEOUT,
                verify=False  # Disable SSL verification
            )
            end_time = time.time()
            
            self._print_response_details(response)
            print(f"\n{Colors.BLUE}⏱️ Thời gian phản hồi:{Colors.ENDC} {end_time - start_time:.2f}s")
            
            response.raise_for_status()
            return True
            
        except requests.exceptions.RequestException as e:
            print(f"\n{Colors.RED}{Colors.BOLD}❌ LỖI: Thay đổi SSID thất bại{Colors.ENDC}")
            print(f"{Colors.RED}Loại lỗi: {type(e).__name__}{Colors.ENDC}")
            print(f"{Colors.RED}Chi tiết: {str(e)}{Colors.ENDC}")
            return False

    def enable_mesh(self):
        """Enable mesh networking with debug output"""
        if not self.token:
            print(f"{Colors.RED}{Colors.BOLD}❌ LỖI: Không có token để bật mesh{Colors.ENDC}")
            return False
            
        url = f"{self.base_url}{ENDPOINTS['mesh']}"
        data = {"enabled": True}
        headers = {"Authorization": f"Bearer {self.token}"}
        
        self._print_request_details("POST", url, headers, data)
        
        try:
            print(f"\n{Colors.YELLOW}⏳ ĐANG GỬI REQUEST...{Colors.ENDC}")
            start_time = time.time()
            response = self.session.post(
                url,
                json=data,
                headers=headers,
                timeout=TIMEOUT,
                verify=False  # Disable SSL verification
            )
            end_time = time.time()
            
            self._print_response_details(response)
            print(f"\n{Colors.BLUE}⏱️ Thời gian phản hồi:{Colors.ENDC} {end_time - start_time:.2f}s")
            
            response.raise_for_status()
            return True
            
        except requests.exceptions.RequestException as e:
            print(f"\n{Colors.RED}{Colors.BOLD}❌ LỖI: Bật mesh thất bại{Colors.ENDC}")
            print(f"{Colors.RED}Loại lỗi: {type(e).__name__}{Colors.ENDC}")
            print(f"{Colors.RED}Chi tiết: {str(e)}{Colors.ENDC}")
            return False 