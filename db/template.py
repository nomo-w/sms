# coding: utf-8


from config import Page
from db.base import DBbase
from pymysql import escape_string


"""
CREATE TABLE `sms_template` (
  `id` int(11) unsigned NOT NULL AUTO_INCREMENT,
  `template` varchar(250) NOT NULL,
  `status` varchar(200) DEFAULT 'PENDING',
  `channel_id` int(11) NOT NULL,
  `plateform_id` int(11) NOT NULL,
  `is_active` tinyint(1) DEFAULT 1,
  `template_id` varchar(200) DEFAULT 0,
  `create_time` timestamp NULL DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
"""


class TemplateDB(DBbase):
    """发送模板管理"""
    def __init__(self):
        super().__init__()

    def search_page(self, user_id=None, limit=Page.template_limit):
        if user_id is not None:
            plateform_id_sql = f'(select plateform_id from sms_users where id={user_id})'
            sql = f'select count(id) from sms_template where plateform_id={plateform_id_sql} and is_active=1;'
        else:
            sql = f'select count(id) from sms_template where is_active=1;'
        num = self.execute(sql, fetch=True)
        num = num[0][0] if num else 0
        page_list = [i + 1 for i in range(int(num) // limit)]
        page_list = page_list if page_list else [1]
        if int(num) > limit and (int(num) % limit != 0):
            page_list.append(page_list[-1] + 1)
        return page_list, int(num)

    def search_all_template(self, page, user_id=None, limit=Page.template_limit):
        if user_id is not None:
            plateform_id_sql = f'(select plateform_id from sms_users where id={user_id})'
            sql = 'select id,template,status,create_time,(select name from sms_channel where id=channel_id) as ' \
                  f'channel_name from sms_template where plateform_id={plateform_id_sql} and is_active=1 ' \
                  f'limit {page * limit if page else 0},{limit};'
        else:
            sql = 'select id,template,status,create_time,(select name from sms_channel where id=channel_id) as ' \
                  'channel_name,(select name from sms_plateform where id=plateform_id) as plateform_name from ' \
                  f'sms_template where is_active=1 limit {page * limit if page else 0},{limit};'
        r = self.execute(sql, fetch=True)
        data = []
        for i in r:
            if i:
                if user_id is not None:
                    _ = {
                        'id': i[0],
                        'template': i[1],
                        'status': i[2],
                        'create_time': i[3].strftime('%Y-%m-%d %H:%M:%S'),
                        'channel_name': i[4]
                    }
                else:
                    _ = {
                        'id': i[0],
                        'template': i[1],
                        'status': i[2],
                        'create_time': i[3].strftime('%Y-%m-%d %H:%M:%S'),
                        'channel_name': i[4],
                        'plateform_name': i[5]
                    }
                data.append(_)
        return data

    def is_have_template(self, template, channel_id, plateform_id=None, user_id=None):
        new_template = escape_string(template)
        is_have_sql = f'select id from sms_template where channel_id={channel_id} and template="{new_template}" and plateform_id=' \
                      f'{f"(select plateform_id from sms_users where id={user_id})" if user_id is not None else plateform_id}'
        return True if self.execute(is_have_sql, fetch=True) else False

    def add(self, channel_id, template, template_id, plateform_id=None, user_id=None):
        new_template = escape_string(template)
        if user_id is not None:
            plateform_id_sql = f'(select plateform_id from sms_users where id={user_id})'
            sql = f'insert into sms_template (template,channel_id,plateform_id,template_id) values (' \
                  f'"{new_template}",{channel_id},{plateform_id_sql},"{template_id}");'
        elif plateform_id is not None:
            sql = f'insert into sms_template (template,channel_id,plateform_id,template_id) values (' \
                  f'"{new_template}",{channel_id},{plateform_id},"{template_id}");'
        return '创建成功!' if self.execute(sql, commit=True) else '创建失败!'

    def delete_by_id(self, templates_id):
        for i in templates_id.split(','):
            sql = f'delete from sms_template where id={i};'
            r = self.execute(sql)
        self.commit()
        return r

    def delete_by_plateform(self, user_id, template_id, commit=True):
        plateform_id_sql = f'(select plateform_id from sms_users where id={user_id})'
        sql = f'delete from sms_template where id={template_id} and plateform_id={plateform_id_sql};'
        return self.execute(sql, commit=commit)

    def show_template_by_ChannelPlateform(self, channel_id, user_id):
        plateform_id_sql = f'(select plateform_id from sms_users where id="{user_id}")'
        sql = f'select template from sms_template where channel_id={channel_id} and ' \
              f'plateform_id={plateform_id_sql} and status="SUCCESS";'
        r = self.execute(sql, fetch=True)
        return [i[0] for i in r] if r else []

    def update_status(self, template_id, status):
        sql = f'update sms_template set status="{status}" where template_id="{template_id}";'
        return self.execute(sql, commit=True)

