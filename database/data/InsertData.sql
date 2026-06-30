-- KHACH_HANG
INSERT INTO KHACH_HANG VALUES
('KH001','Nguyen Van An',   'nvan@email.com',     '0901234567', 'So 5 Nguyen Du, Hoan Kiem, Ha Noi'),
('KH002','Tran Thi Binh',   'ttbinh@email.com',   '0912345678', 'So 10 Bach Dang, Hai Chau, Da Nang'),
('KH003','Le Minh Cuong',   'lmcuong@email.com',  '0923456789', 'So 22 Le Loi, Quan 1, TP. Ho Chi Minh'),
('KH004','Pham Thi Dung',   'ptdung@email.com',   '0934567890', 'So 15 Tran Phu, Hong Bang, Hai Phong'),
('KH005','Hoang Van Em',    'hvem@email.com',     '0945678901', 'So 8 Nguyen Trai, Ninh Kieu, Can Tho'),
('KH006','Ngo Thi Phuong',  'ntphuong@email.com', '0956789012', 'So 30 Doi Can, Ba Dinh, Ha Noi'),
('KH007','Bui Van Hoa',     'bvhoa@email.com',    '0967890123', 'So 7 Le Loi, TP. Vinh, Nghe An'),
('KH008','Dang Thi Lan',    'dtlan@email.com',    '0978901234', 'So 15 Tran Phu, TP. Vung Tau, Ba Ria - Vung Tau'),
('KH009','Vu Minh Duc',     'vmduc@email.com',    '0989012345', 'So 20 Hoang Van Thu, TP. Thai Nguyen'),
('KH010','Nguyen Thi Thu',  'ntthu2@email.com',   '0990123456', 'So 3 Hung Vuong, TP. Hue, Thua Thien Hue'),
('KH011','Tran Van Khanh',  'tvkhanh@email.com',  '0901234568', 'So 10 Tran Hung Dao, Hoi An, Quang Nam'),
('KH012','Le Thi Ngoc',     'ltngoc@email.com',   '0912345679', 'So 45 Kim Ma, Ba Dinh, Ha Noi'),
('KH013','Pham Quoc Hung',  'pqhung@email.com',   '0923456780', 'So 25 Tran Phu, Hai Chau, Da Nang'),
('KH014','Hoang Kim Anh',   'hkanh@email.com',    '0934567891', 'So 18 Nguyen Trai, Ninh Kieu, Can Tho'),
('KH015','Do Van Thanh',    'dvthanh@email.com',  '0945678902', 'So 30 To Hieu, Le Chan, Hai Phong'),
('KH016','Nguyen Bich Van', 'nbvan@email.com',    '0956789013', 'So 55 CMT8, Quan 3, TP. Ho Chi Minh');

-- HOA_DON
INSERT INTO HOA_DON VALUES
('HD001','2024-01-15 10:00:00','2024-01-15 14:30:00','Da thanh toan'),
('HD002','2024-01-20 09:00:00','2024-01-22 16:00:00','Da thanh toan'),
('HD003','2024-02-05 11:00:00', NULL,                'Chua thanh toan'),
('HD004','2024-03-05 09:00:00','2024-03-06 10:00:00','Da thanh toan'),
('HD005','2024-03-12 14:00:00','2024-03-14 09:00:00','Da thanh toan'),
('HD006','2024-03-20 11:00:00', NULL,                'Chua thanh toan');

-- LO_TRINH
INSERT INTO LO_TRINH VALUES
('LT001','Ha Noi - Da Nang - TP. Ho Chi Minh','Dang hoat dong'),
('LT002','Ha Noi - Hai Phong',                'Dang hoat dong'),
('LT003','TP. Ho Chi Minh - Can Tho',         'Dang hoat dong'),
('LT004','Ha Noi - Da Nang',                  'Dang hoat dong'),
('LT005','Ha Noi - Vinh - Da Nang',           'Dang hoat dong'),
('LT006','TP. Ho Chi Minh - Vung Tau',        'Dang hoat dong'),
('LT007','Ha Noi - Thai Nguyen',              'Dang hoat dong'),
('LT008','Da Nang - Hoi An',                  'Dang hoat dong');

