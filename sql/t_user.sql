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

 Date: 26/11/2025 01:33:20
*/

SET NAMES utf8mb4;
SET FOREIGN_KEY_CHECKS = 0;

-- ----------------------------
-- Table structure for t_user
-- ----------------------------
DROP TABLE IF EXISTS `t_user`;
CREATE TABLE `t_user` (
  `user_id` varchar(50) COLLATE utf8mb4_unicode_ci NOT NULL COMMENT '用户唯一ID，主键',
  `user_name` varchar(50) COLLATE utf8mb4_unicode_ci NOT NULL COMMENT '用户姓名',
  `phone` char(11) COLLATE utf8mb4_unicode_ci NOT NULL COMMENT '手机号（11位数字字符串）',
  `id_card` char(18) COLLATE utf8mb4_unicode_ci NOT NULL COMMENT '身份证号码（18位，含X）',
  PRIMARY KEY (`user_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci COMMENT='用户信息表';

-- ----------------------------
-- Records of t_user
-- ----------------------------
BEGIN;
INSERT INTO `t_user` (`user_id`, `user_name`, `phone`, `id_card`) VALUES ('550e8400e29b41d4a716446655440000', '张伟', '13812345678', '110101198502143216');
INSERT INTO `t_user` (`user_id`, `user_name`, `phone`, `id_card`) VALUES ('550e8400e29b41d4a716446655440001', '王芳', '13987654321', '310115199011232128');
INSERT INTO `t_user` (`user_id`, `user_name`, `phone`, `id_card`) VALUES ('550e8400e29b41d4a716446655440002', '李强', '15011112222', '44030519780708345X');
INSERT INTO `t_user` (`user_id`, `user_name`, `phone`, `id_card`) VALUES ('550e8400e29b41d4a716446655440003', '刘敏', '18666668888', '210102199205171234');
INSERT INTO `t_user` (`user_id`, `user_name`, `phone`, `id_card`) VALUES ('550e8400e29b41d4a716446655440004', '陈静', '13200001111', '510104198312305672');
INSERT INTO `t_user` (`user_id`, `user_name`, `phone`, `id_card`) VALUES ('550e8400e29b41d4a716446655440005', '杨洋', '15812344321', '420106198808141519');
INSERT INTO `t_user` (`user_id`, `user_name`, `phone`, `id_card`) VALUES ('550e8400e29b41d4a716446655440006', '赵磊', '13777779999', '320102197504223450');
INSERT INTO `t_user` (`user_id`, `user_name`, `phone`, `id_card`) VALUES ('550e8400e29b41d4a716446655440007', '黄娟', '18822223333', '130105199503118886');
INSERT INTO `t_user` (`user_id`, `user_name`, `phone`, `id_card`) VALUES ('550e8400e29b41d4a716446655440008', '周鹏', '13188886666', '610113198010024561');
INSERT INTO `t_user` (`user_id`, `user_name`, `phone`, `id_card`) VALUES ('550e8400e29b41d4a716446655440009', '吴婷', '15299990000', '500103198706197773');
COMMIT;

SET FOREIGN_KEY_CHECKS = 1;
