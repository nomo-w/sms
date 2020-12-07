# coding: utf-8

from db.myredis import mlen, mdelete, mpush, mpipeline, mset
from db.cache_statistics import CacheStatisticsDB
from db.sensitive_words import SensitiveWordsDB
from db.recharge_record import Recharge_Record
from db.cache_history import SmsCacheHistoryDB
from db.handle_callback import Callback
from db.sms_pending import SmsPendingDB
from db.statistics import StatisticsDB
from db.plateform import PlateformDB
from db.history import SmsHistoryDB
from db.white_list import WhiteList
from db.template import TemplateDB
from db.channel import ChannelDB
from db.control import ControlDB
from db.users import UserDB
from functools import wraps
from flask import request
from util import login
from config import *

import traceback
import requests
import random
import xlwt
import time
import json

# 屏蔽https告警
from requests.packages.urllib3.exceptions import InsecureRequestWarning
requests.packages.urllib3.disable_warnings(InsecureRequestWarning)


def handle_httpresponse(data, status=-1, other={}):
    '''
    处理返回结果
    :param data: 数据
    :param status: 返回状态 0(成功) -1(不成功)
    :param other: 其他需要加入的数据
    :return: json格式的数据
    '''
    return_dic = {'data': data, 'status': Return_Statua_Code.error}
    if status == 0:
        return_dic['status'] = Return_Statua_Code.ok
    if other:
        for i in other:
            return_dic[i] = other[i]
    return json.dumps(return_dic)


# --------------------------------------------------------
# 装饰器
# --------------------------------------------------------
def white_required(func):
    # 判断是否是白名单装饰器
    """使用 ->  @white_required"""
    @wraps(func)
    def decorated(*args, **kwargs):
        if is_white_ip(request.headers.get("X-Real-IP"), request.headers.get('Origin')):
            return func(*args, **kwargs)
        else:
            return handle_httpresponse('IP不在白名单!')
    return decorated


def is_superuser_zsq(func):
    # 判断是否是超级管理员装饰器
    @wraps(func)
    def inner(*args, **kwargs):
        with UserDB() as db:
            if db.is_superuser(user_id=login.get_cur_user_id()) != -1:
                value = func(*args, **kwargs)
            else:
                value = handle_httpresponse('抱歉,您无权限访问此界面')
        return value
    return inner


def handle_api_zsq(api_path, method):
    # 处理http response装饰器
    def zsq(func):
        @wraps(func)
        def inner(*args, **kwargs):
            if method == 'get':
                _ = f'{request.headers.get("X-Real-IP")} {method.upper()} => {api_path}{list(kwargs.values())[0]} : 【{request.args}】'
            else:
                _ = f'{request.headers.get("X-Real-IP")} {method.upper()} => {api_path} : ' \
                    f'【{request.args if method == "GET" else request.form if method == "POST" else request.data}】'
            print(_, 0, 'request', LogDefine.request_log_file.format(time.strftime("%Y-%m-%d", time.localtime())))
            try:
                resp = func(*args, **kwargs)
            except KeyError:
                # traceback.print_exc()
                resp = handle_httpresponse('参数错误!')
            except Exception as e:
                # traceback.print_exc()
                er = ";".join(traceback.format_exc().split("\n"))
                print(f'服务器错误, 错误原因 [{er}]!!!', 2, '服务器错误')
                resp = handle_httpresponse(f'服务器错误, 错误原因 [{e}]')
            return resp
        return inner
    return zsq


