from util.handle_nginx import NginxApi
from config import Sql, Page
from db.base import DBbase


"""
CREATE TABLE `sms_plateform` (
  `id` int(11) unsigned NOT NULL AUTO_INCREMENT,
  `name` char(50) NOT NULL,
  `create_time` timestamp NULL DEFAULT CURRENT_TIMESTAMP,
  `domain` char(20) NOT NULL,
  `balance` decimal(15,2) DEFAULT 0.00,
  `need_white_list` tinyint(1) DEFAULT 0,
  `is_active` tinyint(1) DEFAULT 1,
  `nginx_file_name` char(50) NOT NULL,
  `kl_limit` int(11) default 3000,
  `kl` int(11) default 10,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
"""


class PlateformDB(DBbase):
    """发送历史数据表管理"""
    def __init__(self):
        super().__init__()

    def search_plateform_rate_by_channel(self, channel_id, plateform_id):
        rate_sql = f'select rate from sms_rate where plateform_id={plateform_id} and channel_id={channel_id};'
        price = self.execute(rate_sql, fetch=True)
        return price[0][0] if price else 0

    def get_plateform_name(self, user_id):
        sql = f'select name from sms_plateform where id=(select plateform_id from sms_users where id="{user_id}")'
        r = self.execute(sql, fetch=True)
        return r[0][0]

    def yunying_get_plateform_id(self, domain):
        sql = f'select id from sms_plateform where domain="{domain}";'
        _id = self.execute(sql, fetch=True)
        return _id[0][0]

    def search_nobalance_plateform(self):
        plid_list = self.execute('select id,balance from sms_plateform;', fetch=True)
        rate_sql = 'select max(sms_rate.rate) from sms_channel inner join sms_rate on ' \
                   'sms_rate.channel_id=sms_channel.id where plateform_id=%s;'
        nobalance_plateform_list = []
        for i in plid_list:
            if i:
                min_rate = self.execute(rate_sql % i[0], fetch=True)[0][0]
                if i[1] < round(float(min_rate), 2):
                    nobalance_plateform_list.append(i[0])
        return nobalance_plateform_list

    def search_all_plateform(self):
        r = self.execute(f'select id from sms_plateform;', fetch=True)
        return [i[0] for i in r] if r else []

    def search_balance(self, user_id):
        plateform_id_sql = f'(select plateform_id from sms_users where id="{user_id}")'
        sql = f'select balance from sms_plateform where id={plateform_id_sql};'
        r = self.execute(sql, fetch=True)
        return round(float(r[0][0]), 2) if r else 0

    def search_balance_rate(self, user_id=None, plateform_id=None):
        """
        查询平台余额
        :return: true/false
        """
        rate_sql = 'select max(sms_rate.rate) from sms_channel inner join sms_rate on ' \
                   'sms_rate.channel_id=sms_channel.id where plateform_id={};'
        if user_id:
            plateform_id_sql = f'(select plateform_id from sms_users where id="{user_id}")'
            rate_sql = rate_sql.format(plateform_id_sql)
            sql = f'select balance from sms_plateform where id={plateform_id_sql};'
        elif plateform_id:
            rate_sql = rate_sql.format(plateform_id)
            sql = f'select balance from sms_plateform where id={plateform_id};'

        r = self.execute(rate_sql, fetch=True)
        rate = round(float(r[0][0]), 2) if r else 0
        _ = self.execute(sql, fetch=True)
        balance = round(float(_[0][0]), 2) if _ else 0
        return balance, rate

    def search_page(self, plateform_name=None, limit=Page.plateform_limit):
        if plateform_name:
            sql = f'select count(id) from sms_plateform where name like "%{plateform_name}%";'
        else:
            sql = 'select count(id) from sms_plateform;'
        num = self.execute(sql, fetch=True)
        num = num[0][0] if num else 0
        page_list = [i + 1 for i in range(int(num) // limit)]
        page_list = page_list if page_list else [1]
        if int(num) > limit and (int(num) % limit != 0):
            page_list.append(page_list[-1] + 1)
        return page_list, int(num)

    def search_plateform_info(self, page, plateform_name=None, limit=Page.plateform_limit, need_limit=True):
        # 总后台使用
        if need_limit:
            if plateform_name:
                sql = 'select id,name,create_time,balance,domain,is_active from sms_plateform where name ' \
                      f'like "%{plateform_name}%" limit {page * limit if page else 0},{limit};'
            else:
                sql = f'select id,name,create_time,balance,domain,is_active from sms_plateform ' \
                      f'limit {page * limit if page else 0},{limit};'
        else:
            sql = 'select id,name from sms_plateform;'
        r = self.execute(sql, fetch=True)
        rate_sql = 'select sms_rate.id,sms_channel.name,sms_rate.rate from sms_channel inner join ' \
                   'sms_rate on sms_rate.channel_id=sms_channel.id where plateform_id=%s and need_display=1;'
        data = []
        for i in r:
            if i:
                rate = self.execute(rate_sql % i[0], fetch=True)
                rate_list = [{'rate_id': ra[0], 'channel_name': ra[1], 'rate': round(float(ra[2]), 2)} for ra in rate]
                if need_limit:
                    data.append({'id': i[0], 'name': i[1], 'create_time': i[2].strftime('%Y-%m-%d %H:%M:%S'),
                        'rate_list': rate_list, 'balance': round(float(i[3]), 2), 'domain': i[4], 'is_active': i[5]})
                else:
                    data.append({'id': i[0], 'name': i[1]})
        return data

    def backstage_update_plateform_info(self, plateform_id, name, domain, is_active, rate_list):
        # 总后台使用
        dn = self.execute(f'select domain,nginx_file_name from sms_plateform where id={plateform_id};', fetch=True)[0]
        nginx_file, old_domain = dn[1], dn[0]
        if old_domain != domain:
            new_nginx_file = NginxApi.update_conf_file(domain, nginx_file)
        else:
            new_nginx_file = nginx_file
        sql = f'update sms_plateform set name="{name}",domain="{domain}",nginx_file_name="{new_nginx_file}",' \
              f'is_active={is_active} where id={plateform_id};'
        self.execute(sql, commit=True)
        for i in rate_list:
            self.execute(f'update sms_rate set rate={i["rate"]} where id={i["rate_id"]};', commit=True)
        return True

    def backstage_create_plateform(self, name, domain):
        # 总后台使用
        nginx_file = NginxApi.create_new_conf_file(domain)
        # 创建平台
        sql = f'insert into sms_plateform (name,domain,nginx_file_name) values ("{name}","{domain}","{nginx_file}");'
        self.execute(sql, commit=True)
        # 获取平台id
        plateform_id = self.execute('SELECT LAST_INSERT_ID();', fetch=True)[0][0]
        # 创建平台控制
        control_sql = f'insert into sms_control (name,plateform_id,run) values ("main",{plateform_id},0);'
        # 查看所有通道id
        channel = self.execute('select id from sms_channel;', fetch=True)

        rate_sql = 'insert into sms_rate (channel_id,plateform_id) values ({cid},{pid});'
        channel_statistics_sql = 'insert into sms_channel_statistics (channel_id,plateform_id) values ({cid},{pid});'
        cache_statistics_sql = 'insert into sms_cache_all_statistics (channel_id,plateform_id) values ({cid},{pid});'
        for i in channel:
            if i:
                # 创建费率
                self.execute(rate_sql.format(cid=i[0], pid=plateform_id))
                # 添加各个平台的每一个通道的统计信息
                self.execute(channel_statistics_sql.format(cid=i[0], pid=plateform_id))
                # 添加缓存统计
                self.execute(cache_statistics_sql.format(cid=i[0], pid=plateform_id))
        all_statistics_sql = f'insert into sms_all_statistics (plateform_id) values ({plateform_id});'
        # 创建平台成功表
        self.execute(Sql.plateform_success_sql.format(plateform_id))
        # 创建平台失败表
        self.execute(Sql.plateform_failure_sql.format(plateform_id))
        # 创建平台缓存表
        self.execute(Sql.plateform_cache_sql.format(plateform_id))
        # 添加平台总统计信息
        self.execute(all_statistics_sql)
        # 创建平台按天统计信息表
        self.execute(Sql.allday_table_sql.format(plateform_id))
        self.execute(Sql.channelday_table_sql.format(plateform_id))
        # 创建平台控制表并提交
        return self.execute(control_sql, commit=True)

    def backstage_recharge_by_id(self, amount, plateform_id):
        # 总后台使用
        balance_sql = f'select balance from sms_plateform where id={plateform_id};'
        balance_before = self.execute(balance_sql, fetch=True)[0][0]

        sql = f'update sms_plateform set balance = balance + {amount} where id={plateform_id};'
        self.execute(sql, commit=True)
        balance_after = self.execute(balance_sql, fetch=True)[0][0]

        sql = f'insert into sms_recharge (plateform_id,balance_before,balance_after,recharge_amount) ' \
              f'values ({plateform_id},{balance_before},{balance_after},{amount});'
        if int(balance_after) >= 1:
            self.execute(f'update sms_control set run=1 where plateform_id={plateform_id};')
        return self.execute(sql, commit=True)
