# coding: utf-8


from db.base import DBbase
from config import Page

"""
CREATE TABLE `sms_recharge` (
  `id` int unsigned NOT NULL AUTO_INCREMENT,
  `plateform_id` int(11) NOT NULL,
  `balance_before` decimal(15,2) NOT NULL,
  `balance_after` decimal(15,2) NOT NULL,
  `recharge_amount` decimal(15,2) NOT NULL,
  `recharge_time` timestamp NULL DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=31 DEFAULT CHARSET=utf8;
"""


class Recharge_Record(DBbase):
    """平台余额数据表管理"""
    def __init__(self):
        super().__init__()

    @classmethod
    def _recharge_record(cls, balance_before, balance_after, amount, user=None):
        """
        将充值记录写入充值记录表
        :param balance_before: 之前余额
        :param balance_after: 之后余额
        :param amount: 充值金额
        :param user: 用户
        :return: true/false
        """
        plateform_id_sql = f'(select plateform_id from sms_users where user="{user}")'
        sql = f'insert into sms_recharge (plateform_id, balance_before, balance_after, recharge_amount) ' \
              f'values ({plateform_id_sql},{balance_before},{balance_after},{amount});'
        return cls.execute(sql, commit=True)

    def search_page(self, start, end, user_id=None, plateform_id=None, limit=Page.recharge_record_limit):
        """
        处理充值记录页数。返回两个值，页数的列表[1, 2, ..] 总共条数20
        :param start: 开始时间
        :param end: 结束时间
        :param limit: 每页显示数
        :return: [1, 2, 3, ....], 65
        """
        if user_id is None and plateform_id is None:
            sql = 'select count(id) from sms_recharge where is_active=1'
        else:
            if user_id is not None:
                plateform_id = f'(select plateform_id from sms_users where id={user_id})'
            sql = f'select count(id) from sms_recharge where plateform_id={plateform_id} and is_active=1'
        if start and end:
            sql += f' and recharge_time>="{start} 00:00:00" and recharge_time<="{end} 23:59:59"'
        sql += ';'
        db_count = self.execute(sql, fetch=True)
        if db_count[0]:
            page_list = [i + 1 for i in range(db_count[0][0] // limit)]
            page_list = page_list if page_list else [1]
            if db_count[0][0] > limit and (db_count[0][0] % limit != 0):
                page_list.append(page_list[-1] + 1)
            return page_list, db_count[0][0]
        return [], 0

    def search_recharge_record(self, start, end, page, user_id=None, plateform_id=None, need_excel=None, limit=Page.recharge_record_limit):
        """
        查询充值记录
        :param start: 开始时间
        :param end: 结束时间
        :param page: 页数
        :param limit: 每页显示数
        :return: ((200.11, "2019-09-08 12:15:35", 200.22), ...)
        """
        if user_id is None and plateform_id is None:
            sql = 'select (select name from sms_plateform where id=plateform_id) as plateform_name,recharge_amount,' \
                  'recharge_time,balance_after from sms_recharge where is_active=1'
        else:
            if user_id is not None:
                sql = 'select recharge_amount,recharge_time,balance_after from sms_recharge where ' \
                      f'plateform_id=(select plateform_id from sms_users where id={user_id}) and is_active=1'
            else:
                sql = 'select (select name from sms_plateform where id=plateform_id) as plateform_name,recharge_amount,' \
                      f'recharge_time,balance_after from sms_recharge where plateform_id={plateform_id} and is_active=1'
        if start and end:
            sql += f' and recharge_time>="{start} 00:00:00" and recharge_time<="{end} 23:59:59"'
        if need_excel == 0:
            sql += ' order by recharge_time desc;'
        else:
            sql += ' order by recharge_time desc limit {},{};'.format(page * limit if page is not None else 0, limit)
        r = self.execute(sql, fetch=True)
        data = []
        for i in r:
            if i:
                if user_id is not None:
                    data.append({
                        'recharge_amount': round(float(i[0]), 2),
                        'recharge_time': i[1].strftime('%Y-%m-%d %H:%M:%S'),
                        'balance_after': round(float(i[2]), 2)
                    })
                else:
                    data.append({
                        'plateform_name': i[0],
                        'recharge_amount': round(float(i[1]), 2),
                        'recharge_time': i[2].strftime('%Y-%m-%d %H:%M:%S'),
                        'balance_after': round(float(i[3]), 2)
                    })
        return data


# test
if __name__ == '__main__':
    with Recharge_Record() as db:
        db.recharge('Jay', 150000.11)
