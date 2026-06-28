"""
SQLAlchemy ORM models ánh xạ từ schema cargo_db (MySQL 8.0).
Thứ tự khai báo theo dependency: bảng không có FK trước.
"""

from sqlalchemy import (
    Column, String, Integer, DateTime, Numeric,
    ForeignKey, UniqueConstraint, CheckConstraint, text,
)
from sqlalchemy.orm import relationship
from app.database import Base


# ─────────────────────────────────────────────
# 1. KHACH_HANG
# ─────────────────────────────────────────────
class KhachHang(Base):
    __tablename__ = "KHACH_HANG"

    ID_KH   = Column(String(10),  primary_key=True)
    TEN_KH  = Column(String(100), nullable=False)
    EMAIL   = Column(String(100), unique=True)
    SDT     = Column(String(15),  nullable=False)
    DIA_CHI = Column(String(200), nullable=False)

    don_hang_gui  = relationship("DonHang", foreign_keys="DonHang.ID_KH_GUI",  back_populates="nguoi_gui")
    don_hang_nhan = relationship("DonHang", foreign_keys="DonHang.ID_KH_NHAN", back_populates="nguoi_nhan")


# ─────────────────────────────────────────────
# 2. HOA_DON
# ─────────────────────────────────────────────
class HoaDon(Base):
    __tablename__ = "HOA_DON"

    ID_HD                = Column(String(10),  primary_key=True)
    THOI_GIAN_TAO        = Column(DateTime,    nullable=False)
    THOI_GIAN_HOAN_THANH = Column(DateTime,    nullable=True)
    TRANG_THAI           = Column(String(50),  nullable=False)

    __table_args__ = (
        CheckConstraint(
            "TRANG_THAI IN ('Chua thanh toan','Da thanh toan')",
            name="CK_HD_TT"
        ),
        CheckConstraint(
            "THOI_GIAN_HOAN_THANH IS NULL OR THOI_GIAN_HOAN_THANH > THOI_GIAN_TAO",
            name="CK_HD_TGIAN"
        ),
    )

    don_hangs = relationship("DonHang", back_populates="hoa_don")


# ─────────────────────────────────────────────
# 3. LO_TRINH
# ─────────────────────────────────────────────
class LoTrinh(Base):
    __tablename__ = "LO_TRINH"

    ID_LT      = Column(String(10),  primary_key=True)
    TEN_LT     = Column(String(200), nullable=False)
    TRANG_THAI = Column(String(50),  nullable=False)

    __table_args__ = (
        CheckConstraint(
            "TRANG_THAI IN ('Dang hoat dong','Tam dung')",
            name="CK_LT_TT"
        ),
    )

    don_hangs    = relationship("DonHang",    back_populates="lo_trinh")
    chang_duongs = relationship("ChangDuong", back_populates="lo_trinh")


