/*
 Navicat Premium Data Transfer

 Source Server         : localhost
 Source Server Type    : MySQL
 Source Server Version : 50553
 Source Host           : localhost:3306
 Source Schema         : douban

 Target Server Type    : MySQL
 Target Server Version : 50553
 File Encoding         : 65001

 Date: 05/12/2018 09:36:46
*/

SET NAMES utf8mb4;
SET FOREIGN_KEY_CHECKS = 0;

-- ----------------------------
-- Table structure for pz_douban_movie
-- ----------------------------
DROP TABLE IF EXISTS `pz_douban_movie`;
CREATE TABLE `pz_douban_movie`  (
  `id` bigint(11) NOT NULL DEFAULT 0 COMMENT '豆瓣影片id',
  `name` varchar(255) CHARACTER SET utf8 COLLATE utf8_general_ci NOT NULL COMMENT '电影名',
  `subtitle` varchar(255) CHARACTER SET utf8 COLLATE utf8_general_ci NULL DEFAULT NULL COMMENT '又名',
  `score` decimal(9, 2) NOT NULL DEFAULT 0.00 COMMENT '评分',
  `num` int(11) NOT NULL DEFAULT 0 COMMENT '评价人数',
  `link` varchar(255) CHARACTER SET utf8 COLLATE utf8_general_ci NOT NULL DEFAULT '' COMMENT '详情链接',
  `type` varchar(20) CHARACTER SET utf8 COLLATE utf8_general_ci NOT NULL DEFAULT '0' COMMENT '类型',
  `directors` varchar(255) CHARACTER SET utf8 COLLATE utf8_general_ci NOT NULL DEFAULT '' COMMENT '导演',
  `screenwriters` varchar(255) CHARACTER SET utf8 COLLATE utf8_general_ci NOT NULL DEFAULT '' COMMENT '编剧',
  `actors` text CHARACTER SET utf8 COLLATE utf8_general_ci NOT NULL COMMENT '主演',
  `tags` varchar(255) CHARACTER SET utf8 COLLATE utf8_general_ci NOT NULL COMMENT '标签',
  `publish_time` varchar(255) CHARACTER SET utf8 COLLATE utf8_general_ci NOT NULL DEFAULT '' COMMENT '上映时间',
  `length` varchar(255) CHARACTER SET utf8 COLLATE utf8_general_ci NOT NULL DEFAULT '' COMMENT '片长',
  `updated_at` int(11) NOT NULL DEFAULT 0 COMMENT '抓取时间',
  `created_at` int(11) NOT NULL DEFAULT 0 COMMENT '创建时间',
  `detail` varchar(1000) CHARACTER SET utf8 COLLATE utf8_general_ci NULL DEFAULT NULL COMMENT '简介',
  `longtime` varchar(20) CHARACTER SET utf8 COLLATE utf8_general_ci NULL DEFAULT NULL COMMENT '片长',
  `publish_zone` varchar(255) CHARACTER SET utf8 COLLATE utf8_general_ci NULL DEFAULT NULL COMMENT '地区',
  `avatar` varchar(255) CHARACTER SET utf8 COLLATE utf8_general_ci NULL DEFAULT NULL COMMENT '封面',
  `has_tj` int(10) NULL DEFAULT NULL COMMENT '有否图解',
  `tag` varchar(255) CHARACTER SET utf8 COLLATE utf8_general_ci NULL DEFAULT NULL COMMENT 'tag',
  `get_detail` int(11) NOT NULL DEFAULT 0,
  `type_bak` varchar(255) CHARACTER SET utf8 COLLATE utf8_general_ci NULL DEFAULT NULL,
  PRIMARY KEY (`id`) USING BTREE,
  INDEX `idx_film_id`(`id`) USING BTREE
) ENGINE = InnoDB CHARACTER SET = utf8 COLLATE = utf8_general_ci COMMENT = '影片表' ROW_FORMAT = Compact;

SET FOREIGN_KEY_CHECKS = 1;
