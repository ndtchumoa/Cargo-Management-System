"""
Router: /api/analytics
Các endpoint phân tích doanh thu, vận hành.
"""

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from sqlalchemy import func, case, text, extract

from app.database import get_db
from app.models.all import DonHang, HoaDon, LoTrinh, PhuongTien, KhachHang
from app.services.cod import tinh_cod

router = APIRouter(prefix="/api/analytics", tags=["Analytics"])


@router.get("/revenue", summary="Doanh thu theo tháng")
def revenue_by_month(db: Session = Depends(get_db)):
    """
    Tổng COD + giá trị hàng của các đơn đã có hóa đơn, nhóm theo tháng.
    Dùng extract() — SQLAlchemy tự dịch sang hàm đúng dialect (MySQL/SQLite).
    """
    thang_expr = extract("month", HoaDon.THOI_GIAN_TAO).label("thang")
    nam_expr   = extract("year",  HoaDon.THOI_GIAN_TAO).label("nam")

    rows = (
        db.query(
            thang_expr,
            nam_expr,
            func.count(DonHang.ID_DH).label("so_don"),
            func.sum(DonHang.THANH_TIEN).label("tong_gia_tri_hang"),
        )
        .join(DonHang, HoaDon.ID_HD == DonHang.ID_HD)
        .group_by("nam", "thang")
        .order_by("nam", "thang")
        .all()
    )

    result = []
    for r in rows:
        thang = int(r.thang)
        nam   = int(r.nam)

        # Lấy các đơn trong tháng đó để tính COD
        don_hangs = (
            db.query(DonHang)
            .join(HoaDon, DonHang.ID_HD == HoaDon.ID_HD)
            .filter(
                extract("year",  HoaDon.THOI_GIAN_TAO) == nam,
                extract("month", HoaDon.THOI_GIAN_TAO) == thang,
            )
            .all()
        )
        tong_cod = sum(float(tinh_cod(dh.KHOI_LUONG, dh.QUANG_DUONG)) for dh in don_hangs)

        result.append({
            "nam":               nam,
            "thang":             thang,
            "so_don":            r.so_don,
            "tong_cod":          tong_cod,
            "tong_gia_tri_hang": float(r.tong_gia_tri_hang or 0),
            "tong_doanh_thu":    tong_cod + float(r.tong_gia_tri_hang or 0),
        })

    return result


@router.get("/return-rate", summary="Tỉ lệ hoàn trả theo lộ trình")
def return_rate_by_route(db: Session = Depends(get_db)):
    rows = (
        db.query(
            LoTrinh.ID_LT,
            LoTrinh.TEN_LT,
            func.count(DonHang.ID_DH).label("tong_don"),
            func.sum(
                case((DonHang.TRANG_THAI == "Hoan tra", 1), else_=0)
            ).label("so_hoan_tra"),
        )
        .join(DonHang, LoTrinh.ID_LT == DonHang.ID_LT)
        .group_by(LoTrinh.ID_LT, LoTrinh.TEN_LT)
        .order_by(LoTrinh.ID_LT)
        .all()
    )

    return [
        {
            "id_lt":       r.ID_LT,
            "ten_lt":      r.TEN_LT,
            "tong_don":    r.tong_don,
            "so_hoan_tra": int(r.so_hoan_tra or 0),
            "ti_le_pct":   round(int(r.so_hoan_tra or 0) / r.tong_don * 100, 1),
        }
        for r in rows
    ]


@router.get("/top-routes", summary="Top lộ trình nhiều đơn nhất")
def top_routes(limit: int = 5, db: Session = Depends(get_db)):
    rows = (
        db.query(
            LoTrinh.ID_LT,
            LoTrinh.TEN_LT,
            func.count(DonHang.ID_DH).label("so_don"),
            func.sum(DonHang.THANH_TIEN).label("tong_gia_tri"),
        )
        .join(DonHang, LoTrinh.ID_LT == DonHang.ID_LT)
        .group_by(LoTrinh.ID_LT, LoTrinh.TEN_LT)
        .order_by(func.count(DonHang.ID_DH).desc())
        .limit(limit)
        .all()
    )

    return [
        {
            "id_lt":       r.ID_LT,
            "ten_lt":      r.TEN_LT,
            "so_don":      r.so_don,
            "tong_gia_tri": float(r.tong_gia_tri or 0),
        }
        for r in rows
    ]


@router.get("/vehicle-status", summary="Trạng thái phương tiện")
def vehicle_status(db: Session = Depends(get_db)):
    rows = (
        db.query(
            PhuongTien.TRANG_THAI,
            PhuongTien.LOAI_PT,
            func.count(PhuongTien.BIEN_SO).label("so_luong"),
        )
        .group_by(PhuongTien.TRANG_THAI, PhuongTien.LOAI_PT)
        .order_by(PhuongTien.TRANG_THAI, PhuongTien.LOAI_PT)
        .all()
    )

    return [
        {
            "trang_thai": r.TRANG_THAI,
            "loai_pt":    r.LOAI_PT,
            "so_luong":   r.so_luong,
        }
        for r in rows
    ]


@router.get("/top-customers", summary="Top khách hàng gửi nhiều nhất")
def top_customers(limit: int = 5, db: Session = Depends(get_db)):
    rows = (
        db.query(
            KhachHang.ID_KH,
            KhachHang.TEN_KH,
            func.count(DonHang.ID_DH).label("so_don"),
            func.sum(DonHang.THANH_TIEN).label("tong_gia_tri"),
        )
        .join(DonHang, KhachHang.ID_KH == DonHang.ID_KH_GUI)
        .group_by(KhachHang.ID_KH, KhachHang.TEN_KH)
        .order_by(func.count(DonHang.ID_DH).desc())
        .limit(limit)
        .all()
    )

    return [
        {
            "id_kh":       r.ID_KH,
            "ten_kh":      r.TEN_KH,
            "so_don":      r.so_don,
            "tong_gia_tri": float(r.tong_gia_tri or 0),
        }
        for r in rows
    ]


@router.get("/order-status-summary", summary="Tổng hợp đơn hàng theo trạng thái")
def order_status_summary(db: Session = Depends(get_db)):
    rows = (
        db.query(
            DonHang.TRANG_THAI,
            func.count(DonHang.ID_DH).label("so_luong"),
        )
        .group_by(DonHang.TRANG_THAI)
        .all()
    )

    return [{"trang_thai": r.TRANG_THAI, "so_luong": r.so_luong} for r in rows]
