# Vietnam Administrative Units API

API đơn giản để tra cứu đơn vị hành chính Việt Nam (Tỉnh/Thành phố, Quận/Huyện, Xã/Phường) được xây dựng bằng FastAPI

Url test: [ https://api-provinces-vietnam-latest.onrender.com/docs]( https://api-provinces-vietnam-latest.onrender.com/docs)

## 📁 Cấu trúc thư mục

```
.
├── main.py
├── requirements.txt
├── README.md
├── Dockerfile
├── docker-compose.yml
├── docker-compose.dev.yml
├── .gitignore
├── .github/
    └── workflows/
        └──docker-build.yml
└── data/
    ├── tinh_tp.json
    ├── quan-huyen/
    │   ├── 01.json
    │   └── ...
    └── xa-phuong/
        ├── 001.json
        └── ...
```

## 🚀 Khởi động nhanh

### Bằng Python

```bash
pip install -r requirements.txt
uvicorn main:app --reload
```

Truy cập docs: [http://localhost:8000/docs](http://localhost:8000/docs)

### Bằng Docker

```bash
docker build -t api_provinces_vietnam .
docker run -p 8000:8000 api_provinces_vietnam
```

## 📚 Các API có sẵn

### ✅ Lấy danh sách cấp tỉnh

```
GET /api/provinces
```

### ✅ Lấy danh sách quận/huyện theo tỉnh

```
GET /api/districts/{province_code}
```

### ✅ Lấy danh sách xã/phường theo huyện

```
GET /api/wards/{district_code}
```

## 🔍 Tìm kiếm theo từng cấp

### Tìm tỉnh/thành phố

```
GET /api/search/provinces?q={keywords}
```

### Tìm quận/huyện

```
GET /api/search/districts?q={keywords}
```

### Tìm xã/phường

```
GET /api/search/wards?q={keywords}
```

## 📌 Tìm kiếm địa chỉ đầy đủ (tự động ghép tên cấp cha)

```
GET /api/search/full-address?q={keywords}
```

### Ví dụ kết quả:

```json
[
  {
    "level": "ward",
    "name": "Phường Trúc Bạch",
    "full_address": "Phường Trúc Bạch, Quận Ba Đình, Hà Nội"
  },
  {
    "level": "district",
    "name": "Quận Ba Đình",
    "full_address": "Quận Ba Đình, Hà Nội"
  },
  {
    "level": "province",
    "name": "Thành phố Hà Nội",
    "full_address": "Thành phố Hà Nội"
  }
]
```

## 📝 Ghi chú

- Dữ liệu được lấy từ repo: [https://github.com/sunrise1002/hanhchinhVN](https://github.com/sunrise1002/hanhchinhVN) (cập nhất đến 2017)
- Các mã `code` dùng để phân cấp: mã tỉnh → mã huyện → mã xã

## 📄 Giấy phép

MIT – Dùng thoải mái vì mục đích học tập, nghiên cứu hoặc tích hợp nội bộ.
