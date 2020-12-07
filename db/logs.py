# coding: utf-8

from db.base import DBbase
from config import Page

"""
CREATE TABLE `logs` (
  `id` int(11) unsigned NOT NULL AUTO_INCREMENT,
  `operation` int(11) DEFAULT NULL,
  `user` char(20) DEFAULT NULL,
  `time` timestamp NULL DEFAULT CURRENT_TIMESTAMP,
  `ip` char(16) DEFAULT NULL,
  `memo` char(50) DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=36 DEFAULT CHARSET=utf8;
"""


class LogDB(DBbase):
    """日志管理"""
    def __init__(self):
        super().__init__()

    def get_all_logs(self, page_id):
        sql = f'select * from logs order by time DESC limit {page_id * Page.count},{Page.count}'
        return self.execute(sql, fetch=True)

    def add(self, operation, opera_user, ip, memo):
        sql = f'insert into logs (operation,user,ip,memo) values ({operation},"{opera_user}","{ip}","{memo}")'
        return self.execute(sql, commit=True)


# test
if __name__ == '__main__':
    with LogDB() as db:
        print(db.add(1, '234', '1.1.1.1', ''))
        print(db.get_all_logs(0))