-- DON_HANG  (ID, KL, QD, TrangThai, ThanhTien, GUI, NHAN, LT, HD)
INSERT INTO DON_HANG VALUES
('DH001', 5.0,  760.0,  'Da giao',         2000000, 'KH001','KH002','LT004','HD001'),
('DH002', 2.5,  760.0,  'Da giao',         500000,  'KH001','KH003','LT004','HD001'),
('DH003', 10.0, 100.0,  'Da giao',         5000000, 'KH006','KH004','LT002','HD002'),
('DH004', 3.0,  1730.0, 'Da giao',         1500000, 'KH001','KH003','LT001','HD003'),
('DH005', 7.0,  100.0,  'Dang van chuyen', 3000000, 'KH001','KH004','LT002', NULL),
('DH006', 1.5,  170.0,  'Dang van chuyen', 300000,  'KH003','KH005','LT003', NULL),
('DH007', 4.0,  760.0,  'Cho xu ly',       800000,  'KH006','KH002','LT004', NULL),
('DH008', 8.5,  1730.0, 'Hoan tra',        4000000, 'KH001','KH003','LT001', NULL),
('DH009', 6.0,  760.0,  'Da giao',         2500000, 'KH006','KH002','LT004','HD002'),
('DH010', 12.0, 170.0,  'Cho xu ly',       8000000, 'KH003','KH005','LT003', NULL),
('DH011', 4.0,  760.0,  'Da giao',         1200000, 'KH001','KH007','LT005','HD004'),
('DH012', 6.5,  90.0,   'Da giao',         2800000, 'KH003','KH008','LT006','HD004'),
('DH013', 3.5,  80.0,   'Da giao',         600000,  'KH012','KH009','LT007','HD005'),
('DH014', 9.0,  30.0,   'Dang van chuyen', 3500000, 'KH013','KH011','LT008', NULL),
('DH015', 2.0,  760.0,  'Da giao',         400000,  'KH012','KH002','LT004','HD005'),
('DH016', 15.0, 1730.0, 'Dang van chuyen', 10000000,'KH001','KH016','LT001', NULL),
('DH017', 5.5,  100.0,  'Da giao',         1800000, 'KH012','KH015','LT002','HD006'),
('DH018', 8.0,  90.0,   'Da giao',         5000000, 'KH014','KH003','LT006','HD006'),
('DH019', 11.0, 80.0,   'Dang van chuyen', 7500000, 'KH009','KH006','LT007', NULL),
('DH020', 7.5,  30.0,   'Dang van chuyen', 4200000, 'KH013','KH010','LT008', NULL);

-- DIEM_TRUNG_CHUYEN
INSERT INTO DIEM_TRUNG_CHUYEN VALUES
('DTC001','Kho Ha Noi',     '18 Le Van Luong, Cau Giay, Ha Noi',          '07:00-19:00'),
('DTC002','Kho Da Nang',    '45 Nguyen Van Linh, Thanh Khe, Da Nang',     '08:00-18:00'),
('DTC003','Kho TP. HCM',    '100 Nguyen Thi Minh Khai, Q3, TP. HCM',      '07:00-21:00'),
('DTC004','Kho Hai Phong',  '23 Tran Phu, Le Chan, Hai Phong',            '08:00-18:00'),
('DTC005','Kho Can Tho',    '56 Duong 30/4, Ninh Kieu, Can Tho',          '08:00-17:00'),
('DTC006','Kho Vinh',       '12 Nguyen Thi Minh Khai, TP. Vinh, Nghe An', '08:00-17:00'),
('DTC007','Kho Vung Tau',   '35 Tran Hung Dao, TP. Vung Tau',             '08:00-18:00'),
('DTC008','Kho Thai Nguyen','25 Hoang Van Thu, TP. Thai Nguyen',          '07:30-17:30'),
('DTC009','Kho Hoi An',     '10 Le Loi, Hoi An, Quang Nam',               '08:00-17:00'),
('DTC010','Kho Hue',        '45 Hung Vuong, TP. Hue, Thua Thien Hue',     '08:00-18:00');

