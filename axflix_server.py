# coding: utf-8

"""从本地的9999端口拿到数据发送给axflix短信商.从第三方短信商不断接收数据并写入redis的axflix_sms表"""
# 从本地tcp9999端口拿数据发送给axflix短信商
# 从axflix接收数据写入到redis
from socketserver import ThreadingTCPServer as TTS
from socketserver import BaseRequestHandler as BRH
from config import SmsApi, LocalSocket, RedisSql
from db.myredis import mpush
from util.my_timer import MyTimer
from util import log

import threading
import binascii
import platform
import socket
import time
import json


TAG_ID_BY_HEX = {
    '01': {'hex': '01', 'name': 'sendsms'},  # 发单条短信
    '02': {'hex': '02', 'name': 'sendsms_response'},
    '03': {'hex': '03', 'name': 'balance'},  # 查询余额
    '04': {'hex': '04', 'name': 'balance_response'},
    '21': {'hex': '21', 'name': 'bulksms'},  # 批量发短信
    '22': {'hex': '22', 'name': 'bulksms_response'},
    '81': {'hex': '81', 'name': 'keep_alive'},  # 发送心跳
    '82': {'hex': '82', 'name': 'keep_alive_response'},
    '99': {'hex': '99', 'name': 'error'},  # 错误响应
}


TAG_ID_BY_NAME = {
    'sendsms': {'hex': '01', 'name': 'sendsms'},  # 发单条短信
    'sendsms_response': {'hex': '02', 'name': 'sendsms_response'},
    'balance': {'hex': '03', 'name': 'balance'},  # 查询余额
    'balance_response': {'hex': '04', 'name': 'balance_response'},
    'bulksms': {'hex': '21', 'name': 'bulksms'},  # 批量发短信
    'bulksms_response': {'hex': '22', 'name': 'bulksms_response'},
    'keep_alive': {'hex': '81', 'name': 'keep_alive'},  # 发送心跳
    'keep_alive_response': {'hex': '82', 'name': 'keep_alive_response'},
    'error': {'hex': '99', 'name': 'error'},  # 错误响应
}


def tag_id_name_by_hex(x):
    """
    通过hex tag编码获取tag名称
    """
    return TAG_ID_BY_HEX.get(x, {}).get('name')


def tag_id_hex_by_name(n):
    """
    通过tag名称获取hex tag编码
    """
    return TAG_ID_BY_NAME.get(n, {}).get('hex')


def encode_data(data):
    """
    数据包封装
    """
    body = json.dumps(data.get('body', {}))
    tag = tag_id_hex_by_name(data.get('tag', {}))
    actual_length = 5 + len(body)
    length = '%08x' % actual_length
    return binascii.a2b_hex(tag + length) + body.encode()


def decode_data(data):
    """
    数据包解封装
    """
    tag_bin = data[:1]
    length_bin = data[1:5]
    body_bin = data[5:]
    result = {}
    if tag_bin and body_bin:
        result['tag'] = tag_id_name_by_hex(binascii.b2a_hex(tag_bin).decode())
        result['length'] = int(binascii.b2a_hex(length_bin), 16)
        result['body'] = json.loads(body_bin)
    return result


def is_json_format(data):
    flag = False
    try:
        data = json.loads(data)
        if data:
            flag = True
    except Exception as e:
        pass
    return flag


