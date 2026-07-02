"""
Router: /api/assignments
Phân công nhân viên + phương tiện vào chặng đường.
MySQL trigger trg_KiemTraPhuongTien và trg_KiemTraHanhTrinh
tự validate — API chỉ cần bắt lỗi từ trigger và trả về message rõ ràng.
"""

from __future__ import annotations
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from sqlalchemy import func, text
from sqlalchemy.exc import OperationalError

from app.database import get_db
from app.models.all import PhanCong, ChangDuong, NhanVienGiaoHang, PhuongTien
from app.dependencies import require_role
from pydantic import BaseModel, Field, ConfigDict

router = APIRouter(prefix="/api/assignments", tags=["Assignments"])


# ── Schemas ──────────────────────────────────

class PhanCongCreate(BaseModel):
    CA_LAM:  str = Field(..., description="VD: Ca sang 06:00-14:00")
    ID_CD:   str = Field(..., max_length=10)
    ID_NV:   str = Field(..., max_length=10)
    BIEN_SO: str = Field(..., max_length=15)


class PhanCongResponse(BaseModel):
    ID_PC: str
    CA_LAM: str
    ID_CD: str
    ten_chang: str
    ID_NV: str
    ten_nv: str
    BIEN_SO: str
    loai_pt: str
    trang_thai_pt: str

    model_config = ConfigDict(from_attributes=True)


# ── Helper ────────────────────────────────────

def _gen_id(db: Session) -> str:
    count = db.query(func.count(PhanCong.ID_PC)).scalar() or 0
    return f"PC{count + 1:03d}"


# ── Endpoints ────────────────────────────────

@router.get("", summary="Danh sách phân công")
def list_assignments(db: Session = Depends(get_db)):
    pcs = db.query(PhanCong).all()
    result = []
    for pc in pcs:
        cd = pc.chang_duong
        nv = pc.nhan_vien
        pt = pc.phuong_tien
        bd = cd.diem_bd if cd else None
        kt = cd.diem_kt if cd else None
        result.append(PhanCongResponse(
            ID_PC         = pc.ID_PC,
            CA_LAM        = pc.CA_LAM,
            ID_CD         = pc.ID_CD,
            ten_chang     = f"{bd.TEN_DTC} → {kt.TEN_DTC}" if bd and kt else pc.ID_CD,
            ID_NV         = pc.ID_NV,
            ten_nv        = nv.TEN_NV if nv else "",
            BIEN_SO       = pc.BIEN_SO,
            loai_pt       = pt.LOAI_PT if pt else "",
            trang_thai_pt = pt.TRANG_THAI if pt else "",
        ))
    return result


@router.post("", status_code=status.HTTP_201_CREATED, summary="Tạo phân công mới")
def create_assignment(body: PhanCongCreate, db: Session = Depends(get_db), _: dict = Depends(require_role("quan_ly"))):
    # Validate FK tồn tại
    if not db.get(ChangDuong,       body.ID_CD):
        raise HTTPException(400, f"Chặng đường '{body.ID_CD}' không tồn tại")
    if not db.get(NhanVienGiaoHang, body.ID_NV):
        raise HTTPException(400, f"Nhân viên '{body.ID_NV}' không tồn tại")
    if not db.get(PhuongTien,       body.BIEN_SO):
        raise HTTPException(400, f"Phương tiện '{body.BIEN_SO}' không tồn tại")

    id_pc = _gen_id(db)
    pc = PhanCong(
        ID_PC   = id_pc,
        CA_LAM  = body.CA_LAM,
        ID_CD   = body.ID_CD,
        ID_NV   = body.ID_NV,
        BIEN_SO = body.BIEN_SO,
    )

    try:
        db.add(pc)
        db.commit()
        db.refresh(pc)
    except OperationalError as e:
        db.rollback()
        # Bắt lỗi từ MySQL trigger và trả về message thân thiện
        err = str(e.orig)
        if "Phuong tien khong o trang thai Hoat dong" in err:
            raise HTTPException(400, "Phương tiện đang bảo trì, không thể phân công")
        if "Chang duong cua phan cong khong thuoc lo trinh" in err:
            raise HTTPException(400, "Chặng đường không thuộc lộ trình của đơn hàng")
        raise HTTPException(500, f"Lỗi database: {err}")

    cd = pc.chang_duong
    nv = pc.nhan_vien
    pt = pc.phuong_tien
    bd = cd.diem_bd if cd else None
    kt = cd.diem_kt if cd else None

    return PhanCongResponse(
        ID_PC         = pc.ID_PC,
        CA_LAM        = pc.CA_LAM,
        ID_CD         = pc.ID_CD,
        ten_chang     = f"{bd.TEN_DTC} → {kt.TEN_DTC}" if bd and kt else pc.ID_CD,
        ID_NV         = pc.ID_NV,
        ten_nv        = nv.TEN_NV if nv else "",
        BIEN_SO       = pc.BIEN_SO,
        loai_pt       = pt.LOAI_PT if pt else "",
        trang_thai_pt = pt.TRANG_THAI if pt else "",
    )