-- CHANG_DUONG (ID, STT, LT, DTC_BD, DTC_KT)
INSERT INTO CHANG_DUONG VALUES
('CD001',1,'LT001','DTC001','DTC002'), -- LT001 Chang 1: HN -> DN
('CD002',2,'LT001','DTC002','DTC003'), -- LT001 Chang 2: DN -> HCM
('CD003',1,'LT002','DTC001','DTC004'), -- LT002 Chang 1: HN -> HP
('CD004',1,'LT003','DTC003','DTC005'), -- LT003 Chang 1: HCM -> CT
('CD005',1,'LT004','DTC001','DTC002'), -- LT004 Chang 1: HN -> DN
('CD006',1,'LT005','DTC001','DTC006'), -- LT005 Chang 1: HN -> Vinh
('CD007',2,'LT005','DTC006','DTC002'), -- LT005 Chang 2: Vinh -> DN
('CD008',1,'LT006','DTC003','DTC007'), -- LT006 Chang 1: HCM -> VT
('CD009',1,'LT007','DTC001','DTC008'), -- LT007 Chang 1: HN  -> TN
('CD010',1,'LT008','DTC002','DTC009'); -- LT008 Chang 1: DN  -> HoiAn

-- PHUONG_TIEN
INSERT INTO PHUONG_TIEN VALUES
('29A-12345','Xe tai nho',   500.0,   'Hoat dong'),
('29B-67890','Xe tai lon',   2000.0,  'Hoat dong'),
('51C-11111','Xe container', 10000.0, 'Bao tri'),
('15D-22222','Xe tai nho',   500.0,   'Hoat dong'),
('51D-33333','Xe tai lon',   3000.0,  'Hoat dong'),
('29C-44444','Xe tai nho',   800.0,   'Hoat dong'),
('30E-55555','Xe container', 15000.0, 'Hoat dong'),
('14F-66666','Xe tai nho',   600.0,   'Bao tri');

-- NHAN_VIEN_GIAO_HANG
INSERT INTO NHAN_VIEN_GIAO_HANG VALUES
('NV001','Nguyen Van Hung', '0901111111','hung.nvh@cty.vn',  '5 Doi Can, Ba Dinh, Ha Noi'),
('NV002','Tran Thi Kim',    '0902222222','kim.tt@cty.vn',    '12 Tran Phu, Hai Chau, Da Nang'),
('NV003','Le Van Son',      '0903333333','son.lv@cty.vn',    '8 Nguyen Hue, Q1, TP. HCM'),
('NV004','Pham Minh Tuan',  '0904444444','tuan.pm@cty.vn',   '20 Giang Vo, Dong Da, Ha Noi'),
('NV005','Hoang Thi Lan',   '0905555555','lan.ht@cty.vn',    '33 Tran Hung Dao, Le Chan, HP'),
('NV006','Nguyen Thi Huong','0906666666','huong.nth@cty.vn', '18 Nguyen Du, Hoan Kiem, Ha Noi'),
('NV007','Tran Van Nam',    '0907777777','nam.tv@cty.vn',    '5 Nguyen Thi Minh Khai, TP. Vinh, Nghe An'),
('NV008','Le Thi Mai',      '0908888888','mai.lt@cty.vn',    '35 Tran Hung Dao, TP. Vung Tau'),
('NV009','Pham Van Duc',    '0909999999','duc.pv@cty.vn',    '25 Hoang Van Thu, TP. Thai Nguyen'),
('NV010','Hoang Van Tuan',  '0910000000','tuan.hv@cty.vn',   '10 Le Loi, Hoi An, Quang Nam');

