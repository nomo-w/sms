# coding: utf-8
# 用户数据库

import util.common
from db.base import DBbase


"""
CREATE TABLE `sms_users` (
  `id` int(11) unsigned NOT NULL AUTO_INCREMENT,
  `user` char(15) DEFAULT NULL,
  `password` char(32) DEFAULT NULL,
  `auth` char(20) DEFAULT NULL COMMENT 'admin / user',
  `create_time` timestamp NULL DEFAULT CURRENT_TIMESTAMP,
  `plateform_id` int(11) NOT NULL,
  `is_active` tinyint(1) DEFAULT 1,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
"""


class UserDB(DBbase):
    """管理用户表"""
    def __init__(self):
        super().__init__()

    def is_have_user(self, user, admin_id=None, plateform_id=None):
        """
        1.平台创建用户时查看是否已经存在该用户调用, admin_id/user
        """
        base_sql = f'select id from sms_users where user="{user}"'
        if admin_id:
            base_sql += f' and plateform_id=(select plateform_id from sms_users where id={admin_id})'
        elif plateform_id:
            base_sql += f'and plateform_id={plateform_id}'
        base_sql += ';'
        return self.execute(base_sql)

    def create_user(self, user, password, admin_id, auth: str = 'admin'):
        """
        平台创建用户调用   user, password, admin_id
        :param user:
        :param password:
        :param auth: 'admin' / 'user'
        :return:
        """
        if user and password and not self.is_have_user(user, admin_id):
            plateform_id_sql = f'(select * from ((select plateform_id from sms_users where id={admin_id}) tmp))'
            sql = f'insert into sms_users (user,password,auth,plateform_id) values ' \
                  f'("{user}","{util.common.md5(password)}","{auth}",{plateform_id_sql});'
            if self.execute(sql, commit=True):
                return '添加成功!'
            else:
                return '添加失败!'
        return '添加失败, 请更换用户名重试!'

    def get_auth(self, user_id):
        """
        返回当前用户的权限
        :param user:
        :return: 'admin' / 'user'
        """
        sql = f'select auth from sms_users where id={user_id};'
        r = self.execute(sql, fetch=True)
        return r[0][0] if r[0] else False

    def get_user_and_plateformid(self, user_id):
        sql = f'select id,kl_limit,kl,(select user from sms_users where id={user_id}) as user from sms_plateform ' \
              f'where id=(select plateform_id from sms_users where id={user_id});'
        r = self.execute(sql, fetch=True)
        return r[0] if r else (None, None, None, None)

    def del_user(self, user_id):
        sql = f'delete from sms_users where id={user_id};'
        if self.execute(sql, commit=True):
            return '成功删除!'
        return '删除失败!'

    def change_password(self, user_id, new_password):
        sql = f'update sms_users set password="{util.common.md5(new_password)}" where id={user_id};'
        return self.execute(sql, commit=True)

    def is_right_password(self, user, password, plateform_domain):
        """
        登录接口调用
        """
        plateform_sql = f'(select id from sms_plateform where domain="{plateform_domain}" and is_active=1)'
        sql = f'select id from sms_users where user="{user}" and ' \
              f'password="{util.common.md5(password)}" and plateform_id={plateform_sql};'
        _id = self.execute(sql, fetch=True)
        return _id[0][0] if _id else -1

    def get_all(self, user_id):
        """返回所有用户"""
        plateform_id_sql = f'(select plateform_id from sms_users where id={user_id})'
        sql = f'select id,user,auth,create_time from sms_users where is_active=1  and plateform_id={plateform_id_sql};'
        rs = self.execute(sql, fetch=True)
        return [{"id": r[0], "name": r[1], "auth": r[2], "create_time": r[3].strftime('%Y-%m-%d %H:%M:%S')} for r in rs]\
            if rs[0] else []

    def get_plateform_id(self, user_id):
        sql = f'select plateform_id from sms_users where id={user_id};'
        r = self.execute(sql, fetch=True)
        return r[0][0] if r else 0

    def backstage_get_users(self, plateform_id):
        # 总后台使用
        sql = f'select id,user,auth,create_time from sms_users where plateform_id={plateform_id};'
        r = self.execute(sql, fetch=True)
        data = []
        for i in r:
            if i:
                data.append({
                    'user_id': i[0],
                    'user_name': i[1],
                    'auth': i[2],
                    'create_time': i[3].strftime('%Y-%m-%d %H:%M:%S')
                })
        return data

        # plateform_sql = 'select id,name from sms_plateform;'
        # plateform = self.execute(plateform_sql, fetch=True)
        # data = []
        # for p in plateform:
        #     if p:
        #         data.append({'plateform_id': p[0], 'plateform_name': p[1], 'users': []})
        # sql = 'select id,user,auth,create_time,(select name from sms_plateform where id=plateform_id) as plateform,' \
        #       'plateform_id from sms_users where is_active=1;'
        # r = self.execute(sql, fetch=True)
        # for u in r:
        #     if u:
        #         for i in range(len(data)):
        #             if data[i]['plateform_id'] == u[5]:
        #                 data[i]['plateform_name'] = u[4]
        #                 data[i]['users'].append({
        #                     'user_id': u[0],
        #                     'user_name': u[1],
        #                     'auth': u[2],
        #                     'create_time': u[3].strftime('%Y-%m-%d %H:%M:%S')
        #                 })
        # return data

    def is_superuser(self, usr=None, pwd=None, user_id=None):
        # 总后台使用
        if user_id:
            sql = f'select id from sms_users where id={user_id} and auth="superuser";'
        else:
            sql = f'select id from sms_users where auth="superuser" and user="{usr}" and password="{util.common.md5(pwd)}";'
        _id = self.execute(sql, fetch=True)
        return _id[0][0] if _id else -1

    def backstage_create_user(self, usr, pwd, auth, plateform_id):
        # 总后台使用
        if not self.is_have_user(usr, plateform_id=plateform_id):
            sql = f'insert into sms_users (user,password,auth,plateform_id) values ' \
                  f'("{usr}","{util.common.md5(pwd)}","{auth}",{plateform_id});'
            if self.execute(sql, commit=True):
                return '添加成功!'
            else:
                return '添加失败!'
        return '添加失败, 请更换用户名重试!'


# test
if __name__ == '__main__':
    with UserDB() as db:
        print(db.del_user('234'))
        print(db.create_user('234', '123456'))
        print(db.get_auth('234'))
        print(db.is_right_password('234', '123'))
        print(db.is_right_password('234', '123456'))
