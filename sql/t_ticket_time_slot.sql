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

 Date: 26/11/2025 01:33:08
*/

SET NAMES utf8mb4;
SET FOREIGN_KEY_CHECKS = 0;

-- ----------------------------
-- Table structure for t_ticket_time_slot
-- ----------------------------
DROP TABLE IF EXISTS `t_ticket_time_slot`;
CREATE TABLE `t_ticket_time_slot` (
  `id` varchar(50) NOT NULL,
  `ticket_id` varchar(50) DEFAULT NULL,
  `scenic_id` varchar(50) DEFAULT NULL,
  `reservation_date` date DEFAULT NULL,
  `start_time` varchar(20) DEFAULT NULL,
  `end_time` varchar(20) DEFAULT NULL,
  `total_quota` int(11) DEFAULT NULL,
  `used_quota` int(11) DEFAULT NULL,
  `remaining_quota` int(11) DEFAULT NULL,
  `create_time` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP,
  `update_time` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- ----------------------------
-- Records of t_ticket_time_slot
-- ----------------------------
BEGIN;
INSERT INTO `t_ticket_time_slot` (`id`, `ticket_id`, `scenic_id`, `reservation_date`, `start_time`, `end_time`, `total_quota`, `used_quota`, `remaining_quota`, `create_time`, `update_time`) VALUES ('TS_FJ_FZ_001_1', 'T_FJ_FZ_001_1', 'FJ_FZ_001', '2025-11-27', '08:30', '12:00', 50, 4, 46, '2025-11-26 00:10:38', '2025-11-26 01:11:10');
INSERT INTO `t_ticket_time_slot` (`id`, `ticket_id`, `scenic_id`, `reservation_date`, `start_time`, `end_time`, `total_quota`, `used_quota`, `remaining_quota`, `create_time`, `update_time`) VALUES ('TS_FJ_FZ_001_2', 'T_FJ_FZ_001_2', 'FJ_FZ_001', '2025-11-27', '13:30', '18:00', 50, 0, 50, '2025-11-26 00:10:38', '2025-11-26 00:10:38');
INSERT INTO `t_ticket_time_slot` (`id`, `ticket_id`, `scenic_id`, `reservation_date`, `start_time`, `end_time`, `total_quota`, `used_quota`, `remaining_quota`, `create_time`, `update_time`) VALUES ('TS_FJ_FZ_002_1', 'T_FJ_FZ_002_1', 'FJ_FZ_002', '2025-11-27', '08:00', '11:30', 50, 0, 50, '2025-11-26 00:10:38', '2025-11-26 00:10:38');
INSERT INTO `t_ticket_time_slot` (`id`, `ticket_id`, `scenic_id`, `reservation_date`, `start_time`, `end_time`, `total_quota`, `used_quota`, `remaining_quota`, `create_time`, `update_time`) VALUES ('TS_FJ_FZ_002_2', 'T_FJ_FZ_002_2', 'FJ_FZ_002', '2025-11-27', '13:00', '16:30', 50, 0, 50, '2025-11-26 00:10:38', '2025-11-26 00:10:38');
INSERT INTO `t_ticket_time_slot` (`id`, `ticket_id`, `scenic_id`, `reservation_date`, `start_time`, `end_time`, `total_quota`, `used_quota`, `remaining_quota`, `create_time`, `update_time`) VALUES ('TS_FJ_LY_001_1', 'T_FJ_LY_001_1', 'FJ_LY_001', '2025-11-27', '08:00', '12:00', 50, 0, 50, '2025-11-26 00:10:38', '2025-11-26 00:10:38');
INSERT INTO `t_ticket_time_slot` (`id`, `ticket_id`, `scenic_id`, `reservation_date`, `start_time`, `end_time`, `total_quota`, `used_quota`, `remaining_quota`, `create_time`, `update_time`) VALUES ('TS_FJ_LY_001_2', 'T_FJ_LY_001_2', 'FJ_LY_001', '2025-11-27', '13:30', '17:30', 50, 0, 50, '2025-11-26 00:10:38', '2025-11-26 00:10:38');
INSERT INTO `t_ticket_time_slot` (`id`, `ticket_id`, `scenic_id`, `reservation_date`, `start_time`, `end_time`, `total_quota`, `used_quota`, `remaining_quota`, `create_time`, `update_time`) VALUES ('TS_FJ_LY_002_1', 'T_FJ_LY_002_1', 'FJ_LY_002', '2025-11-27', '08:00', '11:30', 50, 0, 50, '2025-11-26 00:10:38', '2025-11-26 00:10:38');
INSERT INTO `t_ticket_time_slot` (`id`, `ticket_id`, `scenic_id`, `reservation_date`, `start_time`, `end_time`, `total_quota`, `used_quota`, `remaining_quota`, `create_time`, `update_time`) VALUES ('TS_FJ_LY_002_2', 'T_FJ_LY_002_2', 'FJ_LY_002', '2025-11-27', '13:00', '16:30', 50, 0, 50, '2025-11-26 00:10:38', '2025-11-26 00:10:38');
INSERT INTO `t_ticket_time_slot` (`id`, `ticket_id`, `scenic_id`, `reservation_date`, `start_time`, `end_time`, `total_quota`, `used_quota`, `remaining_quota`, `create_time`, `update_time`) VALUES ('TS_FJ_ND_001_1', 'T_FJ_ND_001_1', 'FJ_ND_001', '2025-11-27', '07:30', '12:00', 50, 0, 50, '2025-11-26 00:10:38', '2025-11-26 00:10:38');
INSERT INTO `t_ticket_time_slot` (`id`, `ticket_id`, `scenic_id`, `reservation_date`, `start_time`, `end_time`, `total_quota`, `used_quota`, `remaining_quota`, `create_time`, `update_time`) VALUES ('TS_FJ_ND_001_2', 'T_FJ_ND_001_2', 'FJ_ND_001', '2025-11-27', '13:30', '16:30', 50, 0, 50, '2025-11-26 00:10:38', '2025-11-26 00:10:38');
INSERT INTO `t_ticket_time_slot` (`id`, `ticket_id`, `scenic_id`, `reservation_date`, `start_time`, `end_time`, `total_quota`, `used_quota`, `remaining_quota`, `create_time`, `update_time`) VALUES ('TS_FJ_ND_002_1', 'T_FJ_ND_002_1', 'FJ_ND_002', '2025-11-27', '06:30', '11:30', 50, 0, 50, '2025-11-26 00:10:38', '2025-11-26 00:10:38');
INSERT INTO `t_ticket_time_slot` (`id`, `ticket_id`, `scenic_id`, `reservation_date`, `start_time`, `end_time`, `total_quota`, `used_quota`, `remaining_quota`, `create_time`, `update_time`) VALUES ('TS_FJ_ND_002_2', 'T_FJ_ND_002_2', 'FJ_ND_002', '2025-11-27', '13:00', '17:00', 50, 0, 50, '2025-11-26 00:10:38', '2025-11-26 00:10:38');
INSERT INTO `t_ticket_time_slot` (`id`, `ticket_id`, `scenic_id`, `reservation_date`, `start_time`, `end_time`, `total_quota`, `used_quota`, `remaining_quota`, `create_time`, `update_time`) VALUES ('TS_FJ_NP_001_1', 'T_FJ_NP_001_1', 'FJ_NP_001', '2025-11-27', '07:00', '12:00', 50, 0, 50, '2025-11-26 00:10:38', '2025-11-26 00:10:38');
INSERT INTO `t_ticket_time_slot` (`id`, `ticket_id`, `scenic_id`, `reservation_date`, `start_time`, `end_time`, `total_quota`, `used_quota`, `remaining_quota`, `create_time`, `update_time`) VALUES ('TS_FJ_NP_001_2', 'T_FJ_NP_001_2', 'FJ_NP_001', '2025-11-27', '13:30', '17:00', 50, 0, 50, '2025-11-26 00:10:38', '2025-11-26 00:10:38');
INSERT INTO `t_ticket_time_slot` (`id`, `ticket_id`, `scenic_id`, `reservation_date`, `start_time`, `end_time`, `total_quota`, `used_quota`, `remaining_quota`, `create_time`, `update_time`) VALUES ('TS_FJ_NP_002_1', 'T_FJ_NP_002_1', 'FJ_NP_002', '2025-11-27', '07:00', '11:30', 50, 0, 50, '2025-11-26 00:10:38', '2025-11-26 00:10:38');
INSERT INTO `t_ticket_time_slot` (`id`, `ticket_id`, `scenic_id`, `reservation_date`, `start_time`, `end_time`, `total_quota`, `used_quota`, `remaining_quota`, `create_time`, `update_time`) VALUES ('TS_FJ_NP_002_2', 'T_FJ_NP_002_2', 'FJ_NP_002', '2025-11-27', '13:00', '16:30', 50, 0, 50, '2025-11-26 00:10:38', '2025-11-26 00:10:38');
INSERT INTO `t_ticket_time_slot` (`id`, `ticket_id`, `scenic_id`, `reservation_date`, `start_time`, `end_time`, `total_quota`, `used_quota`, `remaining_quota`, `create_time`, `update_time`) VALUES ('TS_FJ_PTZX_001_1', 'T_FJ_PTZX_001_1', 'FJ_PTZX_001', '2025-11-27', '08:30', '12:00', 50, 0, 50, '2025-11-26 00:10:38', '2025-11-26 00:10:38');
INSERT INTO `t_ticket_time_slot` (`id`, `ticket_id`, `scenic_id`, `reservation_date`, `start_time`, `end_time`, `total_quota`, `used_quota`, `remaining_quota`, `create_time`, `update_time`) VALUES ('TS_FJ_PTZX_001_2', 'T_FJ_PTZX_001_2', 'FJ_PTZX_001', '2025-11-27', '14:00', '18:00', 50, 0, 50, '2025-11-26 00:10:38', '2025-11-26 00:10:38');
INSERT INTO `t_ticket_time_slot` (`id`, `ticket_id`, `scenic_id`, `reservation_date`, `start_time`, `end_time`, `total_quota`, `used_quota`, `remaining_quota`, `create_time`, `update_time`) VALUES ('TS_FJ_PTZX_002_1', 'T_FJ_PTZX_002_1', 'FJ_PTZX_002', '2025-11-27', '08:00', '12:00', 50, 0, 50, '2025-11-26 00:10:38', '2025-11-26 00:10:38');
INSERT INTO `t_ticket_time_slot` (`id`, `ticket_id`, `scenic_id`, `reservation_date`, `start_time`, `end_time`, `total_quota`, `used_quota`, `remaining_quota`, `create_time`, `update_time`) VALUES ('TS_FJ_PTZX_002_2', 'T_FJ_PTZX_002_2', 'FJ_PTZX_002', '2025-11-27', '13:30', '17:30', 50, 0, 50, '2025-11-26 00:10:38', '2025-11-26 00:10:38');
INSERT INTO `t_ticket_time_slot` (`id`, `ticket_id`, `scenic_id`, `reservation_date`, `start_time`, `end_time`, `total_quota`, `used_quota`, `remaining_quota`, `create_time`, `update_time`) VALUES ('TS_FJ_PT_001_1', 'T_FJ_PT_001_1', 'FJ_PT_001', '2025-11-27', '06:30', '11:30', 50, 0, 50, '2025-11-26 00:10:38', '2025-11-26 00:10:38');
INSERT INTO `t_ticket_time_slot` (`id`, `ticket_id`, `scenic_id`, `reservation_date`, `start_time`, `end_time`, `total_quota`, `used_quota`, `remaining_quota`, `create_time`, `update_time`) VALUES ('TS_FJ_PT_001_2', 'T_FJ_PT_001_2', 'FJ_PT_001', '2025-11-27', '13:30', '17:30', 50, 0, 50, '2025-11-26 00:10:38', '2025-11-26 00:10:38');
INSERT INTO `t_ticket_time_slot` (`id`, `ticket_id`, `scenic_id`, `reservation_date`, `start_time`, `end_time`, `total_quota`, `used_quota`, `remaining_quota`, `create_time`, `update_time`) VALUES ('TS_FJ_PT_002_1', 'T_FJ_PT_002_1', 'FJ_PT_002', '2025-11-27', '08:00', '12:00', 50, 0, 50, '2025-11-26 00:10:38', '2025-11-26 00:10:38');
INSERT INTO `t_ticket_time_slot` (`id`, `ticket_id`, `scenic_id`, `reservation_date`, `start_time`, `end_time`, `total_quota`, `used_quota`, `remaining_quota`, `create_time`, `update_time`) VALUES ('TS_FJ_PT_002_2', 'T_FJ_PT_002_2', 'FJ_PT_002', '2025-11-27', '13:00', '16:30', 50, 0, 50, '2025-11-26 00:10:38', '2025-11-26 00:10:38');
INSERT INTO `t_ticket_time_slot` (`id`, `ticket_id`, `scenic_id`, `reservation_date`, `start_time`, `end_time`, `total_quota`, `used_quota`, `remaining_quota`, `create_time`, `update_time`) VALUES ('TS_FJ_QZ_001_1', 'T_FJ_QZ_001_1', 'FJ_QZ_001', '2025-11-27', '07:30', '12:00', 50, 0, 50, '2025-11-26 00:10:38', '2025-11-26 00:10:38');
INSERT INTO `t_ticket_time_slot` (`id`, `ticket_id`, `scenic_id`, `reservation_date`, `start_time`, `end_time`, `total_quota`, `used_quota`, `remaining_quota`, `create_time`, `update_time`) VALUES ('TS_FJ_QZ_001_2', 'T_FJ_QZ_001_2', 'FJ_QZ_001', '2025-11-27', '13:30', '17:00', 50, 0, 50, '2025-11-26 00:10:38', '2025-11-26 00:10:38');
INSERT INTO `t_ticket_time_slot` (`id`, `ticket_id`, `scenic_id`, `reservation_date`, `start_time`, `end_time`, `total_quota`, `used_quota`, `remaining_quota`, `create_time`, `update_time`) VALUES ('TS_FJ_QZ_002_1', 'T_FJ_QZ_002_1', 'FJ_QZ_002', '2025-11-27', '08:00', '11:30', 50, 0, 50, '2025-11-26 00:10:38', '2025-11-26 00:10:38');
INSERT INTO `t_ticket_time_slot` (`id`, `ticket_id`, `scenic_id`, `reservation_date`, `start_time`, `end_time`, `total_quota`, `used_quota`, `remaining_quota`, `create_time`, `update_time`) VALUES ('TS_FJ_QZ_002_2', 'T_FJ_QZ_002_2', 'FJ_QZ_002', '2025-11-27', '14:00', '17:30', 50, 0, 50, '2025-11-26 00:10:38', '2025-11-26 00:10:38');
INSERT INTO `t_ticket_time_slot` (`id`, `ticket_id`, `scenic_id`, `reservation_date`, `start_time`, `end_time`, `total_quota`, `used_quota`, `remaining_quota`, `create_time`, `update_time`) VALUES ('TS_FJ_QZ_003_1', 'T_FJ_QZ_003_1', 'FJ_QZ_003', '2025-11-27', '08:00', '12:00', 50, 0, 50, '2025-11-26 00:10:38', '2025-11-26 00:10:38');
INSERT INTO `t_ticket_time_slot` (`id`, `ticket_id`, `scenic_id`, `reservation_date`, `start_time`, `end_time`, `total_quota`, `used_quota`, `remaining_quota`, `create_time`, `update_time`) VALUES ('TS_FJ_QZ_003_2', 'T_FJ_QZ_003_2', 'FJ_QZ_003', '2025-11-27', '14:00', '17:30', 50, 0, 50, '2025-11-26 00:10:38', '2025-11-26 00:10:38');
INSERT INTO `t_ticket_time_slot` (`id`, `ticket_id`, `scenic_id`, `reservation_date`, `start_time`, `end_time`, `total_quota`, `used_quota`, `remaining_quota`, `create_time`, `update_time`) VALUES ('TS_FJ_SM_001_1', 'T_FJ_SM_001_1', 'FJ_SM_001', '2025-11-27', '08:00', '12:00', 50, 0, 50, '2025-11-26 00:10:38', '2025-11-26 00:10:38');
INSERT INTO `t_ticket_time_slot` (`id`, `ticket_id`, `scenic_id`, `reservation_date`, `start_time`, `end_time`, `total_quota`, `used_quota`, `remaining_quota`, `create_time`, `update_time`) VALUES ('TS_FJ_SM_001_2', 'T_FJ_SM_001_2', 'FJ_SM_001', '2025-11-27', '13:30', '16:30', 50, 0, 50, '2025-11-26 00:10:38', '2025-11-26 00:10:38');
INSERT INTO `t_ticket_time_slot` (`id`, `ticket_id`, `scenic_id`, `reservation_date`, `start_time`, `end_time`, `total_quota`, `used_quota`, `remaining_quota`, `create_time`, `update_time`) VALUES ('TS_FJ_SM_002_1', 'T_FJ_SM_002_1', 'FJ_SM_002', '2025-11-27', '08:00', '11:30', 50, 0, 50, '2025-11-26 00:10:38', '2025-11-26 00:10:38');
INSERT INTO `t_ticket_time_slot` (`id`, `ticket_id`, `scenic_id`, `reservation_date`, `start_time`, `end_time`, `total_quota`, `used_quota`, `remaining_quota`, `create_time`, `update_time`) VALUES ('TS_FJ_SM_002_2', 'T_FJ_SM_002_2', 'FJ_SM_002', '2025-11-27', '13:30', '17:00', 50, 0, 50, '2025-11-26 00:10:38', '2025-11-26 00:10:38');
INSERT INTO `t_ticket_time_slot` (`id`, `ticket_id`, `scenic_id`, `reservation_date`, `start_time`, `end_time`, `total_quota`, `used_quota`, `remaining_quota`, `create_time`, `update_time`) VALUES ('TS_FJ_XM_001_1', 'T_FJ_XM_001_1', 'FJ_XM_001', '2025-11-27', '07:00', '12:00', 50, 0, 50, '2025-11-26 00:10:38', '2025-11-26 00:10:38');
INSERT INTO `t_ticket_time_slot` (`id`, `ticket_id`, `scenic_id`, `reservation_date`, `start_time`, `end_time`, `total_quota`, `used_quota`, `remaining_quota`, `create_time`, `update_time`) VALUES ('TS_FJ_XM_001_2', 'T_FJ_XM_001_2', 'FJ_XM_001', '2025-11-27', '13:30', '18:00', 50, 0, 50, '2025-11-26 00:10:38', '2025-11-26 00:10:38');
INSERT INTO `t_ticket_time_slot` (`id`, `ticket_id`, `scenic_id`, `reservation_date`, `start_time`, `end_time`, `total_quota`, `used_quota`, `remaining_quota`, `create_time`, `update_time`) VALUES ('TS_FJ_XM_002_1', 'T_FJ_XM_002_1', 'FJ_XM_002', '2025-11-27', '06:30', '12:00', 50, 0, 50, '2025-11-26 00:10:38', '2025-11-26 00:10:38');
INSERT INTO `t_ticket_time_slot` (`id`, `ticket_id`, `scenic_id`, `reservation_date`, `start_time`, `end_time`, `total_quota`, `used_quota`, `remaining_quota`, `create_time`, `update_time`) VALUES ('TS_FJ_XM_002_2', 'T_FJ_XM_002_2', 'FJ_XM_002', '2025-11-27', '13:00', '18:30', 50, 0, 50, '2025-11-26 00:10:38', '2025-11-26 00:10:38');
INSERT INTO `t_ticket_time_slot` (`id`, `ticket_id`, `scenic_id`, `reservation_date`, `start_time`, `end_time`, `total_quota`, `used_quota`, `remaining_quota`, `create_time`, `update_time`) VALUES ('TS_FJ_XM_003_1', 'T_FJ_XM_003_1', 'FJ_XM_003', '2025-11-27', '08:30', '11:30', 50, 0, 50, '2025-11-26 00:10:38', '2025-11-26 00:10:38');
INSERT INTO `t_ticket_time_slot` (`id`, `ticket_id`, `scenic_id`, `reservation_date`, `start_time`, `end_time`, `total_quota`, `used_quota`, `remaining_quota`, `create_time`, `update_time`) VALUES ('TS_FJ_XM_003_2', 'T_FJ_XM_003_2', 'FJ_XM_003', '2025-11-27', '14:30', '17:30', 50, 0, 50, '2025-11-26 00:10:38', '2025-11-26 00:10:38');
INSERT INTO `t_ticket_time_slot` (`id`, `ticket_id`, `scenic_id`, `reservation_date`, `start_time`, `end_time`, `total_quota`, `used_quota`, `remaining_quota`, `create_time`, `update_time`) VALUES ('TS_FJ_ZZ_001_1', 'T_FJ_ZZ_001_1', 'FJ_ZZ_001', '2025-11-27', '08:00', '12:00', 50, 0, 50, '2025-11-26 00:10:38', '2025-11-26 00:10:38');
INSERT INTO `t_ticket_time_slot` (`id`, `ticket_id`, `scenic_id`, `reservation_date`, `start_time`, `end_time`, `total_quota`, `used_quota`, `remaining_quota`, `create_time`, `update_time`) VALUES ('TS_FJ_ZZ_001_2', 'T_FJ_ZZ_001_2', 'FJ_ZZ_001', '2025-11-27', '13:30', '17:30', 50, 0, 50, '2025-11-26 00:10:38', '2025-11-26 00:10:38');
INSERT INTO `t_ticket_time_slot` (`id`, `ticket_id`, `scenic_id`, `reservation_date`, `start_time`, `end_time`, `total_quota`, `used_quota`, `remaining_quota`, `create_time`, `update_time`) VALUES ('TS_FJ_ZZ_002_1', 'T_FJ_ZZ_002_1', 'FJ_ZZ_002', '2025-11-27', '08:00', '12:00', 50, 0, 50, '2025-11-26 00:10:38', '2025-11-26 00:10:38');
INSERT INTO `t_ticket_time_slot` (`id`, `ticket_id`, `scenic_id`, `reservation_date`, `start_time`, `end_time`, `total_quota`, `used_quota`, `remaining_quota`, `create_time`, `update_time`) VALUES ('TS_FJ_ZZ_002_2', 'T_FJ_ZZ_002_2', 'FJ_ZZ_002', '2025-11-27', '14:00', '18:00', 50, 0, 50, '2025-11-26 00:10:38', '2025-11-26 00:10:38');
COMMIT;

SET FOREIGN_KEY_CHECKS = 1;
