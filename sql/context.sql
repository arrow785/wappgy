/*
 Navicat Premium Data Transfer

 Source Server         : local
 Source Server Type    : MySQL
 Source Server Version : 80040
 Source Host           : localhost:3306
 Source Schema         : blog

 Target Server Type    : MySQL
 Target Server Version : 80040
 File Encoding         : 65001

 Date: 26/01/2025 12:19:31
*/

SET NAMES utf8mb4;
SET FOREIGN_KEY_CHECKS = 0;

-- ----------------------------
-- Table structure for context
-- ----------------------------
DROP TABLE IF EXISTS `context`;
CREATE TABLE `context`  (
  `id` int NOT NULL AUTO_INCREMENT COMMENT 'id 唯一标识',
  `title` varchar(255) CHARACTER SET utf8mb3 COLLATE utf8mb3_general_ci NOT NULL COMMENT '标题',
  `username` varchar(50) CHARACTER SET utf8mb3 COLLATE utf8mb3_general_ci NOT NULL COMMENT '作者',
  `contents` longtext CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NOT NULL COMMENT '内容',
  `date` varchar(100) CHARACTER SET utf8mb3 COLLATE utf8mb3_general_ci NOT NULL COMMENT '发布时间',
  `modify_date` varchar(100) CHARACTER SET utf8mb3 COLLATE utf8mb3_general_ci NULL DEFAULT NULL COMMENT '修改时间',
  PRIMARY KEY (`id`) USING BTREE
) ENGINE = InnoDB AUTO_INCREMENT = 98 CHARACTER SET = utf8mb3 COLLATE = utf8mb3_general_ci ROW_FORMAT = DYNAMIC;

