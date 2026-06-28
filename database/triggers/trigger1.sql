-- Trigger 1: Kiem tra phuong tien phai o trang thai 'Hoat dong'
--            truoc khi tao PHAN_CONG moi
DELIMITER //

CREATE TRIGGER trg_KiemTraPhuongTien
BEFORE INSERT ON PHAN_CONG
FOR EACH ROW
BEGIN
    DECLARE v_trang_thai VARCHAR(50);

    SELECT TRANG_THAI INTO v_trang_thai
    FROM   PHUONG_TIEN
    WHERE  BIEN_SO = NEW.BIEN_SO;

    IF v_trang_thai <> 'Hoat dong' THEN
        SIGNAL SQLSTATE '45000'
        SET MESSAGE_TEXT =
            'Phuong tien khong o trang thai Hoat dong, khong the phan cong!';
    END IF;
END//

DELIMITER ;