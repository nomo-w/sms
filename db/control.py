# coding: utf-8

from db.base import DBbase

"""
CREATE TABLE `sms_control` (
  `id` int(11) unsigned NOT NULL AUTO_INCREMENT,
  `name` char(10) DEFAULT NULL,
  `plateform_id` int(11) NOT NULL,
  `run` int(2) COMMENT '0-停止 / 1-启动',
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
"""
# insert into sms_control (name,run) values ('main',0)


class ControlDB(DBbase):
    """队列控制表"""
    def __init__(self):
        super().__init__()

    def is_running(self, user_id=None, plateform_id=None, username=None, domain=None):
        """
        是否正在运行
        :return: bool
        """
        if user_id:
            plateform_id_sql = f'(select plateform_id from sms_users where id={user_id})'
            sql = f'select run from sms_control where plateform_id={plateform_id_sql};'
        elif plateform_id:
            sql = f'select run from sms_control where plateform_id={plateform_id};'
        elif domain:
            plateform_id_sql = f'(select id form sms_plateform where domain="{domain}")'
            sql = f'select run from sms_channel where plateform_id={plateform_id_sql};'
        elif username:
            plateform_id_sql = f'(select plateform_id from sms_users where user="{username}")'
            sql = f'select run from sms_control where plateform_id={plateform_id_sql};'
        r = self.execute(sql, fetch=True)
        return r[0][0] if r else 0

    def set_run(self, status: int, user_id=None, plateform_id=None):
        """
        主开关
        :param status:  0-停止 / 1-启动
        :return: bool
        """
        if user_id:
            plateform_id_sql = f'(select plateform_id from sms_users where id={user_id})'
            sql = f'update sms_control set run={status} where plateform_id={plateform_id_sql};'
        elif plateform_id:
            sql = f'update sms_control set run={status} where plateform_id={plateform_id};'
        return self.execute(sql, commit=True)


# test
if __name__ == '__main__':
    with ControlDB() as db:
        print(db.set_run(0))
        print(db.is_running())