# ─────────────────────────────────────────────
# 4. DON_HANG
# ─────────────────────────────────────────────
class DonHang(Base):
    __tablename__ = "DON_HANG"

    ID_DH       = Column(String(10),    primary_key=True)
    KHOI_LUONG  = Column(Numeric(10,2), nullable=False)
    QUANG_DUONG = Column(Numeric(10,2), nullable=False)
    TRANG_THAI  = Column(String(50),    nullable=False)
    THANH_TIEN  = Column(Numeric(15,2), nullable=False)
    ID_KH_GUI   = Column(String(10),    ForeignKey("KHACH_HANG.ID_KH", ondelete="RESTRICT", onupdate="CASCADE"), nullable=False)
    ID_KH_NHAN  = Column(String(10),    ForeignKey("KHACH_HANG.ID_KH", ondelete="RESTRICT", onupdate="CASCADE"), nullable=False)
    ID_LT       = Column(String(10),    ForeignKey("LO_TRINH.ID_LT",   ondelete="RESTRICT", onupdate="CASCADE"), nullable=False)
    ID_HD       = Column(String(10),    ForeignKey("HOA_DON.ID_HD",    ondelete="SET NULL", onupdate="CASCADE"), nullable=True)

    __table_args__ = (
        CheckConstraint(
            "TRANG_THAI IN ('Cho xu ly','Dang van chuyen','Da giao','Hoan tra')",
            name="CK_DH_TT"
        ),
        CheckConstraint("KHOI_LUONG > 0",   name="CK_DH_KL"),
        CheckConstraint("QUANG_DUONG > 0",  name="CK_DH_QD"),
        CheckConstraint("THANH_TIEN >= 0",  name="CK_DH_TH"),
    )

    nguoi_gui    = relationship("KhachHang", foreign_keys=[ID_KH_GUI],  back_populates="don_hang_gui")
    nguoi_nhan   = relationship("KhachHang", foreign_keys=[ID_KH_NHAN], back_populates="don_hang_nhan")
    lo_trinh     = relationship("LoTrinh",   back_populates="don_hangs")
    hoa_don      = relationship("HoaDon",    back_populates="don_hangs")
    van_dons     = relationship("ChiTietVanDon", back_populates="don_hang")


# ─────────────────────────────────────────────
# 5. DIEM_TRUNG_CHUYEN
# ─────────────────────────────────────────────
class DiemTrungChuyen(Base):
    __tablename__ = "DIEM_TRUNG_CHUYEN"

    ID_DTC             = Column(String(10),  primary_key=True)
    TEN_DTC            = Column(String(100), nullable=False)
    DIA_CHI            = Column(String(200), nullable=False)
    THOI_GIAN_LAY_HANG = Column(String(50),  nullable=True)

    chang_duong_bd = relationship("ChangDuong", foreign_keys="ChangDuong.ID_DTC_BD", back_populates="diem_bd")
    chang_duong_kt = relationship("ChangDuong", foreign_keys="ChangDuong.ID_DTC_KT", back_populates="diem_kt")


# ─────────────────────────────────────────────
# 6. CHANG_DUONG
# ─────────────────────────────────────────────
class ChangDuong(Base):
    __tablename__ = "CHANG_DUONG"

    ID_CD     = Column(String(10), primary_key=True)
    STT       = Column(Integer,    nullable=False)
    ID_LT     = Column(String(10), ForeignKey("LO_TRINH.ID_LT",          ondelete="RESTRICT", onupdate="CASCADE"),  nullable=False)
    ID_DTC_BD = Column(String(10), ForeignKey("DIEM_TRUNG_CHUYEN.ID_DTC", ondelete="RESTRICT", onupdate="RESTRICT"), nullable=False)
    ID_DTC_KT = Column(String(10), ForeignKey("DIEM_TRUNG_CHUYEN.ID_DTC", ondelete="RESTRICT", onupdate="RESTRICT"), nullable=False)

    __table_args__ = (
        UniqueConstraint("ID_LT", "STT", name="UQ_CD_LT_STT"),
        CheckConstraint("STT > 0",               name="CK_CD_STT"),
        CheckConstraint("ID_DTC_BD <> ID_DTC_KT", name="CK_CD_DTC"),
    )

    lo_trinh  = relationship("LoTrinh",        back_populates="chang_duongs")
    diem_bd   = relationship("DiemTrungChuyen", foreign_keys=[ID_DTC_BD], back_populates="chang_duong_bd")
    diem_kt   = relationship("DiemTrungChuyen", foreign_keys=[ID_DTC_KT], back_populates="chang_duong_kt")
    phan_congs = relationship("PhanCong",       back_populates="chang_duong")


