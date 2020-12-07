from db.base import DBbase


class NewChannelEnvConf(DBbase):
    def __init__(self):
        super().__init__()

    def ncec(self, new_channel_id):
        for i in self.execute('select id from sms_plateform;', fetch=True):
            static_sql = f'insert into sms_channel_statistics (plateform_id,channel_id) values ({i[0]},{new_channel_id});'
            rate_sql = f'insert into sms_rate (channel_id,plateform_id) values ({new_channel_id},{i[0]});'
            self.execute(static_sql)
            self.execute(rate_sql)
        self.commit()
        
        
if __name__ == '__main__':
    with NewChannelEnvConf() as db:
        ncid = int(input('请输入新建通道的id号: '))
        db.ncec(ncid)