-- PHAN_CONG (ID, CaLam, CD, NV, XE)
INSERT INTO PHAN_CONG VALUES
('PC001','Ca sang 06:00-14:00', 'CD005','NV001','29A-12345'),
('PC002','Ca chieu 14:00-22:00','CD005','NV004','29B-67890'),
('PC003','Ca sang 06:00-14:00', 'CD001','NV001','29A-12345'),
('PC004','Ca chieu 14:00-22:00','CD002','NV002','29B-67890'),
('PC005','Ca sang 06:00-14:00', 'CD003','NV004','15D-22222'),
('PC006','Ca chieu 14:00-22:00','CD003','NV005','15D-22222'),
('PC007','Ca sang 06:00-14:00', 'CD004','NV003','29A-12345'),
('PC008','Ca sang 06:00-14:00', 'CD006','NV006','29C-44444'),
('PC009','Ca chieu 14:00-22:00','CD007','NV007','51D-33333'),
('PC010','Ca sang 06:00-14:00', 'CD008','NV008','29B-67890'),
('PC011','Ca sang 06:00-14:00', 'CD009','NV009','29C-44444'),
('PC012','Ca sang 06:00-14:00', 'CD010','NV010','29A-12345'),
('PC013','Ca chieu 14:00-22:00','CD003','NV006','51D-33333'),
('PC014','Ca chieu 14:00-22:00','CD008','NV003','29C-44444'),
('PC015','Ca chieu 14:00-22:00','CD005','NV001','51D-33333');

-- CHI_TIET_VAN_DON (ID, TrangThai, TG_Nhan, TG_Giao, DH, PC)
INSERT INTO CHI_TIET_VAN_DON VALUES
('VD001','Da giao',         '2024-01-10 07:30:00','2024-01-12 16:00:00','DH001','PC001'),
('VD002','Da giao',         '2024-01-10 07:30:00','2024-01-12 16:00:00','DH002','PC001'),
('VD003','Da giao',         '2024-01-18 08:00:00','2024-01-18 14:30:00','DH003','PC005'),
('VD004','Da giao',         '2024-02-01 07:00:00','2024-02-03 15:00:00','DH004','PC003'),
('VD005','Da giao',         '2024-02-03 16:00:00','2024-02-05 18:00:00','DH004','PC004'),
('VD006','Dang van chuyen', '2024-02-10 08:00:00', NULL,                'DH005','PC006'),
('VD007','Dang van chuyen', '2024-02-12 09:00:00', NULL,                'DH006','PC007'),
('VD008','Da giao',         '2024-02-01 07:00:00','2024-02-03 15:00:00','DH008','PC003'),
('VD009','Hoan tra',        '2024-02-03 16:00:00','2024-02-04 10:00:00','DH008','PC004'),
('VD010','Da giao',         '2024-01-20 06:30:00','2024-01-22 15:00:00','DH009','PC002'),
('VD011','Da giao',         '2024-03-01 07:00:00','2024-03-03 15:00:00','DH011','PC008'),
('VD012','Da giao',         '2024-03-03 16:00:00','2024-03-04 18:00:00','DH011','PC009'),
('VD013','Da giao',         '2024-03-05 08:00:00','2024-03-05 13:30:00','DH012','PC010'),
('VD014','Da giao',         '2024-03-08 07:30:00','2024-03-08 11:00:00','DH013','PC011'),
('VD015','Dang van chuyen', '2024-03-10 09:00:00', NULL,                'DH014','PC012'),
('VD016','Da giao',         '2024-03-12 06:30:00','2024-03-14 15:00:00','DH015','PC002'),
('VD017','Da giao',         '2024-03-15 08:00:00','2024-03-15 13:00:00','DH017','PC013'),
('VD018','Da giao',         '2024-03-18 09:00:00','2024-03-18 14:30:00','DH018','PC014'),
('VD019','Dang van chuyen', '2024-03-20 07:00:00', NULL,                'DH019','PC011'),
('VD020','Dang van chuyen', '2024-03-22 09:00:00', NULL,                'DH020','PC012');