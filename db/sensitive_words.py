# 敏感词数据库


from pymysql import escape_string
from db.base import DBbase
from config import Page


"""
CREATE TABLE `sms_sensitiveWords` (
  `id` int(11) unsigned NOT NULL AUTO_INCREMENT,
  `sensitive_words` varchar(200) NOT NULL,
  `channel_id` int(11) NOT NULL,
  `create_time` timestamp NULL DEFAULT CURRENT_TIMESTAMP,
  `is_active` tinyint(1) DEFAULT 1,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
"""


class SensitiveWordsDB(DBbase):
    """发敏感词数据表管理"""
    def __init__(self):
        super().__init__()

    def get_sensitive_words_by_channel(self, channel_id):
        sql = f'select sensitive_words from sms_sensitiveWords where is_active=1 and channel_id={channel_id};'
        r = self.execute(sql, fetch=True)
        return [i[0] for i in r] if r else []

    def search_page(self, channel_id, limit=Page.sensitive_limit):
        if channel_id is not None:
            sql = f'select count(id) from sms_sensitiveWords where is_active=1 and channel_id={channel_id};'
        else:
            sql = 'select count(id) from sms_sensitiveWords where is_active=1;'
        num = self.execute(sql, fetch=True)
        num = num[0][0] if num else 0
        page_list = [i + 1 for i in range(int(num) // limit)]
        page_list = page_list if page_list else [1]
        if int(num) > limit and (int(num) % limit != 0):
            page_list.append(page_list[-1] + 1)
        return page_list, int(num)

    def backstage_show_all_sensitive_words(self, channel_id, page, limit=Page.sensitive_limit):
        if channel_id is not None:
            sql = 'select id,sensitive_words,(select name from sms_channel where id=channel_id) as channel_name,' \
                  f'create_time from sms_sensitiveWords where is_active=1 and channel_id={channel_id} ' \
                  f'limit {page * limit if page else 0},{limit};'
        else:
            sql = 'select id,sensitive_words,(select name from sms_channel where id=channel_id) as channel_name,' \
                  f'create_time from sms_sensitiveWords where is_active=1 limit {page * limit if page else 0},{limit};'
        r = self.execute(sql, fetch=True)
        data = []
        for i in r:
            if i:
                data.append({
                    'id': i[0],
                    'sensitive_word': i[1],
                    'channel_name': i[2],
                    'create_time': i[3].strftime('%Y-%m-%d %H:%M:%S'),
                })
        return data

    def backstage_create_sensitive_words(self, channel_id, sensitive):
        for i in sensitive.split(','):
            new_sensitive = escape_string(i)
            if self.execute(f'select id from sms_sensitiveWords where channel_id={channel_id} and sensitive_words="{new_sensitive}";', fetch=True):
                r = True
                continue
            sql = f'insert into sms_sensitiveWords (channel_id,sensitive_words) values ({channel_id},"{new_sensitive}");'
            r = self.execute(sql)
        self.commit()
        return r

    def backstage_delete_sensitive_words(self, sensitive_id):
        for i in sensitive_id.split(','):
            sql = f'delete from sms_sensitiveWords where id={i};'
            r = self.execute(sql)
        self.commit()
        return r