def my_requests(url, method, params=None, headers=None, need_json_resp=True,
                verify=False, need_json_params=False, need_proxies=False, proxies=None, need_content=False):
        '''
        发送requests的请求
        :param url: 目标url
        :param headers: 请求头
        :param params: 请求参数
        :param method: 请求方法
        :param is_json: 是否返回json数据
        :param verify: ssl验证
        :param need_handle_resp: 是否需要处理数据
        :return: 返回响应参数
        '''
        try:
            data = {'url': url, 'verify': verify, 'timeout': (10, 10)}
            if params is not None:
                data['params' if method == 'get' else 'data'] = json.dumps(params) if need_json_params else params
            if need_proxies:
                data['proxies'] = proxies
            if headers is not None:
                data['headers'] = headers

            if method == 'get':
                resp = requests.get(**data)
            elif method == 'post':
                resp = requests.post(**data)

            if resp.status_code is not 200:
                print(f'请求 [{url}] 失败. 返回状态码 [{resp.status_code}]. 失败原因 [{resp.reason}]', 2, '请求短信商错误')
                return None
            return resp.json() if need_json_resp else resp.content if need_content else resp.text
        except Exception as e:
            # traceback.print_exception()
            print(f'请求 [{url}] 失败. 失败原因 [{e}]', 2, '请求短信商错误')
            return None


# --------------------------------------------------------
# 开始/停止/状态
# --------------------------------------------------------
def start_send(user_id):
    """
    开始发送!!!
    :return: {ret:1, msg:启动成功}
    """
    with PlateformDB() as db:
        balance, rate = db.search_balance_rate(user_id)
    if balance < rate:
        return "金额不足，无法启动!"
    with ControlDB() as db:
        if not db.is_running(user_id):
            if db.set_run(1, user_id):
                return '启动成功!'
    return '启动失败!'


def stop_send(user_id):
    """
    停止发送
    :return: {ret:1, msg:停止成功}
    """
    with ControlDB() as db:
        if db.is_running(user_id):
            if db.set_run(0, user_id):
                return '停止成功!'
    return '停止失败!'


def get_is_running(user_id=None, username=None, domain=None):
    """
    是否运行中
    :return: bool
    """
    with ControlDB() as db:
        if user_id:
            return db.is_running(user_id)
        elif username:
            return db.is_running(username=username, domain=domain)


# --------------------------------------------------------
# 用户系统 - 登入/登出/新建/修改密码
# --------------------------------------------------------
def login_api(user, password, domain):
    """
    登陆!!!
    :param user:
    :param password:
    :return: True / False
    """
    with UserDB() as db:
        return db.is_right_password(user, password, domain)


def get_plateform_name(user_id):
    with PlateformDB() as db:
        return db.get_plateform_name(user_id)


def change_password(user_id, newpassword):
    """
    修改密码
    :param user_id:
    :param newpassword:
    :return: True / False
    """
    with UserDB() as db:
        return db.change_password(user_id, newpassword)


def create_user(user, password, admin_id):
    """
    创建账号，只有admin权限的人才可以，而admin权限必须由数据库添加
    :param user:
    :param password:
    :param plateform_id: 平台id
    :return: bool
    """
    with UserDB() as db:
        if db.get_auth(admin_id) == 'admin':
            return db.create_user(user, password, admin_id, 'user')
    return '您无此权限，请联系管理员添加用户!'


def del_user(user_id, admin_id):
    with UserDB() as db:
        if db.get_auth(admin_id) == 'admin' and admin_id != user_id:
            return db.del_user(user_id)
    return '您无此权限，请联系管理员删除用户!'


def get_all_user(user_id):
    """获取账号列表"""
    with UserDB() as db:
        if db.get_auth(user_id) == 'admin':
            return db.get_all(user_id)
    return []


# --------------------------------------------------------
# 白名单         - 新建/删除/获取所有
# --------------------------------------------------------
def change_white_ip_status(user_id, status):
    with WhiteList() as db:
        return db.change_ip_status(status, user_id=user_id)


def add_white_ip(ip, memo, user_id):
    """
    添加白名单ip
    :param ip:
    :param memo: 备注
    :return: bool
    """
    with WhiteList() as db:
        return db.add(ip, memo, user_id)


def del_white_ip_by_id(whitelist_id):
    """
    根据id删除白名单ip行
    :param _id:
    :return: bool
    """
    with WhiteList() as db:
        return db.del_ip_by_id(whitelist_id)


