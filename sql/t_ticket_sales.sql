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

 Date: 26/11/2025 01:32:58
*/

SET NAMES utf8mb4;
SET FOREIGN_KEY_CHECKS = 0;

-- ----------------------------
-- Table structure for t_ticket_sales
-- ----------------------------
DROP TABLE IF EXISTS `t_ticket_sales`;
CREATE TABLE `t_ticket_sales` (
  `id` varchar(50) NOT NULL COMMENT '主键',
  `order_no` varchar(50) DEFAULT NULL COMMENT '订单编号',
  `sales_channel` smallint(6) DEFAULT NULL COMMENT '销售渠道（1 - 官网，2-OTA 平台，3 - 线下窗口，4 - 自助售票机）',
  `channel_name` varchar(100) DEFAULT NULL COMMENT '渠道名称（如 "携程""景区官网"）',
  `scenic_id` varchar(50) DEFAULT NULL COMMENT '景点 ID',
  `scenic_name` varchar(255) DEFAULT NULL COMMENT '景点名称',
  `ticket_type` smallint(6) DEFAULT NULL COMMENT '票务类型（1 - 成人票，2 - 儿童票，3 - 老人票，4 - 联票）',
  `ticket_price` decimal(10,2) DEFAULT NULL COMMENT '单张票价（单位：元）',
  `ticket_quantity` int(11) DEFAULT NULL COMMENT '销售数量',
  `total_amount` decimal(10,2) DEFAULT NULL COMMENT '订单总金额（单位：元）',
  `payment_status` smallint(6) DEFAULT NULL COMMENT '支付状态（1 - 已支付，2 - 未支付，3 - 已退款）',
  `payment_time` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP COMMENT '支付时间',
  `refund_amount` decimal(10,2) DEFAULT NULL COMMENT '退款金额（单位：元）',
  `refund_time` date DEFAULT NULL COMMENT '退款时间',
  `settlement_status` smallint(6) DEFAULT NULL COMMENT '分账状态（1 - 未分账，2 - 已分账，3 - 分账中）',
  `settlement_amount` decimal(10,2) DEFAULT NULL COMMENT '分账金额（单位：元）',
  `settlement_time` date DEFAULT NULL COMMENT '分账时间',
  `create_time` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
  `update_time` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP COMMENT '更新时间',
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- ----------------------------
-- Records of t_ticket_sales
-- ----------------------------
BEGIN;
INSERT INTO `t_ticket_sales` (`id`, `order_no`, `sales_channel`, `channel_name`, `scenic_id`, `scenic_name`, `ticket_type`, `ticket_price`, `ticket_quantity`, `total_amount`, `payment_status`, `payment_time`, `refund_amount`, `refund_time`, `settlement_status`, `settlement_amount`, `settlement_time`, `create_time`, `update_time`) VALUES ('b84a9996-13e4-481f-96e9-f5adca8614ed', 'ORD20251126011105C3ED6803', 1, '官网', 'FJ_FZ_001', '三坊七巷', 0, 15.00, 2, 30.00, 1, '2025-11-26 01:11:05', NULL, NULL, 1, NULL, NULL, '2025-11-26 01:11:05', '2025-11-26 01:11:05');
INSERT INTO `t_ticket_sales` (`id`, `order_no`, `sales_channel`, `channel_name`, `scenic_id`, `scenic_name`, `ticket_type`, `ticket_price`, `ticket_quantity`, `total_amount`, `payment_status`, `payment_time`, `refund_amount`, `refund_time`, `settlement_status`, `settlement_amount`, `settlement_time`, `create_time`, `update_time`) VALUES ('f0faca0f-b8de-49e9-8a2e-c41cc51ea680', 'ORD2025112601111050E02D12', 1, '官网', 'FJ_FZ_001', '三坊七巷', 0, 15.00, 2, 30.00, 1, '2025-11-26 01:11:10', NULL, NULL, 1, NULL, NULL, '2025-11-26 01:11:10', '2025-11-26 01:11:10');
COMMIT;

SET FOREIGN_KEY_CHECKS = 1;
