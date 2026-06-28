"""
Tính phí vận chuyển COD theo công thức Viettel Post.
Mirror chính xác từ hàm fn_TinhCOD() trong MySQL.
"""

from decimal import Decimal, ROUND_HALF_UP


def tinh_cod(khoi_luong: Decimal, quang_duong: Decimal) -> Decimal:
    """
    Tính COD theo công thức phân tầng khoảng cách.

    Phí khối lượng : 5.000 VNĐ/kg
    Phí khoảng cách:
        ≤ 100 km          → 1.000 VNĐ/km
        100 < km ≤ 300    → 800 VNĐ/km (phần vượt 100)
        > 300 km          → 600 VNĐ/km (phần vượt 300)

    Làm tròn đến nghìn đồng gần nhất (ROUND(..., -3)).
    """
    phi_kl = khoi_luong * Decimal("5000")

    if quang_duong <= 100:
        phi_qd = quang_duong * Decimal("1000")
    elif quang_duong <= 300:
        phi_qd = Decimal("100000") + (quang_duong - 100) * Decimal("800")
    else:
        phi_qd = Decimal("260000") + (quang_duong - 300) * Decimal("600")

    tong = phi_kl + phi_qd

    # Làm tròn đến nghìn đồng
    rounded = (tong / 1000).quantize(Decimal("1"), rounding=ROUND_HALF_UP) * 1000
    return rounded
