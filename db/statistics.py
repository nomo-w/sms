from db.base import DBbase
from config import Page


"""
# 统计各个平台的发送总量
CREATE TABLE `sms_all_statistics` (
  `id` int(11) unsigned NOT NULL AUTO_INCREMENT,
  `plateform_id` int(11) NOT NULL,
  `total_count` varchar(150) DEFAULT 0,
  `success_count` varchar(150) DEFAULT 0,
  `failure_count` varchar(150) DEFAULT 0,
  `price_count` decimal(25,2) DEFAULT 0.00,
  `create_time` timestamp NULL DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=31 DEFAULT CHARSET=utf8;
"""

"""
# 统计各个平台每个通道的发送总量
CREATE TABLE `sms_channel_statistics` (
  `id` int(11) unsigned NOT NULL AUTO_INCREMENT,
  `plateform_id` int(11) NOT NULL,
  `channel_id` int(11) NOT NULL,
  `total_count` varchar(150) DEFAULT 0,
  `success_count` varchar(150) DEFAULT 0,
  `failure_count` varchar(150) DEFAULT 0,
  `create_time` timestamp NULL DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=31 DEFAULT CHARSET=utf8;
"""

"""
# 统计各个平台每天的发送总量
CREATE TABLE `sms_plateform*_all_statistics_by_day` (
  `id` int(11) unsigned NOT NULL AUTO_INCREMENT,
  `day` varchar(150) NOT NULL,
  `total_count` varchar(150) DEFAULT 0,
  `success_count` varchar(150) DEFAULT 0,
  `failure_count` varchar(150) DEFAULT 0,
  `price_count` decimal(25,2) DEFAULT 0.00,
  `create_time` timestamp NULL DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`id`),
  UNIQUE KEY (`day`)
) ENGINE=InnoDB AUTO_INCREMENT=31 DEFAULT CHARSET=utf8;
"""

"""
# 统计各个平台每天每个通道的发送量
CREATE TABLE `sms_plateform*_channel_statistics_by_day` (
  `id` int(11) unsigned NOT NULL AUTO_INCREMENT,
  `day` varchar(150) NOT NULL,
  `channel_id` int(11) NOT NULL,
  `total_count` varchar(150) DEFAULT 0,
  `success_count` varchar(150) DEFAULT 0,
  `failure_count` varchar(150) DEFAULT 0,
  `create_time` timestamp NULL DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`id`),
) ENGINE=InnoDB AUTO_INCREMENT=31 DEFAULT CHARSET=utf8;
"""


