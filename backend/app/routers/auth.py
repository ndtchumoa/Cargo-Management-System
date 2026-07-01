"""
Router: /api/auth
Xác thực người dùng và cấp JWT token.
"""

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from pydantic import BaseModel

from app.database import get_db
from app.models.user import User
from app.services.auth import verify_password, create_access_token, hash_password
from app.dependencies import require_auth

router = APIRouter(prefix="/api/auth", tags=["Auth"])


# ── Schemas ──────────────────────────────────────────────────────

class LoginRequest(BaseModel):
    username: str
    password: str


class TokenResponse(BaseModel):
    access_token: str
    token_type:   str = "bearer"
    role:         str
    ten_hien_thi: str


# ── Endpoints ────────────────────────────────────────────────────

@router.post("/login", response_model=TokenResponse, summary="Đăng nhập lấy JWT token")
def login(body: LoginRequest, db: Session = Depends(get_db)):
    user = db.get(User, body.username)
    if not user or not verify_password(body.password, user.hashed_pw):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Tên đăng nhập hoặc mật khẩu không đúng",
        )

    token = create_access_token({
        "sub":  user.username,
        "role": user.role,
    })

    return TokenResponse(
        access_token = token,
        role         = user.role,
        ten_hien_thi = user.ten_hien_thi or user.username,
    )


@router.get("/me", summary="Thông tin người dùng hiện tại")
def get_me(payload: dict = Depends(require_auth)):
    return {
        "username": payload.get("sub"),
        "role":     payload.get("role"),
    }


# ── Seed users (chỉ dùng khi DEV) ───────────────────────────────

@router.post("/seed-users", summary="[DEV] Tạo tài khoản mặc định", include_in_schema=False)
def seed_users(db: Session = Depends(get_db)):
    """
    Tạo 3 tài khoản mặc định tương ứng 3 role đã định nghĩa trong MySQL.
    Chỉ gọi 1 lần khi setup môi trường mới.
    """
    default_users = [
        User(username="nv_hung",  hashed_pw=hash_password("Hung@Secure#2024"),
             role="nv_giao_hang", ten_hien_thi="Nguyễn Văn Hùng"),
        User(username="ql_tuan",  hashed_pw=hash_password("Tuan@Manager#2024"),
             role="quan_ly",      ten_hien_thi="Phạm Minh Tuấn"),
        User(username="kt_mai",   hashed_pw=hash_password("Mai@Ketoan#2024"),
             role="ke_toan",      ten_hien_thi="Lê Thị Mai"),
    ]

    created = []
    for u in default_users:
        existing = db.get(User, u.username)
        if not existing:
            db.add(u)
            created.append(u.username)

    db.commit()
    return {"created": created, "message": f"Đã tạo {len(created)} tài khoản"}
