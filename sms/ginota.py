# coding: utf-8
# 106号段，作废
#

from sms.base import SmsBase
from util.common import is_right_china_number
from urllib.parse import quote
from config import Price, SmsApi
import requests
import time


class Ginota(SmsBase):
    def __init__(self):
        self.api_key = SmsApi.ginota_key
        self.api_secret = SmsApi.ginota_secret

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
        text = '【CODE】' + text
        new_number = '86' + to_number
        url = f'https://www.ginota.com/gemp/sms/json?' \
              f'apiKey={self.api_key}&' \
              f'apiSecret={self.api_secret}&' \
              f'srcAddr=SMS&dstAddr={new_number}&' \
              f'content={quote(text)}'
        print(url)
        try:
            r = requests.get(url)
            if r:
                j = r.json()
                print(j)
                result['err'] = j['status']
                result['err_text'] = j['desc']
                result['price'] = Price.ginota
                result['message_id'] = j['messageId'] if j.get('messageId') else 0
                if result['err'] is None or result['err'] == '0':
                    result['err'] = 0
                if result['err'] == '4':
                    result['err'] = 0

                # 如果余额不足 则等待30s重发
                if result['err_text'] == 'AccessDenied':
                    print('余额不足，等待30s后重发本条...')
                    time.sleep(30)
                    return self.send(seq, to_number, text)
        except Exception as e:
            print(e)
        return result


if __name__ == '__main__':
    c = Ginota()
    print(c.get_balance())
    print(c.send('1111111', '一二三四五六七八九十一二三四五六七八九十一二三四五六七八九十一二三四五六七八九十一二三四五六七八九十一二三四五六七八九十'))
