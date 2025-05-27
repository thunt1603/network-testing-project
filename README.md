# Network Testing Project

Project này được tạo ra để test các chức năng mạng cơ bản như login/logout, ping, thay đổi SSID, đổi mật khẩu, bật/tắt mesh, ...

## Cài đặt

1. Clone repository:
```bash
git clone [your-repository-url]
```

2. Cài đặt các dependencies:
```bash
pip install -r requirements.txt
```

## Cấu trúc Project

```
network_testing_project/
├── src/
│   ├── __init__.py
│   ├── config.py
│   └── network_utils.py
│
├── tests/
│   ├── __init__.py
│   ├── conftest.py
│   ├── test_login_basic.py
│   ├── test_ping.py
│   ├── test_basic_wifi.py
│   ├── test_changepassword.py
│   └── ...
│
├── .env
├── requirements.txt
├── README.md
├── .gitignore
```

- **src/**: Chứa code logic, API, config.
- **tests/**: Chứa toàn bộ các file test, mỗi chức năng một file.
- **.env**: Thông tin cấu hình, tài khoản, mật khẩu, URL...
- **requirements.txt**: Danh sách thư viện cần cài.
- **README.md**: Hướng dẫn sử dụng, cấu trúc, cách chạy test.
- **.gitignore**: Bỏ qua các file không cần thiết khi push lên git.

## Chạy toàn bộ test chỉ với một lệnh

Tại thư mục gốc project, chạy:
```bash
pytest -v --html=report.html
```
- Tất cả các bài test trong thư mục `tests/` sẽ được chạy tự động.
- Kết quả chi tiết sẽ hiển thị trên terminal và lưu vào file `report.html` (có thể mở bằng trình duyệt để xem báo cáo đẹp).

## Cấu hình

Tạo file `.env` trong thư mục gốc với các thông tin sau:
```
API_URL=your_api_url
USERNAME=your_username
PASSWORD=your_password
NEW_PASSWORD=your_new_password
```

## Lưu ý quản lý file
- **Không commit các file log, ảnh chụp màn hình lỗi, dữ liệu tạm thời lên git** (hãy thêm vào `.gitignore`).
- **Không để lộ file `.env` lên git** (hãy thêm `.env` vào `.gitignore`).
- **Sau khi đổi mật khẩu thành công, hãy cập nhật lại `PASSWORD` trong `.env` để các test sau không bị lỗi.** 