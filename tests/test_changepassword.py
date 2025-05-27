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
from dotenv import load_dotenv
from pathlib import Path

# Thiết lập logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler("change_password_test.log", encoding='utf-8'),
        logging.StreamHandler()
    ]
)

logger = logging.getLogger(__name__)

class TestChangePassword(unittest.TestCase):
    def setUp(self):
        """Khởi tạo môi trường test"""
        try:
            # Khởi tạo logger
            self.logger = logging.getLogger(__name__)
            # Load .env
            env_path = Path(__file__).parent.parent / '.env'
            print(f"\n[DEBUG] Loading .env from: {env_path}")
            load_dotenv(env_path, override=True)
            self.url = os.environ.get('API_URL')
            self.username = os.environ.get('USERNAME')
            self.password = os.environ.get('PASSWORD')
            self.new_password = os.environ.get('NEW_PASSWORD', '1234567')
            print(f"[DEBUG] url={self.url}, username={self.username}, password={self.password}, new_password={self.new_password}")
            chrome_options = Options()
            chrome_options.add_argument('--ignore-certificate-errors')
            chrome_options.add_argument('--ignore-ssl-errors')
            user_data_dir = os.path.join(os.getcwd(), "chrome_user_data")
            if not os.path.exists(user_data_dir):
                os.makedirs(user_data_dir)
            chrome_options.add_argument(f'--user-data-dir={user_data_dir}')
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
            logger.info("Đã đóng browser")

    def login(self):
        """Đăng nhập vào router"""
        try:
            self.driver.get(self.url)
            logger.info(f"Đã mở trang đăng nhập: {self.url}")
            time.sleep(2)
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
            WebDriverWait(self.driver, 20).until(
                EC.presence_of_element_located((By.TAG_NAME, "form"))
            )
            username_field = WebDriverWait(self.driver, 10).until(
                EC.presence_of_element_located((By.XPATH, "//div[contains(@class, 'ant-form-item')]//input[1]"))
            )
            username_field.clear()
            username_field.send_keys(self.username)
            logger.info("Đã nhập username")
            password_field = WebDriverWait(self.driver, 10).until(
                EC.presence_of_element_located((By.XPATH, "//input[@type='password']"))
            )
            password_field.clear()
            password_field.send_keys(self.password)
            logger.info("Đã nhập password")
            login_button = WebDriverWait(self.driver, 10).until(
                EC.element_to_be_clickable((By.XPATH, "//button[@type='submit']"))
            )
            login_button.click()
            logger.info("Đã click đăng nhập")
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

    def change_password(self):
        """Thay đổi mật khẩu"""
        try:
            self.driver.get(f"{self.url}/system/system")
            self.logger.info("Đã điều hướng đến trang System Settings")
            time.sleep(3)
            try:
                tab_container = WebDriverWait(self.driver, 10).until(
                    EC.presence_of_element_located((By.XPATH, "//div[contains(@class, 'ant-tabs-nav')]"))
                )
                self.logger.info("Đã tìm thấy container của tabs")
                change_password_tab = WebDriverWait(self.driver, 10).until(
                    EC.element_to_be_clickable((By.XPATH, "//div[text()='Change Password']"))
                )
                try:
                    change_password_tab.click()
                except:
                    try:
                        self.driver.execute_script("arguments[0].click();", change_password_tab)
                    except:
                        actions = ActionChains(self.driver)
                        actions.move_to_element(change_password_tab).click().perform()
                self.logger.info("Đã click vào tab Change Password")
                time.sleep(2)
            except Exception as e:
                self.logger.error(f"Lỗi khi click tab Change Password: {str(e)}")
                self.driver.save_screenshot("change_password_tab_error.png")
                raise Exception("Không thể click vào tab Change Password")
            # Input Current Password
            try:
                current_password = WebDriverWait(self.driver, 10).until(
                    EC.presence_of_element_located((By.XPATH, "//label[contains(text(), 'Current Password')]/../..//input[@type='password']"))
                )
                current_password.clear()
                current_password.send_keys(self.password)
                self.logger.info("Đã nhập Current Password")
                time.sleep(1)
            except Exception as e:
                self.logger.error(f"Lỗi khi nhập Current Password: {str(e)}")
                self.driver.save_screenshot("current_password_error.png")
                raise Exception("Không thể nhập Current Password")
            # Input New Password
            try:
                new_password = WebDriverWait(self.driver, 10).until(
                    EC.presence_of_element_located((By.XPATH, "//label[contains(text(), 'New Password')]/../..//input[@type='password']"))
                )
                new_password.clear()
                new_password.send_keys(self.new_password)
                self.logger.info("Đã nhập New Password")
                time.sleep(1)
            except Exception as e:
                self.logger.error(f"Lỗi khi nhập New Password: {str(e)}")
                self.driver.save_screenshot("new_password_error.png")
                raise Exception("Không thể nhập New Password")
            # Input Confirm New Password
            try:
                confirm_password = WebDriverWait(self.driver, 10).until(
                    EC.presence_of_element_located((By.XPATH, "//label[contains(text(), 'Confirm New Password')]/../..//input[@type='password']"))
                )
                confirm_password.clear()
                confirm_password.send_keys(self.new_password)
                self.logger.info("Đã nhập Confirm New Password")
                time.sleep(1)
            except Exception as e:
                self.logger.error(f"Lỗi khi nhập Confirm New Password: {str(e)}")
                self.driver.save_screenshot("confirm_password_error.png")
                raise Exception("Không thể nhập Confirm New Password")
            # Submit form
            try:
                submit_button = None
                submit_xpaths = [
                    "//button[contains(@class, 'ant-btn') and contains(@class, 'ant-btn-primary')]",
                    "//div[contains(@class, 'ant-tabs-tabpane-active')]//button[contains(@class, 'ant-btn-primary')]",
                    "//div[contains(@class, 'ant-tabs-content')]//button[contains(@class, 'ant-btn-primary')]",
                    "//div[contains(@class, 'ant-tabs-tabpane-active')]//button[text()='Submit']",
                    "//button[contains(@class, 'ant-btn-primary') and text()='Submit']"
                ]
                try:
                    active_tab = self.driver.find_element(By.XPATH, "//div[contains(@class, 'ant-tabs-tabpane-active')]")
                    self.logger.info(f"Active tab content: {active_tab.get_attribute('outerHTML')}")
                except:
                    self.logger.warning("Không thể lấy nội dung của tab hiện tại")
                for xpath in submit_xpaths:
                    try:
                        self.logger.info(f"Thử tìm nút Submit với XPath: {xpath}")
                        submit_button = WebDriverWait(self.driver, 5).until(
                            EC.element_to_be_clickable((By.XPATH, xpath))
                        )
                        if submit_button and submit_button.is_displayed():
                            self.logger.info(f"Tìm thấy nút Submit với XPath: {xpath}")
                            break
                    except:
                        continue
                if not submit_button:
                    buttons = self.driver.find_elements(By.XPATH, "//button")
                    self.logger.info(f"Tổng số buttons trên trang: {len(buttons)}")
                    for idx, btn in enumerate(buttons):
                        try:
                            self.logger.info(f"Button {idx + 1}: Text='{btn.text}', Class='{btn.get_attribute('class')}', Visible={btn.is_displayed()}")
                        except:
                            pass
                    raise Exception("Không tìm thấy nút Submit")
                self.driver.execute_script("arguments[0].scrollIntoView(true);", submit_button)
                time.sleep(1)
                self.logger.info(f"Submit button state - Enabled: {submit_button.is_enabled()}, Displayed: {submit_button.is_displayed()}")
                self.logger.info(f"Submit button HTML: {submit_button.get_attribute('outerHTML')}")
                try:
                    submit_button.click()
                except:
                    try:
                        self.driver.execute_script("arguments[0].click();", submit_button)
                    except:
                        try:
                            actions = ActionChains(self.driver)
                            actions.move_to_element(submit_button).click().perform()
                        except:
                            location = submit_button.location
                            size = submit_button.size
                            x = location['x'] + size['width'] // 2
                            y = location['y'] + size['height'] // 2
                            actions = ActionChains(self.driver)
                            actions.move_by_offset(x, y).click().perform()
                self.logger.info("Đã click nút Submit")
                success_message = WebDriverWait(self.driver, 30).until(
                    EC.presence_of_element_located((By.XPATH, "//div[contains(@class, 'ant-message-success') or contains(@class, 'success')]"))
                )
                self.logger.info(f"Success message: {success_message.text}")
                self.logger.info("Thay đổi mật khẩu thành công")
            except Exception as e:
                self.logger.error(f"Lỗi khi submit form: {str(e)}")
                self.driver.save_screenshot("submit_error.png")
                raise Exception("Không thể submit form")
        except Exception as e:
            self.logger.error(f"Lỗi khi thay đổi mật khẩu: {str(e)}")
            self.driver.save_screenshot("change_password_error.png")
            raise

    def test_change_password(self):
        """Test chức năng thay đổi mật khẩu"""
        try:
            self.login()
            self.change_password()
            self.logger.info("✓ Test thay đổi mật khẩu thành công")
        except Exception as e:
            self.logger.error(f"✗ Lỗi trong quá trình test: {str(e)}")
            if hasattr(self, 'driver'):
                self.driver.save_screenshot("error_screenshot.png")
            raise e

def test_change_password_api():
    """
    Test đổi mật khẩu qua API (nếu có)
    """
    from dotenv import load_dotenv
    from pathlib import Path
    import os
    env_path = Path(__file__).parent.parent / '.env'
    load_dotenv(env_path, override=True)
    url = os.environ.get('API_URL')
    old_password = os.environ.get('PASSWORD')
    new_password = os.environ.get('NEW_PASSWORD', '1234567')
    change_password_url = f"{url}/system/change_password"
    password_data = {
        "old_password": old_password,
        "new_password": new_password
    }
    try:
        response = requests.post(change_password_url, data=password_data)
        if response.status_code == 200:
            print("Đổi mật khẩu thành công qua API!")
            return True
        print(f"Đổi mật khẩu thất bại! Status: {response.status_code}, Response: {response.text}")
        return False
    except Exception as e:
        print(f"Lỗi khi test đổi mật khẩu API: {str(e)}")
        return False

if __name__ == '__main__':
    unittest.main() 