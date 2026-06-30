"""
Pytest configuration & shared fixtures.
Dùng SQLite in-memory thay MySQL để test không phụ thuộc DB thật.
"""

import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from app.main import app
from app.database import Base, get_db

# ── Test database (SQLite in-memory) ─────────────────────────────
SQLALCHEMY_TEST_URL = "sqlite:///./test.db"

engine_test = create_engine(
    SQLALCHEMY_TEST_URL,
    connect_args={"check_same_thread": False},
)
TestingSessionLocal = sessionmaker(
    autocommit=False, autoflush=False, bind=engine_test
)


def override_get_db():
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()


# ── Fixtures ──────────────────────────────────────────────────────

@pytest.fixture(scope="session", autouse=True)
def setup_database():
    """Tạo schema một lần cho toàn bộ test session."""
    Base.metadata.create_all(bind=engine_test)
    yield
    Base.metadata.drop_all(bind=engine_test)


@pytest.fixture()
def db():
    """Session riêng cho mỗi test, rollback sau khi xong."""
    connection = engine_test.connect()
    transaction = connection.begin()
    session = TestingSessionLocal(bind=connection)
    yield session
    session.close()
    transaction.rollback()
    connection.close()


@pytest.fixture()
def client(db):
    """TestClient với DB đã được override."""
    app.dependency_overrides[get_db] = lambda: db
    with TestClient(app) as c:
        yield c
    app.dependency_overrides.clear()


@pytest.fixture()
def seed_data(db):
    """Chèn dữ liệu mẫu tối thiểu để test."""
    from app.models.all import (
        KhachHang, LoTrinh, HoaDon, DonHang,
        DiemTrungChuyen, ChangDuong, PhuongTien, NhanVienGiaoHang,
    )
    from datetime import datetime

    # Khách hàng
    kh1 = KhachHang(ID_KH="KH001", TEN_KH="Nguyen Van An",
                    SDT="0901234567", DIA_CHI="Ha Noi", EMAIL="an@test.com")
    kh2 = KhachHang(ID_KH="KH002", TEN_KH="Tran Thi Binh",
                    SDT="0912345678", DIA_CHI="Da Nang", EMAIL="binh@test.com")

    # Lộ trình
    lt1 = LoTrinh(ID_LT="LT001", TEN_LT="Ha Noi - Da Nang",
                  TRANG_THAI="Dang hoat dong")

    # Hóa đơn
    hd1 = HoaDon(ID_HD="HD001", THOI_GIAN_TAO=datetime(2024, 1, 15, 10, 0),
                 TRANG_THAI="Da thanh toan",
                 THOI_GIAN_HOAN_THANH=datetime(2024, 1, 15, 14, 0))

    # Đơn hàng
    dh1 = DonHang(ID_DH="DH001", KHOI_LUONG=5.0, QUANG_DUONG=760.0,
                  TRANG_THAI="Da giao", THANH_TIEN=2000000,
                  ID_KH_GUI="KH001", ID_KH_NHAN="KH002",
                  ID_LT="LT001", ID_HD="HD001")
    dh2 = DonHang(ID_DH="DH002", KHOI_LUONG=2.5, QUANG_DUONG=100.0,
                  TRANG_THAI="Cho xu ly", THANH_TIEN=500000,
                  ID_KH_GUI="KH001", ID_KH_NHAN="KH002",
                  ID_LT="LT001", ID_HD=None)

    # Điểm trung chuyển
    dtc1 = DiemTrungChuyen(ID_DTC="DTC001", TEN_DTC="Kho Ha Noi",
                           DIA_CHI="Ha Noi", THOI_GIAN_LAY_HANG="07:00-19:00")
    dtc2 = DiemTrungChuyen(ID_DTC="DTC002", TEN_DTC="Kho Da Nang",
                           DIA_CHI="Da Nang", THOI_GIAN_LAY_HANG="08:00-18:00")

    # Chặng đường
    cd1 = ChangDuong(ID_CD="CD001", STT=1, ID_LT="LT001",
                     ID_DTC_BD="DTC001", ID_DTC_KT="DTC002")

    # Phương tiện
    pt1 = PhuongTien(BIEN_SO="29A-12345", LOAI_PT="Xe tai nho",
                     TRONG_TAI=500.0, TRANG_THAI="Hoat dong")
    pt2 = PhuongTien(BIEN_SO="51C-11111", LOAI_PT="Xe container",
                     TRONG_TAI=10000.0, TRANG_THAI="Bao tri")

    # Nhân viên
    nv1 = NhanVienGiaoHang(ID_NV="NV001", TEN_NV="Nguyen Van Hung",
                           SDT="0901111111", EMAIL="hung@cty.vn")

    db.add_all([kh1, kh2, lt1, hd1, dh1, dh2,
                dtc1, dtc2, cd1, pt1, pt2, nv1])
    db.commit()
    return {"kh1": kh1, "kh2": kh2, "lt1": lt1,
            "dh1": dh1, "dh2": dh2, "hd1": hd1,
            "pt1": pt1, "pt2": pt2, "nv1": nv1,
            "cd1": cd1}