-- ----------------------------
-- Records of context
-- ----------------------------
INSERT INTO `context` VALUES (37, '《还珠格格》紫薇与尔康在幽幽谷', '琼瑶', '紫薇和尔康来到幽幽谷，周围绿树成荫，溪水潺潺。尔康深情地看着紫薇，眼中满是爱意，他紧紧握着紫薇的手说：“紫薇，你知道吗？自从见到你的第一眼，我的心就被你填满了。”紫薇羞涩地低下头，尔康继续说道：“山无棱，天地合，乃敢与君绝。我对你的爱，就像这幽幽谷的溪水，源源不断，永不停息。”紫薇感动地抬起头，回应道：“尔康，我也是，你就是我的全部，我的生命中不能没有你。”此时，微风拂过，紫薇的发丝轻轻飘动，尔康轻轻地将紫薇拥入怀中，两人在这美丽的幽幽谷中深情相拥，仿佛时间都停止了，整个世界只剩下他们彼此的心跳和呼吸，他们的爱情如同这山谷中的美景一般，美好而又永恒。', '2020-06-21 20:29', NULL);
INSERT INTO `context` VALUES (38, '《一帘幽梦》费云帆与紫菱在法国', '琼瑶', '费云帆带着紫菱来到了法国的普罗旺斯，他们漫步在薰衣草花田中，紫色的薰衣草在微风中轻轻摇曳，散发出迷人的芬芳。费云帆摘下一朵薰衣草，插在紫菱的发间，温柔地说：“紫菱，你就像这薰衣草一样美丽动人。”紫菱开心地笑着，眼中闪烁着幸福的光芒。他们走进了一座古老的古堡，古堡里的一切都显得那么神秘而又浪漫。费云帆为紫菱准备了一场盛大的晚宴，在晚宴上，他深情地向紫菱求婚：“紫菱，我想让你成为我的妻子，我会用我的一生来爱你，宠你，让你永远幸福。”紫菱感动得热泪盈眶，她看着费云帆，坚定地说：“云帆，我愿意。”随后，两人在众人的祝福下，紧紧相拥，在这浪漫的法国古堡中，开启了他们幸福的爱情之旅。', '2019-03-21 20:30', NULL);
INSERT INTO `context` VALUES (39, '《情深深雨濛濛》依萍和书桓的雨中争吵与相拥', '琼瑶', '在一个下着倾盆大雨的夜晚，依萍和书桓在街头发生了激烈的争吵。依萍满脸泪水，她对着书桓大喊：“我要去找我的刺！”书桓心疼地看着依萍，他知道依萍的坚强背后藏着一颗脆弱的心。他紧紧地抱住依萍，说：“依萍，别这样，我错了，我不该让你伤心。”依萍在书桓的怀里挣扎着，嘴里还念叨着：“你为什么不相信我，为什么要误会我？”书桓轻轻地抚摸着依萍的头发，说：“依萍，我是太在乎你了，所以才会失去理智，你原谅我好不好？”依萍渐渐停止了挣扎，她抬起头，看着书桓，眼中的泪水和雨水交融在一起。最终，两人在雨中紧紧相拥，雨水打湿了他们的衣服，但他们的爱情却在这一刻变得更加坚定。', '2024-11-21 20:31', NULL);
INSERT INTO `context` VALUES (40, '《新月格格》新月和努达海的战场相拥', '琼瑶', '新月跟随努达海来到了战场上，战场上硝烟弥漫，喊杀声震天。新月不顾危险，四处寻找着努达海。突然，一支冷箭向新月射来，努达海见状，发疯似的冲过去，用自己的身体挡住了冷箭，他紧紧地抱住新月，大声地说：“新月，你没事吧，吓死我了。”新月看着受伤的努达海，泪水止不住地流下来，她说：“努达海，你为什么要这么傻，你要是有个三长两短，我该怎么办？”努达海微笑着说：“新月，只要你没事就好，我不能让你受到任何伤害。”周围的士兵们都被他们的爱情所感动，纷纷为他们加油助威。在这战火纷飞的战场上，新月和努达海紧紧相拥，他们的爱情如同这战场上的烽火一般，炽热而又浓烈。', '2024-11-20 22:32', NULL);
INSERT INTO `context` VALUES (41, '《水云间》梅若鸿和杜芊芊的雨中和解', '琼瑶', '梅若鸿和杜芊芊因为一些误会而发生了争吵，梅若鸿一气之下跑了出去，杜芊芊在后面追着，一边追一边哭着喊：“若鸿，你回来，你听我解释。”可是梅若鸿却没有停下脚步。突然，天空中下起了倾盆大雨，杜芊芊在雨中摔倒了，但她仍然挣扎着爬起来继续追赶。终于，她追上了梅若鸿，她紧紧地抱住梅若鸿，说：“若鸿，我错了，你别生气了好不好？”梅若鸿看着浑身湿透、满脸泪水的杜芊芊，心中的怒火一下子就消失了。他心疼地说：“芊芊，是我不好，我不该不听你解释就跑出来。”两人在雨中紧紧相拥，雨水顺着他们的脸颊流下，他们的爱情在这场雨中得到了洗礼和升华，变得更加坚定和美好。', '2024-11-08 01:36', NULL);
INSERT INTO `context` VALUES (47, 'think about ', 'gs1', '沉舟侧畔千帆过，病树前头万木春。\r\n                ', '2025-01-13 09:30', '2025-01-13 23:11');
INSERT INTO `context` VALUES (49, '西游记', 'LZC123456', '猴三棒！', '2025-01-13 11:20', NULL);
INSERT INTO `context` VALUES (50, '易', '英雄联盟', '怀疑是最强大的敌人。\r\n                \r\n                \r\n                \r\n                ', '2025-01-13 13:38', '2025-01-13 23:42');
INSERT INTO `context` VALUES (55, 'You Are Not Alone', 'MJ', 'Another day has gone\r\nI\'m still all alone\r\nHow could this be?\r\nYou\'re not here with me\r\nYou never said goodbye\r\nSomeone tell me why\r\nDid you have to go?\r\nAnd leave my world so cold\r\nEveryday I sit and ask myself\r\nHow did love slip away?\r\nSomething whispers in my ear and says\r\nThat you are not alone\r\nI am here with you\r\nThough you\'re far away\r\nI am here to stay\r\nBut you are not alone\r\nI am here with you\r\nThough we\'re far apart\r\nYou\'re always in my heart\r\nBut you are not alone\r\n\'Lone, \'lone\r\nWhy, \'lone\r\nJust the other night\r\nI thought I heard you cry\r\nAsking me to come\r\nAnd hold you in my arms\r\nI can hear your prayers\r\nYour burdens I will bear\r\nBut first I need your hand\r\nThen forever can begin\r\nEveryday I sit and ask myself\r\nHow did love slip away?\r\nSomething whispers in my ear and says\r\nThat you are not alone\r\nI am here with you\r\nThough you\'re far away\r\nI am here to stay\r\nBut you are not alone\r\nI am here with you\r\nThough we\'re far apart\r\nYou\'re always in my heart\r\nBut you are not alone\r\nWhisper three words and I\'ll come running\r\nAnd girl you know that I\'ll be there\r\nI\'ll be there\r\nThat you are not alone\r\nI am here with you\r\nThough you\'re far away\r\nI am here to stay\r\nBut you are not alone\r\nI am here with you\r\nThough we\'re far apart\r\nYou\'re always in my heart\r\nFor you are not alone (You are not alone)\r\nFor I am here with you (I am here with you)\r\nThough you\'re far away (Though you\'re far away)\r\nI am here to stay (You and me)\r\nFor you are not alone (You\'re always in my heart)\r\nFor I am here with you\r\nThough we\'re far apart\r\nYou\'re always in my heart\r\nFor you are not alone\r\nNot alone, oh\r\nYou are not alone\r\nYou are not alone\r\nSay it again\r\nYou are not alone\r\nYou are not alone\r\nNot alone, not alone\r\nIf you just reach out for me girl\r\nIn the morning, in the evening\r\nNot alone, not alone\r\nYou and me\r\nNot alone\r\nOh, together, together\r\nGotta stop being alone\r\nGotta stop being alone', '2025-01-18 13:14', NULL);
INSERT INTO `context` VALUES (56, 'LOVE', 'LZC123456', '我坚决去拉向你的手，你却转身对我说And one！！！（basketball）', '2025-01-19 13:57', NULL);
INSERT INTO `context` VALUES (63, '拥有恋爱脑的下场', '爱吃鱼的猫', '拥有恋爱脑会让你自我感觉很好，对方很爱你就像你爱他一样，感觉不到对方的冷漠与敷衍……', '2025-01-20 21:45', NULL);
INSERT INTO `context` VALUES (88, 'HAPPY NEW YEAR', 'LZC123456', '新年快乐！！！！', '2025-01-21 22:02', NULL);
INSERT INTO `context` VALUES (94, 'Cambrian-1', '喜欢劈瓜的刘华强', '寒武纪', '2025-01-23 14:56', NULL);
INSERT INTO `context` VALUES (95, '@莫', '123', '春日宴', '2025-01-23 21:01', NULL);
INSERT INTO `context` VALUES (96, '关于一些感情问题', '睡醒没YYY', '两个人既然选择在一起就是不要总是去患得患失的去猜测对方是不是不爱你啊？各种各样的胡思乱想，对方是为什么喜欢我？对方从什么时候不爱我？其实我告诉你们：你在这个世界上你除了你自己猜透你自己，你永远猜不透任何一个人。\n还有一个就是不要一直怀疑对方是不是不爱你？是不是不喜欢你了？其实我跟你们讲，大家用力去爱就可以了，不要在爱的时候去找不爱的证据，要不然两个人在一起最后就会两败俱伤……', '2025-01-22 23:34', NULL);
INSERT INTO `context` VALUES (97, 'CARBRIAN-1', '喜欢劈瓜的刘华强', '1*=:', '2025-01-25 00:32:59', NULL);

SET FOREIGN_KEY_CHECKS = 1;
