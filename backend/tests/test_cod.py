"""
Unit tests cho service tính COD.
Kiểm tra logic mirror với fn_TinhCOD() trong MySQL.
"""

import pytest
from decimal import Decimal
from app.services.cod import tinh_cod


class TestTinhCOD:
    """
    Công thức:
    - Phí KL  : kg × 5.000
    - ≤ 100km : km × 1.000
    - ≤ 300km : 100.000 + (km-100) × 800
    - > 300km : 260.000 + (km-300) × 600
    - Làm tròn đến nghìn đồng
    """

    def test_short_distance_under_100km(self):
        """5kg, 50km → 25000 + 50000 = 75000"""
        result = tinh_cod(Decimal("5"), Decimal("50"))
        assert result == Decimal("75000")

    def test_exact_100km_boundary(self):
        """2kg, 100km → 10000 + 100000 = 110000"""
        result = tinh_cod(Decimal("2"), Decimal("100"))
        assert result == Decimal("110000")

    def test_medium_distance_100_to_300km(self):
        """3kg, 200km → 15000 + 100000 + 100*800 = 195000"""
        result = tinh_cod(Decimal("3"), Decimal("200"))
        assert result == Decimal("195000")

    def test_exact_300km_boundary(self):
        """1kg, 300km → 5000 + 100000 + 200*800 = 265000"""
        result = tinh_cod(Decimal("1"), Decimal("300"))
        assert result == Decimal("265000")

    def test_long_distance_over_300km(self):
        """5kg, 760km → 25000 + 260000 + 460*600 = 561000"""
        result = tinh_cod(Decimal("5"), Decimal("760"))
        assert result == Decimal("561000")

    def test_very_long_distance(self):
        """10kg, 1730km → 50000 + 260000 + 1430*600 = 1168000"""
        result = tinh_cod(Decimal("10"), Decimal("1730"))
        assert result == Decimal("1168000")

    def test_rounding_to_nearest_thousand(self):
        """Kết quả luôn chia hết cho 1000."""
        test_cases = [
            (Decimal("1.5"), Decimal("75")),
            (Decimal("3.7"), Decimal("150")),
            (Decimal("7.2"), Decimal("450")),
        ]
        for kl, qd in test_cases:
            result = tinh_cod(kl, qd)
            assert result % 1000 == 0, f"COD({kl},{qd}) = {result} không chia hết cho 1000"

    def test_small_weight_large_distance(self):
        """0.5kg, 1000km → 2500 + 260000 + 700*600 = 682500 → 683000"""
        result = tinh_cod(Decimal("0.5"), Decimal("1000"))
        assert result == Decimal("683000")

    def test_result_always_positive(self):
        """COD luôn dương."""
        result = tinh_cod(Decimal("0.1"), Decimal("1"))
        assert result > 0

    def test_mirrors_mysql_dh001(self):
        """DH001 trong InsertData: KL=5, QD=760 → COD=561000."""
        result = tinh_cod(Decimal("5.0"), Decimal("760.0"))
        assert result == Decimal("561000")

    def test_mirrors_mysql_dh003(self):
        """DH003 trong InsertData: KL=10, QD=100 → 50000+100000=150000."""
        result = tinh_cod(Decimal("10.0"), Decimal("100.0"))
        assert result == Decimal("150000")
