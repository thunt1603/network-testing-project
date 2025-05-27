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
from dotenv import load_dotenv
from pathlib import Path

# Thiết lập logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler("ping_test.log", encoding='utf-8'),
        logging.StreamHandler()
    ]
)

logger = logging.getLogger(__name__)

class TestPing(unittest.TestCase):
    def setUp(self):
        """Khởi tạo môi trường test"""
        try:
            # Khởi tạo logger
            self.logger = logging.getLogger(__name__)
            
            # Load thông tin từ file .env
            env_path = Path(__file__).parent.parent / '.env'
            print(f"\n[DEBUG] Loading .env from: {env_path}")
            load_dotenv(env_path, override=True)  # Force override existing env vars
            
            self.url = os.environ.get('API_URL')
            self.username = os.environ.get('USERNAME')
            self.password = os.environ.get('PASSWORD')
            
            print("\n=== THÔNG TIN ĐĂNG NHẬP ===")
            print(f"URL: {self.url}")
            print(f"Username: {self.username}")
            print(f"Password: {self.password}")
            
            chrome_options = Options()
            chrome_options.add_argument('--ignore-certificate-errors')
            chrome_options.add_argument('--ignore-ssl-errors')
            
            # Thêm thư mục user data duy nhất
            user_data_dir = os.path.join(os.getcwd(), "chrome_user_data")
            if not os.path.exists(user_data_dir):
                os.makedirs(user_data_dir)
            chrome_options.add_argument(f'--user-data-dir={user_data_dir}')
            
            # Sử dụng ChromeDriver local
            service = Service(executable_path="chromedriver.exe")
            self.driver = webdriver.Chrome(
                service=service,
                options=chrome_options
            )
            
            self.driver.maximize_window()
            self.driver.implicitly_wait(10)
            self.logger.info("Đã khởi tạo WebDriver thành công")
            
        except Exception as e:
            self.logger.error(f"Lỗi khởi tạo WebDriver: {str(e)}")
            raise

    def tearDown(self):
        """Dọn dẹp sau khi test"""
        if hasattr(self, 'driver'):
            self.driver.quit()
            self.logger.info("Đã đóng browser")

    def login(self):
        """Đăng nhập vào router"""
        try:
            self.driver.get(self.url)
            self.logger.info(f"Đã mở trang đăng nhập: {self.url}")
            
            time.sleep(2)  # Đợi trang load
            
            # Handle SSL warning if present
            try:
                advanced_button = WebDriverWait(self.driver, 20).until(
                    EC.element_to_be_clickable((By.ID, "advanced-button"))
                )
                advanced_button.click()
                self.logger.info("Đã click nút Advanced")
                
                proceed_button = WebDriverWait(self.driver, 20).until(
                    EC.element_to_be_clickable((By.ID, "proceed-link"))
                )
                proceed_button.click()
                self.logger.info("Đã click nút Proceed")
                time.sleep(2)
            except:
                self.logger.info("Không có cảnh báo SSL")

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
            self.logger.info("Đã nhập username")
            
            # Nhập password
            password_field = WebDriverWait(self.driver, 10).until(
                EC.presence_of_element_located((By.XPATH, "//input[@type='password']"))
            )
            password_field.clear()
            password_field.send_keys(self.password)
            self.logger.info("Đã nhập password")
            
            # Click nút login
            login_button = WebDriverWait(self.driver, 10).until(
                EC.element_to_be_clickable((By.XPATH, "//button[@type='submit']"))
            )
            login_button.click()
            self.logger.info("Đã click đăng nhập")
            
            # Đợi login thành công
            WebDriverWait(self.driver, 20).until(
                lambda driver: "network" in driver.current_url.lower() or
                len(driver.find_elements(By.XPATH, "//span[contains(text(), 'Network')]")) > 0
            )
            self.logger.info("Đã đăng nhập thành công")
            return True
            
        except Exception as e:
            self.logger.error(f"Lỗi đăng nhập: {str(e)}")
            if hasattr(self, 'driver'):
                self.driver.save_screenshot("login_failure.png")
            raise

    def configure_ping(self):
        """Cấu hình Ping"""
        try:
            # Navigate to Ping page
            self.driver.get(f"{self.url}/system/ping")
            self.logger.info("Đã điều hướng đến trang Ping")
            time.sleep(3)

            # Input Domain or IP address
            try:
                domain_input = WebDriverWait(self.driver, 10).until(
                    EC.presence_of_element_located((By.XPATH, "//label[contains(text(), 'Domain or IP address')]/../..//input"))
                )
                domain_input.clear()
                domain_input.send_keys("192.168.19.1")
                self.logger.info("Đã nhập Domain or IP address: 192.168.19.1")
                time.sleep(1)

            except Exception as e:
                self.logger.error(f"Lỗi khi nhập Domain or IP address: {str(e)}")
                self.driver.save_screenshot("domain_input_error.png")
                raise Exception("Không thể nhập Domain or IP address")

            # Select IP version
            try:
                # Find and click the IP version dropdown
                ip_version_container = WebDriverWait(self.driver, 10).until(
                    EC.presence_of_element_located((By.XPATH, "//label[contains(text(), 'IP version')]/ancestor::div[contains(@class, 'ant-form-item')]"))
                )
                self.logger.info("Đã tìm thấy container của IP version")
                
                # Click the dropdown
                select_element = ip_version_container.find_element(By.XPATH, ".//div[contains(@class, 'ant-select-selector')]")
                self.driver.execute_script("arguments[0].scrollIntoView(true);", select_element)
                time.sleep(1)
                
                # Try different click methods
                try:
                    select_element.click()
                except:
                    try:
                        self.driver.execute_script("arguments[0].click();", select_element)
                    except:
                        actions = ActionChains(self.driver)
                        actions.move_to_element(select_element).click().perform()
                
                self.logger.info("Đã click vào dropdown IP version")
                time.sleep(2)

                # Find and click IPv4 option
                try:
                    # Wait for dropdown to be visible
                    dropdown = WebDriverWait(self.driver, 10).until(
                        EC.visibility_of_element_located((By.XPATH, "//div[contains(@class, 'ant-select-dropdown')]"))
                    )
                    self.logger.info("Dropdown đã hiển thị")

                    # Find and click IPv4 option
                    ipv4_option = dropdown.find_element(By.XPATH, ".//div[contains(@class, 'ant-select-item')]//div[text()='IPv4']")
                    self.driver.execute_script("arguments[0].click();", ipv4_option)
                    self.logger.info("Đã chọn IP version: IPv4")
                    time.sleep(2)

                except Exception as e:
                    self.logger.error(f"Lỗi khi chọn IP version: {str(e)}")
                    self.driver.save_screenshot("ip_version_selection_error.png")
                    raise Exception("Không thể chọn IP version")

            except Exception as e:
                self.logger.error(f"Lỗi khi cấu hình IP version: {str(e)}")
                self.driver.save_screenshot("ip_version_error.png")
                raise Exception("Không thể cấu hình IP version")

            # Input Source IP Address
            try:
                # Print page source for debugging
                self.logger.info("Current page source:")
                self.logger.info(self.driver.page_source[:1000])  # Print first 1000 chars
                
                # Try different selectors with longer wait time
                try:
                    source_ip = WebDriverWait(self.driver, 20).until(
                        EC.presence_of_element_located((By.XPATH, "//input[contains(@placeholder, 'Source IP')]"))
                    )
                except:
                    try:
                        source_ip = WebDriverWait(self.driver, 20).until(
                            EC.presence_of_element_located((By.XPATH, "//div[contains(@class, 'ant-form-item')]//input[contains(@placeholder, 'Source')]"))
                        )
                    except:
                        source_ip = WebDriverWait(self.driver, 20).until(
                            EC.presence_of_element_located((By.XPATH, "//input[contains(@id, 'source') or contains(@name, 'source')]"))
                        )
                
                self.logger.info("Đã tìm thấy Source IP input field")
                source_ip.clear()
                source_ip.send_keys("192.168.19.2")
                self.logger.info("Đã nhập Source IP Address: 192.168.19.2")
                time.sleep(1)

            except Exception as e:
                self.logger.error(f"Lỗi khi nhập Source IP Address: {str(e)}")
                self.driver.save_screenshot("source_ip_error.png")
                raise Exception("Không thể nhập Source IP Address")

            # Click Submit button
            try:
                submit_button = WebDriverWait(self.driver, 20).until(
                    EC.element_to_be_clickable((By.XPATH, "//button[@type='submit']"))
                )
                self.logger.info(f"Submit button state - Enabled: {submit_button.is_enabled()}, Displayed: {submit_button.is_displayed()}")
                
                # Click submit button
                submit_button.click()
                self.logger.info("Đã click nút Submit")
                
                # Wait for ping results
                time.sleep(5)  # Wait for ping to complete
                
                # Check for ping results
                try:
                    results = WebDriverWait(self.driver, 30).until(
                        EC.presence_of_element_located((By.XPATH, "//div[contains(@class, 'ping-results') or contains(@class, 'result')]"))
                    )
                    self.logger.info(f"Ping results: {results.text}")
                except:
                    self.logger.warning("Không tìm thấy kết quả ping")

            except Exception as e:
                self.logger.error(f"Lỗi khi thực hiện ping: {str(e)}")
                self.driver.save_screenshot("ping_error.png")
                raise Exception("Không thể thực hiện ping")

        except Exception as e:
            self.logger.error(f"Lỗi khi cấu hình ping: {str(e)}")
            self.driver.save_screenshot("ping_config_error.png")
            raise

    def test_ping(self):
        """Test chức năng Ping"""
        try:
            self.login()
            self.configure_ping()
            self.logger.info("✓ Test chức năng Ping thành công")
        except Exception as e:
            self.logger.error(f"✗ Lỗi trong quá trình test: {str(e)}")
            if hasattr(self, 'driver'):
                self.driver.save_screenshot("error_screenshot.png")
            raise e

if __name__ == '__main__':
    unittest.main() 