DELIMITER //

CREATE FUNCTION fn_TinhCOD(
    p_khoi_luong   DECIMAL(10,2),
    p_quang_duong  DECIMAL(10,2)
)
RETURNS DECIMAL(15,2)
DETERMINISTIC       -- cung input -> cung output, khong phu thuoc trang thai DB
COMMENT 'Tinh phi van chuyen (COD) theo cong thuc phan tang khoang cach Viettel Post'
BEGIN
    DECLARE v_phi_kl    DECIMAL(15,2);  -- phi khoi luong
    DECLARE v_phi_qd    DECIMAL(15,2);  -- phi khoang cach
    DECLARE v_cod       DECIMAL(15,2);  -- ket qua cuoi

    -- Phi theo khoi luong: 5.000 VND/kg
    SET v_phi_kl = p_khoi_luong * 5000;

    -- Phi theo khoang cach (phan tang)
    SET v_phi_qd =
        CASE
            WHEN p_quang_duong <= 100
                THEN p_quang_duong * 1000
            WHEN p_quang_duong <= 300
                THEN 100000 + (p_quang_duong - 100) * 800
            ELSE
                260000 + (p_quang_duong - 300) * 600
        END;

    -- Tong phi, lam tron den nghin dong gan nhat
    SET v_cod = ROUND(v_phi_kl + v_phi_qd, -3);
    RETURN v_cod;
END//

DELIMITER ;