def get_white_ip(user_id, page):
    """
    获取所有白名单信息
    :return: [{'id': 6, 'ip': '1.1.1.1', 'memo': 'test1'},...]
    """
    with WhiteList() as db:
        status = db.get_white_ip_status(user_id=user_id)
        value_list = db.get_all_ip(page, user_id=user_id)
        page_list, total = db.search_page(user_id=user_id)
        return {'page_list': page_list, 'total': total, 'value_list': value_list, 'status': status}


def is_white_ip(ip, url):
    """
    ip是否在白名单内
    :param ip:
    :return: bool
    """
    with WhiteList() as db:
        return db.is_white_ip(ip, url.split('/')[2])


# --------------------------------------------------------
# 当前发送队列    - 列队数量
# --------------------------------------------------------
def _get_plateofrm_id(user_id):
    with UserDB() as db:
        plateform_id = db.get_plateform_id(user_id)
    return plateform_id


def get_queue_count(user_id):
    """
    队列数量
    :return: 数量
    """
    plateform_id = _get_plateofrm_id(user_id)
    if plateform_id == 0:
        return 0
    return mlen(f'sms_{plateform_id}')


def empty_queue(user_id):
    """
    清空队列
    :return: 数量
    """
    plateform_id = _get_plateofrm_id(user_id)
    if plateform_id == 0:
        return False
    return mdelete(f'sms_{plateform_id}')


# --------------------------------------------------------
# 统计信息
# --------------------------------------------------------
def analysis_all(user_id):
    """
    返回一个总的统计
    :return: (all_count, success_count, price_sum)
    """
    with StatisticsDB() as db:
        count_all = db.show_allcount_by_plateform('total_count,success_count', user_id=user_id)
        if count_all is not None:
            r1, r2 = count_all[0][0], count_all[0][1]
        else:
            r1, r2 = 0, 0
    with PlateformDB() as db:
        balance = db.search_balance(user_id)
    return r1, r2, balance


def analysis_by_day(start, end, user_id):
    """
    返回一个多少天之间的统计
    search_time = time>=start and time<=end  （单位:天）
    :param start: yyyy-MM-dd
    :param end: yyyy-MM-dd
    :return: (all_count, success_count, price_sum)
    """
    with StatisticsDB() as db:
        data = db.show_allcount_by_day(start, end, ['total_count', 'success_count', 'price_count'], need_sum=True, user_id=user_id)
    if data is not None:
        return data[0][0], data[0][1], data[0][2]
    return 0, 0, 0


def analysis_by_day_group(start, end, user_id):
    """
    返回一个多少天之间的，每天的数据统计
    :param start: yyyy-MM-dd
    :param end: yyyy-MM-dd
    :return: ((success_count,price_sum,time('%Y-%m-%d')),(success_count2, price_sum2,time('%Y-%m-%d')),...)
    """
    with StatisticsDB() as db:
        data = db.show_allcount_by_day(start, end, ['total_count', 'price_count', 'day'], user_id=user_id)
    if data is not None:
        return [{'success_sum': i[0], 'price': round(float(i[1]), 2), 'date': i[2]} for i in data]


def search_all_channel_info(user_id):
    with ChannelDB() as db:
        return db.show_all_channel_info(user_id)


def get_template_by_channel(channel_id, user_id):
    with TemplateDB() as db:
        return db.show_template_by_ChannelPlateform(channel_id, user_id)


def search_recharge(start, end, page, user_id=None, plateform_id=None, need_excel=None):
    with Recharge_Record() as db:
        resp = db.search_recharge_record(start, end, page, user_id=user_id, plateform_id=plateform_id, need_excel=need_excel)
        if need_excel == 0:
            return data_to_excel(resp, data_type='recharge')
        page_list, page_count = db.search_page(start, end, user_id=user_id, plateform_id=plateform_id)
        return {'value_list': resp, 'page_list': page_list, 'total': page_count}, None


def handle_phone_number(ph):
    if ph and len(ph) >= 7:
        if ph[:2] in ('+8', '86', '84'):
            star = '*'*(len(ph)-2-2-2)
            ph = ph[:2] + ph[2:4] + star + ph[-2:]
        else:
            star = '*'*(len(ph)-2-2)
            ph = ph[:2] + star + ph[-2:]
    return ph


