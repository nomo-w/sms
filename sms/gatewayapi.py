# coding: utf-8
# 106号段，发几个就封号了噢
#
from sms.base import SmsBase
from util.common import is_right_china_number
from config import Price
import requests
import time


class GatewayApi(SmsBase):
    def __init__(self):
        self.api_key = 'Wfp8JN54TPSaq2FkDKfMOZXHvoT9iwzMXVyoNZn5dD2T81qqbdH_yf40joRFX9Lv'

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

        # 要加 这个  还要审核 不能有特殊字
        text = '[CODE] ' + text
        new_number = '86' + to_number
        url = 'https://gatewayapi.com/rest/mtsms'
        req = {
            'sender': 'ExampleSMS',
            'message': text,
            'encoding': 'UCS2',
            'recipients': [{'msisdn': new_number}],
        }
        ss = requests.session()
        ss.auth = (self.api_key, '')

        try:
            r = ss.post(url, json=req)
            if r:
                j = r.json()
                print(j)
                result['err'] = 0
                result['err_text'] = 'ok'
                result['price'] = Price.plivo
                result['message_id'] = j['ids'][0] if j.get('ids') else 0
            else:
                # 如果余额不足 则等待30s重发
                print('错误？ 等待30s后重发本条...')
                time.sleep(30)
                return self.send(seq, to_number, text)
        except Exception as e:
            print(e)
        return result


if __name__ == '__main__':
    c = GatewayApi()
    print(c.send('13111112222', '6-谁让我爱恨两难!!!! www.baidu.com'))
