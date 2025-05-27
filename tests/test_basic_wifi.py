from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import logging
from selenium.webdriver.common.action_chains import ActionChains
import unittest
from selenium.common.exceptions import TimeoutException
import os
from selenium.webdriver.chrome.service import Service as ChromeService
import requests
from requests.exceptions import RequestException
from dotenv import load_dotenv
from pathlib import Path

# Thiết lập logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler("basic_wifi_test.log", encoding='utf-8'),
        logging.StreamHandler()
    ]
)

logger = logging.getLogger(__name__)

class TestBasicWifi(unittest.TestCase):
    def setUp(self):
        """Khởi tạo môi trường test"""
        try:
            # Load thông tin từ file .env
            env_path = Path(__file__).parent.parent / '.env'
            print(f"\n[DEBUG] Loading .env from: {env_path}")
            load_dotenv(env_path, override=True)  # Force override existing env vars
            self.url = os.environ.get('API_URL')
            self.username = os.environ.get('USERNAME')
            self.password = os.environ.get('PASSWORD')
            
            chrome_options = Options()
            chrome_options.add_argument('--ignore-certificate-errors')
            chrome_options.add_argument('--ignore-ssl-errors')
            
            # Sử dụng ChromeDriver local
            service = Service(executable_path="chromedriver.exe")
            self.driver = webdriver.Chrome(
                service=service,
                options=chrome_options
            )
            
            self.driver.maximize_window()
            self.driver.implicitly_wait(10)
            logger.info("Đã khởi tạo WebDriver thành công")
            
        except Exception as e:
            logger.error(f"Lỗi khởi tạo WebDriver: {str(e)}")
            raise

    def tearDown(self):
        """Dọn dẹp sau khi test"""
        if hasattr(self, 'driver'):
            self.driver.quit()
            logger.info("Đã đóng browser")

    def login(self):
        """Đăng nhập vào router"""
        try:
            self.driver.get(self.url)
            logger.info(f"Đã mở trang đăng nhập: {self.url}")
            
            time.sleep(2)  # Đợi trang load
            
            # Handle SSL warning if present
            try:
                advanced_button = WebDriverWait(self.driver, 20).until(
                    EC.element_to_be_clickable((By.ID, "advanced-button"))
                )
                advanced_button.click()
                logger.info("Đã click nút Advanced")
                
                proceed_button = WebDriverWait(self.driver, 20).until(
                    EC.element_to_be_clickable((By.ID, "proceed-link"))
                )
                proceed_button.click()
                logger.info("Đã click nút Proceed")
                time.sleep(2)
            except:
                logger.info("Không có cảnh báo SSL")

            # Đợi form login xuất hiện
            WebDriverWait(self.driver, 20).until(
                EC.presence_of_element_located((By.TAG_NAME, "form"))
            )
            
            # Nhập username
            username_field = WebDriverWait(self.driver, 10).until(
                EC.presence_of_element_located((By.XPATH, "//div[contains(@class, 'ant-form-item')]//input[1]"))
            )
            username_field.clear()
            username_field.send_keys(self.username)
            logger.info("Đã nhập username")
            
            # Nhập password
            password_field = WebDriverWait(self.driver, 10).until(
                EC.presence_of_element_located((By.XPATH, "//input[@type='password']"))
            )
            password_field.clear()
            password_field.send_keys(self.password)
            logger.info("Đã nhập password")
            
            # Click nút login
            login_button = WebDriverWait(self.driver, 10).until(
                EC.element_to_be_clickable((By.XPATH, "//button[@type='submit']"))
            )
            login_button.click()
            logger.info("Đã click đăng nhập")
            
            # Đợi login thành công
            WebDriverWait(self.driver, 20).until(
                lambda driver: "network" in driver.current_url.lower() or
                len(driver.find_elements(By.XPATH, "//span[contains(text(), 'Network')]")) > 0
            )
            logger.info("Đã đăng nhập thành công")
            return True
            
        except Exception as e:
            logger.error(f"Lỗi đăng nhập: {str(e)}")
            if hasattr(self, 'driver'):
                self.driver.save_screenshot("login_failure.png")
            raise

    def check_and_disable_mesh(self):
        """Kiểm tra và tắt Mesh nếu đang bật"""
        try:
            # Điều hướng đến trang Mesh
            self.driver.get(f"{self.url}/network/mesh")
            logger.info("Đã điều hướng đến trang Mesh")
            time.sleep(2)

            # Đợi cho trang Mesh load hoàn tất
            WebDriverWait(self.driver, 20).until(
                lambda driver: "network/mesh" in driver.current_url.lower()
            )

            # Tìm status switch
            status_switch = WebDriverWait(self.driver, 10).until(
                EC.presence_of_element_located((By.XPATH, "//button[contains(@class, 'ant-switch')]"))
            )

            # Kiểm tra trạng thái của switch
            is_enabled = 'ant-switch-checked' in status_switch.get_attribute('class')
            if is_enabled:
                # Click để tắt Mesh
                status_switch.click()
                logger.info("Đã tắt Mesh Status")
                time.sleep(2)

                # Submit form
                submit_button = WebDriverWait(self.driver, 10).until(
                    EC.element_to_be_clickable((By.XPATH, "//button[@type='submit']"))
                )
                submit_button.click()
                logger.info("Đã submit form tắt Mesh")

                # Đợi thông báo thành công
                try:
                    success_message = WebDriverWait(self.driver, 10).until(
                        EC.presence_of_element_located((By.XPATH, "//div[contains(@class, 'ant-message')]"))
                    )
                    logger.info("Đã tắt Mesh thành công")
                except:
                    logger.warning("Không tìm thấy thông báo sau khi tắt Mesh")
            else:
                logger.info("Mesh Status đã tắt sẵn")

            return True

        except Exception as e:
            logger.error(f"Lỗi khi kiểm tra và tắt Mesh: {str(e)}")
            self.driver.save_screenshot("mesh_disable_error.png")
            raise

    def configure_basic_wifi(self):
        """Cấu hình Basic Wireless"""
        try:
            # Điều hướng đến trang Basic Wireless
            self.driver.get(f"{self.url}/network/basicwifi")
            logger.info("Đã điều hướng đến trang Basic Wireless")
            time.sleep(2)

            # Đợi cho trang load hoàn tất
            WebDriverWait(self.driver, 20).until(
                lambda driver: "network/basicwifi" in driver.current_url.lower()
            )

            # Tìm và xóa SSID cũ, nhập SSID mới
            ssid_field = WebDriverWait(self.driver, 10).until(
                EC.presence_of_element_located((By.XPATH, "//input[@id='ssid']"))
            )
            ssid_field.click()
            ssid_field.send_keys(Keys.CONTROL + "a")  # Select all
            ssid_field.send_keys(Keys.DELETE)  # Delete selected text
            time.sleep(1)
            ssid_field.send_keys("Lancsnet_HT")
            logger.info("Đã cập nhật SSID")

            # Tìm và xóa password cũ, nhập password mới
            password_field = WebDriverWait(self.driver, 10).until(
                EC.presence_of_element_located((By.XPATH, "//input[@type='password']"))
            )
            password_field.click()
            password_field.send_keys(Keys.CONTROL + "a")
            password_field.send_keys(Keys.DELETE)
            time.sleep(1)
            password_field.send_keys("123456789")
            logger.info("Đã cập nhật password")

            # Submit form
            submit_button = WebDriverWait(self.driver, 10).until(
                EC.element_to_be_clickable((By.XPATH, "//button[@type='submit']"))
            )
            submit_button.click()
            logger.info("Đã submit form")

            # Đợi thông báo thành công
            try:
                success_message = WebDriverWait(self.driver, 10).until(
                    EC.presence_of_element_located((By.XPATH, "//div[contains(@class, 'ant-message')]"))
                )
                logger.info("Đã cập nhật Basic Wireless thành công")
                return True
            except TimeoutException:
                raise Exception("Không nhận được thông báo thành công sau khi submit")

        except Exception as e:
            logger.error(f"Lỗi khi cấu hình Basic Wireless: {str(e)}")
            self.driver.save_screenshot("basic_wifi_error.png")
            raise

    def test_basic_wifi(self):
        """Test chức năng Basic Wireless"""
        try:
            # Login thành công
            self.login()
            logger.info("Đăng nhập thành công")

            # Kiểm tra và tắt Mesh nếu cần
            self.check_and_disable_mesh()
            logger.info("Đã kiểm tra và xử lý Mesh Status")
            time.sleep(2)

            # Cấu hình Basic Wireless
            self.configure_basic_wifi()
            logger.info("✓ Test cấu hình Basic Wireless thành công")

        except Exception as e:
            logger.error(f"✗ Lỗi trong quá trình test: {str(e)}")
            if hasattr(self, 'driver'):
                self.driver.save_screenshot("error_screenshot.png")
            raise e

