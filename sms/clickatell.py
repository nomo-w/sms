# coding: utf-8
#
# setup : pip install nexmo
#

from sms.base import SmsBase
from util.common import is_right_china_number
from config import Price, SmsApi
import requests
import time

clickatell_key = SmsApi.clickatell_key


class Clickatell(SmsBase):
    def __init__(self):
        self.api_key = clickatell_key

    def get_balance(self, channel_type=''):
        """
        获取余额
        :return: {'value': 8.9672, 'autoReload': False}
        """
        return {'value': 10, 'autoReload': True}

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
        new_number = '86' + to_number
        url = f"https://xxxxxxxx.xxxxxxx.com/messages/http/send?apiKey={self.api_key}&to={new_number}&content={text}"
        try:
            r = requests.get(url)
            if r:
                j = r.json()
                print(j)
                if j['messages']:
                    result['err'] = j['messages'][0]['errorCode']
                    result['err_text'] = j['messages'][0]['error']
                    result['message_id'] = j['messages'][0]['apiMessageId']
                else:
                    result['err'] = j['errorCode']
                    result['err_text'] = j['error']
                    result['message_id'] = '0'
                result['price'] = Price.clickatell
                if result['err'] is None:
                    result['err'] = 0

                # 如果余额不足 则等待30s重发
                if result['err'] == 301:
                    print('余额不足，等待30s后重发本条...')
                    time.sleep(30)
                    return self.send(seq, to_number, text)
        except Exception as e:
            print(e)
        return result


if __name__ == '__main__':
    c = Clickatell()
    print(c.get_balance())
    print(c.send('13211111111', 'welcome to my channel!'))
