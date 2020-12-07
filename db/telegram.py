# coding: utf-8


from db.base import DBbase


"""
CREATE TABLE `sms_telegram` (
  `id` int(11) unsigned NOT NULL AUTO_INCREMENT,
  `chat_name` varchar(200) NOT NULL,
  `chat_id` varchar(200) NOT NULL,
  `chat_type` varchar(200) NOT NULL,
  `need_notice` tinyint(1) DEFAULT 0,
  `create_time` timestamp NULL DEFAULT CURRENT_TIMESTAMP,
  `is_have_authority` tinyint(1) DEFAULT 0,
  `is_active` tinyint(1) DEFAULT 1,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=1 DEFAULT CHARSET=utf8;
"""


class TelegramDB(DBbase):
    def __init__(self):
        super().__init__()

    def is_have_chat(self, chat_id):
        r = self.execute(f'select id from sms_telegram where chat_id="{chat_id}";', fetch=True)
        return True if r else False

    def add(self, chat_name, chat_id, chat_type):
        if self.is_have_chat(chat_id) is False:
            sql = f'insert into sms_telegram (chat_name,chat_id,chat_type) values ("{chat_name}","{chat_id}","{chat_type}");'
            r = self.execute(sql, commit=True)
            return '注册成功, 请联系管理员添加通知和创建权限!' if r else '创建失败!'
        return '请勿重复注册!'

    def get_auth_by_chatid(self, chat_id, only_auth=False, only_notice=False, need_all=True):
        if need_all:
            sql = f'select * from sms_telegram where chat_id="{chat_id}" and is_active=1;'
        elif only_auth:
            sql = f'select is_have_authority from sms_telegram where chat_id="{chat_id}" and is_active=1;'
        elif only_notice:
            sql = f'select need_notice from sms_telegram where chat_id="{chat_id}" and is_active=1;'
        r = self.execute(sql, fetch=True)
        return r[0] if r else []

    def get_channel_info(self):
        r = self.execute('select name,balance,is_active from sms_channel where need_display=1;', fetch=True)
        resp = ''
        for i in r:
            resp += f'通道: {i[0]}, 余额: {i[1]}, 状态:{"开启" if i[2] else "关闭"}\n'
        return resp[:-1]

    def get_plateform_info(self, need_handle_message=True):
        r = self.execute('select name,balance,is_active from sms_plateform;', fetch=True)
        if need_handle_message:
            resp = ''
            for i in r:
                resp += f'平台: {i[0]}, 余额: {i[1]}, 状态: {"开启" if i[2] else "关闭"}\n'
            resp = resp[:-1]
        else:
            resp = [[i[0]] for i in r]
        return resp

    def show_nobalance_channel(self):
        sql = 'select name,balance,notice_limit_balance from sms_channel where need_display=1 and need_notice_telegram=1 and balance<=notice_limit_balance;'
        r = self.execute(sql, fetch=True)
        resp = ''
        for i in r:
            if i:
                resp += f'{i[0]}的余额为{i[1]}已不足{i[2]}, 请及时充值!\n'
        return resp[:-1]

    def get_notice(self):
        r = self.execute('select chat_id from sms_telegram where need_notice=1 and is_active=1;', fetch=True)
        return r if r else []

    def update_chat(self, chat_id, new_chat_name):
        return self.execute(f'update sms_telegram set chat_name="{new_chat_name}" where chat_id="{chat_id}";', commit=True)

    def recharge_plateform(self, amount, plateform):
        plateform_id = self.execute(f'select id from sms_plateform where name="{plateform}";', fetch=True)
        if plateform_id:
            balance_sql = f'select balance from sms_plateform where id={plateform_id[0][0]};'
            balance_before = self.execute(balance_sql, fetch=True)[0][0]

            sql = f'update sms_plateform set balance=balance+{amount} where id={plateform_id[0][0]};'
            self.execute(sql, commit=True)
            balance_after = self.execute(balance_sql, fetch=True)[0][0]

            sql = f'insert into sms_recharge (plateform_id,balance_before,balance_after,recharge_amount) ' \
                  f'values ({plateform_id[0][0]},{balance_before},{balance_after},{amount});'
            if int(balance_after) >= 1:
                self.execute(f'update sms_control set run=1 where plateform_id={plateform_id[0][0]};')
            return (balance_after, True) if self.execute(sql, commit=True) else (0, False)
        return (0, False)

    def mute_notice(self, chat_id):
        return self.execute(f'update sms_telegram set need_notice=0 where chat_id="{chat_id}";', commit=True)

