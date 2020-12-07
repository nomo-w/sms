from db.base import DBbase
from config import Page


"""
# 统计各个平台前两天的发送总量
CREATE TABLE `sms_cache_all_statistics` (
  `id` int(11) unsigned NOT NULL AUTO_INCREMENT,
  `plateform_id` int(11) NOT NULL,
  `channel_id` int(11) NOT NULL,
  `total_count` varchar(150) DEFAULT 0,
  `success_count` varchar(150) DEFAULT 0,
  `failure_count` varchar(150) DEFAULT 0,
  `create_time` timestamp NULL DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=1 DEFAULT CHARSET=utf8;
"""

"""
CREATE TABLE `sms_cache_all_statistics_by_day` (
  `id` int(11) unsigned NOT NULL AUTO_INCREMENT,
  `day` varchar(200) NOT NULL,
  `plateform_id` int(11) NOT NULL,
  `channel_id` int(11) NOT NULL,
  `total_count` varchar(150) DEFAULT 0,
  `success_count` varchar(150) DEFAULT 0,
  `failure_count` varchar(150) DEFAULT 0,
  `create_time` timestamp NULL DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=1 DEFAULT CHARSET=utf8;
"""


class CacheStatisticsDB(DBbase):
    """发送历史数据表管理"""
    def __init__(self):
        super().__init__()

    def search_cache_statistics(self, start, end, channel_id, user_id, status, page, limit=Page.history_limit):
        plateform_id = f'(select plateform_id from sms_users where id={user_id})'
        if status == 0:
            # 搜索成功
            count_type = '(case when sum(success_count) is not null then sum(success_count) else 0 end) as success_count'
        elif status == 1:
            # 搜索失败
            count_type = '(case when sum(failure_count) is not null then sum(failure_count) else 0 end) as failure_count'
        else:
            # 搜索全部
            count_type = '(case when sum(total_count) is not null then sum(total_count) else 0 end) as total_count'
        if start and end:
            sql = f'select {count_type} from sms_cache_all_statistics_by_day where day>="{start}" and day<="{end}" ' \
                f'and plateform_id={plateform_id}{f" and channel_id={channel_id}" if channel_id is not None else ""};'
        else:
            sql = f'select {count_type} from sms_cache_all_statistics where plateform_id={plateform_id}' \
                  f'{f" and channel_id={channel_id}" if channel_id is not None else ""};'
        r = self.execute(sql, fetch=True)
        if r:
            return True if (int(page) if page else 1) * limit <= int(r[0][0]) else False
        return False

    def update_count(self, plateform_id, channel_id, count_type, day):
        new_count_type = ''
        for i in count_type if count_type.__class__ is list else [count_type]:
            new_count_type += f'{i}={i}+1,'
        new_count_type = new_count_type[:-1]

        count_all_sql = f'update sms_cache_all_statistics set {new_count_type} where plateform_id={plateform_id} ' \
                        f'and channel_id={channel_id};'

        select_count_day_sql = f'select id from sms_cache_all_statistics_by_day where day="{day}" and ' \
                               f'plateform_id={plateform_id} and channel_id={channel_id};'
        r = self.execute(select_count_day_sql, fetch=True)
        if r:
            count_day_sql = f'update sms_cache_all_statistics_by_day set {new_count_type} where day="{day}" and ' \
                            f'plateform_id={plateform_id} and channel_id={channel_id};'
        else:
            new_count_type = ''
            for _ in count_type if count_type.__class__ is list else [count_type]:
                new_count_type += '1,'
            count_day_sql = f'insert into sms_cache_all_statistics_by_day (day,plateform_id,channel_id,' \
                            f'{count_type if count_type.__class__ is str else ",".join(count_type)}) ' \
                            f'values ("{day}",{plateform_id},{channel_id},{new_count_type[:-1]});'
        self.execute(count_all_sql)
        return self.execute(count_day_sql, commit=True)

