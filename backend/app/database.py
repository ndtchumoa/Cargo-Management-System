from sqlalchemy import create_engine, text
from sqlalchemy.orm import declarative_base, sessionmaker
from app.config import settings

# --- Engine ---
engine = create_engine(
    settings.DATABASE_URL,
    pool_pre_ping=True,       # tự kiểm tra connection còn sống không
    pool_recycle=3600,        # recycle connection sau 1 giờ
    echo=settings.DEBUG,      # in SQL ra console khi DEBUG=True
)

# --- Session ---
SessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine,
)

# --- Base cho tất cả ORM models ---
Base = declarative_base()


# --- Dependency dùng trong FastAPI routers ---
def get_db():
    """
    Yield một database session, tự đóng sau khi request xong.
    Dùng với Depends(get_db) trong router.
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def check_connection() -> bool:
    """Kiểm tra kết nối database khi startup."""
    try:
        with engine.connect() as conn:
            conn.execute(text("SELECT 1"))
        return True
    except Exception as e:
        print(f"[DB] Lỗi kết nối: {e}")
        return False
