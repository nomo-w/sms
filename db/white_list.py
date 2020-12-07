# coding: utf-8

from db.base import DBbase
from config import Page

"""
CREATE TABLE `sms_whitelist` (
  `id` int(11) unsigned NOT NULL AUTO_INCREMENT,
  `ip` char(15) DEFAULT NULL,
  `memo` char(20) DEFAULT NULL,
  `plateform_id` int(11) NOT NULL,
  `create_time` timestamp NULL DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=5 DEFAULT CHARSET=utf8;
"""


class WhiteList(DBbase):
    """白名单管理"""
    def __init__(self):
        super().__init__()

    def add(self, ip, memo, user_id):
        if not self.is_white_ip(ip, user_id=user_id):
            plateform_id_sql = f'(select plateform_id from sms_users where id={user_id})'
            sql = f'insert into sms_whitelist (ip,memo,plateform_id) values ("{ip}","{memo}",{plateform_id_sql});'
            self.execute(sql, commit=True)
            return '添加成功!'
        return '请勿重复添加!'

    def del_ip_by_id(self, whitelist_id):
        sql = f'delete from sms_whitelist where id={whitelist_id};'
        self.execute(sql, commit=True)
        return '删除成功!'

    def is_white_ip(self, ip, url=None, user_id=None, plateform_id=None):
        plateform_id_sql = f'(select plateform_id from sms_users where id={user_id})'
        if url:
            r = self.execute(f'select id from sms_plateform where need_white_list=1 and domain="{url}";', fetch=True)
            if r:
                sql = f'select id from sms_whitelist where plateform_id={r[0][0]} and ip="{ip}";'
            else:
                return True
        elif user_id:
            sql = f'select id from sms_whitelist where plateform_id={plateform_id_sql} and ip="{ip}";'
        elif plateform_id:
            sql = f'select id from sms_whitelist where plateform_id={plateform_id} and ip="{ip}";'
        return self.execute(sql)

    def get_white_ip_status(self, user_id=None, plateform_id=None):
        if user_id is not None:
            plateform_id = f'(select plateform_id from sms_users where id={user_id})'
        sql = f'select need_white_list from sms_plateform where id={plateform_id};'
        r = self.execute(sql, fetch=True)
        return r[0][0] if r else 0

    def change_ip_status(self, status, user_id=None, plateform_id=None):
        if user_id is not None:
            plateform_id = f'(select plateform_id from sms_users where id={user_id})'
        sql = f'update sms_plateform set need_white_list={status} where id={plateform_id};'
        return self.execute(sql, commit=True)

    def search_page(self, user_id=None, plateform_id=None, limit=Page.white_ip_limit):
        if user_id is not None:
            plateform_id = f'(select plateform_id from sms_users where id={user_id})'
        num = self.execute(f'select count(id) from sms_whitelist where plateform_id={plateform_id};', fetch=True)
        num = num[0][0] if num else 0
        page_list = [i + 1 for i in range(int(num) // limit)]
        page_list = page_list if page_list else [1]
        if int(num) > limit and (int(num) % limit != 0):
            page_list.append(page_list[-1] + 1)
        return page_list, int(num)

    def get_all_ip(self, page, user_id=None, plateform_id=None, limit=Page.white_ip_limit):
        if user_id is not None:
            plateform_id = f'(select plateform_id from sms_users where id={user_id})'
        sql = f'select id,ip,memo,create_time from sms_whitelist where plateform_id={plateform_id} limit {page * limit if page else 0},{limit};'
        r = self.execute(sql, fetch=True)
        data = []
        for i in r:
            if i:
                data.append({
                    'id': i[0],
                    'ip': i[1],
                    'memo': i[2],
                    'create_time': i[3].strftime('%Y-%m-%d %H:%M:%S')
                })
        return data

    def backstage_add_whitelist(self, ip, memo, plateform_id):
        if not self.is_white_ip(ip, plateform_id=plateform_id):
            sql = f'insert into sms_whitelist (ip,memo,plateform_id) values ("{ip}","{memo}",{plateform_id});'
            self.execute(sql, commit=True)
            return '添加成功!'
        return '请勿重复添加!'

    def backstage_del_whitelist(self, whitelist_id):
        sql = f'delete from sms_whitelist where id={whitelist_id};'
        return self.execute(sql, commit=True)


# test
if __name__ == '__main__':
    with WhiteList() as db:
        print(db.del_ip_by_ip('1.1.1.1'))
        print(db.add('1.1.1.1', 'test1'))  # True
        print(db.is_white_ip('0.0.0.0'))  # False
        print(db.is_white_ip('1.1.1.1'))  # True
        print(db.get_all_ip())

