"""
Unit tests cho /api/invoices
"""


class TestListInvoices:
    def test_list_all_returns_200(self, client, seed_data):
        res = client.get("/api/invoices")
        assert res.status_code == 200
        assert isinstance(res.json(), list)

    def test_list_returns_correct_count(self, client, seed_data):
        res = client.get("/api/invoices")
        assert len(res.json()) == 1  # seed có 1 hóa đơn

    def test_filter_da_thanh_toan(self, client, seed_data):
        res = client.get("/api/invoices?trang_thai=Da thanh toan")
        data = res.json()
        assert len(data) == 1
        assert data[0]["TRANG_THAI"] == "Da thanh toan"

    def test_filter_chua_thanh_toan_returns_empty(self, client, seed_data):
        res = client.get("/api/invoices?trang_thai=Chua thanh toan")
        assert res.json() == []

    def test_invoice_has_required_fields(self, client, seed_data):
        res = client.get("/api/invoices")
        hd = res.json()[0]
        for field in ["ID_HD", "TRANG_THAI", "so_don_hang",
                      "tong_cod", "tong_gia_tri_hang", "tong_tien_phai_thu"]:
            assert field in hd

    def test_tong_tien_equals_cod_plus_hang(self, client, seed_data):
        hd = client.get("/api/invoices").json()[0]
        expected = round(hd["tong_cod"] + hd["tong_gia_tri_hang"], 2)
        assert round(hd["tong_tien_phai_thu"], 2) == expected


class TestGetInvoice:
    def test_get_existing_invoice(self, client, seed_data):
        res = client.get("/api/invoices/HD001")
        assert res.status_code == 200
        assert res.json()["ID_HD"] == "HD001"

    def test_get_nonexistent_invoice_returns_404(self, client, seed_data):
        res = client.get("/api/invoices/HD999")
        assert res.status_code == 404


class TestCreateInvoice:
    def test_create_invoice_from_order(self, client, seed_data):
        """DH002 chưa có hóa đơn → tạo được."""
        res = client.post("/api/invoices", json={"order_ids": ["DH002"]})
        assert res.status_code == 201
        body = res.json()
        assert body["TRANG_THAI"] == "Chua thanh toan"
        assert body["so_don_hang"] == 1

    def test_create_invoice_order_already_has_invoice_returns_400(self, client, seed_data):
        """DH001 đã thuộc HD001 → không tạo được."""
        res = client.post("/api/invoices", json={"order_ids": ["DH001"]})
        assert res.status_code == 400

    def test_create_invoice_nonexistent_order_returns_400(self, client, seed_data):
        res = client.post("/api/invoices", json={"order_ids": ["DH999"]})
        assert res.status_code == 400

    def test_create_invoice_empty_list_returns_422(self, client, seed_data):
        res = client.post("/api/invoices", json={"order_ids": []})
        assert res.status_code == 422


class TestPayInvoice:
    def test_pay_existing_unpaid_invoice(self, client, seed_data):
        # Tạo hóa đơn mới từ DH002
        create_res = client.post("/api/invoices", json={"order_ids": ["DH002"]})
        new_id = create_res.json()["ID_HD"]

        res = client.patch(f"/api/invoices/{new_id}/pay")
        assert res.status_code == 200
        assert res.json()["TRANG_THAI"] == "Da thanh toan"
        assert res.json()["THOI_GIAN_HOAN_THANH"] is not None

    def test_pay_already_paid_invoice_returns_400(self, client, seed_data):
        """HD001 đã Da thanh toan → không pay được lần nữa."""
        res = client.patch("/api/invoices/HD001/pay")
        assert res.status_code == 400

    def test_pay_nonexistent_invoice_returns_404(self, client, seed_data):
        res = client.patch("/api/invoices/HD999/pay")
        assert res.status_code == 404
