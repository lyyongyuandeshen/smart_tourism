-- 文化遗产表
CREATE TABLE IF NOT EXISTS `t_cultural_heritage` (
  `file_id` VARCHAR(50) NOT NULL PRIMARY KEY COMMENT '文件编号（如 CH_FJ_001）',
  `file_name` VARCHAR(200) NOT NULL COMMENT '文件名称',
  `file_type` VARCHAR(10) NOT NULL COMMENT '文件类型：写死为"文件"、"图片"、"视频"之一',
  `tag` VARCHAR(50) NOT NULL COMMENT '所属标签（如"非遗"、"古建"、"民俗"、"文献"）',
  `url` VARCHAR(500) NOT NULL COMMENT '文件存储链接URL（OSS/MinIO/本地路径）',
  `created_at` DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT '上传时间',
  `updated_at` DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP COMMENT '更新时间',
  INDEX idx_file_type (`file_type`),
  INDEX idx_tag (`tag`),
  INDEX idx_created_at (`created_at`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COMMENT='文化遗产表';

-- 插入测试数据
INSERT INTO `t_cultural_heritage` (
  `file_id`, `file_name`, `file_type`, `tag`, `url`
) VALUES
-- ===== 文件（2条）=====
('CH_WJ_001', '福建土楼营造技艺申报文本.pdf', '文件', '非遗', 'https://oss.example.com/cultural/heritage/FJ_Tulou_Technique_2023.pdf'),
('CH_WJ_002', '泉州：宋元中国的世界海洋商贸中心申遗总文本.pdf', '文件', '文献', 'https://oss.example.com/cultural/heritage/Quanzhou_WHS_Dossier.pdf'),

-- ===== 图片（2条）=====
('CH_TP_001', '永定承启楼全景（2024航拍）.jpg', '图片', '古建', 'https://oss.example.com/cultural/heritage/Chengqi_Tulou_Aerial_2024.jpg'),
('CH_TP_002', '湄洲妈祖祭典仪式图集.jpg', '图片', '民俗', 'https://oss.example.com/cultural/heritage/Mazu_Ceremony_Album.jpg'),

-- ===== 视频（2条）=====
('CH_SP_001', '南音《百鸟归巢》表演实录（4K）.mp4', '视频', '非遗', 'https://oss.example.com/cultural/heritage/Nanyin_BaiNiao_Return.mp4'),
('CH_SP_002', '武夷山茶百戏制作技艺纪录片.mp4', '视频', '非遗', 'https://oss.example.com/cultural/heritage/Wuyi_Tea_BaiXi_Docu.mp4');
