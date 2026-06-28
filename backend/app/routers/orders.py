"""
Router: /api/orders
Các endpoint quản lý đơn hàng.
"""

from __future__ import annotations
import uuid
from typing import Optional

from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.orm import Session
from sqlalchemy import func, text

from app.database import get_db
from app.models.all import DonHang, KhachHang, LoTrinh, ChiTietVanDon, ChangDuong, DiemTrungChuyen
from app.schemas.order import (
    DonHangCreate, DonHangStatusUpdate,
    DonHangDetail, DonHangListItem, DonHangCreated, PaginatedOrders,
)
from app.services.cod import tinh_cod

router = APIRouter(prefix="/api/orders", tags=["Orders"])


# ── Helper ────────────────────────────────────

def _get_order_or_404(id_dh: str, db: Session) -> DonHang:
    order = db.get(DonHang, id_dh)
    if not order:
        raise HTTPException(status_code=404, detail=f"Không tìm thấy đơn hàng '{id_dh}'")
    return order


def _gen_id(db: Session) -> str:
    """Tự sinh ID_DH theo format DH + 3 số."""
    count = db.query(func.count(DonHang.ID_DH)).scalar() or 0
    return f"DH{count + 1:03d}"


# ── Endpoints ────────────────────────────────

@router.get("", response_model=PaginatedOrders, summary="Danh sách đơn hàng")
def list_orders(
    status: Optional[str] = Query(None, description="Lọc theo trạng thái"),
    page:   int           = Query(1, ge=1),
    limit:  int           = Query(20, ge=1, le=100),
    db: Session = Depends(get_db),
):
    query = (
        db.query(
            DonHang,
            KhachHang.TEN_KH.label("ten_gui"),
            LoTrinh.TEN_LT.label("ten_lt"),
        )
        .join(KhachHang, DonHang.ID_KH_GUI == KhachHang.ID_KH)
        .join(LoTrinh,   DonHang.ID_LT     == LoTrinh.ID_LT)
    )

    if status:
        query = query.filter(DonHang.TRANG_THAI == status)

    total  = query.count()
    rows   = query.offset((page - 1) * limit).limit(limit).all()

    items = []
    for dh, ten_gui, ten_lt in rows:
        # Lấy tên người nhận riêng
        nhan = db.get(KhachHang, dh.ID_KH_NHAN)
        items.append(DonHangListItem(
            ID_DH          = dh.ID_DH,
            TRANG_THAI     = dh.TRANG_THAI,
            KHOI_LUONG     = dh.KHOI_LUONG,
            QUANG_DUONG    = dh.QUANG_DUONG,
            ten_nguoi_gui  = ten_gui,
            ten_nguoi_nhan = nhan.TEN_KH if nhan else "",
            ten_lo_trinh   = ten_lt,
            cod            = tinh_cod(dh.KHOI_LUONG, dh.QUANG_DUONG),
        ))

    return PaginatedOrders(data=items, total=total, page=page, limit=limit)


@router.post("", response_model=DonHangCreated, status_code=status.HTTP_201_CREATED, summary="Tạo đơn hàng mới")
def create_order(body: DonHangCreate, db: Session = Depends(get_db)):
    # Validate foreign keys tồn tại
    if not db.get(KhachHang, body.ID_KH_GUI):
        raise HTTPException(400, f"Khách hàng gửi '{body.ID_KH_GUI}' không tồn tại")
    if not db.get(KhachHang, body.ID_KH_NHAN):
        raise HTTPException(400, f"Khách hàng nhận '{body.ID_KH_NHAN}' không tồn tại")
    if not db.get(LoTrinh, body.ID_LT):
        raise HTTPException(400, f"Lộ trình '{body.ID_LT}' không tồn tại")

    id_dh = _gen_id(db)
    cod   = tinh_cod(body.KHOI_LUONG, body.QUANG_DUONG)

    order = DonHang(
        ID_DH       = id_dh,
        KHOI_LUONG  = body.KHOI_LUONG,
        QUANG_DUONG = body.QUANG_DUONG,
        TRANG_THAI  = "Cho xu ly",
        THANH_TIEN  = body.THANH_TIEN,
        ID_KH_GUI   = body.ID_KH_GUI,
        ID_KH_NHAN  = body.ID_KH_NHAN,
        ID_LT       = body.ID_LT,
        ID_HD       = None,
    )
    db.add(order)
    db.commit()
    db.refresh(order)

    return DonHangCreated(ID_DH=id_dh, TRANG_THAI="Cho xu ly", cod=cod)


@router.get("/{id_dh}", response_model=DonHangDetail, summary="Chi tiết đơn hàng")
def get_order(id_dh: str, db: Session = Depends(get_db)):
    dh = _get_order_or_404(id_dh, db)
    gui  = db.get(KhachHang, dh.ID_KH_GUI)
    nhan = db.get(KhachHang, dh.ID_KH_NHAN)
    lt   = db.get(LoTrinh,   dh.ID_LT)

    return DonHangDetail(
        **{c.name: getattr(dh, c.name) for c in DonHang.__table__.columns},
        ten_nguoi_gui  = gui.TEN_KH  if gui  else None,
        ten_nguoi_nhan = nhan.TEN_KH if nhan else None,
        ten_lo_trinh   = lt.TEN_LT   if lt   else None,
        cod            = tinh_cod(dh.KHOI_LUONG, dh.QUANG_DUONG),
    )


@router.patch("/{id_dh}/status", response_model=DonHangDetail, summary="Cập nhật trạng thái đơn")
def update_status(id_dh: str, body: DonHangStatusUpdate, db: Session = Depends(get_db)):
    dh = _get_order_or_404(id_dh, db)
    dh.TRANG_THAI = body.TRANG_THAI
    db.commit()
    db.refresh(dh)
    return get_order(id_dh, db)


@router.get("/{id_dh}/tracking", summary="Lịch sử vận chuyển")
def tracking(id_dh: str, db: Session = Depends(get_db)):
    dh = _get_order_or_404(id_dh, db)
    lt = db.get(LoTrinh, dh.ID_LT)

    van_dons = (
        db.query(ChiTietVanDon)
        .filter(ChiTietVanDon.ID_DH == id_dh)
        .order_by(ChiTietVanDon.THOI_GIAN_NHAN_HANG)
        .all()
    )

    history = []
    for vd in van_dons:
        pc = vd.phan_cong
        cd = pc.chang_duong if pc else None
        bd = db.get(DiemTrungChuyen, cd.ID_DTC_BD) if cd else None
        kt = db.get(DiemTrungChuyen, cd.ID_DTC_KT) if cd else None

        history.append({
            "id_vd":          vd.ID_VD,
            "trang_thai":     vd.TRANG_THAI,
            "thoi_gian_nhan": vd.THOI_GIAN_NHAN_HANG,
            "thoi_gian_giao": vd.THOI_GIAN_GIAO_HANG,
            "chang_duong":    f"{bd.TEN_DTC} → {kt.TEN_DTC}" if bd and kt else None,
            "nhan_vien":      pc.nhan_vien.TEN_NV if pc and pc.nhan_vien else None,
            "phuong_tien":    pc.BIEN_SO if pc else None,
        })

    return {
        "id_dh":     dh.ID_DH,
        "trang_thai": dh.TRANG_THAI,
        "lo_trinh":  lt.TEN_LT if lt else None,
        "history":   history,
    }
