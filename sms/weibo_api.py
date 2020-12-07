from util.api import my_requests
from db.channel import ChannelDB
from util.common import sign_
from config import WB

import random
import time


class WeiBo:
    @staticmethod
    def send(_id, to_number, text):
        timestamp = f'{time.strftime("%Y%m%d%H%M%S", time.localtime())}{random.randint(100, 999)}'
        sign = f'{WB.enterprise_no}{WB.account}{timestamp}{WB.key}'
        data = {
            "enterprise_no": WB.enterprise_no,
            "account": WB.account,
            "phones": to_number,
            "content": text,
            "subcode": "0",
            "sendtime": timestamp[:-5],
            "timestamp": timestamp,
            "sign": sign_(sign)
        }
        resp = my_requests(WB.send_url, 'post', data, need_json_params=True)
        return resp if resp is not None else {}

    @staticmethod
    def get_balance():
        timestamp = f'{time.strftime("%Y%m%d%H%M%S", time.localtime())}{random.randint(100, 999)}'
        sign = f'{WB.enterprise_no}{WB.account}{timestamp}{WB.key}'
        data = {
            "enterprise_no": WB.enterprise_no,
            "account": WB.account,
            "timestamp": timestamp,
            "sign": sign_(sign)
        }
        resp = my_requests(WB.balance_url, 'post', data, need_json_params=True)
        if resp is not None:
            with ChannelDB() as db:
                db.update_balance(resp['balance'], channel_type='http_wb')
        return resp


if __name__ == '__main__':
    print(WeiBo.get_balance())
