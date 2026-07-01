"""
Model USER ánh xạ với role MySQL đã định nghĩa:
  - role_nv_giao_hang
  - role_quan_ly
  - role_ke_toan
"""

from sqlalchemy import Column, String
from app.database import Base


class User(Base):
    __tablename__ = "APP_USER"

    username   = Column(String(50),  primary_key=True)
    hashed_pw  = Column(String(200), nullable=False)
    role       = Column(String(50),  nullable=False)   # nv_giao_hang | quan_ly | ke_toan
    ten_hien_thi = Column(String(100), nullable=True)