def test_basic_wifi():
    # Load thông tin từ file .env
    env_path = Path(__file__).parent.parent / '.env'
    print(f"\n[DEBUG] Loading .env from: {env_path}")
    load_dotenv(env_path, override=True)  # Force override existing env vars
    
    url = os.environ.get('API_URL')  # Use environ instead of getenv
    username = os.environ.get('USERNAME')
    password = os.environ.get('PASSWORD')
    
    print("\n=== THÔNG TIN ĐĂNG NHẬP ===")
    print(f"URL: {url}")
    print(f"Username: {username}")
    print(f"Password: {password}")
    
    # Thiết lập Chrome options
    chrome_options = Options()
    chrome_options.add_argument('--ignore-certificate-errors')
    chrome_options.add_argument('--ignore-ssl-errors')
    chrome_options.add_argument('--start-maximized')
    
    try:
        print("\n=== KHỞI TẠO CHROME DRIVER ===")
        driver = webdriver.Chrome(options=chrome_options)
        wait = WebDriverWait(driver, 10)
        
        print("\n=== TRUY CẬP TRANG ĐĂNG NHẬP ===")
        driver.get(url)
        time.sleep(2)
        
        print("\n=== ĐANG ĐĂNG NHẬP... ===")
        # Đăng nhập
        username_field = wait.until(EC.presence_of_element_located((By.ID, "username")))
        password_field = wait.until(EC.presence_of_element_located((By.ID, "password")))
        
        username_field.clear()
        username_field.send_keys(username)
        password_field.clear()
        password_field.send_keys(password)
        
        login_button = wait.until(EC.element_to_be_clickable((By.XPATH, "//button[@type='submit']")))
        login_button.click()
        
        print("\n=== KIỂM TRA ĐĂNG NHẬP ===")
        # Đợi menu xuất hiện
        wait.until(EC.presence_of_element_located((By.XPATH, "//div[contains(@class, 'menu')]")))
        print("✅ Đăng nhập thành công!")
        
        print("\n=== KIỂM TRA THÔNG TIN WIFI ===")
        # Click vào menu WiFi
        wifi_menu = wait.until(EC.element_to_be_clickable((By.XPATH, "//span[contains(text(), 'WiFi')]")))
        wifi_menu.click()
        time.sleep(2)
        
        # Kiểm tra các thông tin WiFi
        try:
            # Kiểm tra SSID
            ssid_element = wait.until(EC.presence_of_element_located((By.XPATH, "//div[contains(text(), 'SSID')]")))
            print(f"✅ Tìm thấy SSID: {ssid_element.text}")
            
            # Kiểm tra trạng thái WiFi
            wifi_status = wait.until(EC.presence_of_element_located((By.XPATH, "//div[contains(text(), 'Status')]")))
            print(f"✅ Trạng thái WiFi: {wifi_status.text}")
            
            # Kiểm tra số lượng thiết bị kết nối
            connected_devices = wait.until(EC.presence_of_element_located((By.XPATH, "//div[contains(text(), 'Connected Devices')]")))
            print(f"✅ Số thiết bị đang kết nối: {connected_devices.text}")
            
            print("\n✅ Kiểm tra WiFi thành công!")
            
        except Exception as e:
            print("❌ Lỗi khi kiểm tra thông tin WiFi!")
            print(f"Lý do: {str(e)}")
            driver.save_screenshot("wifi_check_failure.png")
            assert False, "Kiểm tra WiFi thất bại"
            
    except Exception as e:
        print(f"\n❌ Lỗi: {str(e)}")
        if 'driver' in locals():
            driver.save_screenshot("error.png")
        raise
        
    finally:
        print("\n=== KẾT THÚC TEST ===")
        if 'driver' in locals():
            driver.quit()

if __name__ == '__main__':
    test_basic_wifi() 