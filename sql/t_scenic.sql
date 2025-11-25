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
INSERT INTO `t_scenic` (`scenic_id`, `scenic_name`, `scenic_address`, `scenic_phone`, `business_hour`, `province`, `city`, `district`, `longitude`, `latitude`, `status`, `created_at`, `updated_at`) VALUES ('FJ_FZ_001', '三坊七巷', '福建省福州市鼓楼区南后街', '0591-87558913', '08:30-12:00,13:30-18:00', '福建省', '福州市', '鼓楼区', 119.2976036, 26.0753021, 1, '2025-11-26 00:06:06', '2025-11-26 00:06:06');
INSERT INTO `t_scenic` (`scenic_id`, `scenic_name`, `scenic_address`, `scenic_phone`, `business_hour`, `province`, `city`, `district`, `longitude`, `latitude`, `status`, `created_at`, `updated_at`) VALUES ('FJ_FZ_002', '鼓山涌泉寺', '福建省福州市晋安区鼓山镇', '0591-83961196', '08:00-11:30,13:00-16:30', '福建省', '福州市', '晋安区', 119.4281540, 26.0827210, 1, '2025-11-26 00:06:06', '2025-11-26 00:06:06');
INSERT INTO `t_scenic` (`scenic_id`, `scenic_name`, `scenic_address`, `scenic_phone`, `business_hour`, `province`, `city`, `district`, `longitude`, `latitude`, `status`, `created_at`, `updated_at`) VALUES ('FJ_LY_001', '永定承启楼', '福建省龙岩市永定区高头乡', '0597-5531111', '08:00-12:00,13:30-17:30', '福建省', '龙岩市', '永定区', 116.7890123, 24.7890123, 1, '2025-11-26 00:06:06', '2025-11-26 00:06:06');
INSERT INTO `t_scenic` (`scenic_id`, `scenic_name`, `scenic_address`, `scenic_phone`, `business_hour`, `province`, `city`, `district`, `longitude`, `latitude`, `status`, `created_at`, `updated_at`) VALUES ('FJ_LY_002', '冠豸山石门湖', '福建省龙岩市连城县莲峰镇', '0597-8912345', '08:00-11:30,13:00-16:30', '福建省', '龙岩市', '连城县', 116.7654321, 25.0123456, 1, '2025-11-26 00:06:06', '2025-11-26 00:06:06');
INSERT INTO `t_scenic` (`scenic_id`, `scenic_name`, `scenic_address`, `scenic_phone`, `business_hour`, `province`, `city`, `district`, `longitude`, `latitude`, `status`, `created_at`, `updated_at`) VALUES ('FJ_ND_001', '白水洋浅水广场', '福建省宁德市屏南县双溪镇', '0593-3389588', '07:30-12:00,13:30-16:30', '福建省', '宁德市', '屏南县', 118.8765432, 26.8765432, 1, '2025-11-26 00:06:06', '2025-11-26 00:06:06');
INSERT INTO `t_scenic` (`scenic_id`, `scenic_name`, `scenic_address`, `scenic_phone`, `business_hour`, `province`, `city`, `district`, `longitude`, `latitude`, `status`, `created_at`, `updated_at`) VALUES ('FJ_ND_002', '太姥山夫妻峰', '福建省宁德市福鼎市太姥山镇', '0593-7299111', '06:30-11:30,13:00-17:00', '福建省', '宁德市', '福鼎市', 120.2345678, 27.2345678, 1, '2025-11-26 00:06:06', '2025-11-26 00:06:06');
INSERT INTO `t_scenic` (`scenic_id`, `scenic_name`, `scenic_address`, `scenic_phone`, `business_hour`, `province`, `city`, `district`, `longitude`, `latitude`, `status`, `created_at`, `updated_at`) VALUES ('FJ_NP_001', '武夷山天游峰', '福建省南平市武夷山市武夷街道', '0599-5135111', '07:00-12:00,13:30-17:00', '福建省', '南平市', '武夷山市', 118.0345678, 27.7432109, 1, '2025-11-26 00:06:06', '2025-11-26 00:06:06');
INSERT INTO `t_scenic` (`scenic_id`, `scenic_name`, `scenic_address`, `scenic_phone`, `business_hour`, `province`, `city`, `district`, `longitude`, `latitude`, `status`, `created_at`, `updated_at`) VALUES ('FJ_NP_002', '九曲溪竹筏码头', '福建省南平市武夷山市星村镇', '0599-5135222', '07:00-11:30,13:00-16:30', '福建省', '南平市', '武夷山市', 118.0234567, 27.7543210, 1, '2025-11-26 00:06:06', '2025-11-26 00:06:06');
INSERT INTO `t_scenic` (`scenic_id`, `scenic_name`, `scenic_address`, `scenic_phone`, `business_hour`, `province`, `city`, `district`, `longitude`, `latitude`, `status`, `created_at`, `updated_at`) VALUES ('FJ_PT_001', '湄洲岛妈祖祖庙', '福建省莆田市秀屿区湄洲镇', '0594-5094301', '06:30-11:30,13:30-17:30', '福建省', '莆田市', '秀屿区', 119.0876543, 25.1234567, 1, '2025-11-26 00:06:06', '2025-11-26 00:06:06');
INSERT INTO `t_scenic` (`scenic_id`, `scenic_name`, `scenic_address`, `scenic_phone`, `business_hour`, `province`, `city`, `district`, `longitude`, `latitude`, `status`, `created_at`, `updated_at`) VALUES ('FJ_PT_002', '九鲤湖', '福建省莆田市仙游县钟山镇', '0594-8692123', '08:00-12:00,13:00-16:30', '福建省', '莆田市', '仙游县', 118.6789012, 25.5678901, 1, '2025-11-26 00:06:06', '2025-11-26 00:06:06');
INSERT INTO `t_scenic` (`scenic_id`, `scenic_name`, `scenic_address`, `scenic_phone`, `business_hour`, `province`, `city`, `district`, `longitude`, `latitude`, `status`, `created_at`, `updated_at`) VALUES ('FJ_PTZX_001', '北港村磹水风韵', '福建省平潭综合实验区北港村', '0591-24311234', '08:30-12:00,14:00-18:00', '福建省', '平潭综合实验区', NULL, 119.8123456, 25.5678901, 1, '2025-11-26 00:06:06', '2025-11-26 00:06:06');
INSERT INTO `t_scenic` (`scenic_id`, `scenic_name`, `scenic_address`, `scenic_phone`, `business_hour`, `province`, `city`, `district`, `longitude`, `latitude`, `status`, `created_at`, `updated_at`) VALUES ('FJ_PTZX_002', '仙人井', '福建省平潭综合实验区流水镇', '0591-24351234', '08:00-12:00,13:30-17:30', '福建省', '平潭综合实验区', NULL, 119.7123456, 25.4123456, 1, '2025-11-26 00:06:06', '2025-11-26 00:06:06');
INSERT INTO `t_scenic` (`scenic_id`, `scenic_name`, `scenic_address`, `scenic_phone`, `business_hour`, `province`, `city`, `district`, `longitude`, `latitude`, `status`, `created_at`, `updated_at`) VALUES ('FJ_QZ_001', '清源山老君岩', '福建省泉州市丰泽区清源山', '0595-22770135', '07:30-12:00,13:30-17:00', '福建省', '泉州市', '丰泽区', 118.5678901, 24.9123456, 1, '2025-11-26 00:06:06', '2025-11-26 00:06:06');
INSERT INTO `t_scenic` (`scenic_id`, `scenic_name`, `scenic_address`, `scenic_phone`, `business_hour`, `province`, `city`, `district`, `longitude`, `latitude`, `status`, `created_at`, `updated_at`) VALUES ('FJ_QZ_002', '开元寺', '福建省泉州市鲤城区西街176号', '0595-22272131', '08:00-11:30,14:00-17:30', '福建省', '泉州市', '鲤城区', 118.5876543, 24.8987654, 1, '2025-11-26 00:06:06', '2025-11-26 00:06:06');
INSERT INTO `t_scenic` (`scenic_id`, `scenic_name`, `scenic_address`, `scenic_phone`, `business_hour`, `province`, `city`, `district`, `longitude`, `latitude`, `status`, `created_at`, `updated_at`) VALUES ('FJ_QZ_003', '崇武古城西门', '福建省泉州市惠安县崇武镇', '0595-87691001', '08:00-12:00,14:00-17:30', '福建省', '泉州市', '惠安县', 119.0123456, 24.8765432, 1, '2025-11-26 00:06:06', '2025-11-26 00:06:06');
INSERT INTO `t_scenic` (`scenic_id`, `scenic_name`, `scenic_address`, `scenic_phone`, `business_hour`, `province`, `city`, `district`, `longitude`, `latitude`, `status`, `created_at`, `updated_at`) VALUES ('FJ_SM_001', '泰宁大金湖甘露寺', '福建省三明市泰宁县杉城镇', '0598-7831234', '08:00-12:00,13:30-16:30', '福建省', '三明市', '泰宁县', 117.1234567, 26.8765432, 1, '2025-11-26 00:06:06', '2025-11-26 00:06:06');
INSERT INTO `t_scenic` (`scenic_id`, `scenic_name`, `scenic_address`, `scenic_phone`, `business_hour`, `province`, `city`, `district`, `longitude`, `latitude`, `status`, `created_at`, `updated_at`) VALUES ('FJ_SM_002', '永安桃源洞', '福建省三明市永安市燕西街道', '0598-3631234', '08:00-11:30,13:30-17:00', '福建省', '三明市', '永安市', 117.3456789, 25.9876543, 1, '2025-11-26 00:06:06', '2025-11-26 00:06:06');
INSERT INTO `t_scenic` (`scenic_id`, `scenic_name`, `scenic_address`, `scenic_phone`, `business_hour`, `province`, `city`, `district`, `longitude`, `latitude`, `status`, `created_at`, `updated_at`) VALUES ('FJ_XM_001', '鼓浪屿日光岩', '福建省厦门市思明区鼓浪屿晃岩路', '0592-2066666', '07:00-12:00,13:30-18:00', '福建省', '厦门市', '思明区', 118.0791234, 24.4428765, 1, '2025-11-26 00:06:06', '2025-11-26 00:06:06');
INSERT INTO `t_scenic` (`scenic_id`, `scenic_name`, `scenic_address`, `scenic_phone`, `business_hour`, `province`, `city`, `district`, `longitude`, `latitude`, `status`, `created_at`, `updated_at`) VALUES ('FJ_XM_002', '厦门园林植物园', '福建省厦门市思明区虎园路25号', '0592-2022062', '06:30-12:00,13:00-18:30', '福建省', '厦门市', '思明区', 118.0987654, 24.4567890, 1, '2025-11-26 00:06:06', '2025-11-26 00:06:06');
INSERT INTO `t_scenic` (`scenic_id`, `scenic_name`, `scenic_address`, `scenic_phone`, `business_hour`, `province`, `city`, `district`, `longitude`, `latitude`, `status`, `created_at`, `updated_at`) VALUES ('FJ_XM_003', '集美学村龙舟池', '福建省厦门市集美区银江路', '0592-6101611', '08:30-11:30,14:30-17:30', '福建省', '厦门市', '集美区', 118.0987123, 24.5678901, 1, '2025-11-26 00:06:06', '2025-11-26 00:06:06');
INSERT INTO `t_scenic` (`scenic_id`, `scenic_name`, `scenic_address`, `scenic_phone`, `business_hour`, `province`, `city`, `district`, `longitude`, `latitude`, `status`, `created_at`, `updated_at`) VALUES ('FJ_ZZ_001', '南靖云水谣土楼群', '福建省漳州市南靖县梅林镇', '0596-7776299', '08:00-12:00,13:30-17:30', '福建省', '漳州市', '南靖县', 117.2345678, 24.5678901, 1, '2025-11-26 00:06:06', '2025-11-26 00:06:06');
INSERT INTO `t_scenic` (`scenic_id`, `scenic_name`, `scenic_address`, `scenic_phone`, `business_hour`, `province`, `city`, `district`, `longitude`, `latitude`, `status`, `created_at`, `updated_at`) VALUES ('FJ_ZZ_002', '东山岛风动石景区', '福建省漳州市东山县铜陵镇', '0596-5831111', '08:00-12:00,14:00-18:00', '福建省', '漳州市', '东山县', 117.4567890, 23.7890123, 1, '2025-11-26 00:06:06', '2025-11-26 00:06:06');
COMMIT;

SET FOREIGN_KEY_CHECKS = 1;
