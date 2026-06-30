"""
Unit tests cho /api/optimize/route
"""


class TestOptimizeRoute:
    def test_valid_route_returns_200(self, client, seed_data):
        res = client.post("/api/optimize/route", json={
            "from_dtc":  "DTC001",
            "to_dtc":    "DTC002",
            "weight_kg": 5.0,
        })
        assert res.status_code == 200

    def test_response_has_required_fields(self, client, seed_data):
        res = client.post("/api/optimize/route", json={
            "from_dtc":  "DTC001",
            "to_dtc":    "DTC002",
            "weight_kg": 5.0,
        })
        body = res.json()
        for field in ["path", "path_names", "total_km",
                      "estimated_cod", "available_vehicles"]:
            assert field in body

    def test_path_starts_and_ends_correctly(self, client, seed_data):
        res = client.post("/api/optimize/route", json={
            "from_dtc":  "DTC001",
            "to_dtc":    "DTC002",
            "weight_kg": 5.0,
        })
        body = res.json()
        assert body["path"][0]  == "DTC001"
        assert body["path"][-1] == "DTC002"

    def test_total_km_is_positive(self, client, seed_data):
        res = client.post("/api/optimize/route", json={
            "from_dtc":  "DTC001",
            "to_dtc":    "DTC002",
            "weight_kg": 5.0,
        })
        assert res.json()["total_km"] > 0

    def test_estimated_cod_is_positive(self, client, seed_data):
        res = client.post("/api/optimize/route", json={
            "from_dtc":  "DTC001",
            "to_dtc":    "DTC002",
            "weight_kg": 5.0,
        })
        assert res.json()["estimated_cod"] > 0

    def test_vehicles_filtered_by_weight(self, client, seed_data):
        """Chỉ xe đang Hoat dong và tải trọng >= weight_kg mới được trả về."""
        res = client.post("/api/optimize/route", json={
            "from_dtc":  "DTC001",
            "to_dtc":    "DTC002",
            "weight_kg": 5.0,
        })
        vehicles = res.json()["available_vehicles"]
        for v in vehicles:
            assert v["trong_tai"] >= 5.0

    def test_bao_tri_vehicle_not_in_result(self, client, seed_data):
        """Xe 51C-11111 đang Bao tri không được trả về."""
        res = client.post("/api/optimize/route", json={
            "from_dtc":  "DTC001",
            "to_dtc":    "DTC002",
            "weight_kg": 5.0,
        })
        vehicle_ids = [v["bien_so"] for v in res.json()["available_vehicles"]]
        assert "51C-11111" not in vehicle_ids

    def test_same_origin_destination_returns_400(self, client, seed_data):
        res = client.post("/api/optimize/route", json={
            "from_dtc":  "DTC001",
            "to_dtc":    "DTC001",
            "weight_kg": 5.0,
        })
        assert res.status_code == 400

    def test_nonexistent_dtc_returns_400(self, client, seed_data):
        res = client.post("/api/optimize/route", json={
            "from_dtc":  "DTC999",
            "to_dtc":    "DTC002",
            "weight_kg": 5.0,
        })
        assert res.status_code == 400

    def test_negative_weight_returns_422(self, client, seed_data):
        res = client.post("/api/optimize/route", json={
            "from_dtc":  "DTC001",
            "to_dtc":    "DTC002",
            "weight_kg": -1.0,
        })
        assert res.status_code == 422
