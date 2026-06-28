"""
Router: /api/optimize
Tối ưu lộ trình vận chuyển bằng Dijkstra.
"""

from decimal import Decimal
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from pydantic import BaseModel, Field

from app.database import get_db
from app.services.route_optimizer import find_optimal_route

router = APIRouter(prefix="/api/optimize", tags=["Optimize"])


class OptimizeRequest(BaseModel):
    from_dtc:  str     = Field(..., description="ID điểm xuất phát (VD: DTC001)")
    to_dtc:    str     = Field(..., description="ID điểm đích (VD: DTC005)")
    weight_kg: Decimal = Field(..., gt=0, description="Khối lượng hàng (kg)")


@router.post("/route", summary="Tìm lộ trình tối ưu (Dijkstra)")
def optimize_route(body: OptimizeRequest, db: Session = Depends(get_db)):
    """
    Tìm đường đi ngắn nhất giữa 2 điểm trung chuyển.
    Trả về danh sách các node trên đường đi, tổng km,
    COD ước tính và danh sách xe phù hợp còn khả dụng.
    """
    try:
        result = find_optimal_route(
            from_dtc  = body.from_dtc.strip(),
            to_dtc    = body.to_dtc.strip(),
            weight_kg = body.weight_kg,
            db        = db,
        )
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

    return result
