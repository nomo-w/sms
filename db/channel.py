# 短信通道数据库
from db.base import DBbase

"""
CREATE TABLE `sms_channel` (
  `id` int(11) unsigned NOT NULL AUTO_INCREMENT,
  `name` char(50) DEFAULT NULL,
  `balance` decimal(15,2) DEFAULT 0.00,
  `create_time` timestamp NULL DEFAULT CURRENT_TIMESTAMP,
  `is_have_danfa` tinyint(1) DEFAULT 1,
  `is_have_qunfa` tinyint(1) DEFAULT 1,
  `is_active` tinyint(1) DEFAULT 1,
  `max_send` int(11) DEFAULT 1,
  `min_send` int(11) DEFAULT 1,
  `channel_type` char(10) NOT NULL,
  `description` char(255) DEFAULT '',
  `need_get_result` tinyint(1) DEFAULT 0,
  `max_text_len` int(11) DEFAULT 60,
  `need_display` tinyint(1) DEFAULT 1,
  `need_template` tinyint(1) DEFAULT 0,
  `need_notice_telegram` tinyint(1) DEFAULT 0,
  `notice_limit_balance` int(11) DEFAULT 20000,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
"""


class ChannelDB(DBbase):
    """发送历史数据表管理"""

    def __init__(self):
        super().__init__()

    def show_need_template_channel(self):
        sql = 'select id,name,channel_type from sms_channel where is_active=1 and need_template=1;'
        r = self.execute(sql, fetch=True)
        return [{'id': i[0], 'name': i[1], 'channel_type': i[2]} for i in r] if r else []

    def need_get_result_channel(self):
        sql = 'select channel_type from sms_channel where need_get_result=1 and need_display=1;'
        return self.execute(sql, fetch=True)

    def yunying_is_hanve_channel(self, channel_id):
        sql = f'select id,channel_type from sms_channel where is_active=1 and id={channel_id};'
        _id = self.execute(sql, fetch=True)
        return _id[0] if _id else (-1, -1)

    def get_channel_balance(self, channel_id):
        sql = f'select balance from sms_channel where id={channel_id} and is_active=1;'
        r = self.execute(sql, fetch=True)
        return round(float(r[0][0]), 2) if r else 0

    def close_channel_by_id(self, channel_id):
        sql = f'update sms_channel set is_active=0 where id={channel_id};'
        return self.execute(sql, commit=True)

    def show_all_channel_info(self, user_id):
        plateform_id_sql = f'(select plateform_id from sms_users where id={user_id})'
        sql = 'select sms_channel.id,sms_channel.name,sms_rate.rate,sms_channel.description,sms_channel.is_have_danfa,' \
              'sms_channel.need_template from sms_channel inner join sms_rate on sms_rate.channel_id=sms_channel.id ' \
              f'where sms_rate.plateform_id={plateform_id_sql} and sms_channel.is_active=1;'
        # sql = 'select id,name,rate,description,is_have_danfa from sms_channel where is_active=1;'
        r = self.execute(sql, fetch=True)
        if r:
            data = []
            for i in r:
                sensitive_sql = f'select sensitive_words from sms_sensitiveWords where is_active=1 and channel_id={i[0]};'
                s = self.execute(sensitive_sql, fetch=True)
                data.append({
                    'id': i[0],
                    'name': i[1],
                    'rate': round(float(i[2]), 2),
                    'description': i[3].split('\n'),
                    'sensitive_words': ','.join([sw[0] for sw in s]) if s else '',
                    'is_have_danfa': i[4],
                    'is_have_template': i[5]
                })
        else:
            data = []
        return data

    def show_all_channel(self):
        sql = 'select id,balance,channel_type from sms_channel where need_display=1;'
        r = self.execute(sql, fetch=True)
        return [(i[0], round(float(i[1]), 2), i[2]) for i in r] if r else []

    def show_channel_type(self, channel_id):
        sql = f'select channel_type,is_have_danfa,is_have_qunfa,max_send,min_send,max_text_len,additional_code,' \
              f'need_report from sms_channel where id={channel_id} and is_active=1;'
        r = self.execute(sql, fetch=True)
        return r[0] if r else ('', '', '', '', '', '', '', '')

    def update_balance(self, balance, channel_id=None, channel_type=None):
        sql = f'update sms_channel set balance={balance} where '
        if channel_id:
            sql += f'id={channel_id};'
        elif channel_type:
            sql += f'channel_type="{channel_type}";'
        return self.execute(sql, commit=True)

    def backstage_show_all_channel(self):
        # 总平台使用
        sql = 'select id,name,balance,description,is_active from sms_channel where need_display=1;'
        r = self.execute(sql, fetch=True)
        data = []
        for i in r:
            if i:
                data.append({
                    'id': i[0],
                    'name': i[1],
                    'balance': round(float(i[2]), 2),
                    'description': i[3],
                    'is_active': i[4]
                })
        return data

    def backstage_update_channel(self, channel_id, name, des, is_active):
        # 总平台使用
        sql = f'update sms_channel set name="{name}",description="{des}",is_active={is_active} where id={channel_id};'
        return self.execute(sql, commit=True)

    def backstage_show_need_template_channel(self):
        sql = 'select id,name,channel_type from sms_channel where need_display=1 and need_template=1;'
        r = self.execute(sql, fetch=True)
        return [{'id': i[0], 'name': i[1], 'channel_type': i[2]} for i in r] if r else []