class StatisticsDB(DBbase):
    """发送历史数据表管理"""
    def __init__(self):
        super().__init__()

    def search_page(self, start, end, err, user_id, channel_id, limit=Page.history_limit):
        # :param err: 状态(0/成功, 非0/失败, None或''/查询全部)
        if any([start, end]) is False:
            # 搜索全部
            if channel_id:
                if err == 0:
                    # 成功
                    r = self.show_channelcount_by_plateform(channel_id, ['success_count'], user_id=user_id)
                    num = r[0][0] if r is not None else 0
                elif err == 1:
                    # 失败
                    r = self.show_channelcount_by_plateform(channel_id, ['failure_count'], user_id=user_id)
                    num = r[0][0] if r is not None else 0
                elif err == 2:
                    # 发送中
                    r = self.show_channelcount_by_plateform(channel_id, ['total_count', 'success_count', 'failure_count'], user_id=user_id)
                    num = int(r[0][0])-(int(r[0][1])+int(r[0][2])) if r is not None else 0
                else:
                    r = self.show_channelcount_by_plateform(channel_id, ['total_count'], user_id=user_id)
                    num = r[0][0] if r is not None else 0
            else:
                if err == 0:
                    # 成功
                    r = self.show_allcount_by_plateform('success_count', user_id=user_id)
                    num = r[0][0] if r is not None else 0
                elif err == 1:
                    # 失败
                    r = self.show_allcount_by_plateform('failure_count', user_id=user_id)
                    num = r[0][0] if r is not None else 0
                elif err == 2:
                    # 发送中
                    r = self.show_allcount_by_plateform('total_count,success_count,failure_count', user_id=user_id)
                    num = int(r[0][0])-(int(r[0][1])+int(r[0][2])) if r is not None else 0
                else:
                    r = self.show_allcount_by_plateform('total_count', user_id=user_id)
                    num = r[0][0] if r is not None else 0

        elif any([start, end]) is True:
            # 按照时间搜索
            if channel_id:
                # 按照时间和通道搜索
                if err == 0:
                    # 成功
                    r = self.show_channelcount_by_day(start, end, ['success_count'], channel_id, need_sum=True, user_id=user_id)
                    num = r[0][0] if r is not None else 0
                elif err == 1:
                    # 失败
                    r = self.show_channelcount_by_day(start, end, ['failure_count'], channel_id, need_sum=True, user_id=user_id)
                    num = r[0][0] if r is not None else 0
                elif err == 2:
                    # 发送中
                    r = self.show_channelcount_by_day(start, end, ['total_count', 'success_count', 'failure_count'],
                                                      channel_id, need_sum=True, user_id=user_id)
                    num = int(r[0][0])-(int(r[0][1])+int(r[0][2])) if r is not None else 0
                else:
                    r = self.show_channelcount_by_day(start, end, ['total_count'], channel_id, need_sum=True, user_id=user_id)
                    num = r[0][0] if r is not None else 0
            else:
                if err == 0:
                    # 成功
                    r = self.show_allcount_by_day(start, end, ['success_count'], need_sum=True, user_id=user_id)
                    num = r[0][0] if r is not None else 0
                elif err == 1:
                    # 失败
                    r = self.show_allcount_by_day(start, end, ['failure_count'], need_sum=True, user_id=user_id)
                    num = r[0][0] if r is not None else 0
                elif err == 2:
                    # 发送中
                    r = self.show_allcount_by_day(start, end, ['total_count', 'success_count', 'failure_count'],
                                                      need_sum=True, user_id=user_id)
                    num = int(r[0][0])-(int(r[0][1])+int(r[0][2])) if r is not None else 0
                else:
                    r = self.show_allcount_by_day(start, end, ['total_count'], need_sum=True, user_id=user_id)
                    num = r[0][0] if r is not None else 0
        page_list = [i + 1 for i in range(int(num) // limit)]
        page_list = page_list if page_list else [1]
        if int(num) > limit and (int(num) % limit != 0):
            page_list.append(page_list[-1] + 1)
        return page_list, int(num)

    def show_allcount_by_plateform(self, count_type, plateform_id=None, user_id=None):
        if plateform_id is not None:
            where_sql = f' where plateform_id={plateform_id}'
        elif user_id is not None:
            where_sql = f' where plateform_id=(select plateform_id from sms_users where id={user_id})'
        sql = f'select {count_type} from sms_all_statistics{where_sql};'
        r = self.execute(sql, fetch=True)
        return r if r else None

    def show_channelcount_by_plateform(self, channel_id, count_type, need_sum=False, plateform_id=None, user_id=None):
        if plateform_id is not None:
            where_sql = f' where plateform_id={plateform_id}'
        elif user_id is not None:
            where_sql = f' where plateform_id=(select plateform_id from sms_users where id={user_id})'
        if need_sum:
            new_count_type = ''
            for i in count_type:
                new_count_type += f'(case when sum({i}) is not null then sum({i}) else 0 end) as {i},'
            new_count_type = new_count_type[:-1]
        else:
            new_count_type = ','.join(count_type)
        sql = f'select {new_count_type} from sms_channel_statistics' \
              f'{where_sql} and channel_id={channel_id};'
        r = self.execute(sql, fetch=True)
        return r if r else None

    def show_allcount_by_day(self, start, end, count_type, need_sum=False, plateform_id=None, user_id=None):
        if user_id is not None:
            plateform_id = self.execute(sql=f'select plateform_id from sms_users where id={user_id};', fetch=True)[0][0]
        if need_sum:
            new_count_type = ''
            for i in count_type:
                new_count_type += f'(case when sum({i}) is not null then sum({i}) else 0 end) as {i},'
            new_count_type = new_count_type[:-1]
        else:
            new_count_type = ','.join(count_type)
        sql = f'select {new_count_type} from sms_plateform{plateform_id}_all_statistics_by_day where day>="{start}" and day<="{end}";'
        r = self.execute(sql, fetch=True)
        return r if r else None

    def show_channelcount_by_day(self, start, end, count_type, channel_id, need_sum=False, plateform_id=None, user_id=None):
        if user_id is not None:
            plateform_id = self.execute(sql=f'select plateform_id from sms_users where id={user_id};', fetch=True)[0][0]
        if need_sum:
            new_count_type = ''
            for i in count_type:
                new_count_type += f'(case when sum({i}) is not null then sum({i}) else 0 end) as {i},'
            new_count_type = new_count_type[:-1]
        else:
            new_count_type = ','.join(count_type)
        sql = f'select {new_count_type} from sms_plateform{plateform_id}_channel_statistics_by_day ' \
              f'where channel_id={channel_id} and day>="{start}" and day<="{end}";'
        r = self.execute(sql, fetch=True)
        return r if r else None

    def create_new_count(self, day):
        for i in self.execute('select id from sms_plateform;', fetch=True):
            sql = f'select id from sms_plateform{i[0]}_all_statistics_by_day where day="{day}";'
            if not self.execute(sql, fetch=True):
                self.execute(f'insert into sms_plateform{i[0]}_all_statistics_by_day (day) values ("{day}");', commit=True)
            # for j in self.execute('select id from sms_channel;', fetch=True):
            #     sql = f'-- select id from sms_plateform{i[0]}_channel_statistics_by_day where channel_id={j[0]} and day="{day}";'
            #     if not self.execute(sql, fetch=True):
            #         sql = f'-- insert into sms_plateform{i[0]}_channel_statistics_by_day (day,channel_id) values ("{day}",{j[0]});'
            #         self.execute(sql, commit=True)

    def update_count(self, plateform_id, channel_id, count_type, day, price=0):
        new_count_type = ''
        for i in count_type if count_type.__class__ is list else [count_type]:
            new_count_type += f'{i}={i}+1,'
        new_count_type = new_count_type[:-1]

        count_all_sql = f'update sms_all_statistics set {new_count_type}{f",price_count=price_count+{price}" if price>0 else ""}' \
                        f' where plateform_id={plateform_id};'
        count_channel_sql = f'update sms_channel_statistics set {new_count_type} where ' \
                            f'plateform_id={plateform_id} and channel_id={channel_id};'
        select_count_day_sql = f'select id from sms_plateform{plateform_id}_all_statistics_by_day where day="{day}";'
        r = self.execute(select_count_day_sql, fetch=True)
        if r:
            count_day_sql = f'update sms_plateform{plateform_id}_all_statistics_by_day set {new_count_type}' \
                        f'{f",price_count=price_count+{price}" if price>0 else ""} where id={r[0][0]};'
        else:
            new_count_type = ''
            for _ in count_type if count_type.__class__ is list else [count_type]:
                new_count_type += '1,'
            count_day_sql = f'insert into sms_plateform{plateform_id}_all_statistics_by_day (day,' \
                            f'{count_type if count_type.__class__ is str else ",".join(count_type)},price_count) ' \
                            f'values ("{day}",{new_count_type}{price});'
        select_count_channel_day_sql = f'select id from sms_plateform{plateform_id}_channel_statistics_by_day ' \
                                       f'where day="{day}" and channel_id={channel_id};'
        r = self.execute(select_count_channel_day_sql, fetch=True)
        if r:
            count_channel_day_sql = f'update sms_plateform{plateform_id}_channel_statistics_by_day set ' \
                                    f'{new_count_type} where id={r[0][0]};'
        else:
            new_count_type = ''
            for _ in count_type if count_type.__class__ is list else [count_type]:
                new_count_type += '1,'
            count_channel_day_sql = f'insert into sms_plateform{plateform_id}_channel_statistics_by_day (day,' \
                                    f'{count_type if count_type.__class__ is str else ",".join(count_type)},' \
                                    f'channel_id) values ("{day}",{new_count_type}{channel_id});'
        self.execute(count_all_sql)
        self.execute(count_channel_sql)
        self.execute(count_day_sql)
        return self.execute(count_channel_day_sql, commit=True)