def async_job(to, start, end, err, page, need_excel, user_id, channel_id, need_handle_phone, jobId):
    try:
        data = search_by_number_day_status(to, start, end, err, page, need_excel, user_id, channel_id, need_handle_phone)
        if need_excel == 0:
            file_path, file_name = data_to_excel(data['value_list'])
            mset(jobId, f'{RedisSql.job_status_code["success"]}|file|{file_name}', 30)
        else:
            mset(jobId, f'{RedisSql.job_status_code["success"]}|data|{json.dumps(data)}', 30)
    except Exception as e:
        mset(jobId, f'{RedisSql.job_status_code["failed"]}|{"file" if need_excel else "data"}|{e}', 30)


def search_by_number_day_status(to, start, end, err, page, need_excel, user_id, channel_id, need_handle_phone=True):
    """
    查询数据
    :return: {"data": [{id: "xx", user: "xx", text: "xx", price: "xx", ...}, {...}], "pages": [1,2,...]}
    """
    is_cache = False
    if not to and need_excel != 0 and err != 2:
        with CacheStatisticsDB() as db:
            # 查询数据是否在缓存库里
            if db.search_cache_statistics(start, end, channel_id, user_id, err, page):
                # 数据在缓存库
                with SmsCacheHistoryDB() as db1:
                    data = db1.search_history(start, end, err, page, user_id, channel_id)
                is_cache = True
            else:
                # 数据不在缓存库
                with SmsHistoryDB() as db1:
                    data = db1.search_history(to, start, end, err, int(page) - 1 if page else page, user_id, channel_id,
                        False if need_excel == 0 else True)
    else:
        with SmsHistoryDB() as db:
            data = db.search_history(to, start, end, err, int(page) - 1 if page else page, user_id, channel_id,
                                     False if need_excel == 0 else True)
    # 查询页数
    if need_excel == 0:
        # 0代表需要生成excel, 就不需要查询页数了
        pages, total = [], 0
    else:
        if to:
            total = len(data)
            pages = [i + 1 for i in range(total // Page.history_limit)]
            pages = pages if pages else [1]
            if total > Page.history_limit and (total % Page.history_limit != 0):
                pages.append(pages[-1] + 1)
        else:
            with StatisticsDB() as db:
                pages, total = db.search_page(start, end, err, user_id, channel_id)
    return {
        'value_list': [
            {
                'id': i[0],
                'user': i[1],
                'channel_name': i[2],
                'to_number': handle_phone_number(i[3]) if need_handle_phone else i[3],
                'text': i[4],
                'time': i[5].strftime('%Y-%m-%d %H:%M:%S'),
                'price': round(float(i[6]), 2),
                'status': i[7],
                'is_click': i[8]
            } for i in data],
        'page_list': pages,
        'total': total,
        'is_cache': is_cache
    }


def data_to_excel(data, data_type='history'):
    """
    将数据写入excel表格
    :param data: [{'id': "xx", 'user': "xx", ...}]
    :return:
    """
    excelTabel = xlwt.Workbook()  # exel表格实例
    # 设置时间excel时间显示格式
    style = xlwt.XFStyle()
    style.num_format_str = 'yyyy-mm-dd H:M:S'

    new_data = []
    start = 0
    for i in range(65535, len(data)+1, 65535):
        new_data.append(data[start: i])
        start = i
    if not new_data:
        new_data.append(data)
    else:
        if len(data) % 65535:
            new_data.append(data[i:])
    for i in range(len(new_data)):
        sheet = excelTabel.add_sheet(f'sms_{i}')
        if data_type == 'history':
            title_list = ['', '用户', '内容', '状态', '手机号', '时间', '是否点击']  # 标题行内容
        elif data_type == 'recharge':
            title_list = ['充值日期', '充值金额', '平台', '备注']  # 标题行内容
        for x in range(len(title_list)):
            sheet.write(0, x, title_list[x])

        for c in range(1, len(new_data[i]) + 1):
            if data_type == 'history':
                sheet.write(c, 0, new_data[i][c - 1]['id'])
                sheet.write(c, 1, new_data[i][c - 1]['user'])
                sheet.write(c, 2, new_data[i][c - 1]['text'])
                sheet.write(c, 3, new_data[i][c - 1]['status'])
                sheet.write(c, 4, new_data[i][c - 1]['to_number'])
                sheet.write(c, 5, new_data[i][c - 1]['time'], style)
                sheet.write(c, 6, new_data[i][c - 1]['is_click'])
            elif data_type == 'recharge':
                sheet.write(c, 0, new_data[i][c - 1]['recharge_time'])
                sheet.write(c, 1, new_data[i][c - 1]['recharge_amount'])
                sheet.write(c, 2, new_data[i][c - 1]['plateform_name'])
                sheet.write(c, 4, '')

    now = time.strftime("%Y-%m-%d_%H-%M-%S", time.localtime(int(time.time())))
    file_name = f'{Page.excel_file_path}{now}.xls'
    excelTabel.save(file_name)
    return file_name, f'{now}.xls'


def encode_b64(n):
    table = '0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ-_'
    result = []
    temp = n
    if 0 == temp:
        result.append('0')
    else:
        while 0 < temp:
            result.append(table[temp % 64])
            temp //= 64
    return ''.join([x for x in reversed(result)])


def decode_b64(str):
    table = {"0": 0, "1": 1, "2": 2, "3": 3, "4": 4, "5": 5,
             "6": 6, "7": 7, "8": 8, "9": 9,
             "a": 10, "b": 11, "c": 12, "d": 13, "e": 14, "f": 15, "g": 16,
             "h": 17, "i": 18, "j": 19, "k": 20, "l": 21, "m": 22, "n": 23,
             "o": 24, "p": 25, "q": 26, "r": 27, "s": 28, "t": 29, "u": 30,
             "v": 31, "w": 32, "x": 33, "y": 34, "z": 35,
             "A": 36, "B": 37, "C": 38, "D": 39, "E": 40, "F": 41, "G": 42,
             "H": 43, "I": 44, "J": 45, "K": 46, "L": 47, "M": 48, "N": 49,
             "O": 50, "P": 51, "Q": 52, "R": 53, "S": 54, "T": 55, "U": 56,
             "V": 57, "W": 58, "X": 59, "Y": 60, "Z": 61,
             "-": 62, "_": 63}
    result = 0
    for i in range(len(str)):
        result *= 64
        result += table[str[i]]
    return result


def handle_phone_list(phone_list, kl, kl_limit):
    zl = len(phone_list)
    if zl >= kl_limit:
        kl = int(zl * kl / 100)
        kl_list = phone_list[0: kl]
        phone_list = phone_list[kl:]
        random.shuffle(kl_list), random.shuffle(phone_list)
    else:
        kl_list, phone_list = [], phone_list
    return [[i] for i in kl_list], phone_list


def file_to_db(user_id, text, channel_id, phone_list, url=None):
    with ChannelDB() as db:
        # 查看通道详情
        channel_type, is_have_danfa, is_have_qunfa, max_send, min_send, max_text_len, additional_code, \
        need_report = db.show_channel_type(channel_id)
    with UserDB() as db:
        # 查看平台详情
        plateform_id, kl_limit, kl, user = db.get_user_and_plateformid(user_id)
    # kl
    kl_list, phone_list = handle_phone_list(phone_list, kl, kl_limit)
    new_phone_list = kl_list + phone_list
    random.shuffle(new_phone_list)

    if url not in ['null', None, '']:
        # 需要替换url, 就只能单发
        p = mpipeline()
        for to in new_phone_list:
            with Callback() as db1:
                # 存入callback表
                _id = db1.add(to[0] if isinstance(to, list) else to, url, plateform_id)
            new_text = text.replace(Url.replace_str, Url.base_url + encode_b64(_id))
            _ = str(time.time()).split('.')
            data = {
                'id': int(_[0]) + int(_[1]) + int(user_id),
                'to': to,
                'user': user,
                'user_id': user_id,
                'channel_id': channel_id,
                'plateform_id': plateform_id,
                'text': new_text,
                'callback_id': _id,
                'is_click': '未点击',
                'is_qunfa': False
            }
            p.lpush(f'sms_{plateform_id}', json.dumps(data))
        p.execute()
    elif channel_type == 'manual':
        # 如果是手动发的通道就把数据直接存入pending
        n = 0
        with SmsPendingDB() as db:
            message_id = db.is_have_text(text)
            if message_id is None:
                message_id = int(time.time())
            for to in new_phone_list:
                if db.add(user_id, message_id, to[0] if isinstance(to, list) else to, text, channel_id, commit=False):
                    n += 1
            if n:
                db.commit()
    else:
        # 不需要替换url并且不是手动发送
        if is_have_qunfa:
            # 如果该通道支持群发就按照通道最大发送限制写入redis
            with SmsPendingDB() as db:
                n = 0
                for k in kl_list:
                    if db.add(user_id, Sql.kl_message_id, k[0], text, channel_id, plateform_id, is_click='未设置', user=user, commit=False):
                        n = 1
                if n:
                    db.commit()

            start = 0
            already_handle = 0
            for i in range(max_send, len(phone_list)+1, max_send):
                _ = str(time.time()).split('.')
                data = {
                    'id': int(_[0]) + int(_[1]) + int(user_id),
                    'to': phone_list[start: i],
                    'user': user,
                    'user_id': user_id,
                    'channel_id': channel_id,
                    'plateform_id': plateform_id,
                    'text': text,
                    'is_qunfa': True
                }
                mpush(json.dumps(data), f'sms_{plateform_id}')
                already_handle = 1
                start = i

            if already_handle == 0:
                _ = str(time.time()).split('.')
                data = {
                    'id': int(_[0]) + int(_[1]) + int(user_id),
                    'to': phone_list,
                    'user': user,
                    'user_id': user_id,
                    'channel_id': channel_id,
                    'plateform_id': plateform_id,
                    'text': text,
                    'is_qunfa': True
                }
                mpush(json.dumps(data), f'sms_{plateform_id}')
            elif len(phone_list) % max_send:
                _ = str(time.time()).split('.')
                data = {
                    'id': int(_[0]) + int(_[1]) + int(user_id),
                    'to': phone_list[i:],
                    'user': user,
                    'user_id': user_id,
                    'channel_id': channel_id,
                    'plateform_id': plateform_id,
                    'text': text,
                    'is_qunfa': True
                }
                mpush(json.dumps(data), f'sms_{plateform_id}')
        else:
            # 如果通道不支持群发就一条一条存入redis
            p = mpipeline()
            for to in new_phone_list:
                _ = str(time.time()).split('.')
                data = {
                    'id': int(_[0]) + int(_[1]) + int(user_id),
                    'to': to,
                    'user': user,
                    'user_id': user_id,
                    'channel_id': channel_id,
                    'plateform_id': plateform_id,
                    'text': text,
                    'is_qunfa': False
                }
                p.lpush(f'sms_{plateform_id}', json.dumps(data))
            p.execute()


def delete_template_by_plateform(template_id_list, user_id):
    with TemplateDB() as db:
        for i in template_id_list:
            db.delete_by_plateform(user_id, i)
        return True


def handel_callback(data, channel):
    """
        dcy
        [
            {
                'customparameters': '',
                'taskcode': '1587097497527475013',
                'status': '成功',
                'reportstate': 'DELIVRD',
                'mobile': '18529073798',
                'receivingdate': '2020-04-03 15:37:37'
            }
        ]
        wb
        {
            'result': '0',
            'desc': '成功',
            'sign': '872A27B31693E495CD255FF2EC0E5A5E',
            'timestamp': '20200421115904333',
            'report': [{
                'result': 'faild',
                'phone': '13713871617',
                'netway_code': '0',
                'msgid': 'E15C62A944C26452',
                'seq': '1'}]
        }
        sms123模板创建回调
        {
            'action': 'templateStatusCallback',
            'status': 'Approved',
            'actionCode': 'E00101',
            'messageContent': '测试api创建模板',
            'referenceId': '1594885607'
        }
    """
    report_list = json.loads(data)
    if channel == 'sms123':
        template_id = report_list['referenceId']
        status = 'SUCCESS' if report_list['actionCode'] == SMS123.template_callback_success_code else report_list['status']
        with TemplateDB() as db:
            db.update_status(template_id, status)
        return True

    if channel == 'dcy':
        report_list = report_list
    elif channel == 'wb':
        report_list = report_list['report']

    for i in report_list:
        _ = {'bPartyNumber': ''}
        if channel == 'dcy':
            _['phone'] = i['mobile']
            _['transId'] = i['taskcode']
            _['status'] = 'SUCCESS' if i['status'] == DCY.success_code else 'ERROR'
            _['statusMessage'] = 'SUCCESS' if i['reportstate'] == DCY.success_message else i['reportstate']
        elif channel == 'wb':
            _['phone'] = i['phone']
            _['transId'] = i['msgid']
            _['status'] = 'SUCCESS' if i['result'] == WB.success_code else 'ERROR'
            _['statusMessage'] = 'SUCCESS' if i['result'] == WB.success_code else i['result']
        mpush(json.dumps(_), RedisSql.result_queue_name)


def is_click(_id):
    did = decode_b64(_id)
    with Callback() as db:
        to, url, plateform_id = db.show(did)
    if to is not None:
        with SmsHistoryDB() as db:
            db.update_is_click(did, plateform_id)
    return to, url


# --------------------------------------------------------
# 总后台使用
# --------------------------------------------------------
def super_login(usr, pwd):
    with UserDB() as db:
        return db.is_superuser(usr, pwd)


def backstage_get_user_by_plid(plateform_id):
    with UserDB() as db:
        return db.backstage_get_users(plateform_id)


def backstage_add_user(usr, pwd, auth, plateform_id):
    with UserDB() as db:
        return db.backstage_create_user(usr, pwd, auth, plateform_id)


def backstage_del_user_by_id(u_id):
    with UserDB() as db:
        return db.del_user(u_id)


def backstage_newpassword_by_id(u_id, newpassword):
    with UserDB() as db:
        return db.change_password(u_id, newpassword)


def get_all_plateform_info(page, need_all, plateform_name):
    with PlateformDB() as db:
        if need_all == 1:
            return db.search_plateform_info(page, need_limit=False)
        page_list, all_count = db.search_page(plateform_name=plateform_name)
        value_list = db.search_plateform_info(page, plateform_name=plateform_name)
        return {'page_list': page_list, 'total': all_count, 'value_list': value_list}


def backstage_recharge(amount, plateform_id):
    with PlateformDB() as db:
        return db.backstage_recharge_by_id(amount, plateform_id)


def backstage_update_plateform_by_id(plateform_id, name, domain, is_active, rate_list):
    with PlateformDB() as db:
        return db.backstage_update_plateform_info(plateform_id, name, domain, is_active, json.loads(rate_list))


def backstage_create_plateform(name, domain):
    with PlateformDB() as db:
        return db.backstage_create_plateform(name, domain)


def get_all_channel_info():
    with ChannelDB() as db:
        return db.backstage_show_all_channel()


def backstage_update_channel_by_id(channel_id, name, des, is_active):
    with ChannelDB() as db:
        return db.backstage_update_channel(channel_id, name, des, is_active)


def backstage_change_whitelist_by_plid(plateform_id, status):
    with WhiteList() as db:
        return db.change_ip_status(status, plateform_id=plateform_id)


def backstage_get_whitelist_by_plid(plateform_id, page):
    with WhiteList() as db:
        status = db.get_white_ip_status(plateform_id=plateform_id)
        value_list = db.get_all_ip(page, plateform_id=plateform_id)
        page_list, total = db.search_page(plateform_id=plateform_id)
        return {'page_list': page_list, 'total': total, 'value_list': value_list, 'status': status}


def backstage_add_whitelist(ip, memo, plateform_id):
    with WhiteList() as db:
        return db.backstage_add_whitelist(ip, memo, plateform_id)


def backstage_del_whitelist_by_id(whitelist_id):
    with WhiteList() as db:
        return db.backstage_del_whitelist(whitelist_id)


def get_all_manual(message_id):
    with SmsPendingDB() as db:
        data = db.search_manual(message_id)
    if message_id not in ['null', None, '']:
        excelTabel = xlwt.Workbook()  # exel表格实例
        new_data = []
        start = 0
        for i in range(65535, len(data) + 1, 65535):
            new_data.append(data[start: i])
            start = i
        if not new_data:
            new_data.append(data)
        else:
            if len(data) % 65535:
                new_data.append(data[i:])
        for i in range(len(new_data)):
            sheet = excelTabel.add_sheet(f'sms_{i}')
            for c in range(0, len(new_data[i])):
                sheet.write(c, 0, new_data[i][c][0])
        now = time.strftime("%Y-%m-%d_%H-%M-%S", time.localtime(int(time.time())))
        file_name = f'{Page.excel_file_path}{now}.xls'
        excelTabel.save(file_name)
        return file_name, f'{now}.xls'
    else:
        new_data = []
        for i in data:
            new_data.append({
                "message_id": i[2],
                'text': i[1],
                'success_count': 0,
                'failed_count': 0,
                'pending_count': i[0],
                'all_count': i[0]
            })
        return new_data, None


def update_manual_by_phone(phone_list, message_id):
    p = mpipeline()
    for i in phone_list:
        data = {
            'bPartyNumber': '',
            'status': i[1],
            'transId': message_id,
            'statusMessage': i[1],
            'phone': i[0]
        }
        p.lpush(RedisSql.result_queue_name, json.dumps(data))
    p.execute()


def get_need_template_channel_by_plateform():
    with ChannelDB() as db:
        return db.show_need_template_channel()


def get_all_template_info(page, user_id=None):
    with TemplateDB() as db:
        page_list, all_count = db.search_page(user_id=user_id)
        value_list = db.search_all_template(page, user_id=user_id)
        return {'page_list': page_list, 'total': all_count, 'value_list': value_list}


def get_need_template_channel():
    with ChannelDB() as db:
        return db.backstage_show_need_template_channel()


def create_template_dispather(_id, template, template_title, channel_type):
    if channel_type == 'http_sms123':
        # {'status': 'ok', 'msgCode': 'E00001', 'statusMsg': 'Completed successfully.'}
        data = {
            "apiKey": SMS123.apikey,
            "email": SMS123.email,
            "templateTitle": template_title,
            "messageContent": template,
            "referenceId": _id
        }
        resp = my_requests(SMS123.create_template_url, 'post', params=data, need_json_params=True)
        resp = True if resp and resp['msgCode'] == SMS123.create_template_return_success_code else False
    else:
        resp = False
    return resp


def create_template(channel_id, template, channel_type, plateform_id=None, user_id=None):
    with TemplateDB() as db:
        if db.is_have_template(template, channel_id, plateform_id, user_id):
            return '请勿重复添加!'
        _ = str(time.time()).split('.')
        _id = int(_[0]) + int(_[1])
        resp = create_template_dispather(_id, template, _id, channel_type)
        if resp:
            return db.add(channel_id, template, _id, plateform_id, user_id)
        return '未找到该通道!'


def delete_template_by_id(templates_id):
    with TemplateDB() as db:
        return db.delete_by_id(templates_id)


def get_sentitive_words(channel_id, page):
    with SensitiveWordsDB() as db:
        page_list, all_count = db.search_page(channel_id)
        value_list = db.backstage_show_all_sensitive_words(channel_id, page)
        return {'page_list': page_list, 'total': all_count, 'value_list': value_list}


def create_sensitive_words(channel_id, sentitive):
    with SensitiveWordsDB() as db:
        return db.backstage_create_sensitive_words(channel_id, sentitive)


def delete_sensitive_words(sensitive_id):
    with SensitiveWordsDB() as db:
        return db.backstage_delete_sensitive_words(sensitive_id)

