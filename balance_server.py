from config import LogDefine, Upload, Page, Sql
from db.cache_history import SmsCacheHistoryDB
from util.sms_dispatcher import Dispatcher
from db.sms_pending import SmsPendingDB
from db.statistics import StatisticsDB
from datetime import timedelta, date
from db.plateform import PlateformDB
from multiprocessing import Process
from db.control import ControlDB
from db.channel import ChannelDB
from util.log import init

import time
import os


def thread_all_balance():
    # 每隔60秒查询一下所有通道余额
    """判断余额"""
    while True:
        try:
            # 判断余额
            with ChannelDB() as db:
                r = db.show_all_channel()
                # print(f'开始查询通道余额 [{r}]', 0, '查询通道余额')
            for i in r:
                print(f'开始查询通道余额 [{i}]', 0, '查询通道余额')
                if i[2] == 'manual':
                    continue
                if i[1] <= 300:
                    print(f'通道[{i[0]}]当前余额[{i[1]}] 已不足300,关闭该通道', 1, '通道余额不足')
                    with ChannelDB() as db1:
                        db1.close_channel_by_id(i[0])
                # print(f'查询通道余额 {i}', 0, '查询通道余额')
                Dispatcher.balance(i[2])
                time.sleep(1)

            time.sleep(60)
        except Exception as e:
            # traceback.print_exc()
            print(f'查询通道余额失败: {e}', 2, '通道余额错误')
            time.sleep(60)


def timer_zsq(func):
    def inner(*args, **kwargs):
        day = time.strftime("%Y-%m-%d", time.localtime())
        while True:
            today = time.strftime("%Y-%m-%d", time.localtime())
            if day != today:
                func(*args, **kwargs)
                day = today
            time.sleep(LogDefine.interval_del_time)
    return inner


@timer_zsq
def del_old_log_file():
    today = time.strftime("%Y-%m-%d", time.localtime())
    yesterday = (date.today() + timedelta(days=-1)).strftime("%Y-%m-%d")
    lp = LogDefine.logpath
    for f in os.listdir(lp):
        if today not in f and yesterday not in f:
            print(f'删除日志文件 [{lp}/{f}]', 0, '删除日志')
            os.remove(f'{lp}/{f}')


@timer_zsq
def del_old_excel_file():
    today = time.strftime("%Y-%m-%d", time.localtime())
    for f in os.listdir(Upload.upload_phone_file_path):
        if today not in f:
            print(f'删除上传的手机号码文件 [{Upload.upload_phone_file_path}{f}]', 0, '删除手机号文件')
            os.remove(f'{Upload.upload_phone_file_path}{f}')

    for f in os.listdir(Page.excel_file_path):
        if today not in f:
            print(f'删除生成的短信详情文件 [{Page.excel_file_path}{f}]', 0, '删除短信文件')
            os.remove(f'{Page.excel_file_path}{f}')


@timer_zsq
def handle_statistics():
    with SmsCacheHistoryDB() as db:
        print('处理缓存数据', 0, '处理缓存')
        db.update_cache()
    with StatisticsDB() as db:
        print('创建统计', 0, '创建统计')
        db.create_new_count(time.strftime("%Y-%m-%d", time.localtime()))


def handle_kl():
    while True:
        time.sleep(60 * 60)
        with SmsPendingDB() as db:
            print('更新kl', 0, '更新kl')
            db.update_kl(Sql.kl_message_id)


def thread_plateform_balance():
    """每隔10秒查询一次所有平台的余额,停止余额不足的平台"""
    while True:
        # print('查询所有平台余额', 0, '查询平台余额')
        with PlateformDB() as pdb:
            nobalance_plateform_list = pdb.search_nobalance_plateform()
        if nobalance_plateform_list:
            with ControlDB() as cdb:
                for i in nobalance_plateform_list:
                    if cdb.is_running(plateform_id=i):
                        print(f'平台 {i} 的余额不足, 已停止', 1, '余额不足')
                        cdb.set_run(0, plateform_id=i)
        time.sleep(5)


if __name__ == '__main__':
    init()
    # 每天删除早期excel文件
    Process(target=del_old_excel_file, name='excel_file_server').start()
    # 每天删除早期日志
    Process(target=del_old_log_file, name='log_file_server').start()
    # 每天创建新的统计数据
    Process(target=handle_statistics, name='statistics_server').start()
    # 更新kl
    Process(target=handle_kl, name='kl_server').start()
    # 每10秒查询一次各个平台余额然后停止余额不足的平台
    Process(target=thread_plateform_balance, name='plateform_balance_server').start()
    thread_all_balance()

