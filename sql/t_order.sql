-- 订单表
CREATE TABLE IF NOT EXISTS `t_order` (
  `id` VARCHAR(64) NOT NULL COMMENT '订单ID',
  `order_no` VARCHAR(64) NOT NULL COMMENT '订单号',
  `user_id` VARCHAR(64) NOT NULL COMMENT '用户ID',
  `scenic_id` VARCHAR(64) NOT NULL COMMENT '景点ID',
  `scenic_name` VARCHAR(128) NOT NULL COMMENT '景点名称',
  `order_title` VARCHAR(256) NOT NULL COMMENT '订单标题（票名）',
  `order_price` DECIMAL(10, 2) NOT NULL COMMENT '订单价格',
  `ticket_quantity` INT NOT NULL DEFAULT 1 COMMENT '票数量',
  `reschedule_limit` INT NOT NULL DEFAULT 1 COMMENT '改签次数上限',
  `reschedule_used` INT NOT NULL DEFAULT 0 COMMENT '已使用改签次数',
  `order_time` DATETIME NOT NULL COMMENT '下单时间',
  `order_status` TINYINT NOT NULL DEFAULT 1 COMMENT '订单状态：1-待支付，2-已支付，3-已取消，4-已完成，5-已退款',
  `create_time` DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
  `update_time` DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP COMMENT '更新时间',
  PRIMARY KEY (`id`),
  UNIQUE KEY `uk_order_no` (`order_no`),
  KEY `idx_user_id` (`user_id`),
  KEY `idx_scenic_id` (`scenic_id`),
  KEY `idx_order_time` (`order_time`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COMMENT='订单表';
