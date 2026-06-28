# 🚚 Cargo Management System

A full-stack logistics cargo management system with REST API, analytics dashboard, and route optimization.

![License](https://img.shields.io/badge/license-MIT-blue.svg)
![Python](https://img.shields.io/badge/Python-3.11+-3776AB?logo=python&logoColor=white)
![FastAPI](https://img.shields.io/badge/FastAPI-0.111+-009688?logo=fastapi&logoColor=white)
![React](https://img.shields.io/badge/React-18+-61DAFB?logo=react&logoColor=black)
![MySQL](https://img.shields.io/badge/MySQL-8.0-4479A1?logo=mysql&logoColor=white)

---

## 📋 Tổng quan

Hệ thống quản lý vận chuyển hàng hóa toàn diện, được xây dựng dựa trên cơ sở dữ liệu `cargo_db` gồm 10 bảng, hỗ trợ các nghiệp vụ:

- Quản lý đơn hàng, hóa đơn, khách hàng
- Theo dõi hành trình vận chuyển theo từng chặng
- Phân công tài xế và phương tiện
- Tối ưu hóa lộ trình bằng thuật toán Dijkstra
- Dashboard phân tích doanh thu và vận hành
- Phân quyền theo vai trò (nhân viên / quản lý / kế toán)

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
│   │   ├── database.py
│   │   ├── models/
│   │   ├── routers/
│   │   └── services/
│   ├── requirements.txt
│   └── .env.example
├── frontend/
│   ├── src/
│   │   ├── pages/
│   │   ├── components/
│   │   └── api/
│   └── package.json
├── database/
│   ├── schema/
│   │   └── CreateTab.sql
│   ├── data/
│   │   └── InsertData.sql
│   ├── functions/
│   │   ├── Func_calCOD.sql
│   │   ├── Func_showDH.sql
│   │   ├── Func_View.sql
│   │   ├── Func_Role.sql
│   │   ├── Func_ShowData.sql
│   │   └── Func_ClearData.sql
│   └── triggers/
│       ├── trigger1.sql
│       └── trigger2.sql
└── docs/
    ├── erd.png
    └── api-spec.md
```

---

## ⚙️ Cài đặt và chạy local

### Yêu cầu hệ thống

| Công cụ | Phiên bản |
|---|---|
| Python | 3.11+ |
| Node.js | 18+ |
| MySQL | 8.0+ |

### 1. Clone repository

```bash
git clone https://github.com/<your-username>/Cargo-Management-System.git
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
source venv/bin/activate        # Windows: venv\Scripts\activate
pip install -r requirements.txt
cp .env.example .env            # Điền thông tin database vào .env
uvicorn app.main:app --reload
```

API chạy tại: `http://localhost:8000`  
Swagger UI: `http://localhost:8000/docs`

### 4. Chạy frontend

```bash
cd frontend
npm install
npm run dev
```

Dashboard chạy tại: `http://localhost:5173`

---

## 🔌 API Endpoints

| Method | Endpoint | Mô tả |
|---|---|---|
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
| `POST` | `/api/optimize/route` | Tối ưu lộ trình (Dijkstra) |

---

## 🧠 Route Optimization

Thuật toán **Dijkstra** trên đồ thị có hướng được xây từ bảng `CHANG_DUONG`:

```json
POST /api/optimize/route
{
  "from": "DTC001",
  "to":   "DTC005",
  "weight_kg": 5.0
}

// Response
{
  "path": ["DTC001", "DTC002", "DTC003", "DTC005"],
  "total_km": 2100,
  "estimated_cod": 1485000,
  "available_vehicles": ["29B-67890", "51D-33333"]
}
```

---

## 🔐 Phân quyền

| Role | Quyền |
|---|---|
| `role_nv_giao_hang` | Xem đơn hàng, cập nhật vận đơn |
| `role_quan_ly` | Toàn bộ + tạo phân công |
| `role_ke_toan` | Xem & cập nhật hóa đơn |

---

## 🛠️ Tech Stack

**Backend:** Python · FastAPI · SQLAlchemy · PyMySQL · NetworkX  
**Frontend:** React 18 · Vite · Recharts · Axios · React Router  
**Database:** MySQL 8.0 · Stored Procedures · Triggers · Views  
**Deploy:** Railway (backend) · Vercel (frontend)

---

## 👥 Tác giả

Developed as part of **MI3090 – Cơ sở dữ liệu**, Nhóm 60.

---

## 📄 License

[MIT](LICENSE)
