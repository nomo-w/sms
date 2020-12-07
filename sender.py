from util.sms_dispatcher import Dispatcher
from db.sms_pending import SmsPendingDB
from db.plateform import PlateformDB
from db.history import SmsHistoryDB
from db.myredis import mpop, mlen
from db.channel import ChannelDB
from db.control import ControlDB
from threading import Thread
from config import Sql
from util import log

import traceback
import json
import time


def get_one(plateform_id):
    # 从redis里拿一条返回
    """
    :return: (user, to_number, text) or (None, None, None)
    """
    with ControlDB() as db:
        if db.is_running(plateform_id=plateform_id) == 0:
            return None
    try:
        r = mpop(f'sms_{plateform_id}')
        return json.loads(r) if r else None
    except Exception as e:
        print(f'从redis拿出短信失败: {e}', 2, 'redis错误')
    return None


def send(p_id):
    # print(f'发送者[{p_id}]开启', 0, '发送者')
    for _ in range(0, 100):
        try:
            one = get_one(p_id)
            if one is not None:
                with ChannelDB() as db1:
                    channel_balance = db1.get_channel_balance(one['channel_id'])
                    if channel_balance <= 10:
                        # 通道余额不足直接失败
                        with SmsHistoryDB() as db:
                            if one.get('is_qunfa', False):
                                for i in one['to']:
                                    db.add(one['user'], one['user_id'], 0, i, one['text'], 0, 'channel no balance',
                                    one['channel_id'], one['plateform_id'], need_count_all=True)
                            else:
                                db.add(one['user'], one['user_id'], 0, one['to'][0] if isinstance(one['to'], list) else one['to'],
                                       one['text'], 0, 'channel no balance', one['channel_id'], one['plateform_id'], need_count_all=True)
                        continue
                    # 获取通道类型
                    r, is_have_danfa, is_have_qunfa, max_send, min_send, max_text_len, additional_code, \
                    need_report = db1.show_channel_type(one['channel_id'])
                if one.get('is_qunfa', False):
                    print(f'发送者[{p_id}]发送短信 ## {one["user"]} 群发[{len(one["to"])}]条短信 ## [{one["id"]}]:[{one["text"]}]', 0, '发送短信')
                else:
                    print(f'发送者[{p_id}]发送短信 ## {one["user"]} 发送 ## [{one["id"]}]:[{one["text"]}] => [{one["to"][0] if isinstance(one["to"], list) else one["to"]}]', 0, '发送短信')

                if not one.get('is_qunfa', False) and isinstance(one['to'], list):
                    # kl
                    with SmsPendingDB() as db:
                        db.add(one['user_id'], Sql.kl_message_id, one['to'][0], one['text'], one['channel_id'],
                               one['plateform_id'], one.get('callback_id', 0), one.get('is_click', '未设置'), one['user'])
                    continue
                ret, status = Dispatcher.send(r, one['id'], one['to'], one['text'], one.get('is_qunfa', False))
                print(f'发送者[{p_id}]短信商返回值 [{ret}] 状态 [{status}]', 0, '发送短信返回值')
                if status:
                    # 发送 成功写入pending表
                    if ret:
                        one['id'] = ret

                    if one.get('is_qunfa', False):
                        if need_report:
                            for i in one['to']:
                                with SmsPendingDB() as db:
                                    db.add(one['user_id'], one['id'], i, one['text'], one['channel_id'],
                                           one['plateform_id'], user=one['user'])
                        else:
                            with PlateformDB() as db:
                                price = db.search_plateform_rate_by_channel(one['channel_id'], one['plateform_id'])
                            for i in one['to']:
                                with SmsHistoryDB() as db:
                                    db.add(one['user'], one['user_id'], one['id'], i, one['text'], price, 'success',
                                           one['channel_id'], one['plateform_id'], need_count_all=True)
                        break
                    else:
                        if need_report:
                            with SmsPendingDB() as db:
                                db.add(one['user_id'], one['id'], one['to'], one['text'], one['channel_id'],
                                  one['plateform_id'], one.get('callback_id', 0), one.get('is_click', '未设置'), one['user'])
                        else:
                            with PlateformDB() as db:
                                price = db.search_plateform_rate_by_channel(one['channel_id'], one['plateform_id'])
                            with SmsHistoryDB() as db:
                                db.add(one['user'], one['user_id'], one['id'], one['to'], one['text'], price, 'success',
                                       one['channel_id'], one['plateform_id'], one.get('callback_id', 0),
                                       one.get('is_click', '未设置'), need_count_all=True)
                else:
                    # user, message_id, to, text, price, err, err_text, channel_id, plateform_id
                    # 短信商返回失败, 直接失败
                    if one.get('is_qunfa', False):
                        # 如果是群发就一条一条存到数据库
                        for i in one['to']:
                            with SmsHistoryDB() as db:
                                db.add(one['user'], one['user_id'], one['id'], i, one['text'], 0, 'send text failed',
                                       one['channel_id'], one['plateform_id'], need_count_all=True)
                        break
                    else:
                        with SmsHistoryDB() as db:
                            db.add(one['user'], one['user_id'], one['id'], one['to'], one['text'], 0,
                                   'send text failed', one['channel_id'], one['plateform_id'], need_count_all=True)
                time.sleep(0.5)
            else:
                # print('本次已无数据.')
                break
        except Exception as e:
            # traceback.print_exc()
            print(f'发送者[{p_id}]错误, 错误原因 [{e}]', 2, '发送者错误')


def run_sender_forever():
    while True:
        try:
            with PlateformDB() as db:
                # 查询所有的平台
                all_plateform_list = db.search_all_plateform()
            have_data = False
            for s in [f'sms_{i}' for i in all_plateform_list]:
                if mlen(s) > 0:
                    have_data = True
                    thread_list = [Thread(target=send, args=(i,), name=f'sender_{i}') for i in all_plateform_list]
                    for i in thread_list:
                        i.start()
                    for t in thread_list:
                        t.join()
            if have_data is False:
                time.sleep(20)
        except Exception as e:
            print(f'创建发送者错误, 错误原因[{e}]', 2, '创建发送者错误')
            time.sleep(10)


if __name__ == '__main__':
    log.init()
    # multiprocessing.Process(target=thread_all_balance, name=f'channel_balance_server').start()
    run_sender_forever()

