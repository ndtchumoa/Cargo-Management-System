"""
Unit tests cho /api/analytics
"""


class TestAnalytics:
    def test_revenue_returns_200(self, client, seed_data):
        res = client.get("/api/analytics/revenue")
        assert res.status_code == 200
        assert isinstance(res.json(), list)

    def test_revenue_has_required_fields(self, client, seed_data):
        res = client.get("/api/analytics/revenue")
        data = res.json()
        if data:  # có dữ liệu mới check fields
            item = data[0]
            for field in ["nam", "thang", "so_don",
                          "tong_cod", "tong_gia_tri_hang", "tong_doanh_thu"]:
                assert field in item

    def test_revenue_tong_doanh_thu_equals_sum(self, client, seed_data):
        res = client.get("/api/analytics/revenue")
        for item in res.json():
            expected = round(item["tong_cod"] + item["tong_gia_tri_hang"], 2)
            assert round(item["tong_doanh_thu"], 2) == expected

    def test_return_rate_returns_200(self, client, seed_data):
        res = client.get("/api/analytics/return-rate")
        assert res.status_code == 200
        assert isinstance(res.json(), list)

    def test_return_rate_has_required_fields(self, client, seed_data):
        res = client.get("/api/analytics/return-rate")
        for item in res.json():
            for field in ["id_lt", "ten_lt", "tong_don",
                          "so_hoan_tra", "ti_le_pct"]:
                assert field in item

    def test_return_rate_ti_le_between_0_and_100(self, client, seed_data):
        res = client.get("/api/analytics/return-rate")
        for item in res.json():
            assert 0 <= item["ti_le_pct"] <= 100

    def test_top_routes_returns_200(self, client, seed_data):
        res = client.get("/api/analytics/top-routes")
        assert res.status_code == 200
        assert isinstance(res.json(), list)

    def test_top_routes_default_limit_5(self, client, seed_data):
        res = client.get("/api/analytics/top-routes")
        assert len(res.json()) <= 5

    def test_top_routes_custom_limit(self, client, seed_data):
        res = client.get("/api/analytics/top-routes?limit=1")
        assert len(res.json()) <= 1

    def test_vehicle_status_returns_200(self, client, seed_data):
        res = client.get("/api/analytics/vehicle-status")
        assert res.status_code == 200
        assert isinstance(res.json(), list)

    def test_vehicle_status_has_required_fields(self, client, seed_data):
        res = client.get("/api/analytics/vehicle-status")
        for item in res.json():
            for field in ["trang_thai", "loai_pt", "so_luong"]:
                assert field in item

    def test_order_status_summary_returns_200(self, client, seed_data):
        res = client.get("/api/analytics/order-status-summary")
        assert res.status_code == 200
        data = res.json()
        assert isinstance(data, list)
        # seed có DH001=Da giao, DH002=Cho xu ly
        statuses = {item["trang_thai"] for item in data}
        assert "Da giao" in statuses
        assert "Cho xu ly" in statuses

    def test_top_customers_returns_200(self, client, seed_data):
        res = client.get("/api/analytics/top-customers")
        assert res.status_code == 200
        assert isinstance(res.json(), list)

    def test_top_customers_has_required_fields(self, client, seed_data):
        res = client.get("/api/analytics/top-customers")
        for item in res.json():
            for field in ["id_kh", "ten_kh", "so_don", "tong_gia_tri"]:
                assert field in item
