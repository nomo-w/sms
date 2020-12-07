-- MySQL dump 10.14  Distrib 5.5.68-MariaDB, for Linux (x86_64)
--
-- Host: 35.240.146.85    Database: sms
-- ------------------------------------------------------
-- Server version	5.7.25-google-log

/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8 */;
/*!40103 SET @OLD_TIME_ZONE=@@TIME_ZONE */;
/*!40103 SET TIME_ZONE='+00:00' */;
/*!40014 SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0 */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
/*!40111 SET @OLD_SQL_NOTES=@@SQL_NOTES, SQL_NOTES=0 */;

--
-- Table structure for table `sms_all_statistics`
--

DROP TABLE IF EXISTS `sms_all_statistics`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `sms_all_statistics` (
  `id` int(11) unsigned NOT NULL AUTO_INCREMENT,
  `plateform_id` int(11) NOT NULL,
  `total_count` varchar(150) DEFAULT '0',
  `success_count` varchar(150) DEFAULT '0',
  `failure_count` varchar(150) DEFAULT '0',
  `price_count` decimal(25,2) DEFAULT '0.00',
  `create_time` timestamp NULL DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=51 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `sms_cache_all_statistics`
--

DROP TABLE IF EXISTS `sms_cache_all_statistics`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `sms_cache_all_statistics` (
  `id` int(11) unsigned NOT NULL AUTO_INCREMENT,
  `plateform_id` int(11) NOT NULL,
  `channel_id` int(11) NOT NULL,
  `total_count` varchar(150) DEFAULT '0',
  `success_count` varchar(150) DEFAULT '0',
  `failure_count` varchar(150) DEFAULT '0',
  `create_time` timestamp NULL DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=181 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `sms_cache_all_statistics_by_day`
--

DROP TABLE IF EXISTS `sms_cache_all_statistics_by_day`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `sms_cache_all_statistics_by_day` (
  `id` int(11) unsigned NOT NULL AUTO_INCREMENT,
  `day` varchar(200) NOT NULL,
  `plateform_id` int(11) NOT NULL,
  `channel_id` int(11) NOT NULL,
  `total_count` varchar(150) DEFAULT '0',
  `success_count` varchar(150) DEFAULT '0',
  `failure_count` varchar(150) DEFAULT '0',
  `create_time` timestamp NULL DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=4463 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `sms_cache_plateform10_history`
--

DROP TABLE IF EXISTS `sms_cache_plateform10_history`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `sms_cache_plateform10_history` (
  `id` int(11) unsigned NOT NULL AUTO_INCREMENT,
  `user` char(11) NOT NULL,
  `user_id` int(11) NOT NULL,
  `channel_id` int(11) NOT NULL,
  `to_number` char(100) DEFAULT NULL,
  `text` char(200) DEFAULT NULL,
  `time` timestamp NULL DEFAULT CURRENT_TIMESTAMP,
  `price` decimal(15,2) DEFAULT '0.00',
  `description` char(50) DEFAULT NULL,
  `message_id` varchar(50) DEFAULT '0' COMMENT '唯一id',
  `is_click` char(10) DEFAULT '未设置',
  `callback_id` int(11) DEFAULT '0',
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=105887 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `sms_cache_plateform11_history`
--

DROP TABLE IF EXISTS `sms_cache_plateform11_history`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `sms_cache_plateform11_history` (
  `id` int(11) unsigned NOT NULL AUTO_INCREMENT,
  `user` char(11) NOT NULL,
  `user_id` int(11) NOT NULL,
  `channel_id` int(11) NOT NULL,
  `to_number` char(100) DEFAULT NULL,
  `text` char(200) DEFAULT NULL,
  `time` timestamp NULL DEFAULT CURRENT_TIMESTAMP,
  `price` decimal(15,2) DEFAULT '0.00',
  `description` char(50) DEFAULT NULL,
  `message_id` varchar(50) DEFAULT '0' COMMENT '唯一id',
  `is_click` char(10) DEFAULT '未设置',
  `callback_id` int(11) DEFAULT '0',
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=230871 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `sms_cache_plateform12_history`
--

DROP TABLE IF EXISTS `sms_cache_plateform12_history`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `sms_cache_plateform12_history` (
  `id` int(11) unsigned NOT NULL AUTO_INCREMENT,
  `user` char(11) NOT NULL,
  `user_id` int(11) NOT NULL,
  `channel_id` int(11) NOT NULL,
  `to_number` char(100) DEFAULT NULL,
  `text` char(200) DEFAULT NULL,
  `time` timestamp NULL DEFAULT CURRENT_TIMESTAMP,
  `price` decimal(15,2) DEFAULT '0.00',
  `description` char(50) DEFAULT NULL,
  `message_id` varchar(50) DEFAULT '0' COMMENT '唯一id',
  `is_click` char(10) DEFAULT '未设置',
  `callback_id` int(11) DEFAULT '0',
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=50555 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `sms_cache_plateform13_history`
--

DROP TABLE IF EXISTS `sms_cache_plateform13_history`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `sms_cache_plateform13_history` (
  `id` int(11) unsigned NOT NULL AUTO_INCREMENT,
  `user` char(11) NOT NULL,
  `user_id` int(11) NOT NULL,
  `channel_id` int(11) NOT NULL,
  `to_number` char(100) DEFAULT NULL,
  `text` char(200) DEFAULT NULL,
  `time` timestamp NULL DEFAULT CURRENT_TIMESTAMP,
  `price` decimal(15,2) DEFAULT '0.00',
  `description` char(50) DEFAULT NULL,
  `message_id` varchar(50) DEFAULT '0' COMMENT '唯一id',
  `is_click` char(10) DEFAULT '未设置',
  `callback_id` int(11) DEFAULT '0',
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=27 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `sms_cache_plateform14_history`
--

DROP TABLE IF EXISTS `sms_cache_plateform14_history`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `sms_cache_plateform14_history` (
  `id` int(11) unsigned NOT NULL AUTO_INCREMENT,
  `user` char(11) NOT NULL,
  `user_id` int(11) NOT NULL,
  `channel_id` int(11) NOT NULL,
  `to_number` char(100) DEFAULT NULL,
  `text` char(200) DEFAULT NULL,
  `time` timestamp NULL DEFAULT CURRENT_TIMESTAMP,
  `price` decimal(15,2) DEFAULT '0.00',
  `description` char(50) DEFAULT NULL,
  `message_id` varchar(50) DEFAULT '0' COMMENT '唯一id',
  `is_click` char(10) DEFAULT '未设置',
  `callback_id` int(11) DEFAULT '0',
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `sms_cache_plateform15_history`
--

DROP TABLE IF EXISTS `sms_cache_plateform15_history`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `sms_cache_plateform15_history` (
  `id` int(11) unsigned NOT NULL AUTO_INCREMENT,
  `user` char(11) NOT NULL,
  `user_id` int(11) NOT NULL,
  `channel_id` int(11) NOT NULL,
  `to_number` char(100) DEFAULT NULL,
  `text` char(200) DEFAULT NULL,
  `time` timestamp NULL DEFAULT CURRENT_TIMESTAMP,
  `price` decimal(15,2) DEFAULT '0.00',
  `description` char(50) DEFAULT NULL,
  `message_id` varchar(50) DEFAULT '0' COMMENT '唯一id',
  `is_click` char(10) DEFAULT '未设置',
  `callback_id` int(11) DEFAULT '0',
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `sms_cache_plateform16_history`
--

DROP TABLE IF EXISTS `sms_cache_plateform16_history`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `sms_cache_plateform16_history` (
  `id` int(11) unsigned NOT NULL AUTO_INCREMENT,
  `user` char(11) NOT NULL,
  `user_id` int(11) NOT NULL,
  `channel_id` int(11) NOT NULL,
  `to_number` char(100) DEFAULT NULL,
  `text` char(200) DEFAULT NULL,
  `time` timestamp NULL DEFAULT CURRENT_TIMESTAMP,
  `price` decimal(15,2) DEFAULT '0.00',
  `description` char(50) DEFAULT NULL,
  `message_id` varchar(50) DEFAULT '0' COMMENT '唯一id',
  `is_click` char(10) DEFAULT '未设置',
  `callback_id` int(11) DEFAULT '0',
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=1186129 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `sms_cache_plateform17_history`
--

DROP TABLE IF EXISTS `sms_cache_plateform17_history`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `sms_cache_plateform17_history` (
  `id` int(11) unsigned NOT NULL AUTO_INCREMENT,
  `user` char(11) NOT NULL,
  `user_id` int(11) NOT NULL,
  `channel_id` int(11) NOT NULL,
  `to_number` char(100) DEFAULT NULL,
  `text` char(200) DEFAULT NULL,
  `time` timestamp NULL DEFAULT CURRENT_TIMESTAMP,
  `price` decimal(15,2) DEFAULT '0.00',
  `description` char(50) DEFAULT NULL,
  `message_id` varchar(50) DEFAULT '0' COMMENT '唯一id',
  `is_click` char(10) DEFAULT '未设置',
  `callback_id` int(11) DEFAULT '0',
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=377767 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `sms_cache_plateform18_history`
--

DROP TABLE IF EXISTS `sms_cache_plateform18_history`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `sms_cache_plateform18_history` (
  `id` int(11) unsigned NOT NULL AUTO_INCREMENT,
  `user` char(11) NOT NULL,
  `user_id` int(11) NOT NULL,
  `channel_id` int(11) NOT NULL,
  `to_number` char(100) DEFAULT NULL,
  `text` char(200) DEFAULT NULL,
  `time` timestamp NULL DEFAULT CURRENT_TIMESTAMP,
  `price` decimal(15,2) DEFAULT '0.00',
  `description` char(50) DEFAULT NULL,
  `message_id` varchar(50) DEFAULT '0' COMMENT '唯一id',
  `is_click` char(10) DEFAULT '未设置',
  `callback_id` int(11) DEFAULT '0',
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=262277 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `sms_cache_plateform19_history`
--

DROP TABLE IF EXISTS `sms_cache_plateform19_history`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `sms_cache_plateform19_history` (
  `id` int(11) unsigned NOT NULL AUTO_INCREMENT,
  `user` char(11) NOT NULL,
  `user_id` int(11) NOT NULL,
  `channel_id` int(11) NOT NULL,
  `to_number` char(100) DEFAULT NULL,
  `text` char(200) DEFAULT NULL,
  `time` timestamp NULL DEFAULT CURRENT_TIMESTAMP,
  `price` decimal(15,2) DEFAULT '0.00',
  `description` char(50) DEFAULT NULL,
  `message_id` varchar(50) DEFAULT '0' COMMENT '唯一id',
  `is_click` char(10) DEFAULT '未设置',
  `callback_id` int(11) DEFAULT '0',
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=33401 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `sms_cache_plateform20_history`
--

DROP TABLE IF EXISTS `sms_cache_plateform20_history`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `sms_cache_plateform20_history` (
  `id` int(11) unsigned NOT NULL AUTO_INCREMENT,
  `user` char(11) NOT NULL,
  `user_id` int(11) NOT NULL,
  `channel_id` int(11) NOT NULL,
  `to_number` char(100) DEFAULT NULL,
  `text` char(200) DEFAULT NULL,
  `time` timestamp NULL DEFAULT CURRENT_TIMESTAMP,
  `price` decimal(15,2) DEFAULT '0.00',
  `description` char(50) DEFAULT NULL,
  `message_id` varchar(50) DEFAULT '0' COMMENT '唯一id',
  `is_click` char(10) DEFAULT '未设置',
  `callback_id` int(11) DEFAULT '0',
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=1442526 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `sms_cache_plateform21_history`
--

DROP TABLE IF EXISTS `sms_cache_plateform21_history`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `sms_cache_plateform21_history` (
  `id` int(11) unsigned NOT NULL AUTO_INCREMENT,
  `user` char(11) NOT NULL,
  `user_id` int(11) NOT NULL,
  `channel_id` int(11) NOT NULL,
  `to_number` char(100) DEFAULT NULL,
  `text` char(200) DEFAULT NULL,
  `time` timestamp NULL DEFAULT CURRENT_TIMESTAMP,
  `price` decimal(15,2) DEFAULT '0.00',
  `description` char(50) DEFAULT NULL,
  `message_id` varchar(50) DEFAULT '0' COMMENT '唯一id',
  `is_click` char(10) DEFAULT '未设置',
  `callback_id` int(11) DEFAULT '0',
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=2145 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `sms_cache_plateform2_history`
--

DROP TABLE IF EXISTS `sms_cache_plateform2_history`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `sms_cache_plateform2_history` (
  `id` int(11) unsigned NOT NULL AUTO_INCREMENT,
  `user` char(11) NOT NULL,
  `user_id` int(11) NOT NULL,
  `channel_id` int(11) NOT NULL,
  `to_number` char(100) DEFAULT NULL,
  `text` char(200) DEFAULT NULL,
  `time` timestamp NULL DEFAULT CURRENT_TIMESTAMP,
  `price` decimal(15,2) DEFAULT '0.00',
  `description` char(50) DEFAULT NULL,
  `message_id` varchar(50) DEFAULT '0' COMMENT '唯一id',
  `is_click` char(10) DEFAULT '未设置',
  `callback_id` int(11) DEFAULT '0',
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=1083325 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `sms_cache_plateform3_history`
--

DROP TABLE IF EXISTS `sms_cache_plateform3_history`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `sms_cache_plateform3_history` (
  `id` int(11) unsigned NOT NULL AUTO_INCREMENT,
  `user` char(11) NOT NULL,
  `user_id` int(11) NOT NULL,
  `channel_id` int(11) NOT NULL,
  `to_number` char(100) DEFAULT NULL,
  `text` char(200) DEFAULT NULL,
  `time` timestamp NULL DEFAULT CURRENT_TIMESTAMP,
  `price` decimal(15,2) DEFAULT '0.00',
  `description` char(50) DEFAULT NULL,
  `message_id` varchar(50) DEFAULT '0' COMMENT '唯一id',
  `is_click` char(10) DEFAULT '未设置',
  `callback_id` int(11) DEFAULT '0',
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=586034 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `sms_cache_plateform4_history`
--

DROP TABLE IF EXISTS `sms_cache_plateform4_history`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `sms_cache_plateform4_history` (
  `id` int(11) unsigned NOT NULL AUTO_INCREMENT,
  `user` char(11) NOT NULL,
  `user_id` int(11) NOT NULL,
  `channel_id` int(11) NOT NULL,
  `to_number` char(100) DEFAULT NULL,
  `text` char(200) DEFAULT NULL,
  `time` timestamp NULL DEFAULT CURRENT_TIMESTAMP,
  `price` decimal(15,2) DEFAULT '0.00',
  `description` char(50) DEFAULT NULL,
  `message_id` varchar(50) DEFAULT '0' COMMENT '唯一id',
  `is_click` char(10) DEFAULT '未设置',
  `callback_id` int(11) DEFAULT '0',
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=662045 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `sms_cache_plateform5_history`
--

DROP TABLE IF EXISTS `sms_cache_plateform5_history`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `sms_cache_plateform5_history` (
  `id` int(11) unsigned NOT NULL AUTO_INCREMENT,
  `user` char(11) NOT NULL,
  `user_id` int(11) NOT NULL,
  `channel_id` int(11) NOT NULL,
  `to_number` char(100) DEFAULT NULL,
  `text` char(200) DEFAULT NULL,
  `time` timestamp NULL DEFAULT CURRENT_TIMESTAMP,
  `price` decimal(15,2) DEFAULT '0.00',
  `description` char(50) DEFAULT NULL,
  `message_id` varchar(50) DEFAULT '0' COMMENT '唯一id',
  `is_click` char(10) DEFAULT '未设置',
  `callback_id` int(11) DEFAULT '0',
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=481585 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `sms_cache_plateform6_history`
--

DROP TABLE IF EXISTS `sms_cache_plateform6_history`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `sms_cache_plateform6_history` (
  `id` int(11) unsigned NOT NULL AUTO_INCREMENT,
  `user` char(11) NOT NULL,
  `user_id` int(11) NOT NULL,
  `channel_id` int(11) NOT NULL,
  `to_number` char(100) DEFAULT NULL,
  `text` char(200) DEFAULT NULL,
  `time` timestamp NULL DEFAULT CURRENT_TIMESTAMP,
  `price` decimal(15,2) DEFAULT '0.00',
  `description` char(50) DEFAULT NULL,
  `message_id` varchar(50) DEFAULT '0' COMMENT '唯一id',
  `is_click` char(10) DEFAULT '未设置',
  `callback_id` int(11) DEFAULT '0',
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=188463 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `sms_cache_plateform7_history`
--

DROP TABLE IF EXISTS `sms_cache_plateform7_history`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `sms_cache_plateform7_history` (
  `id` int(11) unsigned NOT NULL AUTO_INCREMENT,
  `user` char(11) NOT NULL,
  `user_id` int(11) NOT NULL,
  `channel_id` int(11) NOT NULL,
  `to_number` char(100) DEFAULT NULL,
  `text` char(200) DEFAULT NULL,
  `time` timestamp NULL DEFAULT CURRENT_TIMESTAMP,
  `price` decimal(15,2) DEFAULT '0.00',
  `description` char(50) DEFAULT NULL,
  `message_id` varchar(50) DEFAULT '0' COMMENT '唯一id',
  `is_click` char(10) DEFAULT '未设置',
  `callback_id` int(11) DEFAULT '0',
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=1110105 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `sms_cache_plateform8_history`
--

DROP TABLE IF EXISTS `sms_cache_plateform8_history`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `sms_cache_plateform8_history` (
  `id` int(11) unsigned NOT NULL AUTO_INCREMENT,
  `user` char(11) NOT NULL,
  `user_id` int(11) NOT NULL,
  `channel_id` int(11) NOT NULL,
  `to_number` char(100) DEFAULT NULL,
  `text` char(200) DEFAULT NULL,
  `time` timestamp NULL DEFAULT CURRENT_TIMESTAMP,
  `price` decimal(15,2) DEFAULT '0.00',
  `description` char(50) DEFAULT NULL,
  `message_id` varchar(50) DEFAULT '0' COMMENT '唯一id',
  `is_click` char(10) DEFAULT '未设置',
  `callback_id` int(11) DEFAULT '0',
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=1223545 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `sms_cache_plateform9_history`
--

DROP TABLE IF EXISTS `sms_cache_plateform9_history`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `sms_cache_plateform9_history` (
  `id` int(11) unsigned NOT NULL AUTO_INCREMENT,
  `user` char(11) NOT NULL,
  `user_id` int(11) NOT NULL,
  `channel_id` int(11) NOT NULL,
  `to_number` char(100) DEFAULT NULL,
  `text` char(200) DEFAULT NULL,
  `time` timestamp NULL DEFAULT CURRENT_TIMESTAMP,
  `price` decimal(15,2) DEFAULT '0.00',
  `description` char(50) DEFAULT NULL,
  `message_id` varchar(50) DEFAULT '0' COMMENT '唯一id',
  `is_click` char(10) DEFAULT '未设置',
  `callback_id` int(11) DEFAULT '0',
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=834446 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `sms_callback`
--

DROP TABLE IF EXISTS `sms_callback`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `sms_callback` (
  `id` int(11) unsigned NOT NULL AUTO_INCREMENT,
  `to_number` varchar(30) NOT NULL,
  `url` varchar(50) NOT NULL,
  `plateform_id` int(11) NOT NULL,
  `time` timestamp NULL DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=544235 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `sms_channel`
--

DROP TABLE IF EXISTS `sms_channel`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `sms_channel` (
  `id` int(11) unsigned NOT NULL AUTO_INCREMENT,
  `name` char(50) DEFAULT NULL,
  `balance` decimal(15,2) DEFAULT '0.00',
  `create_time` timestamp NULL DEFAULT CURRENT_TIMESTAMP,
  `is_active` tinyint(1) DEFAULT '1',
  `channel_type` varchar(50) NOT NULL,
  `description` char(255) DEFAULT '',
  `is_have_danfa` tinyint(1) DEFAULT '1',
  `is_have_qunfa` tinyint(1) DEFAULT '1',
  `max_send` int(11) DEFAULT '1',
  `min_send` int(11) DEFAULT '1',
  `max_text_len` int(11) DEFAULT '60',
  `need_get_result` tinyint(1) DEFAULT '0',
  `need_display` tinyint(1) DEFAULT '1',
  `additional_code` varchar(20) DEFAULT '',
  `need_report` tinyint(1) DEFAULT '1',
  `need_template` tinyint(1) DEFAULT '0',
  `need_notice_telegram` tinyint(1) DEFAULT '0',
  `notice_limit_balance` int(11) DEFAULT '20000',
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=11 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `sms_channel_statistics`
--

DROP TABLE IF EXISTS `sms_channel_statistics`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `sms_channel_statistics` (
  `id` int(11) unsigned NOT NULL AUTO_INCREMENT,
  `plateform_id` int(11) NOT NULL,
  `channel_id` int(11) NOT NULL,
  `total_count` varchar(150) DEFAULT '0',
  `success_count` varchar(150) DEFAULT '0',
  `failure_count` varchar(150) DEFAULT '0',
  `create_time` timestamp NULL DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=265 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `sms_control`
--

DROP TABLE IF EXISTS `sms_control`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `sms_control` (
  `id` int(11) unsigned NOT NULL AUTO_INCREMENT,
  `name` char(10) DEFAULT NULL,
  `plateform_id` int(11) NOT NULL,
  `run` int(2) DEFAULT NULL COMMENT '0-停止 / 1-启动',
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=22 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `sms_pending`
--

DROP TABLE IF EXISTS `sms_pending`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `sms_pending` (
  `id` int(11) unsigned NOT NULL AUTO_INCREMENT,
  `user` char(11) NOT NULL,
  `channel_id` int(11) NOT NULL,
  `plateform_id` int(11) NOT NULL,
  `to_number` char(25) DEFAULT NULL,
  `text` char(200) DEFAULT NULL,
  `time` timestamp NULL DEFAULT CURRENT_TIMESTAMP,
  `message_id` varchar(50) DEFAULT '0' COMMENT '唯一id',
  `is_click` char(10) DEFAULT '未设置',
  `callback_id` int(11) DEFAULT '0',
  `price` decimal(15,2) DEFAULT '0.00',
  `description` char(50) DEFAULT 'pending',
  `user_id` int(11) DEFAULT '-1',
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=16781753 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `sms_plateform`
--

DROP TABLE IF EXISTS `sms_plateform`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `sms_plateform` (
  `id` int(11) unsigned NOT NULL AUTO_INCREMENT,
  `name` char(50) NOT NULL,
  `create_time` timestamp NULL DEFAULT CURRENT_TIMESTAMP,
  `domain` char(20) NOT NULL,
  `balance` decimal(15,2) DEFAULT '0.00',
  `is_active` tinyint(1) DEFAULT '1',
  `nginx_file_name` char(50) NOT NULL,
  `kl_limit` int(11) DEFAULT '3000',
  `kl` int(11) DEFAULT '10',
  `need_white_list` tinyint(1) DEFAULT '0',
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=22 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `sms_plateform10_all_statistics_by_day`
--

DROP TABLE IF EXISTS `sms_plateform10_all_statistics_by_day`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `sms_plateform10_all_statistics_by_day` (
  `id` int(11) unsigned NOT NULL AUTO_INCREMENT,
  `day` varchar(150) NOT NULL,
  `total_count` varchar(150) DEFAULT '0',
  `success_count` varchar(150) DEFAULT '0',
  `failure_count` varchar(150) DEFAULT '0',
  `price_count` decimal(15,2) DEFAULT '0.00',
  `create_time` timestamp NULL DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`id`),
  UNIQUE KEY `day` (`day`)
) ENGINE=InnoDB AUTO_INCREMENT=277 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `sms_plateform10_channel_statistics_by_day`
--

DROP TABLE IF EXISTS `sms_plateform10_channel_statistics_by_day`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `sms_plateform10_channel_statistics_by_day` (
  `id` int(11) unsigned NOT NULL AUTO_INCREMENT,
  `day` varchar(150) NOT NULL,
  `channel_id` int(11) NOT NULL,
  `total_count` varchar(150) DEFAULT '0',
  `success_count` varchar(150) DEFAULT '0',
  `failure_count` varchar(150) DEFAULT '0',
  `create_time` timestamp NULL DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=270 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `sms_plateform10_failure`
--

DROP TABLE IF EXISTS `sms_plateform10_failure`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `sms_plateform10_failure` (
  `id` int(11) unsigned NOT NULL AUTO_INCREMENT,
  `user` char(11) NOT NULL,
  `user_id` int(11) NOT NULL,
  `channel_id` int(11) NOT NULL,
  `to_number` char(100) DEFAULT NULL,
  `text` char(200) DEFAULT NULL,
  `time` timestamp NULL DEFAULT CURRENT_TIMESTAMP,
  `price` decimal(15,2) DEFAULT '0.00',
  `description` char(50) DEFAULT NULL,
  `message_id` varchar(50) DEFAULT '0' COMMENT '唯一id',
  `is_click` char(10) DEFAULT '未设置',
  `callback_id` int(11) DEFAULT '0',
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=100793 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `sms_plateform10_success`
--

DROP TABLE IF EXISTS `sms_plateform10_success`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `sms_plateform10_success` (
  `id` int(11) unsigned NOT NULL AUTO_INCREMENT,
  `user` char(11) NOT NULL,
  `user_id` int(11) NOT NULL,
  `channel_id` int(11) NOT NULL,
  `to_number` char(100) DEFAULT NULL,
  `text` char(200) DEFAULT NULL,
  `time` timestamp NULL DEFAULT CURRENT_TIMESTAMP,
  `price` decimal(15,2) DEFAULT '0.00',
  `description` char(50) DEFAULT NULL,
  `message_id` varchar(50) DEFAULT '0' COMMENT '唯一id',
  `is_click` char(10) DEFAULT '未设置',
  `callback_id` int(11) DEFAULT '0',
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=563490 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `sms_plateform11_all_statistics_by_day`
--

DROP TABLE IF EXISTS `sms_plateform11_all_statistics_by_day`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `sms_plateform11_all_statistics_by_day` (
  `id` int(11) unsigned NOT NULL AUTO_INCREMENT,
  `day` varchar(150) NOT NULL,
  `total_count` varchar(150) DEFAULT '0',
  `success_count` varchar(150) DEFAULT '0',
  `failure_count` varchar(150) DEFAULT '0',
  `price_count` decimal(15,2) DEFAULT '0.00',
  `create_time` timestamp NULL DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`id`),
  UNIQUE KEY `day` (`day`)
) ENGINE=InnoDB AUTO_INCREMENT=279 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `sms_plateform11_channel_statistics_by_day`
--

DROP TABLE IF EXISTS `sms_plateform11_channel_statistics_by_day`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `sms_plateform11_channel_statistics_by_day` (
  `id` int(11) unsigned NOT NULL AUTO_INCREMENT,
  `day` varchar(150) NOT NULL,
  `channel_id` int(11) NOT NULL,
  `total_count` varchar(150) DEFAULT '0',
  `success_count` varchar(150) DEFAULT '0',
  `failure_count` varchar(150) DEFAULT '0',
  `create_time` timestamp NULL DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=294 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `sms_plateform11_failure`
--

DROP TABLE IF EXISTS `sms_plateform11_failure`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `sms_plateform11_failure` (
  `id` int(11) unsigned NOT NULL AUTO_INCREMENT,
  `user` char(11) NOT NULL,
  `user_id` int(11) NOT NULL,
  `channel_id` int(11) NOT NULL,
  `to_number` char(100) DEFAULT NULL,
  `text` char(200) DEFAULT NULL,
  `time` timestamp NULL DEFAULT CURRENT_TIMESTAMP,
  `price` decimal(15,2) DEFAULT '0.00',
  `description` char(50) DEFAULT NULL,
  `message_id` varchar(50) DEFAULT '0' COMMENT '唯一id',
  `is_click` char(10) DEFAULT '未设置',
  `callback_id` int(11) DEFAULT '0',
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=98742 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `sms_plateform11_success`
--

DROP TABLE IF EXISTS `sms_plateform11_success`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `sms_plateform11_success` (
  `id` int(11) unsigned NOT NULL AUTO_INCREMENT,
  `user` char(11) NOT NULL,
  `user_id` int(11) NOT NULL,
  `channel_id` int(11) NOT NULL,
  `to_number` char(100) DEFAULT NULL,
  `text` char(200) DEFAULT NULL,
  `time` timestamp NULL DEFAULT CURRENT_TIMESTAMP,
  `price` decimal(15,2) DEFAULT '0.00',
  `description` char(50) DEFAULT NULL,
  `message_id` varchar(50) DEFAULT '0' COMMENT '唯一id',
  `is_click` char(10) DEFAULT '未设置',
  `callback_id` int(11) DEFAULT '0',
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=551348 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `sms_plateform12_all_statistics_by_day`
--

DROP TABLE IF EXISTS `sms_plateform12_all_statistics_by_day`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `sms_plateform12_all_statistics_by_day` (
  `id` int(11) unsigned NOT NULL AUTO_INCREMENT,
  `day` varchar(150) NOT NULL,
  `total_count` varchar(150) DEFAULT '0',
  `success_count` varchar(150) DEFAULT '0',
  `failure_count` varchar(150) DEFAULT '0',
  `price_count` decimal(15,2) DEFAULT '0.00',
  `create_time` timestamp NULL DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`id`),
  UNIQUE KEY `day` (`day`)
) ENGINE=InnoDB AUTO_INCREMENT=613 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `sms_plateform12_channel_statistics_by_day`
--

DROP TABLE IF EXISTS `sms_plateform12_channel_statistics_by_day`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `sms_plateform12_channel_statistics_by_day` (
  `id` int(11) unsigned NOT NULL AUTO_INCREMENT,
  `day` varchar(150) NOT NULL,
  `channel_id` int(11) NOT NULL,
  `total_count` varchar(150) DEFAULT '0',
  `success_count` varchar(150) DEFAULT '0',
  `failure_count` varchar(150) DEFAULT '0',
  `create_time` timestamp NULL DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=262 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `sms_plateform12_failure`
--

DROP TABLE IF EXISTS `sms_plateform12_failure`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `sms_plateform12_failure` (
  `id` int(11) unsigned NOT NULL AUTO_INCREMENT,
  `user` char(11) NOT NULL,
  `user_id` int(11) NOT NULL,
  `channel_id` int(11) NOT NULL,
  `to_number` char(100) DEFAULT NULL,
  `text` char(200) DEFAULT NULL,
  `time` timestamp NULL DEFAULT CURRENT_TIMESTAMP,
  `price` decimal(15,2) DEFAULT '0.00',
  `description` char(50) DEFAULT NULL,
  `message_id` varchar(50) DEFAULT '0' COMMENT '唯一id',
  `is_click` char(10) DEFAULT '未设置',
  `callback_id` int(11) DEFAULT '0',
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=2619 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `sms_plateform12_success`
--

DROP TABLE IF EXISTS `sms_plateform12_success`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `sms_plateform12_success` (
  `id` int(11) unsigned NOT NULL AUTO_INCREMENT,
  `user` char(11) NOT NULL,
  `user_id` int(11) NOT NULL,
  `channel_id` int(11) NOT NULL,
  `to_number` char(100) DEFAULT NULL,
  `text` char(200) DEFAULT NULL,
  `time` timestamp NULL DEFAULT CURRENT_TIMESTAMP,
  `price` decimal(15,2) DEFAULT '0.00',
  `description` char(50) DEFAULT NULL,
  `message_id` varchar(50) DEFAULT '0' COMMENT '唯一id',
  `is_click` char(10) DEFAULT '未设置',
  `callback_id` int(11) DEFAULT '0',
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=189438 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `sms_plateform13_all_statistics_by_day`
--

DROP TABLE IF EXISTS `sms_plateform13_all_statistics_by_day`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `sms_plateform13_all_statistics_by_day` (
  `id` int(11) unsigned NOT NULL AUTO_INCREMENT,
  `day` varchar(150) NOT NULL,
  `total_count` varchar(150) DEFAULT '0',
  `success_count` varchar(150) DEFAULT '0',
  `failure_count` varchar(150) DEFAULT '0',
  `price_count` decimal(15,2) DEFAULT '0.00',
  `create_time` timestamp NULL DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`id`),
  UNIQUE KEY `day` (`day`)
) ENGINE=InnoDB AUTO_INCREMENT=203 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `sms_plateform13_channel_statistics_by_day`
--

DROP TABLE IF EXISTS `sms_plateform13_channel_statistics_by_day`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `sms_plateform13_channel_statistics_by_day` (
  `id` int(11) unsigned NOT NULL AUTO_INCREMENT,
  `day` varchar(150) NOT NULL,
  `channel_id` int(11) NOT NULL,
  `total_count` varchar(150) DEFAULT '0',
  `success_count` varchar(150) DEFAULT '0',
  `failure_count` varchar(150) DEFAULT '0',
  `create_time` timestamp NULL DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=48 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `sms_plateform13_failure`
--

DROP TABLE IF EXISTS `sms_plateform13_failure`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `sms_plateform13_failure` (
  `id` int(11) unsigned NOT NULL AUTO_INCREMENT,
  `user` char(11) NOT NULL,
  `user_id` int(11) NOT NULL,
  `channel_id` int(11) NOT NULL,
  `to_number` char(100) DEFAULT NULL,
  `text` char(200) DEFAULT NULL,
  `time` timestamp NULL DEFAULT CURRENT_TIMESTAMP,
  `price` decimal(15,2) DEFAULT '0.00',
  `description` char(50) DEFAULT NULL,
  `message_id` varchar(50) DEFAULT '0' COMMENT '唯一id',
  `is_click` char(10) DEFAULT '未设置',
  `callback_id` int(11) DEFAULT '0',
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=55 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `sms_plateform13_success`
--

DROP TABLE IF EXISTS `sms_plateform13_success`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `sms_plateform13_success` (
  `id` int(11) unsigned NOT NULL AUTO_INCREMENT,
  `user` char(11) NOT NULL,
  `user_id` int(11) NOT NULL,
  `channel_id` int(11) NOT NULL,
  `to_number` char(100) DEFAULT NULL,
  `text` char(200) DEFAULT NULL,
  `time` timestamp NULL DEFAULT CURRENT_TIMESTAMP,
  `price` decimal(15,2) DEFAULT '0.00',
  `description` char(50) DEFAULT NULL,
  `message_id` varchar(50) DEFAULT '0' COMMENT '唯一id',
  `is_click` char(10) DEFAULT '未设置',
  `callback_id` int(11) DEFAULT '0',
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=127 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `sms_plateform14_all_statistics_by_day`
--

DROP TABLE IF EXISTS `sms_plateform14_all_statistics_by_day`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `sms_plateform14_all_statistics_by_day` (
  `id` int(11) unsigned NOT NULL AUTO_INCREMENT,
  `day` varchar(150) NOT NULL,
  `total_count` varchar(150) DEFAULT '0',
  `success_count` varchar(150) DEFAULT '0',
  `failure_count` varchar(150) DEFAULT '0',
  `price_count` decimal(15,2) DEFAULT '0.00',
  `create_time` timestamp NULL DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`id`),
  UNIQUE KEY `day` (`day`)
) ENGINE=InnoDB AUTO_INCREMENT=267 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `sms_plateform14_channel_statistics_by_day`
--

DROP TABLE IF EXISTS `sms_plateform14_channel_statistics_by_day`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `sms_plateform14_channel_statistics_by_day` (
  `id` int(11) unsigned NOT NULL AUTO_INCREMENT,
  `day` varchar(150) NOT NULL,
  `channel_id` int(11) NOT NULL,
  `total_count` varchar(150) DEFAULT '0',
  `success_count` varchar(150) DEFAULT '0',
  `failure_count` varchar(150) DEFAULT '0',
  `create_time` timestamp NULL DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=96 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `sms_plateform14_failure`
--

DROP TABLE IF EXISTS `sms_plateform14_failure`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `sms_plateform14_failure` (
  `id` int(11) unsigned NOT NULL AUTO_INCREMENT,
  `user` char(11) NOT NULL,
  `user_id` int(11) NOT NULL,
  `channel_id` int(11) NOT NULL,
  `to_number` char(100) DEFAULT NULL,
  `text` char(200) DEFAULT NULL,
  `time` timestamp NULL DEFAULT CURRENT_TIMESTAMP,
  `price` decimal(15,2) DEFAULT '0.00',
  `description` char(50) DEFAULT NULL,
  `message_id` varchar(50) DEFAULT '0' COMMENT '唯一id',
  `is_click` char(10) DEFAULT '未设置',
  `callback_id` int(11) DEFAULT '0',
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `sms_plateform14_success`
--

DROP TABLE IF EXISTS `sms_plateform14_success`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `sms_plateform14_success` (
  `id` int(11) unsigned NOT NULL AUTO_INCREMENT,
  `user` char(11) NOT NULL,
  `user_id` int(11) NOT NULL,
  `channel_id` int(11) NOT NULL,
  `to_number` char(100) DEFAULT NULL,
  `text` char(200) DEFAULT NULL,
  `time` timestamp NULL DEFAULT CURRENT_TIMESTAMP,
  `price` decimal(15,2) DEFAULT '0.00',
  `description` char(50) DEFAULT NULL,
  `message_id` varchar(50) DEFAULT '0' COMMENT '唯一id',
  `is_click` char(10) DEFAULT '未设置',
  `callback_id` int(11) DEFAULT '0',
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=3026 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `sms_plateform15_all_statistics_by_day`
--

DROP TABLE IF EXISTS `sms_plateform15_all_statistics_by_day`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `sms_plateform15_all_statistics_by_day` (
  `id` int(11) unsigned NOT NULL AUTO_INCREMENT,
  `day` varchar(150) NOT NULL,
  `total_count` varchar(150) DEFAULT '0',
  `success_count` varchar(150) DEFAULT '0',
  `failure_count` varchar(150) DEFAULT '0',
  `price_count` decimal(15,2) DEFAULT '0.00',
  `create_time` timestamp NULL DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`id`),
  UNIQUE KEY `day` (`day`)
) ENGINE=InnoDB AUTO_INCREMENT=266 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `sms_plateform15_channel_statistics_by_day`
--

DROP TABLE IF EXISTS `sms_plateform15_channel_statistics_by_day`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `sms_plateform15_channel_statistics_by_day` (
  `id` int(11) unsigned NOT NULL AUTO_INCREMENT,
  `day` varchar(150) NOT NULL,
  `channel_id` int(11) NOT NULL,
  `total_count` varchar(150) DEFAULT '0',
  `success_count` varchar(150) DEFAULT '0',
  `failure_count` varchar(150) DEFAULT '0',
  `create_time` timestamp NULL DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=96 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `sms_plateform15_failure`
--

DROP TABLE IF EXISTS `sms_plateform15_failure`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `sms_plateform15_failure` (
  `id` int(11) unsigned NOT NULL AUTO_INCREMENT,
  `user` char(11) NOT NULL,
  `user_id` int(11) NOT NULL,
  `channel_id` int(11) NOT NULL,
  `to_number` char(100) DEFAULT NULL,
  `text` char(200) DEFAULT NULL,
  `time` timestamp NULL DEFAULT CURRENT_TIMESTAMP,
  `price` decimal(15,2) DEFAULT '0.00',
  `description` char(50) DEFAULT NULL,
  `message_id` varchar(50) DEFAULT '0' COMMENT '唯一id',
  `is_click` char(10) DEFAULT '未设置',
  `callback_id` int(11) DEFAULT '0',
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=2095 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `sms_plateform15_success`
--

DROP TABLE IF EXISTS `sms_plateform15_success`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `sms_plateform15_success` (
  `id` int(11) unsigned NOT NULL AUTO_INCREMENT,
  `user` char(11) NOT NULL,
  `user_id` int(11) NOT NULL,
  `channel_id` int(11) NOT NULL,
  `to_number` char(100) DEFAULT NULL,
  `text` char(200) DEFAULT NULL,
  `time` timestamp NULL DEFAULT CURRENT_TIMESTAMP,
  `price` decimal(15,2) DEFAULT '0.00',
  `description` char(50) DEFAULT NULL,
  `message_id` varchar(50) DEFAULT '0' COMMENT '唯一id',
  `is_click` char(10) DEFAULT '未设置',
  `callback_id` int(11) DEFAULT '0',
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=43441 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `sms_plateform16_all_statistics_by_day`
--

DROP TABLE IF EXISTS `sms_plateform16_all_statistics_by_day`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `sms_plateform16_all_statistics_by_day` (
  `id` int(11) unsigned NOT NULL AUTO_INCREMENT,
  `day` varchar(150) NOT NULL,
  `total_count` varchar(150) DEFAULT '0',
  `success_count` varchar(150) DEFAULT '0',
  `failure_count` varchar(150) DEFAULT '0',
  `price_count` decimal(15,2) DEFAULT '0.00',
  `create_time` timestamp NULL DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`id`),
  UNIQUE KEY `day` (`day`)
) ENGINE=InnoDB AUTO_INCREMENT=633 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `sms_plateform16_channel_statistics_by_day`
--

DROP TABLE IF EXISTS `sms_plateform16_channel_statistics_by_day`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `sms_plateform16_channel_statistics_by_day` (
  `id` int(11) unsigned NOT NULL AUTO_INCREMENT,
  `day` varchar(150) NOT NULL,
  `channel_id` int(11) NOT NULL,
  `total_count` varchar(150) DEFAULT '0',
  `success_count` varchar(150) DEFAULT '0',
  `failure_count` varchar(150) DEFAULT '0',
  `create_time` timestamp NULL DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=267 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `sms_plateform16_failure`
--

DROP TABLE IF EXISTS `sms_plateform16_failure`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `sms_plateform16_failure` (
  `id` int(11) unsigned NOT NULL AUTO_INCREMENT,
  `user` char(11) NOT NULL,
  `user_id` int(11) NOT NULL,
  `channel_id` int(11) NOT NULL,
  `to_number` char(100) DEFAULT NULL,
  `text` char(200) DEFAULT NULL,
  `time` timestamp NULL DEFAULT CURRENT_TIMESTAMP,
  `price` decimal(15,2) DEFAULT '0.00',
  `description` char(50) DEFAULT NULL,
  `message_id` varchar(50) DEFAULT '0' COMMENT '唯一id',
  `is_click` char(10) DEFAULT '未设置',
  `callback_id` int(11) DEFAULT '0',
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=38324 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `sms_plateform16_success`
--

DROP TABLE IF EXISTS `sms_plateform16_success`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `sms_plateform16_success` (
  `id` int(11) unsigned NOT NULL AUTO_INCREMENT,
  `user` char(11) NOT NULL,
  `user_id` int(11) NOT NULL,
  `channel_id` int(11) NOT NULL,
  `to_number` char(100) DEFAULT NULL,
  `text` char(200) DEFAULT NULL,
  `time` timestamp NULL DEFAULT CURRENT_TIMESTAMP,
  `price` decimal(15,2) DEFAULT '0.00',
  `description` char(50) DEFAULT NULL,
  `message_id` varchar(50) DEFAULT '0' COMMENT '唯一id',
  `is_click` char(10) DEFAULT '未设置',
  `callback_id` int(11) DEFAULT '0',
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=1657754 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `sms_plateform17_all_statistics_by_day`
--

DROP TABLE IF EXISTS `sms_plateform17_all_statistics_by_day`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `sms_plateform17_all_statistics_by_day` (
  `id` int(11) unsigned NOT NULL AUTO_INCREMENT,
  `day` varchar(150) NOT NULL,
  `total_count` varchar(150) DEFAULT '0',
  `success_count` varchar(150) DEFAULT '0',
  `failure_count` varchar(150) DEFAULT '0',
  `price_count` decimal(15,2) DEFAULT '0.00',
  `create_time` timestamp NULL DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`id`),
  UNIQUE KEY `day` (`day`)
) ENGINE=InnoDB AUTO_INCREMENT=378 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `sms_plateform17_channel_statistics_by_day`
--

DROP TABLE IF EXISTS `sms_plateform17_channel_statistics_by_day`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `sms_plateform17_channel_statistics_by_day` (
  `id` int(11) unsigned NOT NULL AUTO_INCREMENT,
  `day` varchar(150) NOT NULL,
  `channel_id` int(11) NOT NULL,
  `total_count` varchar(150) DEFAULT '0',
  `success_count` varchar(150) DEFAULT '0',
  `failure_count` varchar(150) DEFAULT '0',
  `create_time` timestamp NULL DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=206 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `sms_plateform17_failure`
--

DROP TABLE IF EXISTS `sms_plateform17_failure`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `sms_plateform17_failure` (
  `id` int(11) unsigned NOT NULL AUTO_INCREMENT,
  `user` char(11) NOT NULL,
  `user_id` int(11) NOT NULL,
  `channel_id` int(11) NOT NULL,
  `to_number` char(100) DEFAULT NULL,
  `text` char(200) DEFAULT NULL,
  `time` timestamp NULL DEFAULT CURRENT_TIMESTAMP,
  `price` decimal(15,2) DEFAULT '0.00',
  `description` char(50) DEFAULT NULL,
  `message_id` varchar(50) DEFAULT '0' COMMENT '唯一id',
  `is_click` char(10) DEFAULT '未设置',
  `callback_id` int(11) DEFAULT '0',
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=23305 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `sms_plateform17_success`
--

DROP TABLE IF EXISTS `sms_plateform17_success`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `sms_plateform17_success` (
  `id` int(11) unsigned NOT NULL AUTO_INCREMENT,
  `user` char(11) NOT NULL,
  `user_id` int(11) NOT NULL,
  `channel_id` int(11) NOT NULL,
  `to_number` char(100) DEFAULT NULL,
  `text` char(200) DEFAULT NULL,
  `time` timestamp NULL DEFAULT CURRENT_TIMESTAMP,
  `price` decimal(15,2) DEFAULT '0.00',
  `description` char(50) DEFAULT NULL,
  `message_id` varchar(50) DEFAULT '0' COMMENT '唯一id',
  `is_click` char(10) DEFAULT '未设置',
  `callback_id` int(11) DEFAULT '0',
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=1275559 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `sms_plateform18_all_statistics_by_day`
--

DROP TABLE IF EXISTS `sms_plateform18_all_statistics_by_day`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `sms_plateform18_all_statistics_by_day` (
  `id` int(11) unsigned NOT NULL AUTO_INCREMENT,
  `day` varchar(150) NOT NULL,
  `total_count` varchar(150) DEFAULT '0',
  `success_count` varchar(150) DEFAULT '0',
  `failure_count` varchar(150) DEFAULT '0',
  `price_count` decimal(15,2) DEFAULT '0.00',
  `create_time` timestamp NULL DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`id`),
  UNIQUE KEY `day` (`day`)
) ENGINE=InnoDB AUTO_INCREMENT=253 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `sms_plateform18_channel_statistics_by_day`
--

DROP TABLE IF EXISTS `sms_plateform18_channel_statistics_by_day`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `sms_plateform18_channel_statistics_by_day` (
  `id` int(11) unsigned NOT NULL AUTO_INCREMENT,
  `day` varchar(150) NOT NULL,
  `channel_id` int(11) NOT NULL,
  `total_count` varchar(150) DEFAULT '0',
  `success_count` varchar(150) DEFAULT '0',
  `failure_count` varchar(150) DEFAULT '0',
  `create_time` timestamp NULL DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=120 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `sms_plateform18_failure`
--

DROP TABLE IF EXISTS `sms_plateform18_failure`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `sms_plateform18_failure` (
  `id` int(11) unsigned NOT NULL AUTO_INCREMENT,
  `user` char(11) NOT NULL,
  `user_id` int(11) NOT NULL,
  `channel_id` int(11) NOT NULL,
  `to_number` char(100) DEFAULT NULL,
  `text` char(200) DEFAULT NULL,
  `time` timestamp NULL DEFAULT CURRENT_TIMESTAMP,
  `price` decimal(15,2) DEFAULT '0.00',
  `description` char(50) DEFAULT NULL,
  `message_id` varchar(50) DEFAULT '0' COMMENT '唯一id',
  `is_click` char(10) DEFAULT '未设置',
  `callback_id` int(11) DEFAULT '0',
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=70165 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `sms_plateform18_success`
--

DROP TABLE IF EXISTS `sms_plateform18_success`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `sms_plateform18_success` (
  `id` int(11) unsigned NOT NULL AUTO_INCREMENT,
  `user` char(11) NOT NULL,
  `user_id` int(11) NOT NULL,
  `channel_id` int(11) NOT NULL,
  `to_number` char(100) DEFAULT NULL,
  `text` char(200) DEFAULT NULL,
  `time` timestamp NULL DEFAULT CURRENT_TIMESTAMP,
  `price` decimal(15,2) DEFAULT '0.00',
  `description` char(50) DEFAULT NULL,
  `message_id` varchar(50) DEFAULT '0' COMMENT '唯一id',
  `is_click` char(10) DEFAULT '未设置',
  `callback_id` int(11) DEFAULT '0',
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=1263195 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `sms_plateform19_all_statistics_by_day`
--

DROP TABLE IF EXISTS `sms_plateform19_all_statistics_by_day`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `sms_plateform19_all_statistics_by_day` (
  `id` int(11) unsigned NOT NULL AUTO_INCREMENT,
  `day` varchar(150) NOT NULL,
  `total_count` varchar(150) DEFAULT '0',
  `success_count` varchar(150) DEFAULT '0',
  `failure_count` varchar(150) DEFAULT '0',
  `price_count` decimal(15,2) DEFAULT '0.00',
  `create_time` timestamp NULL DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`id`),
  UNIQUE KEY `day` (`day`)
) ENGINE=InnoDB AUTO_INCREMENT=203 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `sms_plateform19_channel_statistics_by_day`
--

DROP TABLE IF EXISTS `sms_plateform19_channel_statistics_by_day`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `sms_plateform19_channel_statistics_by_day` (
  `id` int(11) unsigned NOT NULL AUTO_INCREMENT,
  `day` varchar(150) NOT NULL,
  `channel_id` int(11) NOT NULL,
  `total_count` varchar(150) DEFAULT '0',
  `success_count` varchar(150) DEFAULT '0',
  `failure_count` varchar(150) DEFAULT '0',
  `create_time` timestamp NULL DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=202 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `sms_plateform19_failure`
--

DROP TABLE IF EXISTS `sms_plateform19_failure`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `sms_plateform19_failure` (
  `id` int(11) unsigned NOT NULL AUTO_INCREMENT,
  `user` char(11) NOT NULL,
  `user_id` int(11) NOT NULL,
  `channel_id` int(11) NOT NULL,
  `to_number` char(100) DEFAULT NULL,
  `text` char(200) DEFAULT NULL,
  `time` timestamp NULL DEFAULT CURRENT_TIMESTAMP,
  `price` decimal(15,2) DEFAULT '0.00',
  `description` char(50) DEFAULT NULL,
  `message_id` varchar(50) DEFAULT '0' COMMENT '唯一id',
  `is_click` char(10) DEFAULT '未设置',
  `callback_id` int(11) DEFAULT '0',
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=377 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `sms_plateform19_success`
--

DROP TABLE IF EXISTS `sms_plateform19_success`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `sms_plateform19_success` (
  `id` int(11) unsigned NOT NULL AUTO_INCREMENT,
  `user` char(11) NOT NULL,
  `user_id` int(11) NOT NULL,
  `channel_id` int(11) NOT NULL,
  `to_number` char(100) DEFAULT NULL,
  `text` char(200) DEFAULT NULL,
  `time` timestamp NULL DEFAULT CURRENT_TIMESTAMP,
  `price` decimal(15,2) DEFAULT '0.00',
  `description` char(50) DEFAULT NULL,
  `message_id` varchar(50) DEFAULT '0' COMMENT '唯一id',
  `is_click` char(10) DEFAULT '未设置',
  `callback_id` int(11) DEFAULT '0',
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=52764 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `sms_plateform20_all_statistics_by_day`
--

DROP TABLE IF EXISTS `sms_plateform20_all_statistics_by_day`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `sms_plateform20_all_statistics_by_day` (
  `id` int(11) unsigned NOT NULL AUTO_INCREMENT,
  `day` varchar(150) NOT NULL,
  `total_count` varchar(150) DEFAULT '0',
  `success_count` varchar(150) DEFAULT '0',
  `failure_count` varchar(150) DEFAULT '0',
  `price_count` decimal(15,2) DEFAULT '0.00',
  `create_time` timestamp NULL DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`id`),
  UNIQUE KEY `day` (`day`)
) ENGINE=InnoDB AUTO_INCREMENT=138 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `sms_plateform20_channel_statistics_by_day`
--

DROP TABLE IF EXISTS `sms_plateform20_channel_statistics_by_day`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `sms_plateform20_channel_statistics_by_day` (
  `id` int(11) unsigned NOT NULL AUTO_INCREMENT,
  `day` varchar(150) NOT NULL,
  `channel_id` int(11) NOT NULL,
  `total_count` varchar(150) DEFAULT '0',
  `success_count` varchar(150) DEFAULT '0',
  `failure_count` varchar(150) DEFAULT '0',
  `create_time` timestamp NULL DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=138 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `sms_plateform20_failure`
--

DROP TABLE IF EXISTS `sms_plateform20_failure`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `sms_plateform20_failure` (
  `id` int(11) unsigned NOT NULL AUTO_INCREMENT,
  `user` char(11) NOT NULL,
  `user_id` int(11) NOT NULL,
  `channel_id` int(11) NOT NULL,
  `to_number` char(100) DEFAULT NULL,
  `text` char(200) DEFAULT NULL,
  `time` timestamp NULL DEFAULT CURRENT_TIMESTAMP,
  `price` decimal(15,2) DEFAULT '0.00',
  `description` char(50) DEFAULT NULL,
  `message_id` varchar(50) DEFAULT '0' COMMENT '唯一id',
  `is_click` char(10) DEFAULT '未设置',
  `callback_id` int(11) DEFAULT '0',
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=17724 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `sms_plateform20_success`
--

DROP TABLE IF EXISTS `sms_plateform20_success`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `sms_plateform20_success` (
  `id` int(11) unsigned NOT NULL AUTO_INCREMENT,
  `user` char(11) NOT NULL,
  `user_id` int(11) NOT NULL,
  `channel_id` int(11) NOT NULL,
  `to_number` char(100) DEFAULT NULL,
  `text` char(200) DEFAULT NULL,
  `time` timestamp NULL DEFAULT CURRENT_TIMESTAMP,
  `price` decimal(15,2) DEFAULT '0.00',
  `description` char(50) DEFAULT NULL,
  `message_id` varchar(50) DEFAULT '0' COMMENT '唯一id',
  `is_click` char(10) DEFAULT '未设置',
  `callback_id` int(11) DEFAULT '0',
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=1424863 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `sms_plateform21_all_statistics_by_day`
--

DROP TABLE IF EXISTS `sms_plateform21_all_statistics_by_day`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `sms_plateform21_all_statistics_by_day` (
  `id` int(11) unsigned NOT NULL AUTO_INCREMENT,
  `day` varchar(150) NOT NULL,
  `total_count` varchar(150) DEFAULT '0',
  `success_count` varchar(150) DEFAULT '0',
  `failure_count` varchar(150) DEFAULT '0',
  `price_count` decimal(15,2) DEFAULT '0.00',
  `create_time` timestamp NULL DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`id`),
  UNIQUE KEY `day` (`day`)
) ENGINE=InnoDB AUTO_INCREMENT=96 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `sms_plateform21_channel_statistics_by_day`
--

DROP TABLE IF EXISTS `sms_plateform21_channel_statistics_by_day`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `sms_plateform21_channel_statistics_by_day` (
  `id` int(11) unsigned NOT NULL AUTO_INCREMENT,
  `day` varchar(150) NOT NULL,
  `channel_id` int(11) NOT NULL,
  `total_count` varchar(150) DEFAULT '0',
  `success_count` varchar(150) DEFAULT '0',
  `failure_count` varchar(150) DEFAULT '0',
  `create_time` timestamp NULL DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=70 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `sms_plateform21_failure`
--

DROP TABLE IF EXISTS `sms_plateform21_failure`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `sms_plateform21_failure` (
  `id` int(11) unsigned NOT NULL AUTO_INCREMENT,
  `user` char(11) NOT NULL,
  `user_id` int(11) NOT NULL,
  `channel_id` int(11) NOT NULL,
  `to_number` char(100) DEFAULT NULL,
  `text` char(200) DEFAULT NULL,
  `time` timestamp NULL DEFAULT CURRENT_TIMESTAMP,
  `price` decimal(15,2) DEFAULT '0.00',
  `description` char(50) DEFAULT NULL,
  `message_id` varchar(50) DEFAULT '0' COMMENT '唯一id',
  `is_click` char(10) DEFAULT '未设置',
  `callback_id` int(11) DEFAULT '0',
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=61 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `sms_plateform21_success`
--

DROP TABLE IF EXISTS `sms_plateform21_success`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `sms_plateform21_success` (
  `id` int(11) unsigned NOT NULL AUTO_INCREMENT,
  `user` char(11) NOT NULL,
  `user_id` int(11) NOT NULL,
  `channel_id` int(11) NOT NULL,
  `to_number` char(100) DEFAULT NULL,
  `text` char(200) DEFAULT NULL,
  `time` timestamp NULL DEFAULT CURRENT_TIMESTAMP,
  `price` decimal(15,2) DEFAULT '0.00',
  `description` char(50) DEFAULT NULL,
  `message_id` varchar(50) DEFAULT '0' COMMENT '唯一id',
  `is_click` char(10) DEFAULT '未设置',
  `callback_id` int(11) DEFAULT '0',
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=2145 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `sms_plateform2_all_statistics_by_day`
--

DROP TABLE IF EXISTS `sms_plateform2_all_statistics_by_day`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `sms_plateform2_all_statistics_by_day` (
  `id` int(11) unsigned NOT NULL AUTO_INCREMENT,
  `day` varchar(150) NOT NULL,
  `total_count` varchar(150) DEFAULT '0',
  `success_count` varchar(150) DEFAULT '0',
  `failure_count` varchar(150) DEFAULT '0',
  `price_count` decimal(15,2) DEFAULT '0.00',
  `create_time` timestamp NULL DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`id`),
  UNIQUE KEY `day` (`day`)
) ENGINE=InnoDB AUTO_INCREMENT=277 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `sms_plateform2_channel_statistics_by_day`
--

DROP TABLE IF EXISTS `sms_plateform2_channel_statistics_by_day`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `sms_plateform2_channel_statistics_by_day` (
  `id` int(11) unsigned NOT NULL AUTO_INCREMENT,
  `day` varchar(150) NOT NULL,
  `channel_id` int(11) NOT NULL,
  `total_count` varchar(150) DEFAULT '0',
  `success_count` varchar(150) DEFAULT '0',
  `failure_count` varchar(150) DEFAULT '0',
  `create_time` timestamp NULL DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=738 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `sms_plateform2_failure`
--

DROP TABLE IF EXISTS `sms_plateform2_failure`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `sms_plateform2_failure` (
  `id` int(11) unsigned NOT NULL AUTO_INCREMENT,
  `user` char(11) NOT NULL,
  `user_id` int(11) NOT NULL,
  `channel_id` int(11) NOT NULL,
  `to_number` char(100) DEFAULT NULL,
  `text` char(200) DEFAULT NULL,
  `time` timestamp NULL DEFAULT CURRENT_TIMESTAMP,
  `price` decimal(15,2) DEFAULT '0.00',
  `description` char(50) DEFAULT NULL,
  `message_id` varchar(50) DEFAULT '0' COMMENT '唯一id',
  `is_click` char(10) DEFAULT '未设置',
  `callback_id` int(11) DEFAULT '0',
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=39939 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `sms_plateform2_success`
--

DROP TABLE IF EXISTS `sms_plateform2_success`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `sms_plateform2_success` (
  `id` int(11) unsigned NOT NULL AUTO_INCREMENT,
  `user` char(11) NOT NULL,
  `user_id` int(11) NOT NULL,
  `channel_id` int(11) NOT NULL,
  `to_number` char(100) DEFAULT NULL,
  `text` char(200) DEFAULT NULL,
  `time` timestamp NULL DEFAULT CURRENT_TIMESTAMP,
  `price` decimal(15,2) DEFAULT '0.00',
  `description` char(50) DEFAULT NULL,
  `message_id` varchar(50) DEFAULT '0' COMMENT '唯一id',
  `is_click` char(10) DEFAULT '未设置',
  `callback_id` int(11) DEFAULT '0',
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=1532838 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `sms_plateform3_all_statistics_by_day`
--

DROP TABLE IF EXISTS `sms_plateform3_all_statistics_by_day`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `sms_plateform3_all_statistics_by_day` (
  `id` int(11) unsigned NOT NULL AUTO_INCREMENT,
  `day` varchar(150) NOT NULL,
  `total_count` varchar(150) DEFAULT '0',
  `success_count` varchar(150) DEFAULT '0',
  `failure_count` varchar(150) DEFAULT '0',
  `price_count` decimal(15,2) DEFAULT '0.00',
  `create_time` timestamp NULL DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`id`),
  UNIQUE KEY `day` (`day`)
) ENGINE=InnoDB AUTO_INCREMENT=276 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `sms_plateform3_channel_statistics_by_day`
--

DROP TABLE IF EXISTS `sms_plateform3_channel_statistics_by_day`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `sms_plateform3_channel_statistics_by_day` (
  `id` int(11) unsigned NOT NULL AUTO_INCREMENT,
  `day` varchar(150) NOT NULL,
  `channel_id` int(11) NOT NULL,
  `total_count` varchar(150) DEFAULT '0',
  `success_count` varchar(150) DEFAULT '0',
  `failure_count` varchar(150) DEFAULT '0',
  `create_time` timestamp NULL DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=606 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `sms_plateform3_failure`
--

DROP TABLE IF EXISTS `sms_plateform3_failure`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `sms_plateform3_failure` (
  `id` int(11) unsigned NOT NULL AUTO_INCREMENT,
  `user` char(11) NOT NULL,
  `user_id` int(11) NOT NULL,
  `channel_id` int(11) NOT NULL,
  `to_number` char(100) DEFAULT NULL,
  `text` char(200) DEFAULT NULL,
  `time` timestamp NULL DEFAULT CURRENT_TIMESTAMP,
  `price` decimal(15,2) DEFAULT '0.00',
  `description` char(50) DEFAULT NULL,
  `message_id` varchar(50) DEFAULT '0' COMMENT '唯一id',
  `is_click` char(10) DEFAULT '未设置',
  `callback_id` int(11) DEFAULT '0',
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=12450 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `sms_plateform3_success`
--

DROP TABLE IF EXISTS `sms_plateform3_success`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `sms_plateform3_success` (
  `id` int(11) unsigned NOT NULL AUTO_INCREMENT,
  `user` char(11) NOT NULL,
  `user_id` int(11) NOT NULL,
  `channel_id` int(11) NOT NULL,
  `to_number` char(100) DEFAULT NULL,
  `text` char(200) DEFAULT NULL,
  `time` timestamp NULL DEFAULT CURRENT_TIMESTAMP,
  `price` decimal(15,2) DEFAULT '0.00',
  `description` char(50) DEFAULT NULL,
  `message_id` varchar(50) DEFAULT '0' COMMENT '唯一id',
  `is_click` char(10) DEFAULT '未设置',
  `callback_id` int(11) DEFAULT '0',
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=743388 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `sms_plateform4_all_statistics_by_day`
--

DROP TABLE IF EXISTS `sms_plateform4_all_statistics_by_day`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `sms_plateform4_all_statistics_by_day` (
  `id` int(11) unsigned NOT NULL AUTO_INCREMENT,
  `day` varchar(150) NOT NULL,
  `total_count` varchar(150) DEFAULT '0',
  `success_count` varchar(150) DEFAULT '0',
  `failure_count` varchar(150) DEFAULT '0',
  `price_count` decimal(15,2) DEFAULT '0.00',
  `create_time` timestamp NULL DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`id`),
  UNIQUE KEY `day` (`day`)
) ENGINE=InnoDB AUTO_INCREMENT=293 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `sms_plateform4_channel_statistics_by_day`
--

DROP TABLE IF EXISTS `sms_plateform4_channel_statistics_by_day`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `sms_plateform4_channel_statistics_by_day` (
  `id` int(11) unsigned NOT NULL AUTO_INCREMENT,
  `day` varchar(150) NOT NULL,
  `channel_id` int(11) NOT NULL,
  `total_count` varchar(150) DEFAULT '0',
  `success_count` varchar(150) DEFAULT '0',
  `failure_count` varchar(150) DEFAULT '0',
  `create_time` timestamp NULL DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=411 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `sms_plateform4_failure`
--

DROP TABLE IF EXISTS `sms_plateform4_failure`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `sms_plateform4_failure` (
  `id` int(11) unsigned NOT NULL AUTO_INCREMENT,
  `user` char(11) NOT NULL,
  `user_id` int(11) NOT NULL,
  `channel_id` int(11) NOT NULL,
  `to_number` char(100) DEFAULT NULL,
  `text` char(200) DEFAULT NULL,
  `time` timestamp NULL DEFAULT CURRENT_TIMESTAMP,
  `price` decimal(15,2) DEFAULT '0.00',
  `description` char(50) DEFAULT NULL,
  `message_id` varchar(50) DEFAULT '0' COMMENT '唯一id',
  `is_click` char(10) DEFAULT '未设置',
  `callback_id` int(11) DEFAULT '0',
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=129126 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `sms_plateform4_success`
--

DROP TABLE IF EXISTS `sms_plateform4_success`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `sms_plateform4_success` (
  `id` int(11) unsigned NOT NULL AUTO_INCREMENT,
  `user` char(11) NOT NULL,
  `user_id` int(11) NOT NULL,
  `channel_id` int(11) NOT NULL,
  `to_number` char(100) DEFAULT NULL,
  `text` char(200) DEFAULT NULL,
  `time` timestamp NULL DEFAULT CURRENT_TIMESTAMP,
  `price` decimal(15,2) DEFAULT '0.00',
  `description` char(50) DEFAULT NULL,
  `message_id` varchar(50) DEFAULT '0' COMMENT '唯一id',
  `is_click` char(10) DEFAULT '未设置',
  `callback_id` int(11) DEFAULT '0',
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=1451492 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `sms_plateform5_all_statistics_by_day`
--

DROP TABLE IF EXISTS `sms_plateform5_all_statistics_by_day`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `sms_plateform5_all_statistics_by_day` (
  `id` int(11) unsigned NOT NULL AUTO_INCREMENT,
  `day` varchar(150) NOT NULL,
  `total_count` varchar(150) DEFAULT '0',
  `success_count` varchar(150) DEFAULT '0',
  `failure_count` varchar(150) DEFAULT '0',
  `price_count` decimal(15,2) DEFAULT '0.00',
  `create_time` timestamp NULL DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`id`),
  UNIQUE KEY `day` (`day`)
) ENGINE=InnoDB AUTO_INCREMENT=382 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `sms_plateform5_channel_statistics_by_day`
--

DROP TABLE IF EXISTS `sms_plateform5_channel_statistics_by_day`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `sms_plateform5_channel_statistics_by_day` (
  `id` int(11) unsigned NOT NULL AUTO_INCREMENT,
  `day` varchar(150) NOT NULL,
  `channel_id` int(11) NOT NULL,
  `total_count` varchar(150) DEFAULT '0',
  `success_count` varchar(150) DEFAULT '0',
  `failure_count` varchar(150) DEFAULT '0',
  `create_time` timestamp NULL DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=275 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `sms_plateform5_failure`
--

DROP TABLE IF EXISTS `sms_plateform5_failure`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `sms_plateform5_failure` (
  `id` int(11) unsigned NOT NULL AUTO_INCREMENT,
  `user` char(11) NOT NULL,
  `user_id` int(11) NOT NULL,
  `channel_id` int(11) NOT NULL,
  `to_number` char(100) DEFAULT NULL,
  `text` char(200) DEFAULT NULL,
  `time` timestamp NULL DEFAULT CURRENT_TIMESTAMP,
  `price` decimal(15,2) DEFAULT '0.00',
  `description` char(50) DEFAULT NULL,
  `message_id` varchar(50) DEFAULT '0' COMMENT '唯一id',
  `is_click` char(10) DEFAULT '未设置',
  `callback_id` int(11) DEFAULT '0',
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=8591 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `sms_plateform5_success`
--

DROP TABLE IF EXISTS `sms_plateform5_success`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `sms_plateform5_success` (
  `id` int(11) unsigned NOT NULL AUTO_INCREMENT,
  `user` char(11) NOT NULL,
  `user_id` int(11) NOT NULL,
  `channel_id` int(11) NOT NULL,
  `to_number` char(100) DEFAULT NULL,
  `text` char(200) DEFAULT NULL,
  `time` timestamp NULL DEFAULT CURRENT_TIMESTAMP,
  `price` decimal(15,2) DEFAULT '0.00',
  `description` char(50) DEFAULT NULL,
  `message_id` varchar(50) DEFAULT '0' COMMENT '唯一id',
  `is_click` char(10) DEFAULT '未设置',
  `callback_id` int(11) DEFAULT '0',
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=590937 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `sms_plateform6_all_statistics_by_day`
--

DROP TABLE IF EXISTS `sms_plateform6_all_statistics_by_day`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `sms_plateform6_all_statistics_by_day` (
  `id` int(11) unsigned NOT NULL AUTO_INCREMENT,
  `day` varchar(150) NOT NULL,
  `total_count` varchar(150) DEFAULT '0',
  `success_count` varchar(150) DEFAULT '0',
  `failure_count` varchar(150) DEFAULT '0',
  `price_count` decimal(15,2) DEFAULT '0.00',
  `create_time` timestamp NULL DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`id`),
  UNIQUE KEY `day` (`day`)
) ENGINE=InnoDB AUTO_INCREMENT=276 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `sms_plateform6_channel_statistics_by_day`
--

DROP TABLE IF EXISTS `sms_plateform6_channel_statistics_by_day`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `sms_plateform6_channel_statistics_by_day` (
  `id` int(11) unsigned NOT NULL AUTO_INCREMENT,
  `day` varchar(150) NOT NULL,
  `channel_id` int(11) NOT NULL,
  `total_count` varchar(150) DEFAULT '0',
  `success_count` varchar(150) DEFAULT '0',
  `failure_count` varchar(150) DEFAULT '0',
  `create_time` timestamp NULL DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=274 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `sms_plateform6_failure`
--

DROP TABLE IF EXISTS `sms_plateform6_failure`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `sms_plateform6_failure` (
  `id` int(11) unsigned NOT NULL AUTO_INCREMENT,
  `user` char(11) NOT NULL,
  `user_id` int(11) NOT NULL,
  `channel_id` int(11) NOT NULL,
  `to_number` char(100) DEFAULT NULL,
  `text` char(200) DEFAULT NULL,
  `time` timestamp NULL DEFAULT CURRENT_TIMESTAMP,
  `price` decimal(15,2) DEFAULT '0.00',
  `description` char(50) DEFAULT NULL,
  `message_id` varchar(50) DEFAULT '0' COMMENT '唯一id',
  `is_click` char(10) DEFAULT '未设置',
  `callback_id` int(11) DEFAULT '0',
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=9074 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `sms_plateform6_success`
--

DROP TABLE IF EXISTS `sms_plateform6_success`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `sms_plateform6_success` (
  `id` int(11) unsigned NOT NULL AUTO_INCREMENT,
  `user` char(11) NOT NULL,
  `user_id` int(11) NOT NULL,
  `channel_id` int(11) NOT NULL,
  `to_number` char(100) DEFAULT NULL,
  `text` char(200) DEFAULT NULL,
  `time` timestamp NULL DEFAULT CURRENT_TIMESTAMP,
  `price` decimal(15,2) DEFAULT '0.00',
  `description` char(50) DEFAULT NULL,
  `message_id` varchar(50) DEFAULT '0' COMMENT '唯一id',
  `is_click` char(10) DEFAULT '未设置',
  `callback_id` int(11) DEFAULT '0',
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=267503 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `sms_plateform7_all_statistics_by_day`
--

DROP TABLE IF EXISTS `sms_plateform7_all_statistics_by_day`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `sms_plateform7_all_statistics_by_day` (
  `id` int(11) unsigned NOT NULL AUTO_INCREMENT,
  `day` varchar(150) NOT NULL,
  `total_count` varchar(150) DEFAULT '0',
  `success_count` varchar(150) DEFAULT '0',
  `failure_count` varchar(150) DEFAULT '0',
  `price_count` decimal(15,2) DEFAULT '0.00',
  `create_time` timestamp NULL DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`id`),
  UNIQUE KEY `day` (`day`)
) ENGINE=InnoDB AUTO_INCREMENT=440 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `sms_plateform7_channel_statistics_by_day`
--

DROP TABLE IF EXISTS `sms_plateform7_channel_statistics_by_day`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `sms_plateform7_channel_statistics_by_day` (
  `id` int(11) unsigned NOT NULL AUTO_INCREMENT,
  `day` varchar(150) NOT NULL,
  `channel_id` int(11) NOT NULL,
  `total_count` varchar(150) DEFAULT '0',
  `success_count` varchar(150) DEFAULT '0',
  `failure_count` varchar(150) DEFAULT '0',
  `create_time` timestamp NULL DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=272 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `sms_plateform7_failure`
--

DROP TABLE IF EXISTS `sms_plateform7_failure`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `sms_plateform7_failure` (
  `id` int(11) unsigned NOT NULL AUTO_INCREMENT,
  `user` char(11) NOT NULL,
  `user_id` int(11) NOT NULL,
  `channel_id` int(11) NOT NULL,
  `to_number` char(100) DEFAULT NULL,
  `text` char(200) DEFAULT NULL,
  `time` timestamp NULL DEFAULT CURRENT_TIMESTAMP,
  `price` decimal(15,2) DEFAULT '0.00',
  `description` char(50) DEFAULT NULL,
  `message_id` varchar(50) DEFAULT '0' COMMENT '唯一id',
  `is_click` char(10) DEFAULT '未设置',
  `callback_id` int(11) DEFAULT '0',
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=51726 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `sms_plateform7_success`
--

DROP TABLE IF EXISTS `sms_plateform7_success`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `sms_plateform7_success` (
  `id` int(11) unsigned NOT NULL AUTO_INCREMENT,
  `user` char(11) NOT NULL,
  `user_id` int(11) NOT NULL,
  `channel_id` int(11) NOT NULL,
  `to_number` char(100) DEFAULT NULL,
  `text` char(200) DEFAULT NULL,
  `time` timestamp NULL DEFAULT CURRENT_TIMESTAMP,
  `price` decimal(15,2) DEFAULT '0.00',
  `description` char(50) DEFAULT NULL,
  `message_id` varchar(50) DEFAULT '0' COMMENT '唯一id',
  `is_click` char(10) DEFAULT '未设置',
  `callback_id` int(11) DEFAULT '0',
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=1312202 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `sms_plateform8_all_statistics_by_day`
--

DROP TABLE IF EXISTS `sms_plateform8_all_statistics_by_day`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `sms_plateform8_all_statistics_by_day` (
  `id` int(11) unsigned NOT NULL AUTO_INCREMENT,
  `day` varchar(150) NOT NULL,
  `total_count` varchar(150) DEFAULT '0',
  `success_count` varchar(150) DEFAULT '0',
  `failure_count` varchar(150) DEFAULT '0',
  `price_count` decimal(15,2) DEFAULT '0.00',
  `create_time` timestamp NULL DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`id`),
  UNIQUE KEY `day` (`day`)
) ENGINE=InnoDB AUTO_INCREMENT=276 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `sms_plateform8_channel_statistics_by_day`
--

DROP TABLE IF EXISTS `sms_plateform8_channel_statistics_by_day`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `sms_plateform8_channel_statistics_by_day` (
  `id` int(11) unsigned NOT NULL AUTO_INCREMENT,
  `day` varchar(150) NOT NULL,
  `channel_id` int(11) NOT NULL,
  `total_count` varchar(150) DEFAULT '0',
  `success_count` varchar(150) DEFAULT '0',
  `failure_count` varchar(150) DEFAULT '0',
  `create_time` timestamp NULL DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=327 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `sms_plateform8_failure`
--

DROP TABLE IF EXISTS `sms_plateform8_failure`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `sms_plateform8_failure` (
  `id` int(11) unsigned NOT NULL AUTO_INCREMENT,
  `user` char(11) NOT NULL,
  `user_id` int(11) NOT NULL,
  `channel_id` int(11) NOT NULL,
  `to_number` char(100) DEFAULT NULL,
  `text` char(200) DEFAULT NULL,
  `time` timestamp NULL DEFAULT CURRENT_TIMESTAMP,
  `price` decimal(15,2) DEFAULT '0.00',
  `description` char(50) DEFAULT NULL,
  `message_id` varchar(50) DEFAULT '0' COMMENT '唯一id',
  `is_click` char(10) DEFAULT '未设置',
  `callback_id` int(11) DEFAULT '0',
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=54967 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `sms_plateform8_success`
--

DROP TABLE IF EXISTS `sms_plateform8_success`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `sms_plateform8_success` (
  `id` int(11) unsigned NOT NULL AUTO_INCREMENT,
  `user` char(11) NOT NULL,
  `user_id` int(11) NOT NULL,
  `channel_id` int(11) NOT NULL,
  `to_number` char(100) DEFAULT NULL,
  `text` char(200) DEFAULT NULL,
  `time` timestamp NULL DEFAULT CURRENT_TIMESTAMP,
  `price` decimal(15,2) DEFAULT '0.00',
  `description` char(50) DEFAULT NULL,
  `message_id` varchar(50) DEFAULT '0' COMMENT '唯一id',
  `is_click` char(10) DEFAULT '未设置',
  `callback_id` int(11) DEFAULT '0',
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=1904454 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `sms_plateform9_all_statistics_by_day`
--

DROP TABLE IF EXISTS `sms_plateform9_all_statistics_by_day`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `sms_plateform9_all_statistics_by_day` (
  `id` int(11) unsigned NOT NULL AUTO_INCREMENT,
  `day` varchar(150) NOT NULL,
  `total_count` varchar(150) DEFAULT '0',
  `success_count` varchar(150) DEFAULT '0',
  `failure_count` varchar(150) DEFAULT '0',
  `price_count` decimal(15,2) DEFAULT '0.00',
  `create_time` timestamp NULL DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`id`),
  UNIQUE KEY `day` (`day`)
) ENGINE=InnoDB AUTO_INCREMENT=276 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `sms_plateform9_channel_statistics_by_day`
--

DROP TABLE IF EXISTS `sms_plateform9_channel_statistics_by_day`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `sms_plateform9_channel_statistics_by_day` (
  `id` int(11) unsigned NOT NULL AUTO_INCREMENT,
  `day` varchar(150) NOT NULL,
  `channel_id` int(11) NOT NULL,
  `total_count` varchar(150) DEFAULT '0',
  `success_count` varchar(150) DEFAULT '0',
  `failure_count` varchar(150) DEFAULT '0',
  `create_time` timestamp NULL DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=291 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `sms_plateform9_failure`
--

DROP TABLE IF EXISTS `sms_plateform9_failure`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `sms_plateform9_failure` (
  `id` int(11) unsigned NOT NULL AUTO_INCREMENT,
  `user` char(11) NOT NULL,
  `user_id` int(11) NOT NULL,
  `channel_id` int(11) NOT NULL,
  `to_number` char(100) DEFAULT NULL,
  `text` char(200) DEFAULT NULL,
  `time` timestamp NULL DEFAULT CURRENT_TIMESTAMP,
  `price` decimal(15,2) DEFAULT '0.00',
  `description` char(50) DEFAULT NULL,
  `message_id` varchar(50) DEFAULT '0' COMMENT '唯一id',
  `is_click` char(10) DEFAULT '未设置',
  `callback_id` int(11) DEFAULT '0',
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=52306 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `sms_plateform9_success`
--

DROP TABLE IF EXISTS `sms_plateform9_success`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `sms_plateform9_success` (
  `id` int(11) unsigned NOT NULL AUTO_INCREMENT,
  `user` char(11) NOT NULL,
  `user_id` int(11) NOT NULL,
  `channel_id` int(11) NOT NULL,
  `to_number` char(100) DEFAULT NULL,
  `text` char(200) DEFAULT NULL,
  `time` timestamp NULL DEFAULT CURRENT_TIMESTAMP,
  `price` decimal(15,2) DEFAULT '0.00',
  `description` char(50) DEFAULT NULL,
  `message_id` varchar(50) DEFAULT '0' COMMENT '唯一id',
  `is_click` char(10) DEFAULT '未设置',
  `callback_id` int(11) DEFAULT '0',
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=1441408 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `sms_rate`
--

DROP TABLE IF EXISTS `sms_rate`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `sms_rate` (
  `id` int(11) unsigned NOT NULL AUTO_INCREMENT,
  `channel_id` int(11) NOT NULL,
  `plateform_id` int(11) NOT NULL,
  `rate` decimal(5,2) DEFAULT '0.36',
  `create_time` timestamp NULL DEFAULT CURRENT_TIMESTAMP,
  `is_active` tinyint(1) DEFAULT '1',
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=235 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `sms_recharge`
--

DROP TABLE IF EXISTS `sms_recharge`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `sms_recharge` (
  `id` int(10) unsigned NOT NULL AUTO_INCREMENT,
  `plateform_id` int(11) NOT NULL,
  `balance_before` decimal(15,2) NOT NULL,
  `balance_after` decimal(15,2) NOT NULL,
  `recharge_amount` decimal(15,2) NOT NULL,
  `recharge_time` timestamp NULL DEFAULT CURRENT_TIMESTAMP,
  `is_active` tinyint(1) DEFAULT '1',
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=435 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `sms_sending`
--

DROP TABLE IF EXISTS `sms_sending`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `sms_sending` (
  `id` int(11) unsigned NOT NULL AUTO_INCREMENT,
  `to_number` char(25) DEFAULT NULL,
  `user` char(50) NOT NULL,
  `channel_id` int(11) NOT NULL,
  `plateform_id` int(11) NOT NULL,
  `text` char(200) DEFAULT NULL,
  `time` timestamp NULL DEFAULT CURRENT_TIMESTAMP,
  `is_click` char(10) DEFAULT '未设置',
  `callback_id` int(11) DEFAULT '0',
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `sms_sensitiveWords`
--

DROP TABLE IF EXISTS `sms_sensitiveWords`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `sms_sensitiveWords` (
  `id` int(11) unsigned NOT NULL AUTO_INCREMENT,
  `sensitive_words` varchar(200) NOT NULL,
  `channel_id` int(11) NOT NULL,
  `create_time` timestamp NULL DEFAULT CURRENT_TIMESTAMP,
  `is_active` tinyint(1) DEFAULT '1',
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=19 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `sms_telegram`
--

DROP TABLE IF EXISTS `sms_telegram`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `sms_telegram` (
  `id` int(11) unsigned NOT NULL AUTO_INCREMENT,
  `chat_name` varchar(200) NOT NULL,
  `chat_id` varchar(200) NOT NULL,
  `chat_type` varchar(200) NOT NULL,
  `need_notice` tinyint(1) DEFAULT '0',
  `create_time` timestamp NULL DEFAULT CURRENT_TIMESTAMP,
  `is_have_authority` tinyint(1) DEFAULT '0',
  `is_active` tinyint(1) DEFAULT '1',
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=4 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `sms_template`
--

DROP TABLE IF EXISTS `sms_template`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `sms_template` (
  `id` int(11) unsigned NOT NULL AUTO_INCREMENT,
  `template` varchar(250) NOT NULL,
  `status` varchar(200) DEFAULT 'PENDING',
  `channel_id` int(11) NOT NULL,
  `plateform_id` int(11) NOT NULL,
  `is_active` tinyint(1) DEFAULT '1',
  `template_id` varchar(200) DEFAULT '0',
  `create_time` timestamp NULL DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=11 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `sms_users`
--

DROP TABLE IF EXISTS `sms_users`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `sms_users` (
  `id` int(11) unsigned NOT NULL AUTO_INCREMENT,
  `user` char(15) DEFAULT NULL,
  `password` char(32) DEFAULT NULL,
  `auth` char(20) DEFAULT NULL COMMENT 'admin / user',
  `create_time` timestamp NULL DEFAULT CURRENT_TIMESTAMP,
  `plateform_id` int(11) NOT NULL,
  `is_active` tinyint(1) DEFAULT '1',
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=59 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `sms_whitelist`
--

DROP TABLE IF EXISTS `sms_whitelist`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `sms_whitelist` (
  `id` int(11) unsigned NOT NULL AUTO_INCREMENT,
  `ip` char(15) DEFAULT NULL,
  `memo` char(20) DEFAULT NULL,
  `plateform_id` int(11) NOT NULL,
  `create_time` timestamp NULL DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=23 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2020-12-07 15:52:48
