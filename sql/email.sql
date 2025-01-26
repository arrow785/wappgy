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

 Date: 26/01/2025 12:19:37
*/

SET NAMES utf8mb4;
SET FOREIGN_KEY_CHECKS = 0;

-- ----------------------------
-- Table structure for email
-- ----------------------------
DROP TABLE IF EXISTS `email`;
CREATE TABLE `email`  (
  `id` int NOT NULL AUTO_INCREMENT COMMENT 'id',
  `send_username` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NOT NULL COMMENT '发送者',
  `send_email` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NOT NULL COMMENT '发送者的邮箱',
  `send_content` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NOT NULL COMMENT '发送的内容',
  `send_date` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NOT NULL COMMENT '发送时间',
  `is_send` varchar(20) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NOT NULL COMMENT '发送是否成功',
  PRIMARY KEY (`id`) USING BTREE
) ENGINE = InnoDB AUTO_INCREMENT = 17 CHARACTER SET = utf8mb4 COLLATE = utf8mb4_general_ci ROW_FORMAT = Dynamic;

-- ----------------------------
-- Records of email
-- ----------------------------
INSERT INTO `email` VALUES (1, 'MJ', 'mj@163.com', 'MJ123', '2025-01-23 17:45', '成功');
INSERT INTO `email` VALUES (2, 'd', '未知邮箱', '向天在借500年', '2025-01-23 20:53', '成功');
INSERT INTO `email` VALUES (3, '游客1', '2310907129@qq.com', '测试1', '2025-01-23 20:56', '成功');
INSERT INTO `email` VALUES (4, '123', '1582215621@qq.com', '111', '2025-01-23 20:57', '成功');
INSERT INTO `email` VALUES (7, '游客1', 'youke@youke@163.com', 'yoke', '2025-01-24 16:26:39', '成功');
INSERT INTO `email` VALUES (8, '喜欢劈瓜的刘华强', 'luoruiGeng@163.com', '我是摸鱼怪', '2025-01-24 16:28:19', '成功');
INSERT INTO `email` VALUES (9, '游客1', 'youke@youke@163.com', 'ceg', '2025-01-25 00:04:12', '成功');
INSERT INTO `email` VALUES (10, '游客1', 'jkss@163.com', '123', '2025-01-25 00:05:06', '成功');
INSERT INTO `email` VALUES (11, '游客1', 's@163.com', 'TTTTTTTTTT', '2025-01-25 00:06:09', '成功');
INSERT INTO `email` VALUES (12, '摸鱼怪', '2310907129@qq.com', '谢谢你', '2025-01-25 00:07:25', '成功');
INSERT INTO `email` VALUES (13, '游客1', '', '谢谢你,,', '2025-01-25 00:07:53', '成功');
INSERT INTO `email` VALUES (14, '游客1', '', 'assas', '2025-01-25 00:08:30', '成功');
INSERT INTO `email` VALUES (15, '游客1', 'youke@youke@163.com', 'assas', '2025-01-25 00:09:02', '成功');
INSERT INTO `email` VALUES (16, '游客1', 'youke@youke@163.com', '哈哈哈哈ffg', '2025-01-25 00:09:16', '成功');

SET FOREIGN_KEY_CHECKS = 1;
