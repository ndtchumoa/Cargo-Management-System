"""
Unit tests cho health check endpoints.
"""


class TestHealth:
    def test_root_returns_200(self, client):
        res = client.get("/")
        assert res.status_code == 200

    def test_root_has_required_fields(self, client):
        body = client.get("/").json()
        assert body["app"]    == "Cargo Management System"
        assert body["status"] == "running"
        assert "docs" in body

    def test_health_endpoint_returns_200(self, client):
        res = client.get("/health")
        assert res.status_code == 200

    def test_health_api_ok(self, client):
        assert client.get("/health").json()["api"] == "ok"
