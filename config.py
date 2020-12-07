# coding: utf-8
import os


class TelegramConf:
    bot_token = 'xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx'
    help = '/help'
    register = '/register'
    channel_info = '/channel_info'
    plateform_info = '/plateform_info'
    recharge = '/recharge'
    mute = '/mute'
    recharge_redis_key = 'telegram:recharge{}_{}'


class Nginx:
    nginx_path = '/etc/nginx/conf.d/'
    index_path = '/usr/share/nginx/html/sms/dist'
    backend_path = 'http://127.0.0.1:8888'
    base_format = """
server {
    listen 80;
    server_name %s;

    location / {
        root   %s;
        index  index.html;
    }

    location /api {
        proxy_pass %s;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
    }
}
"""


class Url:
    base_url = 'xxxx.com/'
    replace_str = 'URL'


class Upload:
    """上传的文件"""
    upload_phone_file_path = os.path.abspath(os.path.dirname(__file__)) + '/uploaded/'


class Page:
    """分页配置"""
    # 每页数量
    count = 20
    history_limit = 15
    recharge_record_limit = 15
    template_limit = 15
    plateform_limit = 5
    sensitive_limit = 15
    white_ip_limit = 15
    excel_file_path = os.path.abspath(os.path.dirname(__file__)) + '/excel_data/'


class LogDefine:
    """log定义"""
    Login = 1
    Logout = 2
    Start = 3
    Stop = 4
    # del_log_time = '02:00:00'
    interval_del_time = 60 * 60
    logpath = os.path.abspath(os.path.dirname(__file__)) + '/logs'
    request_log_file = logpath + '/{}_request.log'
    telegram_log_file = logpath + '/{}_telegram.log'
    log_level = {
        0: 'DEBUG',
        1: 'WARING',
        2: 'ERROR'
    }


class Return_Statua_Code:
    """返回状态定义"""
    ok = 200
    error = 500
    job_success = 200
    job_failed = 500
    job_pending = 300


class Price:
    """
    价格设置 [欧元]
    3通道   / 0.04欧    =  3毛
    6通道   / 0.0375欧  =  2毛8
    axfilx = 3毛
    """
    nexmo = '0.03'
    clickatell = '0.037'
    plivo = '0.037'
    ginota = '0.037'
    hk = '0.040'
    axflix = '1'


class SmsApi:
    # 关于axflix短信的配置
    # BILL 2018-06-28 START
    # ----------------------------------------------------------------
    plivo_id = 'xxxxxxxxxxxxxxxx'
    plivo_token = 'xxxxxxxxxxxxxxxx'
    clickatell_key = 'xxxxxxxxxxxxxxxxxxxxxxxx'
    nexmo_key = 'None'
    nexmo_secret = 'None'
    ginota_key = 'xxxxxxxxxxxxxxxxxxxxxxx'
    ginota_secret = 'xxxxxxxxxxxxxxxx'
    axflix_host = '1.1.1.1'
    axflix_port = 11111
    axflix_china_client_id = 111111
    axflix_vietnam_client_id = 111111
    # 查询余额的transId号
    balance_transId_china = 2
    balance_transId_vietnam = 3
    # 检测心跳的transId号
    heartbeat_transId_china = 1
    heartbeat_transId_vietnam = 4


class WB:
    send_url = 'http://xxxx.com/json/submit'
    balance_url = 'http://xxxx.com/json/balance'
    enterprise_no = 'xxxxxxxxxxxxxxx'
    account = 'xxxxxxxx'
    key = 'xxxxxxxxxxxxx'
    success_code = 'success'
    return_success_code = '0'


class LDY:
    balance_resp_err_code = '-4'
    status_resp_err_code = '-4'
    return_success_code = '0'
    success_code = 'DELIVRD'
    user = 'xxxxxxxx'
    password = 'xxxxxxx'
    send_url = 'http://1.1.1.1:8088/sms_utf.jsp'
    balance_url = 'http://1.1.1.1/stardy/balance.jsp'
    status_url = 'http://1.1.1.1/stardy/status.jsp'


class DCY:
    appid = 'xxxxxxxxxxxx'
    secret = 'xxxxxxxxxxxxx'
    yingxiao_code = '4'
    yanzhengma_code = '1'
    return_success_code = '0'
    balance_code = '4'
    success_code = '成功'
    success_message = 'DELIVRD'
    send_url = 'http://xxxx.com/send'
    balance_url = 'http://xxxx.com/surplus'


class JK:
    # 0:GBK/1:UTF-8
    charset = 1
    # 0:短信内容全部为ASCII/8:中英文
    dsc = 8
    # 主叫号码
    caller = 'xxxxxxxx'
    username = 'xxxxx'
    password = 'xxxxxxx'
    success_code = "DELIVRD"
    return_success_code = '0'
    status_url = 'http://1.1.1.1:8138/5.dox'
    balance_url = 'http://1.1.1.1:8138/1.dox'
    qunfa_send_url = 'http://1.1.1.1:8138/14.dox'
    danfa_send_url = 'http://1.1.1.1:8138/4.dox'


