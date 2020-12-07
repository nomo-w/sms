# coding: utf-8
#
# setup : pip install nexmo
#

from sms.base import SmsBase
from config import Price, SmsApi
import nexmo as nexmoapi
from util.common import is_right_china_number

# configuration
nexmo_key = SmsApi.nexmo_key
nexmo_secret = SmsApi.nexmo_secret


class Nexmo(SmsBase):
    def __init__(self):
        self.client = nexmoapi.Client(key=nexmo_key, secret=nexmo_secret)

    def get_balance(self, channel_type=''):
        """
        获取余额
        :return: {'value': 8.9672, 'autoReload': False}
        """
        ret = {'value': 0, 'autoReload': False}
        try:
            r = self.client.get_balance()
            r = r.decode('utf-8').replace('false', 'False')
            print(r)
            r = dict(eval(r))
            print(r)
            ret['value'] = r['value']
            ret['autoReload'] = r['autoReload']
        except Exception as e:
            print(f'get_balance error: {e}')
        return ret

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
            # from 写 Nexmo  好像是以106 号段发送的?
            r = self.client.send_message({
                'from': '86' + to_number,
                'to': '86' + to_number,
                'text': text,
                'type': 'unicode',
            })
            print(r)
            result['price'] = Price.nexmo  # r['messages'][0].get('message-price')
            result['err'] = r['messages'][0].get('status')
            result['err_text'] = r['messages'][0].get('error-text')
            result['message_id'] = r['messages'][0].get('message-id')
        except Exception as e:
            print('Nexmo cath Exception : ', e)
        return result
