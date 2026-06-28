"""
Router: /api/invoices
Các endpoint quản lý hóa đơn.
"""

from __future__ import annotations
from datetime import datetime
from typing import Optional

from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.orm import Session
from sqlalchemy import func

from app.database import get_db
from app.models.all import HoaDon, DonHang
from app.services.cod import tinh_cod
from pydantic import BaseModel, Field

router = APIRouter(prefix="/api/invoices", tags=["Invoices"])


# ── Schemas ──────────────────────────────────

class HoaDonCreate(BaseModel):
    order_ids: list[str] = Field(..., min_length=1, description="Danh sách ID_DH cần gộp")


class HoaDonResponse(BaseModel):
    ID_HD:                str
    THOI_GIAN_TAO:        datetime
    THOI_GIAN_HOAN_THANH: Optional[datetime]
    TRANG_THAI:           str
    so_don_hang:          int
    tong_cod:             float
    tong_gia_tri_hang:    float
    tong_tien_phai_thu:   float

    class Config:
        from_attributes = True


# ── Helper ────────────────────────────────────

def _gen_id(db: Session) -> str:
    count = db.query(func.count(HoaDon.ID_HD)).scalar() or 0
    return f"HD{count + 1:03d}"


def _build_response(hd: HoaDon, db: Session) -> HoaDonResponse:
    don_hangs = db.query(DonHang).filter(DonHang.ID_HD == hd.ID_HD).all()
    tong_cod  = sum(float(tinh_cod(dh.KHOI_LUONG, dh.QUANG_DUONG)) for dh in don_hangs)
    tong_hang = sum(float(dh.THANH_TIEN) for dh in don_hangs)

    return HoaDonResponse(
        ID_HD                = hd.ID_HD,
        THOI_GIAN_TAO        = hd.THOI_GIAN_TAO,
        THOI_GIAN_HOAN_THANH = hd.THOI_GIAN_HOAN_THANH,
        TRANG_THAI           = hd.TRANG_THAI,
        so_don_hang          = len(don_hangs),
        tong_cod             = tong_cod,
        tong_gia_tri_hang    = tong_hang,
        tong_tien_phai_thu   = tong_cod + tong_hang,
    )


# ── Endpoints ────────────────────────────────

@router.get("", summary="Danh sách hóa đơn")
def list_invoices(
    trang_thai: Optional[str] = Query(None, description="Chua thanh toan | Da thanh toan"),
    db: Session = Depends(get_db),
):
    query = db.query(HoaDon)
    if trang_thai:
        query = query.filter(HoaDon.TRANG_THAI == trang_thai)

    hoa_dons = query.order_by(HoaDon.THOI_GIAN_TAO.desc()).all()
    return [_build_response(hd, db) for hd in hoa_dons]


@router.get("/{id_hd}", summary="Chi tiết hóa đơn")
def get_invoice(id_hd: str, db: Session = Depends(get_db)):
    hd = db.get(HoaDon, id_hd)
    if not hd:
        raise HTTPException(404, f"Không tìm thấy hóa đơn '{id_hd}'")
    return _build_response(hd, db)


@router.post("", status_code=status.HTTP_201_CREATED, summary="Tạo hóa đơn từ nhiều đơn hàng")
def create_invoice(body: HoaDonCreate, db: Session = Depends(get_db)):
    # Validate tất cả đơn hàng tồn tại và chưa có hóa đơn
    orders = []
    for id_dh in body.order_ids:
        dh = db.get(DonHang, id_dh.strip())
        if not dh:
            raise HTTPException(400, f"Đơn hàng '{id_dh}' không tồn tại")
        if dh.ID_HD:
            raise HTTPException(400, f"Đơn hàng '{id_dh}' đã thuộc hóa đơn '{dh.ID_HD}'")
        orders.append(dh)

    # Tạo hóa đơn mới
    id_hd = _gen_id(db)
    hd = HoaDon(
        ID_HD                = id_hd,
        THOI_GIAN_TAO        = datetime.now(),
        THOI_GIAN_HOAN_THANH = None,
        TRANG_THAI           = "Chua thanh toan",
    )
    db.add(hd)
    db.flush()  # lấy ID trước khi gán FK

    # Gán các đơn hàng vào hóa đơn
    for dh in orders:
        dh.ID_HD = id_hd

    db.commit()
    db.refresh(hd)
    return _build_response(hd, db)


@router.patch("/{id_hd}/pay", summary="Đánh dấu hóa đơn đã thanh toán")
def pay_invoice(id_hd: str, db: Session = Depends(get_db)):
    hd = db.get(HoaDon, id_hd)
    if not hd:
        raise HTTPException(404, f"Không tìm thấy hóa đơn '{id_hd}'")
    if hd.TRANG_THAI == "Da thanh toan":
        raise HTTPException(400, "Hóa đơn này đã được thanh toán")

    hd.TRANG_THAI           = "Da thanh toan"
    hd.THOI_GIAN_HOAN_THANH = datetime.now()
    db.commit()
    db.refresh(hd)
    return _build_response(hd, db)
