# coding: utf-8
#
# setup : pip install plivo
#

from sms.base import SmsBase
from util.common import is_right_china_number
import plivo as plivoapi
from config import Price, SmsApi

auth_id = SmsApi.plivo_id
auth_token = SmsApi.plivo_token


class Plivo(SmsBase):
    def __init__(self):
        self.auth_id = auth_id
        self.auth_token = auth_token
        self.client = plivoapi.RestClient(self.auth_id, self.auth_token)

    def get_balance(self, channel_type=''):
        """
        获取余额
        :return: {'value': 8.9672, 'autoReload': False}
        """
        value = self.client.account.get()['cash_credits']
        return dict(value=value, autoReload=False)

    def send(self, seq, to_number, text):
        """
        发送短信到指定号码
        注意：这里不验证号码和内容，只负责发送
        :param to_number: 要发送的电话号码  13800001111  不带86
        :param text: 短信内容，最多70个字符 (unicode)
        :return: dict(message_id='1231fi', to_number='xxxx',price='0.02820000',err=0/>0,err_text='Invalid Message Type')
        """
        result = dict(message_id='0', to_number=to_number, price='0', err='10', err_text='pending')
        if not is_right_china_number(to_number):
            result['status'] = 9
            result['err_text'] = 'error to-number'
            return result
        try:
            src_number = '+21' + to_number  # 不能为字母
            new_number = '+86' + to_number  # +8613111112222
            j = self.client.messages.create(src=src_number, dst=new_number, text=text)
            result['message_id'] = j['message_uuid'][0]
            # 暂时不获取状态，发过去就扣钱就是了
            # time.sleep(2)  # 等等再获取  'message_state': 'sent' / 'delivered',
            # response = self.client.messages.get(message_uuid=result['message_id'])
            # print(response)
            result['price'] = Price.plivo
            result['err'] = 0
            result['err_text'] = 'success'
        except Exception as e:
            print(e)
            result['err'] = 1
            result['err_text'] = 'error'
        print(result)
        return result


if __name__ == '__main__':
    c = Plivo()
    print(c.get_balance())
    print(c.send('13111111111', 'hello X,welcome to my channel!!!'))
