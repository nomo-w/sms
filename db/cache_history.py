# coding: utf-8


from db.base import DBbase
from config import Page, Sql
from pymysql import escape_string
from db.cache_statistics import CacheStatisticsDB
import time


"""
CREATE TABLE `sms_cache_plateform*_history` (
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


class SmsCacheHistoryDB(DBbase):
    def __init__(self):
        super().__init__()

    def update_cache(self, min_limit=Sql.min_cache_limit, max_limit=Sql.max_cache_limit):
        for i in self.execute('select id from sms_plateform where is_active=1;', fetch=True):
            while True:
                all_num = self.execute(f'select (case when sum(total_count) is not null then sum(total_count) else 0 end) '
                                   f'as total_count from sms_cache_all_statistics where plateform_id={i[0]};', fetch=True)
                if all_num and int(all_num[0][0]) >= max_limit:
                    old_day = self.execute(f'select day from sms_cache_all_statistics_by_day where plateform_id={i[0]} '
                                           f'order by day limit 1;', fetch=True)
                    if old_day:
                        nu_day = self.execute(f'select (case when sum(total_count) is not null then sum(total_count) '
                                              f'else 0 end) as total_count from sms_cache_all_statistics_by_day '
                                              f'where plateform_id={i[0]} and day="{old_day[0][0]}";', fetch=True)
                        if nu_day and int(all_num[0][0]) - int(nu_day[0][0]) >= min_limit:
                            for j in self.execute(f'select channel_id,total_count,success_count,failure_count from '
                                                  f'sms_cache_all_statistics_by_day where plateform_id={i[0]} and '
                                                  f'day="{old_day[0][0]}";', fetch=True):
                                self.execute(f'update sms_cache_all_statistics set total_count=total_count-{j[1]},'
                                             f'success_count=success_count-{j[2]},failure_count=failure_count-{j[3]} '
                                             f'where plateform_id={i[0]} and channel_id={j[0]};')
                            self.execute(f'delete from sms_cache_all_statistics_by_day where plateform_id={i[0]} and day="{old_day[0][0]}";')
                            self.execute(f'delete from sms_cache_plateform{i[0]}_history where '
                                         f'time>="{old_day[0][0]} 00:00:00" and time<="{old_day[0][0]} 23:59:59";', commit=True)
                        else:
                            break
                    else:
                        break
                else:
                    break

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
        sql = f'insert into sms_cache_plateform{plateform_id}_history (user,user_id,channel_id,to_number,text,price,' \
              f'description,message_id,callback_id,is_click{"" if time_ is None else ",time"}) values ("{user}",{user_id}' \
              f',{channel_id},"{to}","{new_text}",{price},"{description.upper()}","{message_id}",{callback},"{is_click}"' \
              f'''{"" if time_ is None else f',"{time_}"'});'''
        with CacheStatisticsDB() as db:
            new_count_type = "success_count" if description == 'success' else "failure_count"
            db.update_count(plateform_id, channel_id, [new_count_type, "total_count"] if need_count_all else new_count_type,
                            time.strftime("%Y-%m-%d", time.localtime()) if time_ is None else time_.strftime("%Y-%m-%d"))
        return self.execute(sql, commit=True)

    @staticmethod
    def _handle_query(start, end, user_id, channel_id, err=None, need_excel=False, plateform_id=None):
        where_sql = ''
        if need_excel:
            # 导出表格的话只能导出当前用户发的
            where_sql += f'where user_id={user_id}'
        if err in (0, 1):
            where_sql += f'{" and" if where_sql else "where"} description' + ('="SUCCESS"' if err == 0 else '!="SUCCESS"')
        if plateform_id is not None:
            where_sql += f'{" and" if where_sql else "where"} plateform_id={plateform_id}'
        if channel_id:
            where_sql += f'{" and" if where_sql else "where"} channel_id={channel_id}'
        if start and end:
            where_sql += f'{" and" if where_sql else "where"} time>="{start} 00:00:00" and time <="{end} 23:59:59"'
        return where_sql

    def search_history(self, start, end, err, page, user_id, channel_id, need_limit=True, limit=Page.history_limit):
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
        base_sql = f'select id,user,%s,to_number,text,time,price,description,is_click from'
        channel_name_sql = '(select name from sms_channel where id=channel_id) as channel_name'
        where_sql = self._handle_query(start, end, user_id, channel_id, err, need_excel=False if need_limit else True)
        if err in (0, 1):
            # 搜索成功或失败
            sql = f'{base_sql % channel_name_sql} sms_cache_plateform{plateform_id}_history {where_sql}'
        else:
            plateform_where_sql = self._handle_query(start, end, user_id, channel_id,
                                                need_excel=False if need_limit else True, plateform_id=plateform_id)
            sql = f'{base_sql % channel_name_sql} ({base_sql % "channel_id"} sms_cache_plateform{plateform_id}_history ' \
                  f'{where_sql} union all {base_sql % "channel_id"} sms_pending {plateform_where_sql}) as c'
        if need_limit:
            limit_sql = ' order by time desc limit {},{};'.format((int(page) - 1) * limit if page else 0, limit)
            sql += limit_sql
        else:
            sql += ' order by time desc;'
        return self.execute(sql, fetch=True)

    # def update_is_click(self, callback_id, plateform_id):
    #     sql = f'update sms_pending set is_click="已点击" where callback_id={callback_id};'
    #     if self.execute(sql, commit=True):
    #         return True
    #     else:
    #         sql = f'update sms_cache_plateform{plateform_id}_history set is_click="已点击" where callback_id={callback_id};'
    #         return self.execute(sql, commit=True)

