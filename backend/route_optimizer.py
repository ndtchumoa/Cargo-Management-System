"""
Tối ưu lộ trình bằng thuật toán Dijkstra.
Xây đồ thị có hướng từ bảng CHANG_DUONG, mỗi chặng là 1 cạnh
với trọng số là QUANG_DUONG (km).
"""

from __future__ import annotations
import networkx as nx
from decimal import Decimal
from sqlalchemy.orm import Session

from app.models.all import ChangDuong, DiemTrungChuyen, PhuongTien
from app.services.cod import tinh_cod


def build_graph(db: Session) -> nx.DiGraph:
    """
    Xây đồ thị có hướng từ toàn bộ chặng đường trong DB.
    Node  = ID_DTC (điểm trung chuyển)
    Cạnh  = (ID_DTC_BD → ID_DTC_KT) với trọng số = khoảng cách km.

    Lưu ý: CHANG_DUONG hiện chưa có cột KHOANG_CACH — dùng
    giá trị ước tính mặc định theo lộ trình thực tế Việt Nam.
    Khi thêm ALTER TABLE CHANG_DUONG ADD COLUMN KHOANG_CACH thì
    chỉ cần thay dòng weight=... bên dưới.
    """
    # Khoảng cách ước tính (km) theo chặng thực tế
    DISTANCE_ESTIMATE = {
        ("DTC001", "DTC002"): 760,   # HN → DN
        ("DTC002", "DTC003"): 970,   # DN → HCM
        ("DTC001", "DTC004"): 100,   # HN → HP
        ("DTC003", "DTC005"): 170,   # HCM → CT
        ("DTC001", "DTC006"): 290,   # HN → Vinh
        ("DTC006", "DTC002"): 470,   # Vinh → DN
        ("DTC003", "DTC007"): 90,    # HCM → VT
        ("DTC001", "DTC008"): 80,    # HN → TN
        ("DTC002", "DTC009"): 30,    # DN → HoiAn
    }

    G = nx.DiGraph()

    chang_duongs = db.query(ChangDuong).all()
    for cd in chang_duongs:
        km = DISTANCE_ESTIMATE.get((cd.ID_DTC_BD, cd.ID_DTC_KT), 100)
        G.add_edge(
            cd.ID_DTC_BD,
            cd.ID_DTC_KT,
            weight   = km,
            id_cd    = cd.ID_CD,
            id_lt    = cd.ID_LT,
        )

    return G


def find_optimal_route(
    from_dtc:   str,
    to_dtc:     str,
    weight_kg:  Decimal,
    db:         Session,
) -> dict:
    """
    Tìm lộ trình ngắn nhất giữa 2 điểm trung chuyển.
    Trả về path, tổng km, COD ước tính, và xe còn khả dụng.
    """
    G = build_graph(db)

    # Validate nodes tồn tại trong đồ thị
    if from_dtc not in G.nodes:
        raise ValueError(f"Điểm xuất phát '{from_dtc}' không có trong đồ thị")
    if to_dtc not in G.nodes:
        raise ValueError(f"Điểm đích '{to_dtc}' không có trong đồ thị")

    try:
        path      = nx.dijkstra_path(G, source=from_dtc, target=to_dtc, weight="weight")
        total_km  = nx.dijkstra_path_length(G, source=from_dtc, target=to_dtc, weight="weight")
    except nx.NetworkXNoPath:
        raise ValueError(f"Không tìm thấy đường đi từ '{from_dtc}' đến '{to_dtc}'")

    # Lấy tên điểm trung chuyển
    dtc_map   = {d.ID_DTC: d.TEN_DTC for d in db.query(DiemTrungChuyen).all()}
    path_names = [dtc_map.get(p, p) for p in path]

    # Tính COD ước tính
    cod = tinh_cod(weight_kg, Decimal(str(total_km)))

    # Tìm xe đang hoạt động và đủ tải trọng
    available_vehicles = (
        db.query(PhuongTien)
        .filter(
            PhuongTien.TRANG_THAI == "Hoat dong",
            PhuongTien.TRONG_TAI  >= float(weight_kg),
        )
        .order_by(PhuongTien.TRONG_TAI)
        .all()
    )

    return {
        "path":       path,
        "path_names": path_names,
        "total_km":   total_km,
        "estimated_cod": float(cod),
        "available_vehicles": [
            {
                "bien_so":   v.BIEN_SO,
                "loai_pt":   v.LOAI_PT,
                "trong_tai": float(v.TRONG_TAI),
            }
            for v in available_vehicles
        ],
    }
