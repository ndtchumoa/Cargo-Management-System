# 🚚 Cargo Management System

A full-stack logistics cargo management system with REST API, analytics dashboard, and route optimization.

![License](https://img.shields.io/badge/license-MIT-blue.svg)
![Python](https://img.shields.io/badge/Python-3.13+-3776AB?logo=python&logoColor=white)
![FastAPI](https://img.shields.io/badge/FastAPI-0.115-009688?logo=fastapi&logoColor=white)
![React](https://img.shields.io/badge/React-18+-61DAFB?logo=react&logoColor=black)
![MySQL](https://img.shields.io/badge/MySQL-8.0-4479A1?logo=mysql&logoColor=white)
![Tests](https://img.shields.io/badge/tests-73%20passed-22c55e)
![Deploy](https://img.shields.io/badge/deploy-Railway%20%2B%20Vercel-black)

---

## 🚀 Live Demo

| | URL |
|---|---|
| **Frontend** | https://cargo-management-system-iz5o.vercel.app |
| **API Docs** | https://cargo-management-system-production-4399.up.railway.app/docs |
| **Health Check** | https://cargo-management-system-production-4399.up.railway.app/health |

---

## 📋 Tổng quan

Hệ thống quản lý vận chuyển hàng hóa toàn diện, được xây dựng dựa trên cơ sở dữ liệu `cargo_db` gồm 10 bảng, hỗ trợ các nghiệp vụ:

- Quản lý đơn hàng, hóa đơn, khách hàng
- Theo dõi hành trình vận chuyển theo từng chặng
- Phân công tài xế và phương tiện
- Tối ưu hóa lộ trình bằng thuật toán Dijkstra
- Dashboard phân tích doanh thu và vận hành
- Phân quyền theo vai trò (nhân viên / quản lý / kế toán)
- JWT Authentication với role-based access control

---

## 🏗️ Kiến trúc hệ thống

```
┌─────────────────────────────────────┐
│         FRONTEND (React + Recharts) │
│  Dashboard · Tracking · Optimizer   │
└────────────────┬────────────────────┘
                 │ REST API (HTTP/JSON)
┌────────────────▼────────────────────┐
│         BACKEND (FastAPI)           │
│  /orders · /invoices · /analytics   │
│  /routes · /assignments · /optimize │
│  /auth (JWT)                        │
└────────────────┬────────────────────┘
                 │ SQLAlchemy ORM
┌────────────────▼────────────────────┐
│         DATABASE (MySQL 8.0)        │
│  10 tables · Triggers · Views       │
│  Stored Procedures · Role-based ACL │
└────────────────┬────────────────────┘
                 │ NetworkX
┌────────────────▼────────────────────┐
│         ANALYTICS / AI LAYER        │
│  Dijkstra route optimization        │
└─────────────────────────────────────┘
```

---

## 🗂️ Cấu trúc thư mục

```
Cargo-Management-System/
├── backend/
│   ├── app/
│   │   ├── main.py
│   │   ├── config.py
│   │   ├── database.py
│   │   ├── dependencies.py
│   │   ├── models/
│   │   ├── routers/
│   │   ├── schemas/
│   │   └── services/
│   ├── tests/                  # 73 unit tests
│   ├── requirements.txt
│   ├── railway.json
│   └── .env.example
├── frontend/
│   ├── src/
│   │   ├── pages/
│   │   ├── components/
│   │   └── api/
│   ├── vercel.json
│   └── package.json
├── database/
│   ├── schema/CreateTab.sql
│   ├── data/InsertData.sql
│   ├── functions/
│   └── triggers/
└── docs/
    └── api-spec.md
```

---

## ⚙️ Cài đặt và chạy local

### Yêu cầu hệ thống

| Công cụ | Phiên bản |
|---|---|
| Python | 3.13 |
| Node.js | 18+ |
| MySQL | 8.0+ |

### 1. Clone repository

```bash
git clone https://github.com/ndtchumoa/Cargo-Management-System.git
cd Cargo-Management-System
```

### 2. Khởi tạo database

```bash
mysql -u root -p < database/schema/CreateTab.sql
mysql -u root -p cargo_db < database/data/InsertData.sql
mysql -u root -p cargo_db < database/functions/Func_calCOD.sql
mysql -u root -p cargo_db < database/functions/Func_showDH.sql
mysql -u root -p cargo_db < database/functions/Func_View.sql
mysql -u root -p cargo_db < database/functions/Func_Role.sql
mysql -u root -p cargo_db < database/triggers/trigger1.sql
mysql -u root -p cargo_db < database/triggers/trigger2.sql
```

### 3. Chạy backend

```bash
cd backend
python -m venv venv
venv\Scripts\activate        # Windows
# source venv/bin/activate   # Linux/Mac
pip install -r requirements.txt
cp .env.example .env         # Điền thông tin database vào .env
uvicorn app.main:app --reload
```

API: `http://localhost:8000`  
Swagger UI: `http://localhost:8000/docs`

### 4. Chạy frontend

```bash
cd frontend
npm install
cp .env.example .env         # Điền VITE_API_URL=http://localhost:8000
npm run dev
```

Dashboard: `http://localhost:5173`

### 5. Chạy unit tests

```bash
cd backend
python -m pytest -v
# 73 passed
```

---

## 🔌 API Endpoints

| Method | Endpoint | Mô tả |
|---|---|---|
| `POST` | `/api/auth/login` | Đăng nhập lấy JWT token |
| `GET` | `/api/auth/me` | Thông tin người dùng hiện tại |
| `GET` | `/api/orders` | Danh sách đơn hàng, filter theo trạng thái |
| `POST` | `/api/orders` | Tạo đơn hàng mới, tự tính COD |
| `GET` | `/api/orders/{id}` | Chi tiết 1 đơn hàng |
| `PATCH` | `/api/orders/{id}/status` | Cập nhật trạng thái đơn |
| `GET` | `/api/orders/{id}/tracking` | Lịch sử vận chuyển |
| `GET` | `/api/invoices` | Danh sách hóa đơn |
| `POST` | `/api/invoices` | Tạo hóa đơn từ nhiều đơn hàng |
| `POST` | `/api/assignments` | Phân công tài xế + phương tiện |
| `GET` | `/api/analytics/revenue` | Doanh thu theo tháng |
| `GET` | `/api/analytics/return-rate` | Tỉ lệ hoàn trả theo lộ trình |
| `GET` | `/api/analytics/top-routes` | Top lộ trình nhiều đơn nhất |
| `GET` | `/api/analytics/top-customers` | Top khách hàng gửi nhiều nhất |
| `POST` | `/api/optimize/route` | Tối ưu lộ trình (Dijkstra) |

---

## 🧠 Route Optimization

Thuật toán **Dijkstra** trên đồ thị có hướng được xây từ bảng `CHANG_DUONG`:

```json
POST /api/optimize/route
{
  "from_dtc": "DTC001",
  "to_dtc":   "DTC005",
  "weight_kg": 5.0
}

// Response
{
  "path": ["DTC001", "DTC002", "DTC003", "DTC005"],
  "path_names": ["Kho Hà Nội", "Kho Đà Nẵng", "Kho TP.HCM", "Kho Cần Thơ"],
  "total_km": 2100,
  "estimated_cod": 1485000,
  "available_vehicles": [
    { "bien_so": "29B-67890", "loai_pt": "Xe tải lớn", "trong_tai": 2000 }
  ]
}
```

---

## 🔐 Authentication & Phân quyền

```
POST /api/auth/login  →  { access_token, role }
Authorization: Bearer <token>
```

| Role | Quyền |
|---|---|
| `nv_giao_hang` | Xem đơn hàng, cập nhật vận đơn |
| `quan_ly` | Toàn bộ + tạo phân công |
| `ke_toan` | Xem & cập nhật hóa đơn |

---

## 🛠️ Tech Stack

**Backend:** Python 3.13 · FastAPI 0.115 · SQLAlchemy 2.0 · PyMySQL · NetworkX · python-jose · passlib  
**Frontend:** React 18 · Vite · Recharts · Axios · React Router · Lucide React  
**Database:** MySQL 8.0 · Stored Procedures · Triggers · Views · Role-based ACL  
**Testing:** pytest · httpx · SQLite in-memory (73 tests)  
**Deploy:** Railway (backend + MySQL) · Vercel (frontend)

---

## 👥 Project Evolution

**Origin:** Dự án được khởi đầu từ bài tập lớn nhóm trong khuôn khổ môn học **MI3090 – Cơ sở dữ liệu** (Nhóm 60).

**Current Status:** Được mở rộng, tái cấu trúc và phát triển độc lập bởi **ndtchumoa** thành một dự án cá nhân full-stack. Dự án đã được nâng cấp toàn diện từ việc tối ưu hóa cơ sở dữ liệu MySQL, xây dựng hệ thống REST API với FastAPI, hoàn thiện giao diện Analytics Dashboard bằng React, tích hợp thuật toán tối ưu lộ trình Dijkstra, JWT authentication, đến deploy production trên Railway và Vercel.

---

## 📄 License

[MIT](LICENSE)