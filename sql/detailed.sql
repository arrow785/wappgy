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

 Date: 26/01/2025 12:19:43
*/

SET NAMES utf8mb4;
SET FOREIGN_KEY_CHECKS = 0;

-- ----------------------------
-- Table structure for detailed
-- ----------------------------
DROP TABLE IF EXISTS `detailed`;
CREATE TABLE `detailed`  (
  `id` int NOT NULL AUTO_INCREMENT,
  `username` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL,
  `comment_time` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL,
  `comment_context` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL,
  `context_id` int NOT NULL,
  `zhuti` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NOT NULL,
  PRIMARY KEY (`id`) USING BTREE
) ENGINE = InnoDB AUTO_INCREMENT = 50 CHARACTER SET = utf8mb4 COLLATE = utf8mb4_0900_ai_ci ROW_FORMAT = Dynamic;

-- ----------------------------
-- Records of detailed
-- ----------------------------
INSERT INTO `detailed` VALUES (3, 'lisi', '2025-01-13 19:10', '哈哈哈哈哈哈哈哈哈', 50, '易');
INSERT INTO `detailed` VALUES (4, 'gous', '2025-01-13 19:11', '可以哦', 50, '易');
INSERT INTO `detailed` VALUES (19, '英雄联盟', '2025-01-13 21:54', 'say something?', 50, '易');
INSERT INTO `detailed` VALUES (20, 'arros', '2025-01-13 22:08', '很好', 49, '西游记');
INSERT INTO `detailed` VALUES (21, 'arros', '2025-01-13 22:09', 'ss', 50, '易');
INSERT INTO `detailed` VALUES (22, 'arros', '2025-01-13 22:15', '', 49, '西游记');
INSERT INTO `detailed` VALUES (23, 'arros', '2025-01-13 22:20', '哈哈哈哈', 49, '西游记');
INSERT INTO `detailed` VALUES (24, 'arros', '2025-01-13 22:20', 'say something', 47, 'think about ');
INSERT INTO `detailed` VALUES (25, 'arros', '2025-01-13 22:21', '，她抬起头，看着书桓，眼中的泪水和雨水交融在一起。最终，两人在雨中紧紧相拥，雨水打湿了他们的衣服，但他们的爱情却在这一刻变得更加坚定。', 39, '《情深深雨濛濛》依萍和书桓的雨中争吵与相拥');
INSERT INTO `detailed` VALUES (28, '英雄联盟', '2025-01-13 22:42', '开心，哈哈哈?', 50, '易');
INSERT INTO `detailed` VALUES (29, '英雄联盟', '2025-01-13 22:42', '开心，哈哈哈?', 50, '易');
INSERT INTO `detailed` VALUES (30, 'LZC123456', '2025-01-13 22:44', 'jsims', 49, '西游记');
INSERT INTO `detailed` VALUES (31, 'LZC123456', '2025-01-13 22:45', 'MAN！What can i say！！', 49, '西游记');
INSERT INTO `detailed` VALUES (32, 'gs1', '2025-01-13 23:12', 'Good luck ', 50, '易');
INSERT INTO `detailed` VALUES (33, 'dcb', '2025-01-13 23:25', '很强', 50, '易');
INSERT INTO `detailed` VALUES (34, 'MJ', '2025-01-18 13:15', 'You Are Not Alone', 55, 'You Are Not Alone');
INSERT INTO `detailed` VALUES (35, 'MJ', '2025-01-18 13:31', '测试1', 50, '易');
INSERT INTO `detailed` VALUES (36, 'MJ', '2025-01-18 13:34', 's', 47, 'think about ');
INSERT INTO `detailed` VALUES (37, '喜欢劈瓜的刘华强', '2025-01-19 14:02', '分开一千天，天天盼会见面。只怕是你先找到我，但直行直过，天都帮你去躲，躲开不见我?', 56, 'LOVE');
INSERT INTO `detailed` VALUES (38, '喜欢劈瓜的刘华强', '2025-01-20 18:14:30', 'SAVE', 58, 'ABG');
INSERT INTO `detailed` VALUES (39, '喜欢劈瓜的刘华强', '2025-01-20 18:14:48', '哈哈哈哈哈哈哈哈哈', 50, '易');
INSERT INTO `detailed` VALUES (41, '喜欢劈瓜的刘华强', '2025-01-20 18:57:47', '我是克里斯', 50, '易');
INSERT INTO `detailed` VALUES (42, '爱吃鱼的猫', '2025-01-20 21:41', '这个爱情有点恋爱脑哎', 39, '《情深深雨濛濛》依萍和书桓的雨中争吵与相拥');
INSERT INTO `detailed` VALUES (43, '喜欢劈瓜的刘华强', '2025-01-20 21:57', '我不懂，但是我大受震惊?', 63, '拥有恋爱脑的下场');
INSERT INTO `detailed` VALUES (44, 'gs1', '2025-01-20 23:18', 'Dutch', 47, 'think about ');
INSERT INTO `detailed` VALUES (45, '喜欢劈瓜的刘华强', '2025-01-22 17:20', '新年快乐！', 88, 'HAPPY NEW YEAR');
INSERT INTO `detailed` VALUES (46, '喜欢劈瓜的刘华强', '2025-01-22 14:17', '芜湖', 88, 'HAPPY NEW YEAR');
INSERT INTO `detailed` VALUES (47, '英雄联盟', '2025-01-24 15:27:50', '我喜欢劈瓜', 88, 'HAPPY NEW YEAR');
INSERT INTO `detailed` VALUES (48, '喜欢劈瓜的刘华强', '2025-01-22 23:44', '自己有时候都猜不透自己呢，怀疑是最强大的敌人，无论任何时候。', 96, '关于一些感情问题');
INSERT INTO `detailed` VALUES (49, '十面埋伏', '2025-01-24 22:57:14', '有头像了，⛏', 95, '@莫');

SET FOREIGN_KEY_CHECKS = 1;
