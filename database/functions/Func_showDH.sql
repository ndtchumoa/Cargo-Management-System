DELIMITER //

CREATE PROCEDURE sp_ThongKeDonHang(
    IN  p_trang_thai  VARCHAR(50),  -- NULL = lay tat ca trang thai
    OUT p_so_luong    INT           -- Tra ve tong so don hang tim duoc
)
COMMENT 'Tra cuu don hang theo trang thai, tra ve danh sach va tong so luong'
BEGIN
    -- Hien thi danh sach chi tiet
    SELECT
        dh.ID_DH,
        kh_gui.TEN_KH                               AS Nguoi_Gui,
        kh_nhan.TEN_KH                              AS Nguoi_Nhan,
        lt.TEN_LT                                   AS Lo_Trinh,
        dh.KHOI_LUONG,
        fn_TinhCOD(dh.KHOI_LUONG, dh.QUANG_DUONG)  AS COD_VND,
        dh.TRANG_THAI
    FROM DON_HANG dh
        JOIN KHACH_HANG kh_gui  ON dh.ID_KH_GUI  = kh_gui.ID_KH
        JOIN KHACH_HANG kh_nhan ON dh.ID_KH_NHAN = kh_nhan.ID_KH
        JOIN LO_TRINH   lt      ON dh.ID_LT       = lt.ID_LT
    WHERE p_trang_thai IS NULL
       OR dh.TRANG_THAI = p_trang_thai
    ORDER BY dh.ID_DH;

    -- Phan 2: Dem tong so luong va gan vao bien OUT
    SELECT COUNT(*) INTO p_so_luong
    FROM DON_HANG
    WHERE p_trang_thai IS NULL
       OR TRANG_THAI = p_trang_thai;
END//

DELIMITER ;

-- Cach goi thu tuc:

-- 1. Lay tat ca don hang 'Da giao' va biet tong so luong
CALL sp_ThongKeDonHang('Da giao', @tong);
SELECT @tong AS Tong_Don_Da_Giao;

-- 2. Lay tat ca don hang khong loc trang thai (truyen NULL)
CALL sp_ThongKeDonHang(NULL, @tong);
SELECT @tong AS Tong_Toan_Bo_Don_Hang;