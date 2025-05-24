# Network Testing Project

Project này được tạo ra để test các chức năng mạng cơ bản như login/logout, ping, thay đổi SSID và bật mesh.

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
├── tests/
│   ├── test_login.py
│   ├── test_ping.py
│   ├── test_ssid.py
│   └── test_mesh.py
├── src/
│   ├── __init__.py
│   ├── network_utils.py
│   └── config.py
├── requirements.txt
└── README.md
```

## Chạy Tests

Để chạy tất cả các tests:
```bash
pytest
```

Để chạy test cụ thể:
```bash
pytest tests/test_login.py
```

## Cấu hình

Tạo file `.env` trong thư mục gốc với các thông tin sau:
```
API_URL=your_api_url
USERNAME=your_username
PASSWORD=your_password
``` 