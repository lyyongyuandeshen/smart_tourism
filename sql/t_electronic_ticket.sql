/*
 Navicat Premium Dump SQL

 Source Server         : mysql
 Source Server Type    : MySQL
 Source Server Version : 50710 (5.7.10-log)
 Source Host           : localhost:3306
 Source Schema         : db_smart_tourism

 Target Server Type    : MySQL
 Target Server Version : 50710 (5.7.10-log)
 File Encoding         : 65001

 Date: 26/11/2025 01:32:10
*/

SET NAMES utf8mb4;
SET FOREIGN_KEY_CHECKS = 0;

-- ----------------------------
-- Table structure for t_electronic_ticket
-- ----------------------------
DROP TABLE IF EXISTS `t_electronic_ticket`;
CREATE TABLE `t_electronic_ticket` (
  `id` varchar(50) NOT NULL,
  `order_id` varchar(50) DEFAULT NULL,
  `ticket_id` varchar(50) DEFAULT NULL,
  `qr_code_url` varchar(512) DEFAULT NULL,
  `verification_code` varchar(50) DEFAULT NULL,
  `valid_start_date` date DEFAULT NULL,
  `valid_end_date` date DEFAULT NULL,
  `verification_status` smallint(6) DEFAULT NULL,
  `refund_status` smallint(6) DEFAULT NULL,
  `create_time` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP,
  `update_time` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- ----------------------------
-- Records of t_electronic_ticket
-- ----------------------------
BEGIN;
INSERT INTO `t_electronic_ticket` (`id`, `order_id`, `ticket_id`, `qr_code_url`, `verification_code`, `valid_start_date`, `valid_end_date`, `verification_status`, `refund_status`, `create_time`, `update_time`) VALUES ('04da703e-b6d7-4ddb-bcb6-346836a0c7bf', 'ORD2025112601111050E02D12', 'T_FJ_FZ_001_1', 'https://qrcode.example.com/ticket/04da703e-b6d7-4ddb-bcb6-346836a0c7bf?code=CD5BA518AECA8AAD', 'CD5BA518AECA8AAD', '2025-11-25', '2025-11-25', 1, 1, '2025-11-26 01:11:10', '2025-11-26 01:11:10');
INSERT INTO `t_electronic_ticket` (`id`, `order_id`, `ticket_id`, `qr_code_url`, `verification_code`, `valid_start_date`, `valid_end_date`, `verification_status`, `refund_status`, `create_time`, `update_time`) VALUES ('62443bf0-390c-4ff3-8a5d-d566a00d5534', 'ORD20251126011105C3ED6803', 'T_FJ_FZ_001_1', 'https://qrcode.example.com/ticket/62443bf0-390c-4ff3-8a5d-d566a00d5534?code=8039A759F354426B', '8039A759F354426B', '2025-11-25', '2025-11-25', 1, 1, '2025-11-26 01:11:05', '2025-11-26 01:11:05');
INSERT INTO `t_electronic_ticket` (`id`, `order_id`, `ticket_id`, `qr_code_url`, `verification_code`, `valid_start_date`, `valid_end_date`, `verification_status`, `refund_status`, `create_time`, `update_time`) VALUES ('d1791f2b-3f34-401f-9763-01323af5e032', 'ORD2025112601111050E02D12', 'T_FJ_FZ_001_1', 'https://qrcode.example.com/ticket/d1791f2b-3f34-401f-9763-01323af5e032?code=ED9620C412AADAFD', 'ED9620C412AADAFD', '2025-11-25', '2025-11-25', 1, 1, '2025-11-26 01:11:10', '2025-11-26 01:11:10');
INSERT INTO `t_electronic_ticket` (`id`, `order_id`, `ticket_id`, `qr_code_url`, `verification_code`, `valid_start_date`, `valid_end_date`, `verification_status`, `refund_status`, `create_time`, `update_time`) VALUES ('de773305-7a10-44c2-89a5-7c0842bad71e', 'ORD20251126011105C3ED6803', 'T_FJ_FZ_001_1', 'https://qrcode.example.com/ticket/de773305-7a10-44c2-89a5-7c0842bad71e?code=27E1E6F61718EFB4', '27E1E6F61718EFB4', '2025-11-25', '2025-11-25', 1, 1, '2025-11-26 01:11:05', '2025-11-26 01:11:05');
COMMIT;

SET FOREIGN_KEY_CHECKS = 1;
