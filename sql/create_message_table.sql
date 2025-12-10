-- 消息通知表
CREATE TABLE IF NOT EXISTS `tbkf_message_info` (
  `message_id` varchar(30) NOT NULL COMMENT '消息ID',
  `user_id` varchar(30) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL COMMENT '接收用户ID',
  `message_type` varchar(20) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL COMMENT '消息类型：work_order_timeout-工单超时, work_order_assigned-工单分配, work_order_feedback-工单反馈, system-系统通知',
  `title` varchar(200) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL COMMENT '消息标题',
  `content` text CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci COMMENT '消息内容',
  `related_id` varchar(30) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT NULL COMMENT '关联ID（如工单ID）',
  `is_read` tinyint DEFAULT 0 COMMENT '是否已读：0-未读, 1-已读',
  `read_time` datetime DEFAULT NULL COMMENT '阅读时间',
  `priority` varchar(10) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT 'normal' COMMENT '优先级：low-低, normal-普通, high-高, urgent-紧急',
  `create_time` datetime DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
  PRIMARY KEY (`message_id`) USING BTREE,
  KEY `idx_user_id` (`user_id`),
  KEY `idx_message_type` (`message_type`),
  KEY `idx_is_read` (`is_read`),
  KEY `idx_create_time` (`create_time`),
  KEY `idx_related_id` (`related_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci ROW_FORMAT=DYNAMIC COMMENT='消息通知表';

