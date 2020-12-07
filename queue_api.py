from db.myredis import mpop, mlen, mpush, mpipeline
from config import LDY, RedisSql, JK, SmsApi
from sms.lingdaoyi_api import LingDaoYi
from db.sms_pending import SmsPendingDB
from multiprocessing import Process
from db.channel import ChannelDB
from sms.jieke import JieKe
from util import log

import traceback
import time
import json


def update_axflix_balance():
    while True:
        try:
            r = mpop(RedisSql.balance_queue_name)
            if r:
                d = json.loads(r.decode())
                print(f'处理余额数据：{d}', 0, '处理余额')
                with ChannelDB() as db:
                    if 'transId' in d:
                        db.update_balance(d['balance'], channel_type='socket_axflix_china' if d['transId'] == SmsApi.balance_transId_china else 'socket_axflix_vietnam')
                    elif 'channelId' in d:
                        db.update_balance(d['balance'], channel_id=d['channelId'])
                time.sleep(30)
        except Exception as e:
            print(f'处理axflix余额错误, 错误原因 [{e}]', 2, 'axflix余额出错')


def handle_text_result():
    while True:
        try:
            num = mlen(RedisSql.result_queue_name)
            if num > 0:
                time.sleep(10)
                for n in range(num):
                    # 循环从result_sms表拿出数据
                    r = mpop(RedisSql.result_queue_name)
                    d = json.loads(r.decode())
                    if 'balance' in d.keys():
                        # 如果key中有"balance"就代表是余额
                        continue
                    elif 'bPartyNumber' in d.keys():
                        # 如果key中有"bPartyNumber"就代表是发送短信结果
                        print(f'处理短信数据：{d}', 0, '处理短信结果')
                        err = 1
                        status = d.get('status')
                        message_id = d.get('transId')
                        description = d.get('statusMessage')
                        description = description if description else status
                        if status == 'SUCCESS':
                            err = 0
                        with SmsPendingDB() as db:
                            result = db.update(message_id, err, description, d.get('phone', None))
                            if not result:
                                if d.get('count', 0) < 3:
                                    d['count'] = d.get('count', 0) + 1
                                    mpush(json.dumps(d), RedisSql.result_queue_name)
                                else:
                                    print(f'更新短信结果失败, 当前数据[{d}]', 2, '更新短信结果失败')
        except Exception as e:
            er = ";".join(traceback.format_exc().split("\n"))
            print(f'处理短信结果错误, 错误原因 [{er}]', 2, '处理短信结果出错')


def recv_http_text():
    while True:
        with ChannelDB() as db:
            channel_list = db.need_get_result_channel()
        for c in channel_list:
            try:
                print(f'获取[{c[0]}]短信结果', 0, '获取短信结果')
                if c[0] == 'http_ldy':
                    resp = LingDaoYi.get_result()
                elif c[0] == 'http_jk':
                    resp = JieKe.get_result()
                else:
                    resp = None
                if resp:
                    print(f'获取[{c[0]}]短信结果, 一共[{len(resp)}]条数据', 0, '短信状态更新')
                    p = mpipeline()
                    for i in resp:
                        data = {'bPartyNumber': ''}
                        if c[0] == 'http_ldy':
                            data['status'] = 'SUCCESS' if i['code'] == LDY.success_code else 'ERROR'
                            data['transId'] = i['tjpc']
                            data['statusMessage'] = 'SUCCESS' if i['code'] == LDY.success_code else i['code']
                            data['phone'] = i['dest_tele_num']
                        elif c[0] == 'http_jk':
                            data['status'] = 'SUCCESS' if i['State'] == JK.success_code else 'ERROR'
                            data['transId'] = i['MsgID']
                            data['statusMessage'] = 'SUCCESS' if i['State'] == JK.success_code else i['State']
                            data['phone'] = i['Caller']
                        p.lpush(RedisSql.result_queue_name, json.dumps(data))
                    p.execute()
                time.sleep(10)
            except Exception as e:
                print(f'获取[{c[0]}]短信结果出错, 错误原因 [{e}]', 2, '获取短信结果错误')
                time.sleep(10)


if __name__ == '__main__':
    log.init()
    Process(target=update_axflix_balance, name='axflix_balance_server').start()
    # 处理短信和金额的返回结果
    handle_text_result()

