# 短信费率数据库
from db.base import DBbase

"""
CREATE TABLE `sms_rate` (
  `id` int(11) unsigned NOT NULL AUTO_INCREMENT,
  `channel_id` int(11) NOT NULL,
  `plateform_id` int(11) NOT NULL,
  `rate` decimal(5,2) DEFAULT 0.36,
  `create_time` timestamp NULL DEFAULT CURRENT_TIMESTAMP,
  `is_active` tinyint(1) DEFAULT 1,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
"""


class RateDB(DBbase):
    """费率表"""

    def __init__(self):
        super().__init__()

    def add(self, plateform_id, channel_id=[]):
        if channel_id:
            for i in channel_id:
                sql = f'insert into sms_rate (channel_id,plateform_id) values ({i},{plateform_id});'
                self.execute(sql)
            return self.commit()

    def show(self, plateform_id, channel_id):
        sql = f'select rate from sms_rate where plateform_id={plateform_id} and channel_id={channel_id};'
        r = self.execute(sql, fetch=True)
        return r[0][0] if r else 0