class AxflixSocketClient(object):
    def __init__(self, address):
        """
        标记socket是否重连中
        """
        self.is_connecting = False

        """
        Axflix SMS Gateway服务器IP、Port
        """
        self.address = address

        """
        保存socket客户端对象
        """
        self.sc = None

        """
        创建socket客户端
        """
        self.create_socket()

        """
        连接Axflix SMS Gateway服务器
        """
        self.connect_axflix()

    def __del__(self):
        """
        析构函数，关闭socket客户端连接
        """
        if self.sc is not None:
            self.sc.close()
            self.sc = None

    def create_socket(self):
        """
        创建socket客户端对象
        """
        self.sc = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        """
        TCP持久会话保持
        """
        self.sc.setsockopt(socket.SOL_SOCKET, socket.SO_KEEPALIVE, 1)
        os_platform = platform.system()
        if os_platform == 'Darwin':
            self.sc.setsockopt(socket.IPPROTO_TCP, 0x10, 30)
        elif os_platform == 'Linux':
            self.sc.setsockopt(socket.IPPROTO_TCP, socket.TCP_KEEPIDLE, 60)
            self.sc.setsockopt(socket.IPPROTO_TCP, socket.TCP_KEEPINTVL, 30)
            self.sc.setsockopt(socket.IPPROTO_TCP, socket.TCP_KEEPCNT, 10)
        """
        设置超时时间
        """
        self.sc.settimeout(2 * 60)

    def connect_axflix(self):
        """
        连接、重连 Axflix SMS Gateway
        """
        self.create_socket()
        try:
            # print(self.sc)
            self.sc.connect(self.address)
            self.is_connecting = False
            print(f'socket已连接{self.sc}', 0, 'axflix连接')
            # print(self.sc)
        except (OSError, TimeoutError, socket.timeout) as err:
            print(f'错误消息：{err}，尝试重连socket中...', 2, 'axflix错误')
            try:
                self.reconnect_axflix()
            except RecursionError as err:
                pass

    def reconnect_axflix(self):
        self.is_connecting = True
        time.sleep(30)
        if self.sc is not None:
            print('close...', 0, 'axflix连接关闭')
            self.sc.close()
            self.sc = None
        self.connect_axflix()

    def send_heartbeat(self):
        """
        发送心跳数据包
        """
        data_china = {
            "tag": "keep_alive",
            "body": {
                "clientId": SmsApi.axflix_china_client_id,
                "transId": SmsApi.heartbeat_transId_china,
                "timestamp": time.time()
            }
        }
        data_vietnam = {
            "tag": "keep_alive",
            "body": {
                "clientId": SmsApi.axflix_vietnam_client_id,
                "transId": SmsApi.heartbeat_transId_vietnam,
                "timestamp": time.time()
            }
        }
        print(f'发送axflix心跳包', 0, 'axflix心跳检测')
        self.send_data(encode_data(data_china))
        self.send_data(encode_data(data_vietnam))

    def send_data(self, data):
        """
        发送数据包
        """
        if self.is_connecting is False:
            try:
                self.sc.send(data)
            except (OSError, BrokenPipeError, AttributeError) as err:
                print(f'错误消息：{err}，Axflix客户端连接可能已断开，正尝试重连中...', 2, 'axflix错误')
                self.reconnect_axflix()

    def recv_data(self):
        # 不间断从第三方短信平台接收数据并写入到redis的axflix_sms表
        # 接收到的数据有发送短信的返回结果。和查询余额的结果
        """
        接收数据包
        """
        cur_buf_size = 5
        part_data = b''
        while True:
            if self.is_connecting is True:
                continue
            data, cur_buf_size, is_part = self.recv_by_4bytes(cur_buf_size)
            if data:
                if is_part is True:
                    part_data += data
                    if is_json_format(part_data) is True:
                        # data = part_data
                        print(f'部分数据：{part_data}', 0, '获取axflix数据')
                        mpush(part_data.decode(), RedisSql.result_queue_name)
                        part_data = b''
                else:
                    print(f'完整数据：{data}', 0, '获取axflix数据')
                    if 'balance' in json.loads(data.decode()).keys():
                        mpush(data.decode(), RedisSql.balance_queue_name)
                    else:
                        mpush(data.decode(), RedisSql.result_queue_name)

    def recv_by_4bytes(self, cur_buf_size):
        # 数据
        data = b''
        # 下次读取数据长度
        buffer_size = 5
        # 数据是否完整
        is_part = False
        try:
            # 测试的时候莫名不接收数据了
            # MSG_WAITALL 此坑巨坑，防止返回小于cur_buf_size的数据
            chunk = self.sc.recv(cur_buf_size, socket.MSG_WAITALL)
            chunk_size = len(chunk)
            if chunk_size > 0:
                if chunk_size < cur_buf_size:
                    # 残缺数据
                    data = chunk
                    # 下次读取剩余的数据
                    buffer_size = cur_buf_size - chunk_size
                    if is_json_format(data) is False:
                        is_part = True
                elif chunk_size == cur_buf_size:
                    # 完整数据
                    if chunk_size > 5:
                        # 数据
                        data = chunk
                        # 剩余部分要标记为不完整
                        if is_json_format(data) is False:
                            is_part = True
                    elif chunk_size == 5:
                        # 包头数据，无数据，下次读取完整的数据
                        bin_len = binascii.b2a_hex(chunk[1:5])
                        buffer_size = int(bin_len, 16) - 5
            elif chunk_size == 0:
                print('axflix返回空数据了', 1, 'axflix返回空')
        except (TimeoutError, socket.timeout) as err:
            print(f'错误消息：{err}，接收数据超时了', 2, 'axflix错误')
        except (OSError, AttributeError) as err:
            pass
        return [data, buffer_size, is_part]


class ThreadedTCPRequestHandler(BRH):
    def setup(self):
        """
        获取当前线程
        """
        self.ct = threading.current_thread()

        """
        本地返回数据
        """
        self.res_data = ''

    def handle(self):
        """
        处理本地TCP客户端请求
        """
        data = self.request.recv(1024).decode()

        """
        将数据发送给Axflix SMS Gateway，并接收数据
        """
        try:
            data = encode_data(json.loads(data))
            if self.server.axflix_socket.is_connecting is False:
                # print(f'线程：{self.ct.name} 发送数据给Axflix短信网关：{data}', 0, '发送axflix')
                self.server.axflix_socket.send_data(data)
                self.res_data = 'SUCCESS'
            else:
                self.res_data = 'FAIL'

            """
            将从Axflix SMS Gateway接收到的数据发送给本地TCP客户端
            """
            self.request.send(self.res_data.encode())
        except Exception as e:
            print(f"发送短信错误!: {e}", 2, 'axflix错误')

    def finish(self):
        pass


if __name__ == "__main__":
    log.init()
    LOCALHOST = (LocalSocket.ip, LocalSocket.port)
    # 模拟环境
    # AXFLIXHOST = ('18.136.139.90', 30303)
    AXFLIXHOST = (SmsApi.axflix_host, SmsApi.axflix_port)
    # 实例化Axflix短信网关
    axflix_socket = AxflixSocketClient(AXFLIXHOST)
    # 长连接，心跳检测
    MyTimer(40, axflix_socket.send_heartbeat).start()
    # 接收Axflix短信网关返回的数据
    threading.Thread(target=axflix_socket.recv_data).start()
    # 本地TCP服务，端口9999
    server = TTS(LOCALHOST, ThreadedTCPRequestHandler)
    # 注入Axflix短信网关, 从本地tcp9999端口拿数据发送给Axflix短信商
    server.axflix_socket = axflix_socket
    server.allow_reuse_address = True
    server.serve_forever()
