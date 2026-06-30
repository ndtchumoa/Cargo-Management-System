-- NGUYEN DUC THANH - 202419099 
-- View 1: Thong tin don hang danh cho nhan vien giao hang
--         An email va dia chi; chi hien 3 chu so cuoi SDT

CREATE VIEW vw_DonHang_NhanVien AS
SELECT
    dh.ID_DH,
    dh.TRANG_THAI,
    dh.KHOI_LUONG,
    -- An thong tin nhay cam nguoi gui
    CONCAT(LEFT(kh_gui.TEN_KH, 2), N'***')     AS Ten_Nguoi_Gui,
    CONCAT(N'*******', RIGHT(kh_gui.SDT, 3))   AS SDT_Nguoi_Gui,
    -- An thong tin nhay cam nguoi nhan
    kh_nhan.TEN_KH                              AS Ten_Nguoi_Nhan,
    CONCAT(N'*******', RIGHT(kh_nhan.SDT, 3))   AS SDT_Nguoi_Nhan,
    lt.TEN_LT                                   AS Lo_Trinh
FROM DON_HANG dh
    JOIN KHACH_HANG kh_gui  ON dh.ID_KH_GUI  = kh_gui.ID_KH
    JOIN KHACH_HANG kh_nhan ON dh.ID_KH_NHAN = kh_nhan.ID_KH
    JOIN LO_TRINH   lt      ON dh.ID_LT      = lt.ID_LT;

-- View 2: Thong tin hoa don danh cho ke toan
--         An SDT, email khach hang; chi hien ten va ma KH

CREATE VIEW vw_HoaDon_KeToan AS
SELECT
    hd.ID_HD,
    hd.THOI_GIAN_TAO,
    hd.THOI_GIAN_HOAN_THANH,
    hd.TRANG_THAI                                           AS TT_Hoa_Don,
    COUNT(dh.ID_DH)                                         AS So_Don_Hang,
    SUM(fn_TinhCOD(dh.KHOI_LUONG, dh.QUANG_DUONG))          AS Tong_COD,
    SUM(dh.THANH_TIEN)                                      AS Tong_Gia_Tri_Hang,
    SUM(fn_TinhCOD(dh.KHOI_LUONG, dh.QUANG_DUONG))
        + SUM(dh.THANH_TIEN)                                AS Tong_Tien_Phai_Thu
FROM HOA_DON hd
    JOIN DON_HANG dh ON hd.ID_HD = dh.ID_HD
GROUP BY hd.ID_HD, hd.THOI_GIAN_TAO,
         hd.THOI_GIAN_HOAN_THANH, hd.TRANG_THAI;

-- Phan quyen: cap quyen xem VIEW, khong cap quyen bang goc

GRANT SELECT ON cargo_db.vw_DonHang_NhanVien TO 'role_nv_giao_hang';
GRANT SELECT ON cargo_db.vw_HoaDon_KeToan    TO 'role_ke_toan';

-- Thu hoi quyen truy cap bang goc KHACH_HANG tu nhan vien giao hang
-- (neu truoc do da cap)
REVOKE SELECT ON cargo_db.KHACH_HANG FROM 'role_nv_giao_hang';

FLUSH PRIVILEGES;
