-- NGUYEN DUC THANH - 202419099
-- Buoc 1: Tao cac vai tro (Role) theo chuc nang

CREATE ROLE 'role_nv_giao_hang';   -- Nhan vien giao hang
CREATE ROLE 'role_quan_ly';        -- Quan ly van hanh
CREATE ROLE 'role_ke_toan';        -- Ke toan / thu ngan

-- Buoc 2: Cap quyen cho tung vai tro

-- Nhan vien giao hang: chi xem thong tin can thiet de giao hang
GRANT SELECT ON cargo_db.PHAN_CONG          TO 'role_nv_giao_hang';
GRANT SELECT ON cargo_db.CHANG_DUONG        TO 'role_nv_giao_hang';
GRANT SELECT ON cargo_db.DIEM_TRUNG_CHUYEN  TO 'role_nv_giao_hang';
GRANT SELECT ON cargo_db.DON_HANG           TO 'role_nv_giao_hang';
GRANT SELECT, INSERT, UPDATE
             ON cargo_db.CHI_TIET_VAN_DON   TO 'role_nv_giao_hang';

-- Quan ly: xem tat ca + tao phan cong + cap nhat don hang
GRANT SELECT ON cargo_db.*                  TO 'role_quan_ly';
GRANT INSERT, UPDATE ON cargo_db.PHAN_CONG  TO 'role_quan_ly';
GRANT UPDATE (TRANG_THAI)
             ON cargo_db.DON_HANG           TO 'role_quan_ly';

-- Ke toan: chi xem va cap nhat hoa don, xem don hang
GRANT SELECT ON cargo_db.HOA_DON            TO 'role_ke_toan';
GRANT SELECT ON cargo_db.DON_HANG           TO 'role_ke_toan';
GRANT UPDATE (TRANG_THAI, THOI_GIAN_HOAN_THANH)
             ON cargo_db.HOA_DON            TO 'role_ke_toan';

-- Buoc 3: Tao tai khoan nguoi dung va gan vai tro

CREATE USER 'nv_hung'@'localhost'
    IDENTIFIED BY 'Hung@Secure#2024';
CREATE USER 'ql_tuan'@'localhost'
    IDENTIFIED BY 'Tuan@Manager#2024';
CREATE USER 'kt_mai'@'localhost'
    IDENTIFIED BY 'Mai@Ketoan#2024';

GRANT 'role_nv_giao_hang'  TO 'nv_hung'@'localhost';
GRANT 'role_quan_ly'       TO 'ql_tuan'@'localhost';
GRANT 'role_ke_toan'       TO 'kt_mai'@'localhost';

-- Bat role mac dinh khi dang nhap
SET DEFAULT ROLE 'role_nv_giao_hang'  TO 'nv_hung'@'localhost';
SET DEFAULT ROLE 'role_quan_ly'       TO 'ql_tuan'@'localhost';
SET DEFAULT ROLE 'role_ke_toan'       TO 'kt_mai'@'localhost';

FLUSH PRIVILEGES;

-- Buoc 4 (neu can): Thu hoi quyen

-- REVOKE INSERT ON cargo_db.CHI_TIET_VAN_DON FROM 'role_nv_giao_hang';