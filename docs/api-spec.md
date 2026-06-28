# API Specification — Cargo Management System

Base URL: `http://localhost:8000/api`

---

## Orders `/orders`

### GET /orders
Lấy danh sách đơn hàng, có thể lọc theo trạng thái.

**Query params:**
| Param | Type | Mô tả |
|---|---|---|
| `status` | string | `Cho xu ly` · `Dang van chuyen` · `Da giao` · `Hoan tra` |
| `page` | int | Trang hiện tại (default: 1) |
| `limit` | int | Số bản ghi mỗi trang (default: 20) |

**Response 200:**
```json
{
  "data": [
    {
      "id_dh": "DH001",
      "khoi_luong": 5.0,
      "quang_duong": 760.0,
      "trang_thai": "Da giao",
      "thanh_tien": 2000000,
      "cod": 881000,
      "nguoi_gui": "Nguyen Van An",
      "nguoi_nhan": "Tran Thi Binh",
      "lo_trinh": "Ha Noi - Da Nang"
    }
  ],
  "total": 20,
  "page": 1,
  "limit": 20
}
```

---

### POST /orders
Tạo đơn hàng mới. COD được tính tự động bằng `fn_TinhCOD`.

**Request body:**
```json
{
  "khoi_luong": 5.0,
  "quang_duong": 760.0,
  "thanh_tien": 2000000,
  "id_kh_gui": "KH001",
  "id_kh_nhan": "KH002",
  "id_lt": "LT004"
}
```

**Response 201:**
```json
{
  "id_dh": "DH021",
  "trang_thai": "Cho xu ly",
  "cod": 881000
}
```

---

### GET /orders/{id}
Chi tiết 1 đơn hàng.

---

### PATCH /orders/{id}/status
Cập nhật trạng thái đơn hàng.

**Request body:**
```json
{ "trang_thai": "Dang van chuyen" }
```

---

### GET /orders/{id}/tracking
Lịch sử vận chuyển của đơn hàng, dùng view `vw_DonHang_NhanVien`.

**Response 200:**
```json
{
  "id_dh": "DH001",
  "lo_trinh": "Ha Noi - Da Nang",
  "history": [
    {
      "id_vd": "VD001",
      "trang_thai": "Da giao",
      "thoi_gian_nhan": "2024-01-10T07:30:00",
      "thoi_gian_giao": "2024-01-12T16:00:00",
      "chang_duong": "Ha Noi → Da Nang"
    }
  ]
}
```

---

## Invoices `/invoices`

### GET /invoices
Danh sách hóa đơn, dùng view `vw_HoaDon_KeToan`.

### POST /invoices
Tạo hóa đơn mới và gộp các đơn hàng vào.

**Request body:**
```json
{
  "order_ids": ["DH005", "DH007", "DH010"]
}
```

---

## Assignments `/assignments`

### POST /assignments
Phân công nhân viên + phương tiện vào chặng đường.  
MySQL trigger `trg_KiemTraPhuongTien` tự validate xe phải đang `Hoat dong`.  
MySQL trigger `trg_KiemTraHanhTrinh` tự validate chặng phải thuộc lộ trình của đơn.

**Request body:**
```json
{
  "ca_lam": "Ca sang 06:00-14:00",
  "id_cd": "CD005",
  "id_nv": "NV001",
  "bien_so": "29A-12345"
}
```

---

## Analytics `/analytics`

### GET /analytics/revenue
Doanh thu theo tháng.

**Response 200:**
```json
{
  "data": [
    { "thang": 1, "doanh_thu": 15480000 },
    { "thang": 2, "doanh_thu": 23100000 },
    { "thang": 3, "doanh_thu": 41200000 }
  ]
}
```

### GET /analytics/return-rate
Tỉ lệ hoàn trả theo lộ trình.

### GET /analytics/top-routes
Top lộ trình có nhiều đơn hàng nhất.

### GET /analytics/vehicle-status
Số lượng xe đang hoạt động / bảo trì.

---

## Optimize `/optimize`

### POST /optimize/route
Tìm lộ trình ngắn nhất giữa 2 điểm trung chuyển bằng Dijkstra.

**Request body:**
```json
{
  "from": "DTC001",
  "to": "DTC005",
  "weight_kg": 5.0
}
```

**Response 200:**
```json
{
  "path": ["DTC001", "DTC002", "DTC003", "DTC005"],
  "path_names": ["Kho Ha Noi", "Kho Da Nang", "Kho TP. HCM", "Kho Can Tho"],
  "total_km": 2100,
  "estimated_cod": 1485000,
  "available_vehicles": [
    { "bien_so": "29B-67890", "loai_pt": "Xe tai lon", "trong_tai": 2000.0 }
  ]
}
```

---

## Error Responses

| Status | Mô tả |
|---|---|
| `400` | Request không hợp lệ |
| `404` | Không tìm thấy resource |
| `422` | Validation error (Pydantic) |
| `500` | Lỗi server / trigger MySQL bắn lỗi |
