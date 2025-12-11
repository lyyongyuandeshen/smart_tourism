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

 Date: 26/11/2025 01:32:42
*/

SET NAMES utf8mb4;
SET FOREIGN_KEY_CHECKS = 0;

-- ----------------------------
-- Table structure for t_scenic_guide
-- ----------------------------
DROP TABLE IF EXISTS `t_scenic_guide`;
CREATE TABLE `t_scenic_guide` (
  `id` varchar(50) NOT NULL,
  `scenic_id` varchar(50) DEFAULT NULL,
  `guide_title` varchar(255) DEFAULT NULL,
  `historical_background` text,
  `cultural_value` text,
  `architectural_features` text,
  `historical_stories` text,
  `ecological_science` text,
  `open_status` smallint(6) DEFAULT NULL,
  `last_bus_time` varchar(20) DEFAULT NULL,
  `evacuation_route_url` varchar(512) DEFAULT NULL,
  `create_time` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP,
  `update_time` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- ----------------------------
-- Records of t_scenic_guide
-- ----------------------------
BEGIN;
COMMIT;

SET FOREIGN_KEY_CHECKS = 1;
