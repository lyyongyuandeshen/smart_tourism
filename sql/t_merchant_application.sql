-- 商户申请表
CREATE TABLE IF NOT EXISTS `t_merchant_application` (
  `id` BIGINT NOT NULL AUTO_INCREMENT COMMENT '主键ID',
  `application_no` VARCHAR(32) NOT NULL COMMENT '申请编号',
  `shop_name` VARCHAR(255) NOT NULL COMMENT '店名',
  `applicant_name` varchar(50) NOT NULL COMMENT '申请人名称',
  `business_scope` VARCHAR(255) NOT NULL COMMENT '经营范围',
  `service_content` VARCHAR(255) DEFAULT NULL COMMENT '服务内容',
  `status` TINYINT NOT NULL DEFAULT '0' COMMENT '状态: 0-未完成, 1-审核中, 2-已完成, 3-已撤回',
  `created_time` DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
  `updated_time` DATETIME DEFAULT NULL COMMENT '最后更新时间',
  `deleted` TINYINT NOT NULL DEFAULT '0' COMMENT '逻辑删除: 0-未删除, 1-已删除',
  PRIMARY KEY (`id`),
  UNIQUE KEY `uk_application_no` (`application_no`),
  INDEX `idx_shop_name` (`shop_name`),
  INDEX `idx_applicant_name` (`applicant_name`),
  INDEX `idx_status` (`status`),
  INDEX `idx_created_time` (`created_time`),
  INDEX `idx_deleted` (`deleted`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COMMENT='商户申请表';

-- 插入测试数据
INSERT INTO `t_merchant_application` (
    `application_no`, `shop_name`, `applicant_name`, `business_scope`, 
    `service_content`, `status`, `created_time`, `updated_time`, `deleted`
) VALUES
-- 状态 0: 未完成（updated_time 为 NULL）
('SN20251129XJ0001', '西湖醋鱼馆', '张伟', '餐饮业', '杭帮菜', 0, '2025-11-29 09:15:22', NULL, 0),
('SN20251128XJ0002', '灵隐素斋', '王芳', '餐饮业', '素食', 0, '2025-11-28 14:30:45', NULL, 0),
('SN20251127XJ0003', '龙井茶社', '李强', '零售业', '茶叶', 0, '2025-11-27 16:20:11', NULL, 0),
('SN20251126XJ0004', '苏堤文创', '刘敏', '零售业', '文创产品', 0, '2025-11-26 10:45:33', NULL, 0),
('SN20251125XJ0005', '断桥汉服馆', '陈静', '服务业', '汉服租赁', 0, '2025-11-25 11:12:09', NULL, 0),

-- 状态 1: 审核中（有 updated_time，模拟提交后修改或审核触发更新）
('SN20251124XJ0006', '楼外楼分店', '杨洋', '餐饮业', '杭帮菜', 1, '2025-11-24 08:55:17', '2025-11-24 09:00:00', 0),
('SN20251123XJ0007', '知味观糕点', '赵磊', '零售业', '糕点', 1, '2025-11-23 13:40:28', '2025-11-23 13:45:10', 0),
('SN20251122XJ0008', '雷峰塔纪念品', '黄婷', '零售业', '旅游纪念品', 1, '2025-11-22 15:33:52', '2025-11-22 15:38:20', 0),
('SN20251121XJ0009', '曲院风荷茶艺', '周杰', '服务业', '茶艺体验', 1, '2025-11-21 11:27:41', '2025-11-21 11:30:05', 0),
('SN20251120XJ0010', '花港观鱼摄影', '吴霞', '服务业', '旅拍服务', 1, '2025-11-20 16:18:37', '2025-11-20 16:22:14', 0),

-- 状态 2: 已完成（updated_time 为审核通过时间）
('SN20251119XJ0011', '张小泉剪刀铺', '孙浩', '零售业', '刀具', 2, '2025-11-19 09:10:05', '2025-11-19 14:25:30', 0),
('SN20251118XJ0012', '王星记扇庄', '郑洁', '零售业', '工艺品', 2, '2025-11-18 10:05:12', '2025-11-18 13:40:22', 0),
('SN20251117XJ0013', '外婆家(湖滨店)', '王勇', '餐饮业', '家常菜', 2, '2025-11-17 11:33:48', '2025-11-17 15:15:00', 0),
('SN20251116XJ0014', '南宋官窑馆', '高敏', '零售业', '陶瓷', 2, '2025-11-16 14:22:37', '2025-11-16 16:50:18', 0),
('SN20251115XJ0015', '西湖游船服务', '徐伟', '服务业', '游船租赁', 2, '2025-11-15 15:44:09', '2025-11-15 17:30:45', 0),

-- 状态 3: 已撤回（updated_time 为撤回时间）
('SN20251114XJ0016', '北高峰素面', '胡军', '餐饮业', '面食', 3, '2025-11-14 08:30:15', '2025-11-14 10:20:33', 0),
('SN20251113XJ0017', '宝石山登山杖', '郭芳', '零售业', '户外装备', 3, '2025-11-13 09:45:22', '2025-11-13 11:10:07', 0),
('SN20251112XJ0018', '杨公堤茶室', '何强', '服务业', '茶歇', 3, '2025-11-12 13:12:44', '2025-11-12 14:55:29', 0),
('SN20251111XJ0019', '白堤咖啡', '马丽', '餐饮业', '咖啡饮品', 3, '2025-11-11 16:33:51', '2025-11-11 17:40:18', 0),
('SN20251110XJ0020', '孤山文房四宝', '罗伟', '零售业', '文具', 3, '2025-11-10 10:08:37', '2025-11-10 12:15:42', 0);