# ─────────────────────────────────────────────
# 7. PHUONG_TIEN
# ─────────────────────────────────────────────
class PhuongTien(Base):
    __tablename__ = "PHUONG_TIEN"

    BIEN_SO    = Column(String(15),   primary_key=True)
    LOAI_PT    = Column(String(50),   nullable=False)
    TRONG_TAI  = Column(Numeric(10,2),nullable=False)
    TRANG_THAI = Column(String(50),   nullable=False)

    __table_args__ = (
        CheckConstraint("TRANG_THAI IN ('Hoat dong','Bao tri')", name="CK_PT_TT"),
        CheckConstraint("TRONG_TAI > 0",                         name="CK_PT_TL"),
    )

    phan_congs = relationship("PhanCong", back_populates="phuong_tien")


# ─────────────────────────────────────────────
# 8. NHAN_VIEN_GIAO_HANG
# ─────────────────────────────────────────────
class NhanVienGiaoHang(Base):
    __tablename__ = "NHAN_VIEN_GIAO_HANG"

    ID_NV   = Column(String(10),  primary_key=True)
    TEN_NV  = Column(String(100), nullable=False)
    SDT     = Column(String(15),  nullable=False, unique=True)
    EMAIL   = Column(String(100), unique=True)
    DIA_CHI = Column(String(200), nullable=True)

    phan_congs = relationship("PhanCong", back_populates="nhan_vien")


# ─────────────────────────────────────────────
# 9. PHAN_CONG
# ─────────────────────────────────────────────
class PhanCong(Base):
    __tablename__ = "PHAN_CONG"

    ID_PC   = Column(String(10),  primary_key=True)
    CA_LAM  = Column(String(100), nullable=False)
    ID_CD   = Column(String(10),  ForeignKey("CHANG_DUONG.ID_CD",        ondelete="RESTRICT", onupdate="CASCADE"), nullable=False)
    ID_NV   = Column(String(10),  ForeignKey("NHAN_VIEN_GIAO_HANG.ID_NV", ondelete="RESTRICT", onupdate="CASCADE"), nullable=False)
    BIEN_SO = Column(String(15),  ForeignKey("PHUONG_TIEN.BIEN_SO",      ondelete="RESTRICT", onupdate="CASCADE"), nullable=False)

    chang_duong  = relationship("ChangDuong",       back_populates="phan_congs")
    nhan_vien    = relationship("NhanVienGiaoHang", back_populates="phan_congs")
    phuong_tien  = relationship("PhuongTien",       back_populates="phan_congs")
    van_dons     = relationship("ChiTietVanDon",    back_populates="phan_cong")


# ─────────────────────────────────────────────
# 10. CHI_TIET_VAN_DON
# ─────────────────────────────────────────────
class ChiTietVanDon(Base):
    __tablename__ = "CHI_TIET_VAN_DON"

    ID_VD               = Column(String(10), primary_key=True)
    TRANG_THAI          = Column(String(50), nullable=False)
    THOI_GIAN_NHAN_HANG = Column(DateTime,   nullable=True)
    THOI_GIAN_GIAO_HANG = Column(DateTime,   nullable=True)
    ID_DH               = Column(String(10), ForeignKey("DON_HANG.ID_DH",  ondelete="RESTRICT", onupdate="CASCADE"), nullable=False)
    ID_PC               = Column(String(10), ForeignKey("PHAN_CONG.ID_PC", ondelete="RESTRICT", onupdate="CASCADE"), nullable=False)

    __table_args__ = (
        UniqueConstraint("ID_DH", "ID_PC", name="UQ_VD_DH_PC"),
        CheckConstraint(
            "TRANG_THAI IN ('Dang van chuyen','Da giao','Hoan tra')",
            name="CK_VD_TT"
        ),
        CheckConstraint(
            "THOI_GIAN_GIAO_HANG IS NULL OR THOI_GIAN_NHAN_HANG IS NULL OR THOI_GIAN_GIAO_HANG > THOI_GIAN_NHAN_HANG",
            name="CK_VD_TGIAN"
        ),
    )

    don_hang  = relationship("DonHang",  back_populates="van_dons")
    phan_cong = relationship("PhanCong", back_populates="van_dons")
