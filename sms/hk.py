# coding: utf-8
#
#
from sms.base import SmsBase
from util.common import is_right_china_number
from config import Price
import requests
import time
import re


class Hk(SmsBase):
    def __init__(self):
        self.userid = 336
        self.account = '2977011587'
        self.password = 'asd@***0085'

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

        url = "http://118.190.211.56:8088/sms.aspx"
        data = dict(userid=self.userid, account=self.account, password=self.password, sendTime='', mobile=to_number,
                    content=text, action='send')
        try:
            r = requests.post(url, data=data, timeout=20)
            if r:
                print(r.text)
                status = re.findall('<returnstatus>(.*?)</returnstatus>', r.text)[0]
                msg = re.findall('<message>(.*?)</message>', r.text)[0]
                mid = re.findall('<taskID>(.*?)</taskID>', r.text)[0]
                if status == 'Success':
                    result['err'] = 0
                    result['price'] = Price.hk
                else:
                    result['err'] = 1
                    result['price'] = 0
                result['err_text'] = msg
                result['message_id'] = mid
                print('result: ', result)

                # 如果余额不足 则等待30s重发
                if result['err'] == 1:
                    print('错误:%s，等待30s后重发本条...' % result['err_text'])
                    time.sleep(30)
                    return self.send(seq, to_number, text)
        except Exception as e:
            print(e)
        return result


if __name__ == '__main__':
    c = Hk()
