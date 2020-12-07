# coding: utf-8


from db.base import DBbase


"""
CREATE TABLE `sms_callback` (
  `id` int(11) unsigned NOT NULL AUTO_INCREMENT,
  `to_number` varchar(30) NOT NULL,
  `url` varchar(50) NOT NULL,
  `plateform_id` int(11) NOT NULL,
  `time` timestamp NULL DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
"""


class Callback(DBbase):
    """发送历史数据表管理"""
    def __init__(self):
        super().__init__()

    def add(self, to, url, plateform_id):
        sql = f'insert into sms_callback (to_number,url,plateform_id) values ("{to}","{url}",{plateform_id});'
        self.execute(sql, commit=True)
        r = self.execute('select last_insert_id();', fetch=True)
        return r[0][0]

    def show(self, _id):
        sql = f'select to_number,url,plateform_id from sms_callback where id={_id};'
        r = self.execute(sql, fetch=True)
        return r[0] if r else (None, None, None)

