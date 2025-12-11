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

 Date: 26/11/2025 01:32:30
*/

SET NAMES utf8mb4;
SET FOREIGN_KEY_CHECKS = 0;

-- ----------------------------
-- Table structure for t_scenic
-- ----------------------------
DROP TABLE IF EXISTS `t_scenic`;
CREATE TABLE `t_scenic` (
  `scenic_id` varchar(50) COLLATE utf8mb4_unicode_ci NOT NULL COMMENT '景区唯一ID（建议：行政区划码+自增序号，如110101001）',
  `scenic_name` varchar(100) COLLATE utf8mb4_unicode_ci NOT NULL COMMENT '景区名称',
  `scenic_address` varchar(255) COLLATE utf8mb4_unicode_ci NOT NULL COMMENT '详细地址（省市区+街道门牌）',
  `scenic_phone` varchar(20) COLLATE utf8mb4_unicode_ci DEFAULT NULL COMMENT '联系电话（支持固话/手机，如010-12345678或13800138000）',
  `business_hour` text COLLATE utf8mb4_unicode_ci NOT NULL COMMENT '营业时间段',
  `province` varchar(20) COLLATE utf8mb4_unicode_ci NOT NULL COMMENT '省份（用于地区统计）',
  `city` varchar(30) COLLATE utf8mb4_unicode_ci NOT NULL COMMENT '城市',
  `district` varchar(30) COLLATE utf8mb4_unicode_ci DEFAULT NULL COMMENT '区/县',
  `longitude` decimal(10,7) DEFAULT NULL COMMENT '经度（用于地图展示）',
  `latitude` decimal(10,7) DEFAULT NULL COMMENT '纬度',
  `status` tinyint(4) NOT NULL DEFAULT '1' COMMENT '状态：1-正常营业，0-暂停开放，2-永久关闭',
  `created_at` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP,
  `updated_at` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  PRIMARY KEY (`scenic_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci COMMENT='景区信息表';

-- ----------------------------
-- Records of t_scenic
-- ----------------------------
BEGIN;
INSERT INTO `t_scenic` (`scenic_id`, `scenic_name`, `scenic_address`, `scenic_phone`, `business_hour`, `province`, `city`, `district`, `longitude`, `latitude`, `status`) VALUES
('350203001', '菽庄花园', '福建省厦门市思明区鼓浪屿港仔后路7号', '0592-2063744', '08:00-18:00', '福建省', '厦门市', '思明区', 118.0649500, 24.4419800, 1),
('350203002', '日光岩', '福建省厦门市思明区鼓浪屿晃岩路62号', '0592-2063744', '07:30-18:30', '福建省', '厦门市', '思明区', 118.0627300, 24.4458900, 1),
('350203003', '海底世界', '福建省厦门市思明区鼓浪屿龙头路1-3号', '0592-2060777', '08:30-17:30', '福建省', '厦门市', '思明区', 118.0656700, 24.4472100, 1);
COMMIT;

SET FOREIGN_KEY_CHECKS = 1;