class TELEHOO:
    cpid = 'xxxxxxx'
    cppwd = 'xxxxxx'
    danfa_command = 'MT_REQUEST'
    qunfa_command = 'MULTI_MT_REQUEST'
    send_url = 'http://xxxxx.com/http/submit'
    status_url = 'http://xxxxxx.com/http/get-rptstatus'
    success_mterrocde = '000'
    success_mtstat = 'ACCEPTD'


class SMS123:
    create_template_url = 'https://xxxxx.net/api/smsAddTemplate.php'
    balance_url = 'https://xxxxxx.net/api/getBalance.php'
    send_url = 'https://xxxxx.net/api/send.php'
    apikey = 'xxxxxxxxxxxxx'
    email = 'xxxxxxx'
    balance_return_success_code = 'E00001'
    create_template_return_success_code = 'E00001'
    send_return_success_status = 'ok'
    template_callback_success_code = 'E00101'


class Sql:
    """mysql连接配置"""
    # BILL 2018-06-28 START
    allday_table_sql = """
CREATE TABLE `sms_plateform{}_all_statistics_by_day` (
  `id` int(11) unsigned NOT NULL AUTO_INCREMENT,
  `day` varchar(150) NOT NULL,
  `total_count` varchar(150) DEFAULT 0,
  `success_count` varchar(150) DEFAULT 0,
  `failure_count` varchar(150) DEFAULT 0,
  `price_count` decimal(15,2) DEFAULT 0.00,
  `create_time` timestamp NULL DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`id`),
  UNIQUE KEY (`day`)
) ENGINE=InnoDB AUTO_INCREMENT=31 DEFAULT CHARSET=utf8;
"""
    channelday_table_sql = """
CREATE TABLE `sms_plateform{}_channel_statistics_by_day` (
  `id` int(11) unsigned NOT NULL AUTO_INCREMENT,
  `day` varchar(150) NOT NULL,
  `channel_id` int(11) NOT NULL,
  `total_count` varchar(150) DEFAULT 0,
  `success_count` varchar(150) DEFAULT 0,
  `failure_count` varchar(150) DEFAULT 0,
  `create_time` timestamp NULL DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=31 DEFAULT CHARSET=utf8;
"""
    plateform_success_sql = """
CREATE TABLE `sms_plateform{}_success` (
  `id` int(11) unsigned NOT NULL AUTO_INCREMENT,
  `user` char(11) NOT NULL,
  `user_id` int(11) NOT NULL,
  `channel_id` int(11) NOT NULL,
  `to_number` char(100) DEFAULT NULL,
  `text` char(200) DEFAULT NULL,
  `time` timestamp NULL DEFAULT CURRENT_TIMESTAMP,
  `price` decimal(15,2) DEFAULT 0.00,
  `description` char(50) DEFAULT NULL,
  `message_id` varchar(50) DEFAULT '0' COMMENT '唯一id',
  `is_click` char(10) DEFAULT '未设置',
  `callback_id` int DEFAULT 0,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=31 DEFAULT CHARSET=utf8;
"""
    plateform_failure_sql = """
CREATE TABLE `sms_plateform{}_failure` (
  `id` int(11) unsigned NOT NULL AUTO_INCREMENT,
  `user` char(11) NOT NULL,
  `user_id` int(11) NOT NULL,
  `channel_id` int(11) NOT NULL,
  `to_number` char(100) DEFAULT NULL,
  `text` char(200) DEFAULT NULL,
  `time` timestamp NULL DEFAULT CURRENT_TIMESTAMP,
  `price` decimal(15,2) DEFAULT 0.00,
  `description` char(50) DEFAULT NULL,
  `message_id` varchar(50) DEFAULT '0' COMMENT '唯一id',
  `is_click` char(10) DEFAULT '未设置',
  `callback_id` int DEFAULT 0,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=31 DEFAULT CHARSET=utf8;
"""
    plateform_cache_sql = """
CREATE TABLE `sms_cache_plateform{}_history` (
  `id` int(11) unsigned NOT NULL AUTO_INCREMENT,
  `user` char(11) NOT NULL,
  `user_id` int(11) NOT NULL,
  `channel_id` int(11) NOT NULL,
  `to_number` char(100) DEFAULT NULL,
  `text` char(200) DEFAULT NULL,
  `time` timestamp NULL DEFAULT CURRENT_TIMESTAMP,
  `price` decimal(15,2) DEFAULT 0.00,
  `description` char(50) DEFAULT NULL,
  `message_id` varchar(50) DEFAULT '0' COMMENT '唯一id',
  `is_click` char(10) DEFAULT '未设置',
  `callback_id` int(11) DEFAULT 0,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=1 DEFAULT CHARSET=utf8;
"""
    host = '127.0.0.1'
    password = 'xxxxxxxxx'
    port = 3306
    user = 'root'
    db = 'sms'
    max_cached = 10
    kl_message_id = -10
    min_cache_limit = 20000
    max_cache_limit = 50000


class RedisSql:
    host = '127.0.0.1'
    port = 6379
    result_queue_name = "result_sms"
    balance_queue_name = 'balance_sms'
    job_status_code = {'pending': '300', 'success': '200', 'failed': '500'}
    db = 0


class LocalSocket:
    ip = "127.0.0.1"
    port = 9999
