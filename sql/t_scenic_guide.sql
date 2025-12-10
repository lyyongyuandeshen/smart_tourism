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
INSERT INTO `t_scenic_guide` (`id`, `scenic_id`, `guide_title`, `historical_background`, `cultural_value`, `architectural_features`, `historical_stories`, `ecological_science`, `open_status`, `last_bus_time`, `evacuation_route_url`) VALUES
('SG001', '350203001', '菽庄花园',
'菽庄花园建于1913年,是台湾富商林尔嘉为怀念台湾板桥故居而建造的私家园林。园名取自《诗经》"菽水承欢"之意,体现了主人对父母的孝心。1955年献给国家,成为鼓浪屿著名的园林景观。', 
'菽庄花园是闽南园林艺术的杰出代表,融合了江南园林的精致与闽南建筑的特色,体现了中国传统园林"虽由人作,宛自天开"的造园理念。园内的"藏海"、"补山"手法堪称园林艺术的经典之作。', 
'园林采用"藏海"手法,入园时看不到大海,转过月洞门才豁然开朗。园内建有四十四桥、渡月亭、千波亭等景观,巧妙利用地形高差,形成层次丰富的空间布局。钢琴博物馆收藏了世界各地的古钢琴,展现了鼓浪屿"钢琴之岛"的文化底蕴。', 
'林尔嘉先生在台湾板桥拥有一座名为"菽庄"的花园,1895年甲午战争后台湾被割让,林家举家迁往鼓浪屿。为寄托对故土的思念,林尔嘉在此建造了菽庄花园,园内的四十四桥象征着他44岁那年离开台湾的心境。', 
'菽庄花园依山傍海,园内植被丰富,有榕树、龙眼、荔枝等亚热带植物。海边礁石上生长着各种海洋生物,退潮时可观察到螃蟹、海螺等潮间带生物,是了解海洋生态的绝佳场所。', 
1, '17:30', 'http://example.com/evacuation/shuzhuang'),

('SG002', '350203002', '日光岩',
'日光岩又称晃岩,海拔92.7米,是鼓浪屿的最高峰。明代万历年间,泉州知府丁一中在此题刻"鼓浪洞天",成为鼓浪屿的代名词。1641年,郑成功曾在此屯兵操练,留下了"郑成功水操台"等历史遗迹。', 
'日光岩是鼓浪屿的标志性景观,承载着厦门人民抗击外来侵略的历史记忆。郑成功在此操练水师,为收复台湾做准备,体现了中华民族不屈不挠的精神。岩顶可俯瞰整个鼓浪屿和厦门市区,是观赏"鹭江第一"的最佳位置。', 
'日光岩由两块巨石相倚而立,形成天然的石洞。岩顶建有圆形观景平台,可360度观赏周边景色。岩壁上有历代名人题刻,其中以明代丁一中的"鼓浪洞天"最为著名。山腰建有郑成功纪念馆,展示了民族英雄的生平事迹。', 
'相传郑成功来到晃岩,见这里的景色胜过日本的日光山,便把"晃"字拆开,称之为"日光岩"。1641年,郑成功驻军鼓浪屿,在日光岩上建立水操台,操练水师,为收复台湾积蓄力量。岩上至今还保留着"闽海雄风"等摩崖石刻。', 
'日光岩是典型的花岗岩地貌,经过亿万年的风化侵蚀形成了独特的巨石景观。岩石表面的球状风化现象清晰可见,是研究地质演变的天然教科书。山上植被以榕树、相思树为主,形成了独特的海岛植物群落。', 
1, '18:00', 'http://example.com/evacuation/riguangyan'),

('SG003', '350203003', '海底世界',
'鼓浪屿海底世界建于1998年,是厦门市重点旅游项目。场馆利用鼓浪屿独特的海岛地理位置,引进先进的海洋生物展示技术,打造了一个集观赏、科普、娱乐为一体的现代化海洋馆。', 
'海底世界是厦门市重要的海洋科普教育基地,通过展示丰富多样的海洋生物,让游客了解海洋生态系统的奥秘,增强海洋环保意识。馆内的海洋生物标本和互动展项,为青少年提供了生动的海洋科学教育课堂。', 
'海底世界采用现代化的展馆设计,拥有80米长的海底隧道,游客可以在隧道中近距离观赏鲨鱼、海龟、魔鬼鱼等大型海洋生物。馆内还设有触摸池、海豹表演池等互动区域,以及珊瑚礁生态展示区,全方位展现海洋世界的魅力。', 
'海底世界所在的位置原是鼓浪屿的一处天然海湾,20世纪90年代,为了丰富鼓浪屿的旅游业态,厦门市政府决定在此建设海洋馆。建设过程中充分考虑了海岛生态保护,采用了环保的建筑材料和节能技术,成为海岛可持续发展的典范。', 
'海底世界展示了300多种、10000多尾海洋生物,包括来自世界各地的珍稀鱼类。馆内模拟了不同的海洋生态环境,如珊瑚礁区、深海区、极地区等,让游客了解不同海域的生物多样性。通过科学的饲养管理,这里成为海洋生物保护和繁育的重要基地。', 
1, '17:00', 'http://example.com/evacuation/haidishijie');
COMMIT;

SET FOREIGN_KEY_CHECKS = 1;
