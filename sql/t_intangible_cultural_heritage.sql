-- 非遗技艺教学视频管理表
CREATE TABLE IF NOT EXISTS `t_intangible_cultural_heritage` (
  `id` INT NOT NULL AUTO_INCREMENT PRIMARY KEY COMMENT '主键ID',
  `heritage_number` VARCHAR(50) NOT NULL UNIQUE COMMENT '非遗编号（格式：SNYYYYMMDDXXXXX）',
  `heritage_name` VARCHAR(200) NOT NULL COMMENT '非遗名称',
  `interactive_question_bank` VARCHAR(100) NOT NULL COMMENT '互动题库',
  `video_url` VARCHAR(500) NOT NULL COMMENT '视频URL地址链接（TOS存储路径）',
  `is_published` TINYINT(1) NOT NULL DEFAULT 0 COMMENT '是否发布（0-未发布，1-已发布）',
  `created_at` DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
  `updated_at` DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP COMMENT '更新时间',
  INDEX idx_heritage_number (`heritage_number`),
  INDEX idx_heritage_name (`heritage_name`),
  INDEX idx_interactive_question_bank (`interactive_question_bank`),
  INDEX idx_is_published (`is_published`),
  INDEX idx_created_at (`created_at`),
  INDEX idx_updated_at (`updated_at`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COMMENT='非遗技艺教学视频管理表';

-- 插入测试数据
INSERT INTO `t_intangible_cultural_heritage` (
  `heritage_number`, `heritage_name`, `interactive_question_bank`, `video_url`, `is_published`
) VALUES
-- 已发布的非遗技艺
('SN2024121200001', '福建土楼营造技艺教学视频', '福建土楼非遗题库', 'tos://mt-znwl-tos/intangible_cultural_heritage/videos/2024/12/12/7c5e8f9a3b1d4e2f6a8c9b0e7d3f1a5.mp4', 1),
('SN2024121200002', '南音表演技艺教学视频', '南音非遗题库', 'tos://mt-znwl-tos/intangible_cultural_heritage/videos/2024/12/12/8d6f9a3b1c4e2f7a9c0b1e8d4f2a6.mp4', 1),
('SN2024121200003', '武夷岩茶制作技艺教学视频', '武夷岩茶非遗题库', 'tos://mt-znwl-tos/intangible_cultural_heritage/videos/2024/12/12/9e7a0b2c3d5f1g8h0i1j9k3l5m7.mp4', 1),

-- 未发布的非遗技艺
('SN2024121200004', '闽剧表演技艺教学视频', '闽剧非遗题库', 'tos://mt-znwl-tos/intangible_cultural_heritage/videos/2024/12/12/a0b1c2d3e4f5g6h7i8j9k0l1m2.mp4', 0),
('SN2024121200005', '木偶戏表演技艺教学视频', '木偶戏非遗题库', 'tos://mt-znwl-tos/intangible_cultural_heritage/videos/2024/12/12/b1c2d3e4f5g6h7i8j9k0l1m2n3.mp4', 0),

-- 更多非遗技艺示例
('SN2024121200006', '福州脱胎漆器技艺教学视频', '脱胎漆器非遗题库', 'tos://mt-znwl-tos/intangible_cultural_heritage/videos/2024/12/12/c2d3e4f5g6h7i8j9k0l1m2n3o4.mp4', 1),
('SN2024121200007', '寿山石雕技艺教学视频', '寿山石雕非遗题库', 'tos://mt-znwl-tos/intangible_cultural_heritage/videos/2024/12/12/d3e4f5g6h7i8j9k0l1m2n3o4p5.mp4', 1),
('SN2024121200008', '闽南传统建筑营造技艺教学视频', '闽南建筑非遗题库', 'tos://mt-znwl-tos/intangible_cultural_heritage/videos/2024/12/12/e4f5g6h7i8j9k0l1m2n3o4p5q6.mp4', 0),
('SN2024121200009', '福建剪纸技艺教学视频', '福建剪纸非遗题库', 'tos://mt-znwl-tos/intangible_cultural_heritage/videos/2024/12/12/f5g6h7i8j9k0l1m2n3o4p5q6r7.mp4', 1),
('SN2024121200010', '闽菜烹饪技艺教学视频', '闽菜非遗题库', 'tos://mt-znwl-tos/intangible_cultural_heritage/videos/2024/12/12/g6h7i8j9k0l1m2n3o4p5q6r7s8.mp4', 1);