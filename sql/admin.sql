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

 Date: 26/01/2025 12:19:20
*/

SET NAMES utf8mb4;
SET FOREIGN_KEY_CHECKS = 0;

-- ----------------------------
-- Table structure for admin
-- ----------------------------
DROP TABLE IF EXISTS `admin`;
CREATE TABLE `admin`  (
  `id` int NOT NULL AUTO_INCREMENT COMMENT 'id 唯一值',
  `username` varchar(60) CHARACTER SET utf8mb3 COLLATE utf8mb3_general_ci NULL DEFAULT NULL COMMENT '用户名',
  `nick_name` varchar(255) CHARACTER SET utf8mb3 COLLATE utf8mb3_general_ci NOT NULL COMMENT '昵称',
  `email` varchar(255) CHARACTER SET utf8mb3 COLLATE utf8mb3_general_ci NULL DEFAULT NULL COMMENT '邮箱',
  `pwd` varchar(60) CHARACTER SET utf8mb3 COLLATE utf8mb3_general_ci NOT NULL COMMENT '登录密码',
  `introduce` varchar(255) CHARACTER SET utf8mb3 COLLATE utf8mb3_general_ci NULL DEFAULT NULL COMMENT '个人简介',
  `avatar` varchar(255) CHARACTER SET utf8mb3 COLLATE utf8mb3_general_ci NULL DEFAULT NULL COMMENT '头像',
  `register_date` varchar(255) CHARACTER SET utf8mb3 COLLATE utf8mb3_general_ci NULL DEFAULT NULL COMMENT '注册时间',
  PRIMARY KEY (`id`) USING BTREE
) ENGINE = InnoDB AUTO_INCREMENT = 53 CHARACTER SET = utf8mb3 COLLATE = utf8mb3_general_ci ROW_FORMAT = DYNAMIC;

