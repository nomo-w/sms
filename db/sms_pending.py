# coding: utf-8
# 发送短信历史数据库

from config import Sql
from db.base import DBbase
from pymysql import escape_string
from db.history import SmsHistoryDB
from db.statistics import StatisticsDB
from db.cache_statistics import CacheStatisticsDB
import datetime
import random
import time


"""
CREATE TABLE `sms_pending` (
  `id` int(11) unsigned NOT NULL AUTO_INCREMENT,
  `user` char(11) NOT NULL,
  `user_id` int(11) DEFAULT -1,
  `channel_id` int(11) NOT NULL,
  `plateform_id` int(11) NOT NULL,
  `to_number` char(100) DEFAULT NULL,
  `text` char(200) DEFAULT NULL,
  `time` timestamp NULL DEFAULT CURRENT_TIMESTAMP,
  `price` decimal(15,2) DEFAULT 0.00,
  `description` char(50) DEFAULT 'pending',
  `message_id` varchar(50) DEFAULT '0' COMMENT '唯一id',
  `is_click` char(10) DEFAULT '未设置',
  `callback_id` int(11) DEFAULT 0,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
"""


class SmsPendingDB(DBbase):
    """发送等待返回结果表"""
    def __init__(self):
        super().__init__()

    def is_have_text(self, text):
        sql = f'select message_id from sms_pending where text="{text}" and message_id!="{Sql.kl_message_id}" limit 1;'
        r = self.execute(sql, fetch=True)
        return r[0][0] if r else None

    def search_manual(self, message_id):
        channel_id_sql = 'channel_id=(select id from sms_channel where channel_type="manual")'
        if message_id in ['null', None, '']:
            sql = f'select distinct message_id from sms_pending where {channel_id_sql} and ' \
                  f'message_id!="{Sql.kl_message_id}";'
            r = []
            for i in self.execute(sql, fetch=True):
                _ = self.execute(f'select count(to_number),text from sms_pending where message_id="{i[0]}";', fetch=True)
                r.append(_[0] + (i[0],))

        else:
            # text = escape_string(text)
            sql = f'select to_number from sms_pending where {channel_id_sql} and message_id="{message_id}";'
            r = self.execute(sql, fetch=True)
        return r if r else []

    def update_kl(self, message_id):
        sql = f'select id,user,user_id,channel_id,plateform_id,to_number,text,is_click,callback_id,time from ' \
              f'sms_pending where message_id="{message_id}";'
        r = self.execute(sql, fetch=True)
        for i in r:
            if i:
                i = list(i)
                i[-1] = i[-1] + datetime.timedelta(seconds=+random.randint(1, 50))
                keys = ['user', 'user_id', 'channel_id', 'plateform_id', 'to', 'text', 'is_click', 'callback', 'time_']
                dic = dict(zip(keys, i[1:]))
                # 扣钱
                rate_sql = f'select rate from sms_rate where plateform_id={dic["plateform_id"]} and channel_id={dic["channel_id"]}'
                price = self.execute(rate_sql + ';', fetch=True)[0][0]
                c_b_sql = f'update sms_plateform set balance=balance-({price}) where id={dic["plateform_id"]};'
                # c_b_sql = f'-- update sms_plateform set balance=balance-({price}) where balance>=({rate_sql}) and id={dic["plateform_id"]};'
                self.execute(c_b_sql)
                with SmsHistoryDB() as db:
                    db.add(**dic, message_id=message_id, price=price, description='success')
                del_sql = f'delete from sms_pending where id={i[0]};'
                self.execute(del_sql, commit=True)
        return True

    def add(self, user_id, message_id, to, text, channel_id, plateform_id=None, callback=0, is_click='未设置', user=None, commit=True):
        """
        :param user:  operator
        :param message_id: unique message id
        :param to:  to-number
        :param text:  to-sms-text-body
        :param price:  sms-price / per
        :param err: ret-code
        :param err_text: ret error text
        :return:
        """
        new_text = escape_string(text)
        if user is None:
            user = f'(select user from sms_users where id={user_id})'
        else:
            user = f'"{user}"'
        if plateform_id is None:
            plateform_id = self.execute(f'select plateform_id from sms_users where id={user_id};', fetch=True)[0][0]
        sql = f'insert into sms_pending (user,user_id,channel_id,plateform_id,to_number,text,message_id,' \
              f'callback_id,is_click) values ({user},{user_id},{channel_id},{plateform_id},"{to}","{new_text}",' \
              f'"{message_id}",{callback},"{is_click}");'
        self.execute(sql, commit=commit)
        with StatisticsDB() as db:
            db.update_count(plateform_id, channel_id, "total_count", time.strftime("%Y-%m-%d", time.localtime()))
        with CacheStatisticsDB() as db:
            db.update_count(plateform_id, channel_id, "total_count", time.strftime("%Y-%m-%d", time.localtime()))
        return True

    def update(self, message_id, err, err_text, to=None):
        # price 价格
        # err   1为错误/
        sql = f'select user,user_id,channel_id,plateform_id,to_number,text,is_click,callback_id,time from sms_pending ' \
              f'where message_id="{message_id}"'
        if to:
            sql += f' and to_number="{to}";'
        else:
            sql += ';'
        r = self.execute(sql, fetch=True)
        if r:
            keys = ['user', 'user_id', 'channel_id', 'plateform_id', 'to', 'text', 'is_click', 'callback', 'time_']
            dic = dict(zip(keys, r[0]))
            price = 0
            if err == 0:
                # 扣钱
                rate_sql = f'select rate from sms_rate where plateform_id={dic["plateform_id"]} and channel_id={dic["channel_id"]}'
                price = self.execute(rate_sql+';', fetch=True)[0][0]
                c_b_sql = f'update sms_plateform set balance=balance-({price}) where id={dic["plateform_id"]};'
                # c_b_sql = f'-- update sms_plateform set balance=balance-({price}) where balance>=({rate_sql}) and id={dic["plateform_id"]};'
                self.execute(c_b_sql)
            with SmsHistoryDB() as db:
                db.add(**dic, message_id=message_id, price=price, description='success' if err == 0 else err_text)
            del_sql = f'delete from sms_pending where message_id="{message_id}"'
            if to:
                del_sql += f' and to_number="{to}" limit 1;'
            else:
                del_sql += ' limit 1;'
            return self.execute(del_sql, commit=True)
        return False

