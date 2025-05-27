from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time

def test_login_basic():
    # Thông tin đăng nhập
    url = "http://192.168.19.1"
    username = "admin"
    password = "123456"
    
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
        # Khởi tạo Chrome driver
        driver = webdriver.Chrome(options=chrome_options)
        wait = WebDriverWait(driver, 10)
        
        print("\n=== TRUY CẬP TRANG ĐĂNG NHẬP ===")
        # Mở trang web
        driver.get(url)
        time.sleep(2)  # Đợi trang load
        
        print("\n=== ĐANG ĐĂNG NHẬP... ===")
        # Tìm và điền thông tin đăng nhập
        username_field = wait.until(EC.presence_of_element_located((By.ID, "username")))
        password_field = wait.until(EC.presence_of_element_located((By.ID, "password")))
        
        username_field.clear()
        username_field.send_keys(username)
        password_field.clear()
        password_field.send_keys(password)
        
        # Click nút đăng nhập
        login_button = wait.until(EC.element_to_be_clickable((By.XPATH, "//button[@type='submit']")))
        login_button.click()
        
        print("\n=== KIỂM TRA KẾT QUẢ ===")
        # Đợi và kiểm tra đăng nhập thành công
        try:
            # Đợi menu xuất hiện để xác nhận đăng nhập thành công
            wait.until(EC.presence_of_element_located((By.XPATH, "//div[contains(@class, 'menu')]")))
            print("✅ Đăng nhập thành công!")
            print("Đã tìm thấy menu sau khi đăng nhập")
            
        except Exception as e:
            print("❌ Đăng nhập thất bại!")
            print(f"Lý do: {str(e)}")
            # Chụp ảnh màn hình khi thất bại
            driver.save_screenshot("login_failure.png")
            assert False, "Đăng nhập thất bại"
            
    except Exception as e:
        print(f"\n❌ Lỗi: {str(e)}")
        if 'driver' in locals():
            driver.save_screenshot("error.png")
        raise
        
    finally:
        print("\n=== KẾT THÚC TEST ===")
        if 'driver' in locals():
            driver.quit() 