-- ----------------------------
-- Records of admin
-- ----------------------------
INSERT INTO `admin` VALUES (1, 'lisi', '', 'no_email', '202cb962ac59075b964b07152d234b70', '什么都没有！', 'static\\upload_img\\mr.png', NULL);
INSERT INTO `admin` VALUES (2, 'zhangsan', '', 'z@163.com', '202cb962ac59075b964b07152d234b70', '什么都没有！', 'static\\upload_img\\mr.png', NULL);
INSERT INTO `admin` VALUES (3, 'gousheng', '', '12@163.com', 'gs', '什么都没有！', 'static\\upload_img\\mr.png', NULL);
INSERT INTO `admin` VALUES (4, '英雄联盟', '我是傻逼', '2211672436@qq.com', '202cb962ac59075b964b07152d234b70', '我是傻逼!!!!!!!!', 'static\\upload_img\\4_avatar.jpg', NULL);
INSERT INTO `admin` VALUES (5, '琼瑶', '', '123@123', '202cb962ac59075b964b07152d234b70', '什么都没有！', 'static\\upload_img\\mr.png', NULL);
INSERT INTO `admin` VALUES (6, '李四', '', 'no_email', '202cb962ac59075b964b07152d234b70', '什么都没有！', 'static\\upload_img\\mr.png', NULL);
INSERT INTO `admin` VALUES (7, '哈哈', '', 'no_email', '202cb962ac59075b964b07152d234b70', '什么都没有！', 'static\\upload_img\\mr.png', NULL);
INSERT INTO `admin` VALUES (8, '莫德凯撒', '', 'luoruiGeng@163.com', '202cb962ac59075b964b07152d234b70', '什么都没有！', 'static\\upload_img\\mr.png', NULL);
INSERT INTO `admin` VALUES (9, 'gs1', '', '123@qq.com', '202cb962ac59075b964b07152d234b70', '什么都没有！', 'static\\upload_img\\mr.png', NULL);
INSERT INTO `admin` VALUES (11, '123', 'arr13JHSfsaS', '1582215621@qq.com', '81dc9bdb52d04dc20036dbd8313ed055', '什么都没有！', 'static\\upload_img\\11_avatar.jpg', NULL);
INSERT INTO `admin` VALUES (12, 'lzc123456', '', '2995872922@qq.com', 'e10adc3949ba59abbe56e057f20f883e', '什么都没有！', 'static\\upload_img\\mr.png', NULL);
INSERT INTO `admin` VALUES (29, 'arros', '', 'no_email', '202cb962ac59075b964b07152d234b70', '什么都没有！', 'static\\upload_img\\mr.png', NULL);
INSERT INTO `admin` VALUES (30, 'dcb', '', 'no_email', 'e10adc3949ba59abbe56e057f20f883e', '什么都没有！', 'static\\upload_img\\mr.png', NULL);
INSERT INTO `admin` VALUES (31, 'MJ', '', 'mj@163.com', '202cb962ac59075b964b07152d234b70', '什么都没有！', 'static\\upload_img\\mr.png', NULL);
INSERT INTO `admin` VALUES (32, '大司马', '', 'no_email', '202cb962ac59075b964b07152d234b70', '什么都没有！', 'static\\upload_img\\mr.png', NULL);
INSERT INTO `admin` VALUES (33, 'sgh', '', 'no_email', '202cb962ac59075b964b07152d234b70', '什么都没有！', 'static\\upload_img\\mr.png', NULL);
INSERT INTO `admin` VALUES (34, '喜欢劈瓜的刘华强', 'linkinpark_vc', 'luoruiGeng@163.com', '81dc9bdb52d04dc20036dbd8313ed055', 'lust for life', 'static\\upload_img\\34_avatar.jpg', NULL);
INSERT INTO `admin` VALUES (40, '爱吃鱼的猫', '', 'no_email', '5105fce7397916fcf85234f6fc895178', '什么都没有！', 'static\\upload_img\\mr.png', NULL);
INSERT INTO `admin` VALUES (42, '567', '', '1582215621@qq.com', 'c4ca4238a0b923820dcc509a6f75849b', '什么都没有！', 'static\\upload_img\\mr.png', NULL);
INSERT INTO `admin` VALUES (45, 'zhangsan8', 'arr1336225HMnT', '2211672436@qq.com', '202cb962ac59075b964b07152d234b70', '什么都没有！', 'static\\upload_img\\lyy-2.jpg', '2025-01-24 13:36:22');
INSERT INTO `admin` VALUES (49, 'amomentapart', 'arrows_dev', '123@qq.com', '202cb962ac59075b964b07152d234b70', '什么都没有！', 'static\\upload_img\\mr.png', '2025-01-24 13:47:32');
INSERT INTO `admin` VALUES (50, 'ght', '', '1232@13.com', '202cb962ac59075b964b07152d234b70', '什么都没有！', 'static\\upload_img\\mr.png', '2025-01-24 15:01:41');
INSERT INTO `admin` VALUES (51, '睡醒没YYY', 'arr43566JASn', 'no_email', '202cb962ac59075b964b07152d234b70', '什么都没有！', 'static\\upload_img\\mr.png', NULL);
INSERT INTO `admin` VALUES (52, '十面埋伏', '', 'zsan30547@163.com', '202cb962ac59075b964b07152d234b70', '什么都没有！', 'static\\upload_img\\52_avatar.jpg', '2025-01-24 22:55:41');
INSERT INTO `admin` VALUES (53, '我拿什么留住你', '', '2310907129@qq.com', '202cb962ac59075b964b07152d234b70', '什么都没有！', 'static\\upload_img\\mr.png', '2025-01-26 11:02:01');
INSERT INTO `admin` VALUES (54, 'dfff', '李四', 'dfff@qq.com', '202cb962ac59075b964b07152d234b70', '什么都没有！', 'static\\upload_img\\mr.png', '2025-01-26 11:10:40');

SET FOREIGN_KEY_CHECKS = 1;
