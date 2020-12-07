# coding: utf-8
# 发送短信历史数据库


from config import Page
from db.base import DBbase
from pymysql import escape_string
from db.statistics import StatisticsDB
from db.cache_history import SmsCacheHistoryDB
import time


"""
CREATE TABLE `sms_plateform*_success` (
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
) ENGINE=InnoDB AUTO_INCREMENT=31 DEFAULT CHARSET=utf8;
"""

"""
CREATE TABLE `sms_plateform*_failure` (
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
) ENGINE=InnoDB AUTO_INCREMENT=31 DEFAULT CHARSET=utf8;
"""


class SmsHistoryDB(DBbase):
    """发送历史数据表管理"""
    def __init__(self):
        super().__init__()

    def add(self, user, user_id, message_id, to, text, price, description, channel_id, plateform_id, callback=0,
            is_click='未设置', time_=None, need_count_all=False):
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
        sql = f'insert into sms_plateform{plateform_id}_{"success" if description == "success" else "failure"} (user,' \
              f'user_id,channel_id,to_number,text,price,description,message_id,callback_id,is_click' \
              f'{"" if time_ is None else ",time"}) values ("{user}",{user_id},{channel_id},"{to}","{new_text}",' \
              f'{price},"{description.upper()}","{message_id}",{callback},"{is_click}"' \
              f'''{"" if time_ is None else f',"{time_}"'});'''
        with StatisticsDB() as db:
            new_count_type = "success_count" if description == 'success' else "failure_count"
            db.update_count(plateform_id, channel_id, [new_count_type, "total_count"] if need_count_all else new_count_type,
                            time.strftime("%Y-%m-%d", time.localtime()) if time_ is None else time_.strftime("%Y-%m-%d"),
                            price=price)
        with SmsCacheHistoryDB() as db:
            db.add(user, user_id, message_id, to, text, price, description, channel_id, plateform_id, callback,
                   is_click, time_, need_count_all)
        return self.execute(sql, commit=True)

    @staticmethod
    def _handle_query(to, start, end, user_id, channel_id, need_end=True, need_excel=False, plateform_id=None):
        where_sql = ''
        if need_excel:
            # 导出表格的话只能导出当前用户发的
            where_sql += f'where user_id={user_id}'
        if plateform_id is not None:
            where_sql += f'{" and" if where_sql else "where"} plateform_id={plateform_id}'
        if channel_id:
            where_sql += f'{" and" if where_sql else "where"} channel_id={channel_id}'
        if to:
            where_sql += f'{" and" if where_sql else "where"} to_number like "%{to}"'
        if start and end:
            where_sql += f'{" and" if where_sql else "where"} time>="{start} 00:00:00" and time <="{end} 23:59:59"'
        return where_sql + ';' if need_end else where_sql

    def search_history(self, to, start, end, err, page, user_id, channel_id, need_limit=True, limit=Page.history_limit):
        """
        根据页数和条件返回信息，每页15个，如果页数为None或''默认显示第一页
        :param to: 手机号码
        :param start: 开始时间
        :param end: 结束时间
        :param err: 状态(0/成功, 非0/失败, None或''/查询全部)
        :param page: 页数
        :return: (("admin", ...), )
        """
        plateform_id = self.execute(f'select plateform_id from sms_users where id={user_id};', fetch=True)[0][0]
        channel_name_sql = '(select name from sms_channel where id=channel_id) as channel_name'
        base_sql = 'select id,user,%s,to_number,text,time,price,description,is_click from'
        where_sql = self._handle_query(to, start, end, user_id, channel_id, False, need_excel=False if need_limit else True)
        plateform_where_sql = self._handle_query(to, start, end, user_id, channel_id, False,
                                                 need_excel=False if need_limit else True, plateform_id=plateform_id)
        if err == 0:
            # 搜索成功
            sql = f'{base_sql % channel_name_sql} sms_plateform{plateform_id}_success {where_sql}'
        elif err == 1:
            # 搜索失败
            sql = f'{base_sql % channel_name_sql} sms_plateform{plateform_id}_failure {where_sql}'
        elif err == 2:
            # 搜索发送中
            sql = f'{base_sql % channel_name_sql} sms_pending {plateform_where_sql}'
        else:
            # 搜索全部
            sql = f'{base_sql % channel_name_sql} ({base_sql % "channel_id"} sms_plateform{plateform_id}_success ' \
                  f'{where_sql} union all {base_sql % "channel_id"} sms_plateform{plateform_id}_failure {where_sql} ' \
                  f'union all {base_sql % "channel_id"} sms_pending {plateform_where_sql}) as c'

        if need_limit:
            limit_sql = ' order by time desc limit {},{};'.format(page * limit if page else 0, limit)
            sql += limit_sql
        else:
            sql += ' order by time desc;'
        return self.execute(sql, fetch=True)

    def update_is_click(self, callback_id, plateform_id):
        sql = f'update sms_pending set is_click="已点击" where callback_id={callback_id};'
        if self.execute(sql, commit=True):
            return True
        else:
            self.execute(f'update sms_plateform{plateform_id}_success set is_click="已点击" where callback_id={callback_id};')
            cache_sql = f'update sms_cache_plateform{plateform_id}_history set is_click="已点击" where callback_id={callback_id};'
            return self.execute(cache_sql, commit=True)


if __name__ == '__main__':
    db = SmsHistoryDB()
    db.search_history('', '', '', 0, '', 5)
