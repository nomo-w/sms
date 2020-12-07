# coding: utf-8

import time
import json
import socket
import platform

from config import SmsApi, LocalSocket
from sms.base import SmsBase
from util.common import is_right_china_number


def is_include_hanzi(text):
    # 是否包含汉字
    # for python 3.x
    # sample: ishan('一') == True, ishan('我&&你') == True
    for char in text:
        if '\u4e00' <= char <= '\u9fff':
            return True
    return False


class Axflix(SmsBase):

    def __init__(self):
        self.socket_client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.socket_client.setsockopt(socket.SOL_SOCKET, socket.SO_KEEPALIVE, 1)
        os_platform = platform.system()
        if os_platform == 'Darwin':
            self.socket_client.setsockopt(socket.IPPROTO_TCP, 0x10, 30)
        elif os_platform == 'Linux':
            self.socket_client.setsockopt(socket.IPPROTO_TCP, socket.TCP_KEEPIDLE, 60)
            self.socket_client.setsockopt(socket.IPPROTO_TCP, socket.TCP_KEEPINTVL, 30)
            self.socket_client.setsockopt(socket.IPPROTO_TCP, socket.TCP_KEEPCNT, 10)
        self.socket_client.settimeout(1 * 60)
        self.socket_client.connect((LocalSocket.ip, LocalSocket.port))

    def get_balance(self, channel_type):
        data = {
            "tag": "balance",
            "body": {
                "clientId": SmsApi.axflix_china_client_id if channel_type=='socket_axflix_china' else SmsApi.axflix_vietnam_client_id,
                "transId": SmsApi.balance_transId_china if channel_type=='socket_axflix_china' else SmsApi.balance_transId_vietnam,
                "timestamp": time.time()
            }
        }
        self.socket_client.send(json.dumps(data).encode())
        return True

    def send(self, seq, to_number, text):
        data = {
            "tag": "sendsms",
            "body": {
                "clientId": SmsApi.axflix_china_client_id if to_number.split(':')[1] == 'socket_axflix_china' else SmsApi.axflix_vietnam_client_id,
                "transId": seq,
                "bPartyNumber": to_number.split(':')[0],
                "content": text,
                "messageType": "L",
                "serviceType": "T",
                "timestamp": time.time(),
                "dataCoding": 8 if is_include_hanzi(text) else 0
            }
        }
        self.socket_client.send(json.dumps(data).encode())

        result = dict(message_id=0, to_number=to_number, price='0', err='10', err_text='pending')
        result['err'] = 2
        result['price'] = 0
        result['err_text'] = 'pending'
        result['message_id'] = seq

        """
        这里就不接收了，Axflix短信网关是异步返回的数据，这里将发出去的数据标记为pending
        """
        # response = json.loads(self.socket_client.recv(4096).decode())

        # status = response.get('body', {}).get('status', '')
        # if status == 'SUCCESS':
        #     result['err'] = 0
        #     result['price'] = Price.axflix
        #     result['err_text'] = 'success'
        # else:
        #     result['err'] = 1
        #     result['price'] = 0
        #     result['err_text'] = response.get('body', {}).get('statusMessage', '未知')
        # result['message_id'] = response.get('body', {}).get('transId', 3)

        return result


if __name__ == "__main__":
    pass
    # axflix = Axflix()
    # balance = axflix.get_balance()
    # print(balance)
    # result = axflix.send('13538731667', '测试短信发送')
    # print(result)
