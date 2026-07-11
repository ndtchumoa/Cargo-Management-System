-- ============================================================
-- Cargo Management System — Cloud Database Init Script
-- Chạy script này SAU KHI Railway tạo xong MySQL instance
-- Thứ tự: CreateTab → Func_calCOD → Func_View → Func_Role → trigger → InsertData
-- ============================================================

-- Đảm bảo dùng đúng database
CREATE DATABASE IF NOT EXISTS cargo_db
  CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
USE cargo_db;

-- Sau đó chạy lần lượt:
-- SOURCE database/schema/CreateTab.sql
-- SOURCE database/functions/Func_calCOD.sql
-- SOURCE database/functions/Func_showDH.sql
-- SOURCE database/functions/Func_View.sql
-- SOURCE database/functions/Func_Role.sql
-- SOURCE database/triggers/trigger1.sql
-- SOURCE database/triggers/trigger2.sql
-- SOURCE database/data/InsertData.sql
