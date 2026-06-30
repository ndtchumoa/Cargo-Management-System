"""
Unit tests cho /api/orders
"""

import pytest


class TestListOrders:
    def test_list_all_returns_200(self, client, seed_data):
        res = client.get("/api/orders")
        assert res.status_code == 200
        body = res.json()
        assert "data" in body
        assert "total" in body
        assert body["total"] == 2

    def test_filter_by_status_da_giao(self, client, seed_data):
        res = client.get("/api/orders?status=Da giao")
        assert res.status_code == 200
        data = res.json()["data"]
        assert len(data) == 1
        assert data[0]["ID_DH"] == "DH001"

    def test_filter_by_status_cho_xu_ly(self, client, seed_data):
        res = client.get("/api/orders?status=Cho xu ly")
        assert res.status_code == 200
        data = res.json()["data"]
        assert len(data) == 1
        assert data[0]["ID_DH"] == "DH002"

    def test_filter_nonexistent_status_returns_empty(self, client, seed_data):
        res = client.get("/api/orders?status=Khong ton tai")
        assert res.status_code == 200
        assert res.json()["total"] == 0

    def test_pagination_limit(self, client, seed_data):
        res = client.get("/api/orders?limit=1&page=1")
        assert res.status_code == 200
        assert len(res.json()["data"]) == 1

    def test_order_has_cod_field(self, client, seed_data):
        res = client.get("/api/orders")
        data = res.json()["data"]
        for order in data:
            assert "cod" in order
            assert order["cod"] is not None


class TestGetOrder:
    def test_get_existing_order(self, client, seed_data):
        res = client.get("/api/orders/DH001")
        assert res.status_code == 200
        body = res.json()
        assert body["ID_DH"] == "DH001"
        assert body["TRANG_THAI"] == "Da giao"
        assert body["ten_nguoi_gui"] == "Nguyen Van An"
        assert body["ten_nguoi_nhan"] == "Tran Thi Binh"
        assert body["ten_lo_trinh"] == "Ha Noi - Da Nang"

    def test_get_nonexistent_order_returns_404(self, client, seed_data):
        res = client.get("/api/orders/DH999")
        assert res.status_code == 404

    def test_cod_calculated_correctly(self, client, seed_data):
        """
        DH001: KL=5kg, QD=760km
        phi_kl = 5 * 5000 = 25000
        phi_qd = 100000 + (300-100)*800 + (760-300)*600
               = 100000 + 160000 + 276000 = 536000
        tong = 561000 → làm tròn = 561000
        """
        res = client.get("/api/orders/DH001")
        assert res.status_code == 200
        cod = res.json()["cod"]
        assert float(cod) == 561000.0


class TestCreateOrder:
    def test_create_valid_order(self, client, seed_data):
        payload = {
            "KHOI_LUONG":  3.0,
            "QUANG_DUONG": 100.0,
            "THANH_TIEN":  1000000,
            "ID_KH_GUI":   "KH001",
            "ID_KH_NHAN":  "KH002",
            "ID_LT":       "LT001",
        }
        res = client.post("/api/orders", json=payload)
        assert res.status_code == 201
        body = res.json()
        assert "ID_DH" in body
        assert body["TRANG_THAI"] == "Cho xu ly"
        assert float(body["cod"]) > 0

    def test_create_order_invalid_kh_gui_returns_400(self, client, seed_data):
        payload = {
            "KHOI_LUONG":  3.0,
            "QUANG_DUONG": 100.0,
            "THANH_TIEN":  1000000,
            "ID_KH_GUI":   "KH999",   # không tồn tại
            "ID_KH_NHAN":  "KH002",
            "ID_LT":       "LT001",
        }
        res = client.post("/api/orders", json=payload)
        assert res.status_code == 400

    def test_create_order_invalid_lt_returns_400(self, client, seed_data):
        payload = {
            "KHOI_LUONG":  3.0,
            "QUANG_DUONG": 100.0,
            "THANH_TIEN":  1000000,
            "ID_KH_GUI":   "KH001",
            "ID_KH_NHAN":  "KH002",
            "ID_LT":       "LT999",   # không tồn tại
        }
        res = client.post("/api/orders", json=payload)
        assert res.status_code == 400

    def test_create_order_negative_weight_returns_422(self, client, seed_data):
        payload = {
            "KHOI_LUONG":  -1.0,      # không hợp lệ
            "QUANG_DUONG": 100.0,
            "THANH_TIEN":  1000000,
            "ID_KH_GUI":   "KH001",
            "ID_KH_NHAN":  "KH002",
            "ID_LT":       "LT001",
        }
        res = client.post("/api/orders", json=payload)
        assert res.status_code == 422

    def test_create_order_strips_whitespace_id(self, client, seed_data):
        payload = {
            "KHOI_LUONG":  2.0,
            "QUANG_DUONG": 50.0,
            "THANH_TIEN":  500000,
            "ID_KH_GUI":   " KH001 ",  # có khoảng trắng
            "ID_KH_NHAN":  "KH002",
            "ID_LT":       "LT001",
        }
        res = client.post("/api/orders", json=payload)
        assert res.status_code == 201  # validator strip whitespace


class TestUpdateStatus:
    def test_update_status_valid(self, client, seed_data):
        res = client.patch("/api/orders/DH002/status",
                           json={"TRANG_THAI": "Dang van chuyen"})
        assert res.status_code == 200
        assert res.json()["TRANG_THAI"] == "Dang van chuyen"

    def test_update_status_invalid_value_returns_422(self, client, seed_data):
        res = client.patch("/api/orders/DH001/status",
                           json={"TRANG_THAI": "Trang thai sai"})
        assert res.status_code == 422

    def test_update_status_nonexistent_order_returns_404(self, client, seed_data):
        res = client.patch("/api/orders/DH999/status",
                           json={"TRANG_THAI": "Da giao"})
        assert res.status_code == 404


class TestTracking:
    def test_tracking_existing_order(self, client, seed_data):
        res = client.get("/api/orders/DH001/tracking")
        assert res.status_code == 200
        body = res.json()
        assert body["id_dh"] == "DH001"
        assert "lo_trinh" in body
        assert "history" in body
        assert isinstance(body["history"], list)

    def test_tracking_nonexistent_order_returns_404(self, client, seed_data):
        res = client.get("/api/orders/DH999/tracking")
        assert res.status_code == 404
