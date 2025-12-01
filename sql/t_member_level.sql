-- 会员等级表
CREATE TABLE IF NOT EXISTS `t_member_level` (
  `id` INT AUTO_INCREMENT COMMENT '会员等级ID',
  `level` INT NOT NULL COMMENT '会员等级（1-10）',
  `level_name` VARCHAR(64) NOT NULL COMMENT '等级名称',
  `points_min` INT NOT NULL DEFAULT 0 COMMENT '所需积分下限',
  `points_max` INT NOT NULL COMMENT '所需积分上限',
  `discount_rate` DECIMAL(5, 2) NOT NULL DEFAULT 100.00 COMMENT '专属折扣（百分比，如95.00表示95折）',
  `priority_booking` TINYINT(1) NOT NULL DEFAULT 0 COMMENT '优先预约权限（0-无，1 -有）',
  `is_deleted` TINYINT(1) NOT NULL DEFAULT 0 COMMENT '是否删除（0-未删除，1-已删除）',
  `create_time` DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
  `update_time` DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP COMMENT '更新时间',
  PRIMARY KEY (`id`),
  UNIQUE KEY `uk_level` (`level`, `is_deleted`),
  KEY `idx_points` (`points_min`, `points_max`),
  KEY `idx_is_deleted` (`is_deleted`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COMMENT='会员等级表';

-- 插入初始数据
INSERT INTO `t_member_level` (`id`, `level`, `level_name`, `points_min`, `points_max`, `discount_rate`, `priority_booking`) VALUES
('1', 1, '等级1', 0, 0, 95.00, 0),
('2', 2, '等级2', 0, 200, 90.00, 0),
('3', 3, '等级3', 200, 500, 85.00, 0),
('4', 4, '等级4', 500, 1000, 80.00, 0),
('5', 5, '等级5', 1000, 2000, 75.00, 1),
('6', 6, '等级6', 2000, 5000, 70.00, 1),
('7', 7, '等级7', 5000, 10000, 65.00, 1),
('8', 8, '等级8', 10000, 15000, 60.00, 1);
