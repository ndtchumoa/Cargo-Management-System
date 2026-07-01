"""
FastAPI dependencies dùng để bảo vệ các route cần xác thực.

Cách dùng trong router:
    from app.dependencies import require_auth, require_role

    @router.get("/secret")
    def secret(user = Depends(require_auth)):
        return {"user": user["sub"]}

    @router.post("/admin")
    def admin(user = Depends(require_role("quan_ly"))):
        ...
"""

from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from jose import JWTError

from app.services.auth import decode_token

bearer_scheme = HTTPBearer()


def require_auth(
    credentials: HTTPAuthorizationCredentials = Depends(bearer_scheme),
) -> dict:
    """
    Validate JWT token từ header Authorization: Bearer <token>.
    Trả về payload nếu hợp lệ, raise 401 nếu không.
    """
    exc = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Token không hợp lệ hoặc đã hết hạn",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = decode_token(credentials.credentials)
        if "sub" not in payload:
            raise exc
        return payload
    except JWTError:
        raise exc


def require_role(*allowed_roles: str):
    """
    Factory trả về dependency kiểm tra role.
    Dùng: Depends(require_role("quan_ly", "ke_toan"))
    """
    def _check(payload: dict = Depends(require_auth)) -> dict:
        role = payload.get("role", "")
        if role not in allowed_roles:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail=f"Chức năng này yêu cầu quyền: {', '.join(allowed_roles)}",
            )
        return payload
    return _check
