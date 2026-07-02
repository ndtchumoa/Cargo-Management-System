"""
Pydantic schemas cho DON_HANG.
- Request schemas: validate input từ client
- Response schemas: định dạng output trả về
"""

from __future__ import annotations
from decimal import Decimal
from typing import Optional, Literal
from pydantic import BaseModel, Field, field_validator, ConfigDict


TrangThaiDonHang = Literal[
    "Cho xu ly",
    "Dang van chuyen",
    "Da giao",
    "Hoan tra",
]


# ── Request ──────────────────────────────────

class DonHangCreate(BaseModel):
    """Body để tạo đơn hàng mới."""
    KHOI_LUONG:  Decimal = Field(..., gt=0, description="Khối lượng (kg)")
    QUANG_DUONG: Decimal = Field(..., gt=0, description="Khoảng cách (km)")
    THANH_TIEN:  Decimal = Field(..., ge=0, description="Giá trị hàng hóa (VNĐ)")
    ID_KH_GUI:   str     = Field(..., max_length=10)
    ID_KH_NHAN:  str     = Field(..., max_length=10)
    ID_LT:       str     = Field(..., max_length=10)

    @field_validator("ID_KH_GUI", "ID_KH_NHAN", "ID_LT")
    @classmethod
    def strip_whitespace(cls, v: str) -> str:
        return v.strip()


class DonHangStatusUpdate(BaseModel):
    """Body để cập nhật trạng thái."""
    TRANG_THAI: TrangThaiDonHang


# ── Response ─────────────────────────────────

class DonHangBase(BaseModel):
    ID_DH:       str
    KHOI_LUONG:  Decimal
    QUANG_DUONG: Decimal
    TRANG_THAI:  str
    THANH_TIEN:  Decimal
    ID_KH_GUI:   str
    ID_KH_NHAN:  str
    ID_LT:       str
    ID_HD:       Optional[str]

    model_config = ConfigDict(from_attributes=True)


class DonHangDetail(DonHangBase):
    """Chi tiết đơn hàng kèm tên người gửi/nhận và COD."""
    ten_nguoi_gui:  Optional[str] = None
    ten_nguoi_nhan: Optional[str] = None
    ten_lo_trinh:   Optional[str] = None
    cod:            Optional[Decimal] = None


class DonHangListItem(BaseModel):
    ID_DH:          str
    TRANG_THAI:     str
    KHOI_LUONG:     Decimal
    QUANG_DUONG:    Decimal
    ten_nguoi_gui:  str
    ten_nguoi_nhan: str
    ten_lo_trinh:   str
    cod:            Optional[Decimal] = None

    model_config = ConfigDict(from_attributes=True)


class DonHangCreated(BaseModel):
    """Response sau khi tạo đơn thành công."""
    ID_DH:      str
    TRANG_THAI: str
    cod:        Decimal


class PaginatedOrders(BaseModel):
    data:  list[DonHangListItem]
    total: int
    page:  int
    limit: int
