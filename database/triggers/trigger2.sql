-- Trigger 2: Kiem tra chang duong cua phan cong phai thuoc
--            lo trinh ma don hang dang di theo
--            (bao toan tinh nhat quan cua chu trinh trong ERD)
DELIMITER //

CREATE TRIGGER trg_KiemTraHanhTrinh
BEFORE INSERT ON CHI_TIET_VAN_DON
FOR EACH ROW
BEGIN
    DECLARE v_lt_don_hang   VARCHAR(10);
    DECLARE v_lt_phan_cong  VARCHAR(10);

    -- Lo trinh cua don hang
    SELECT ID_LT INTO v_lt_don_hang
    FROM   DON_HANG
    WHERE  ID_DH = NEW.ID_DH;

    -- Lo trinh cua chang duong trong phan cong
    SELECT cd.ID_LT INTO v_lt_phan_cong
    FROM   PHAN_CONG pc
        JOIN CHANG_DUONG cd ON pc.ID_CD = cd.ID_CD
    WHERE  pc.ID_PC = NEW.ID_PC;

    IF v_lt_don_hang <> v_lt_phan_cong THEN
        SIGNAL SQLSTATE '45000'
        SET MESSAGE_TEXT =
            'Chang duong cua phan cong khong thuoc lo trinh cua don hang!';
    END IF;
END//

DELIMITER ;