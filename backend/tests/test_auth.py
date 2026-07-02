"""
Unit tests cho /api/auth
"""

import pytest
from app.models.user import User
from app.services.auth import hash_password


@pytest.fixture()
def seed_users(db):
    """Tạo 2 user test."""
    u1 = User(username="test_ql",  hashed_pw=hash_password("pass123"),
              role="quan_ly",    ten_hien_thi="Test Quản Lý")
    u2 = User(username="test_nv",  hashed_pw=hash_password("pass456"),
              role="nv_giao_hang", ten_hien_thi="Test Nhân Viên")
    db.add_all([u1, u2])
    db.commit()
    return {"ql": u1, "nv": u2}


class TestLogin:
    def test_login_valid_returns_token(self, client, seed_users):
        res = client.post("/api/auth/login",
                          json={"username": "test_ql", "password": "pass123"})
        assert res.status_code == 200
        body = res.json()
        assert "access_token" in body
        assert body["token_type"] == "bearer"
        assert body["role"] == "quan_ly"

    def test_login_wrong_password_returns_401(self, client, seed_users):
        res = client.post("/api/auth/login",
                          json={"username": "test_ql", "password": "sai_mat_khau"})
        assert res.status_code == 401

    def test_login_nonexistent_user_returns_401(self, client, seed_users):
        res = client.post("/api/auth/login",
                          json={"username": "khong_ton_tai", "password": "abc"})
        assert res.status_code == 401

    def test_login_returns_role_correctly(self, client, seed_users):
        res = client.post("/api/auth/login",
                          json={"username": "test_nv", "password": "pass456"})
        assert res.json()["role"] == "nv_giao_hang"


class TestGetMe:
    def _get_token(self, client, seed_users, username, password):
        res = client.post("/api/auth/login",
                          json={"username": username, "password": password})
        return res.json()["access_token"]

    def test_me_with_valid_token(self, client, seed_users):
        token = self._get_token(client, seed_users, "test_ql", "pass123")
        res = client.get("/api/auth/me",
                         headers={"Authorization": f"Bearer {token}"})
        assert res.status_code == 200
        assert res.json()["username"] == "test_ql"
        assert res.json()["role"] == "quan_ly"

    def test_me_without_token_returns_403(self, client, seed_users):
        res = client.get("/api/auth/me")
        assert res.status_code in (401, 403)

    def test_me_with_invalid_token_returns_403(self, client, seed_users):
        res = client.get("/api/auth/me",
                         headers={"Authorization": "Bearer token_gia_mao"})
        assert res.status_code in (401, 403)


class TestProtectedRoutes:
    def _get_token(self, client, seed_users, username, password):
        res = client.post("/api/auth/login",
                          json={"username": username, "password": password})
        return res.json()["access_token"]

    def test_create_assignment_requires_quan_ly(self, client, seed_users):
        """Nhân viên giao hàng không tạo được phân công."""
        token = self._get_token(client, seed_users, "test_nv", "pass456")
        res = client.post("/api/assignments",
                          json={"CA_LAM": "Ca sang", "ID_CD": "CD001",
                                "ID_NV": "NV001", "BIEN_SO": "29A-12345"},
                          headers={"Authorization": f"Bearer {token}"})
        assert res.status_code == 403

    def test_create_assignment_quan_ly_allowed(self, client, seed_users):
        """Quản lý tạo phân công được — 400 vì thiếu dữ liệu seed, không phải 403."""
        token = self._get_token(client, seed_users, "test_ql", "pass123")
        res = client.post("/api/assignments",
                          json={"CA_LAM": "Ca sang", "ID_CD": "CD001",
                                "ID_NV": "NV001", "BIEN_SO": "29A-12345"},
                          headers={"Authorization": f"Bearer {token}"})
        # 400 = passed auth, failed business logic (không có dữ liệu seed)
        assert res.status_code != 403
