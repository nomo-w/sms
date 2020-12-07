# coding: utf-8


from flask import Flask, request, make_response, send_file, redirect, render_template
from config import Upload, RedisSql, Return_Statua_Code, Page, Url
from db.sensitive_words import SensitiveWordsDB
from db.myredis import mset, mget
from util import api, log, login
from db.channel import ChannelDB
from util.excel import Excel
from flask_cors import CORS
from db.users import UserDB

import threading
import time
import json
import os


app = Flask('web')
CORS(app, supports_credentials=True)
app.secret_key = 'ABCAz47j22AA#R~X@H!jLwf/A'
login.init(app, 'login_failed')
log.init()


@app.route('/api/login_failed')
@api.handle_api_zsq('/api/login_failed', 'GET')
def login_failed():
    """登陆失败后的返回"""
    return api.handle_httpresponse('未登录!')


# --------------------------------------------------------
# 插入信息到数据库sms_sending
# 给外部的接口
# --------------------------------------------------------
@app.route('/api/send', methods=['post'])
@api.handle_api_zsq('/api/send', 'POST')
def yunying_send():
    domain = request.form['domain']
    channel_id, usr, pwd = request.form['channel_id'], request.form['user'], request.form['password']
    to_number, text = request.form['to_number'], request.form['text']

    with UserDB() as db:
        uid = db.is_right_password(usr, pwd, domain)
    if uid == -1:
        return api.handle_httpresponse('用户名或密码错误!')
    if not api.get_is_running(user_id=uid, domain=domain):
        return api.handle_httpresponse('平台已停止!')

    with SensitiveWordsDB() as db:
        for i in db.get_sensitive_words_by_channel(channel_id):
            if i in text:
                return api.handle_httpresponse(f'短信内容包含敏感词[{i}], 请修改之后重新发送!')

    with ChannelDB() as db:
        channel_type, is_have_danfa, is_have_qunfa, max_send, min_send, max_text_len, additional_code, \
        need_report = db.show_channel_type(channel_id)
    phone_list = [f'{additional_code}{i}' if additional_code else i for i in to_number.split(',')]

    if channel_type == '':
        return api.handle_httpresponse('该通道已关闭, 请选择其他通道!')

    if len(phone_list) < min_send:
        return api.handle_httpresponse(f'手机号数量不足, 该通道最小发送量为{min_send}条每次')
    if len(text) > max_text_len:
        return api.handle_httpresponse(f'短信内容过长, 短信长度限制为{max_text_len}个字符内')

    # user_id, text, channel_id, phone_list, url=None
    threading.Thread(target=api.file_to_db, args=(uid, text, channel_id, phone_list, None)).start()
    return api.handle_httpresponse('发送成功!', 0)


# --------------------------------------------------------
# 关于用户的操作
# 用户系统 - 登入/登出/新建/修改密码
# --------------------------------------------------------
@app.route('/api/user/login', methods=['post'])
@api.handle_api_zsq('/api/user/login', 'POST')
@api.white_required
def login_request():
    """
    登陆!!!
    method: post
    args: user,password
    :return: {"ret":true}
    """
    url = request.headers.get('Origin')
    user, password = request.form['user'], request.form['password']
    user_id = api.login_api(user, password, url.split('/')[2])
    if user_id != -1:
        # 找到用户
        login.login(user_id)
        return api.handle_httpresponse('登陆成功!', 0)
    return api.handle_httpresponse('账户或密码错误!')


@app.route('/api/get_plateform')
@login.login_required
@api.handle_api_zsq('/api/get_plateform', 'GET')
def get_plateform():
    """
    获取平台名
    """
    uid = login.get_cur_user_id()
    plateform_name = api.get_plateform_name(uid)
    return api.handle_httpresponse(plateform_name, 0)


@app.route('/api/user/logout', methods=['post'])
@login.login_required
@api.handle_api_zsq('/api/user/logout', 'POST')
def logout():
    login.logout()
    return api.handle_httpresponse('登出!', 0)


@app.route('/api/user/change_self_password', methods=['post'])
@login.login_required
@api.handle_api_zsq('/api/user/change_self_password', 'POST')
def change_self_password():
    """
    修改密码
    method: post
    args: newpassword
    :return: {"ret":true}
    """
    user_id, newpassword = login.get_cur_user_id(), request.form['password']
    if api.change_password(user_id, newpassword):
        return api.handle_httpresponse('修改成功!', 0)
    return api.handle_httpresponse('修改失败!')


@app.route('/api/user/add', methods=['post'])
@login.login_required
@api.handle_api_zsq('/api/user/add', 'POST')
def create_user():
    """
    创建用户
    :return:
    """
    user, password = request.form['user'], request.form['password']
    resp = api.create_user(user, password, login.get_cur_user_id())
    return api.handle_httpresponse(resp, 0 if resp == '添加成功!' else -1)


@app.route('/api/user/get_all')
@login.login_required
@api.handle_api_zsq('/api/user/get_all', 'GET')
def get_all_user():
    """
    获取所有用户
    """
    return api.handle_httpresponse(api.get_all_user(login.get_cur_user_id()), 0)


@app.route('/api/user/del_by_id', methods=['post'])
@login.login_required
@api.handle_api_zsq('/api/user/del_by_id', 'POST')
def del_user_by_id():
    """
    删除用户
    :return: {"ret":true}
    """
    user_id = request.form['user_id']
    resp = api.del_user(user_id, login.get_cur_user_id())
    return api.handle_httpresponse(resp, 0 if resp == '成功删除!' else -1)


# --------------------------------------------------------
# 关于项目的状态的操控
# 开始/停止/状态
# --------------------------------------------------------
@app.route('/api/main/is_running')
@login.login_required
@api.handle_api_zsq('/api/main/is_running', 'GET')
def get_is_running():
    """
    是否运行中
    :return: {"ret":true}
    """
    user_id = login.get_cur_user_id()
    return api.handle_httpresponse(api.get_is_running(user_id), 0)


@app.route('/api/main/start', methods=['post'])
@login.login_required
@api.handle_api_zsq('/api/main/start', 'POST')
def start_send():
    """
    :return: {ret:true, msg:启动成功}
    """
    user_id = login.get_cur_user_id()
    resp = api.start_send(user_id)
    return api.handle_httpresponse(resp, 0 if resp == '启动成功!' else -1)


@app.route('/api/main/stop', methods=['post'])
@login.login_required
@api.handle_api_zsq('/api/main/stop', 'POST')
def stop_send():
    """
    停止发送
    :return: {"ret":true, "msg":"停止成功"}
    """
    user_id = login.get_cur_user_id()
    resp = api.stop_send(user_id)
    return api.handle_httpresponse(resp, 0 if resp == '停止成功!' else -1)


# --------------------------------------------------------
# 关于白名单的操作
# 白名单         - 新建/删除/获取所有
# --------------------------------------------------------
@app.route('/api/white_ip/changeStatus', methods=['post'])
@login.login_required
@api.handle_api_zsq('/api/white_ip/changeStatus', 'POST')
def change_white_ip_status():
    user_id, status = login.get_cur_user_id(), request.form['status']
    resp = api.change_white_ip_status(user_id, int(status))
    return api.handle_httpresponse('更改成功!' if resp else '更改失败!', 0 if resp else -1)


@app.route('/api/white_ip/get_all', methods=['post'])
@login.login_required
@api.handle_api_zsq('/api/white_ip/get_all', 'POST')
def get_white_ip():
    """
    获取所有白名单信息
    :return: [
              {
                "id": 6,
                "ip": "1.1.1.1",
                "memo": "test1"
              },
              {
                "id": 8,
                "ip": "2.2.2.2",
                "memo": "A2"
              }
            ]
    """
    user_id, page = login.get_cur_user_id(), request.form.get('page', None)
    page = int(page) - 1 if page not in ['null', None, '', 0, '0'] else 0
    return api.handle_httpresponse(api.get_white_ip(user_id, page), 0)


@app.route('/api/white_ip/add', methods=['post'])
@login.login_required
@api.handle_api_zsq('/api/white_ip/add', 'POST')
def add_white_ip():
    """
    添加白名单ip
    :method post
    param ip:
    param memo: 备注
    :return: {"ret":true}
    """
    ip, memo = request.form['ip'], request.form.get('memo', '')
    resp = api.add_white_ip(ip, memo, login.get_cur_user_id())
    return api.handle_httpresponse(resp, 0 if resp == '添加成功!' else -1)


@app.route('/api/white_ip/del_by_id', methods=['post'])
@login.login_required
@api.handle_api_zsq('/api/white_ip/del_by_id', 'POST')
def del_white_ip_by_id():
    """
    根据id删除白名单ip行
    :method post
    param _id:
    :return: {"ret":true}
    """
    whitelist_id = request.form['id']
    return api.handle_httpresponse(api.del_white_ip_by_id(whitelist_id), 0)


# --------------------------------------------------------
# 关于redis队列的操作
# 当前发送队列    - 列队数量
# --------------------------------------------------------
@app.route('/api/queue/get_count')
@login.login_required
@api.handle_api_zsq('/api/queue/get_count', 'GET')
def get_queue_count():
    """
    队列数量
    :return: {"count":153}
    """
    return api.handle_httpresponse(api.get_queue_count(login.get_cur_user_id()), 0)


@app.route('/api/queue/empty', methods=['post'])
@login.login_required
@api.handle_api_zsq('/api/queue/empty', 'POST')
def empty_queue():
    """
    清空列队
    :return: {"ret":True}
    """
    resp = api.empty_queue(login.get_cur_user_id())
    return api.handle_httpresponse(resp, 0)


# --------------------------------------------------------
# 个人页面信息
# 关于统计信息查询
# 统计信息
# --------------------------------------------------------
@app.route('/api/search/days', methods=['post'])
@login.login_required
@api.handle_api_zsq('/api/search/days', 'POST')
def analysis_by_day():
    """
    返回一个多少天之间的统计，展示在统计信息页面
    search_time = time>=start and time<=end  （单位:天）
    param start: yyyy-MM-dd
    param end: yyyy-MM-dd
    :return: {"all_count":10, "success_count":8, "price_sum":"8.30200"}
    """
    start, end, user_id = request.form['start'], request.form['end'], login.get_cur_user_id()
    all_count, success_count, price_sum = api.analysis_by_day(start, end, user_id)
    return api.handle_httpresponse(
        dict(all_count=all_count, suc_count=success_count, price_sum=round(float(price_sum), 2)), 0)


@app.route('/api/search/group_days', methods=['post'])
@login.login_required
@api.handle_api_zsq('/api/search/group_days', 'POST')
def analysis_by_day_group():
    """
    返回一个多少天之间的，每天的数据统计，展示在个人页面
    param start: yyyy-MM-dd
    param end: yyyy-MM-dd
    :return: ((success_count,price_sum,time('%Y-%m-%d')),(success_count2, price_sum2,time('%Y-%m-%d')),...)
    """
    start, end, user_id = request.form['start'], request.form['end'], login.get_cur_user_id()
    return api.handle_httpresponse(api.analysis_by_day_group(start, end, user_id), 0)


@app.route('/api/search/all')
@login.login_required
@api.handle_api_zsq('/api/search/all', 'GET')
def analysis_all():
    """
    查询可用余额，用来展示在个人页面的
    发送总数/发送成功总数/余额
    :return: {"all_count":10, "success_count":8, "all_balance":"100.36"}
    """
    all_count, success_count, balance = api.analysis_all(login.get_cur_user_id())
    return api.handle_httpresponse(dict(
        all_count=all_count, suc_count=success_count, all_balance=balance
    ), 0)


# --------------------------------------------------------
# 查询所有通道
# --------------------------------------------------------
@app.route('/api/search/all_channels')
@login.login_required
@api.handle_api_zsq('/api/search/all_channels', 'GET')
def search_channel():
    """
    返回通道信息 {'data': ['id': 1, 'name': '菲律宾线路', 'rate': 0.36], 'status': 200}
    :return:
    """
    data = api.search_all_channel_info(login.get_cur_user_id())
    return api.handle_httpresponse(data, 0)


# --------------------------------------------------------
# 查询历史记录
# --------------------------------------------------------
@app.route("/api/download/file")
@login.login_required
@api.handle_api_zsq("/api/download/file", "GET")
def download_file():
    # 根据文件名下载文件
    user_id = login.get_cur_user_id()
    file_name = request.args['file_name']
    file_path = f'{Page.excel_file_path}{file_name}'
    with UserDB() as db:
        if db.get_auth(user_id) == 'admin':
            if os.path.exists(file_path):
                response = make_response(send_file(file_path))
                response.headers["Content-Disposition"] = f"p_w_upload; filename={file_name};"
                return response
            else:
                return api.handle_httpresponse(f'未找到该文件[{file_name}]')
        else:
            return api.handle_httpresponse('您无导出权限,请联系管理员下载')


@app.route('/api/search/get_auth')
@login.login_required
@api.handle_api_zsq('/api/search/get_auth', 'GET')
def is_admin():
    with UserDB() as db:
        return api.handle_httpresponse(db.get_auth(login.get_cur_user_id()), 0)


@app.route("/api/search/jobStatus", methods=['post'])
@login.login_required
@api.handle_api_zsq("/api/search/jobStatus", 'POST')
def get_file_status():
    jobId = request.form['jobId']
    data = mget(jobId)
    if data is None:
        resp = api.handle_httpresponse({'job_status': Return_Statua_Code.job_failed}, 0)
    elif data[:3] == RedisSql.job_status_code['success']:
        resp = api.handle_httpresponse({'job_status': Return_Statua_Code.job_success, 'data':
            json.loads(data[9:]) if data[4:8] == 'data' else data[9:]}, 0)
    elif data[:3] == RedisSql.job_status_code['pending']:
        resp = api.handle_httpresponse({'job_status': Return_Statua_Code.job_pending}, 0)
    else:
        resp = api.handle_httpresponse({'job_status': Return_Statua_Code.job_failed}, 0)
    return resp


@app.route('/api/search/history', methods=['post'])
@login.login_required
@api.handle_api_zsq('/api/search/history', 'POST')
def search_by_number_day_status():
    """
    按照号码/状态/开始时间/结束时间搜索，分页返回所有查询到的数据。默认每页显示15个
    param number: 号码
    param status: 状态(数据库err字段。非0代表失败)
    param start: 开始时间 yyyy-MM-dd hh:mm:ss
    param end: 结束时间 yyyy-MM-dd hh:mm:ss
    param page: 页数
    param excel: 是否生成excel表格(0代表需要生成excel表格)
    :return: ((xxx,xxx,xxx),(yyy,yyy,yyy),...)
    """
    user_id = login.get_cur_user_id()
    to_number = request.form.get('number')
    start, end = request.form.get('start'), request.form.get('end')
    page = request.form.get('page')
    status = request.form.get('status')
    channel_id = request.form.get('channel_id', None)
    channel_id = channel_id if channel_id not in [None, '', 'null'] else None
    status = int(status) if status not in [None, '', 'null'] else ''
    need_excel = request.form.get('excel')
    need_excel = int(need_excel) if need_excel else ''
    _ = str(time.time()).split('.')
    jobId = str(int(_[0]) + int(_[1]) + int(user_id))
    if need_excel == 0:
        with UserDB() as db:
            if db.get_auth(user_id) == 'admin':
                mset(jobId, f'{RedisSql.job_status_code["pending"]}|file|', 60*20)
                threading.Thread(target=api.async_job, args=(to_number, start, end, status, page, 0,
                                user_id, channel_id, False, jobId)).start()
                return api.handle_httpresponse(jobId, 0)
            else:
                return api.handle_httpresponse('您无导出权限,请联系管理员下载')
    else:
        mset(jobId, f'{RedisSql.job_status_code["pending"]}|data|', 60 * 20)
        threading.Thread(target=api.async_job, args=(to_number, start, end, status, page,
                        1, user_id, channel_id, True, jobId)).start()
        return api.handle_httpresponse(jobId, 0)


# --------------------------------------------------------
# 查询充值记录
# --------------------------------------------------------
@app.route('/api/search/recharge_record', methods=['post'])
@login.login_required
@api.handle_api_zsq('/api/search/recharge_record', 'POST')
def search_recharge_record():
    """
    查询充值记录
    param start: 开始时间 yyyy-MM-dd hh:mm:ss
    param end: 结束时间 yyyy-MM-dd hh:mm:ss
    param page: 页数
    :return: {"data": [{"recharge_amount": 2.11, "recharge_time": "...", ...}, "page_list": [1, 2], "total": 21]}
    """
    user_id = login.get_cur_user_id()
    start, end, page = request.form.get('start'), request.form.get('end'), request.form.get('page')
    start, end = [i if i not in (None, 'none', '', 'None', 'null') else None for i in [start, end]]
    page = int(page) - 1 if page not in (None, 'none', '', 'None', 'null', 0, '0') else None
    resp, _ = api.search_recharge(start, end, page, user_id=user_id)
    return api.handle_httpresponse(resp, 0)


# --------------------------------------------------------
# 文件上传
# --------------------------------------------------------
@app.route('/api/upload/phone_file', methods=['post'])
@login.login_required
@api.handle_api_zsq('/api/upload/phone_file', 'POST')
def upload_phone_file():
    """
    上传文件
    :return: {"ret":true,"err":"上传完成"} / {"ret":false,"err":"请输入短信内容"}
    """
    user_id = login.get_cur_user_id()
    sms_text, channel_id, domain = request.form['sms_text'], request.form['channel_id'], request.form.get('domain', None)
    if not api.get_is_running(user_id):
        return api.handle_httpresponse('平台已停止, 请启动平台后再次尝试!')
    file = request.files.get('file')
    if file and '.xlsx' in file.filename:
        save_path = f'{Upload.upload_phone_file_path}{user_id}_{time.strftime("%Y-%m-%d_%H-%M-%S", time.localtime())}.xlsx'
        file.save(save_path)

        with SensitiveWordsDB() as db:
            for i in db.get_sensitive_words_by_channel(channel_id):
                if i in sms_text:
                    return api.handle_httpresponse(f'短信内容包含敏感词[{i}], 请修改之后重新发送!')

        with ChannelDB() as db:
            channel_type, is_have_danfa, is_have_qunfa, max_send, min_send, max_text_len, additional_code, \
            need_report = db.show_channel_type(channel_id)
        if channel_type == '':
            return api.handle_httpresponse('该通道已关闭, 请使用其他通道发送短信!')
        if domain not in ['null', None, '']:
            if (len(sms_text) - 3 + len(Url.base_url) + 5) > max_text_len:
                return api.handle_httpresponse(f'短信内容过长, 短信长度限制为{max_text_len-(len(Url.base_url)+5-3)}个字符内, 当前长度为{len(sms_text)}')
        elif len(sms_text) > max_text_len:
            return api.handle_httpresponse(f'短信内容过长, 短信长度限制为{max_text_len}个字符内, 当前长度为{len(sms_text)}')
        if domain not in ['null', None, ''] and not is_have_danfa:
            return api.handle_httpresponse(f'该通道不支持单独发送, 替换url需要每条单独发送, 请选择其他通道!')
        # 解析xlsx
        el = Excel(filename=save_path)
        ct = []
        for row in el.rows():
            ct.append(tuple([str(cell.value).replace('"', '') for cell in row]))
        to_numbers = []
        for r in ct:
            if r[0] not in (None, 'none', '', 'None', 'null') and len(r[0]) <= 20:
                if additional_code:
                    to_numbers.append(f'{additional_code}{r[0]}')
                else:
                    to_numbers.append(r[0])
        phone_list = list(set(to_numbers))
        if len(phone_list) < min_send:
            return api.handle_httpresponse(f'手机号数量不足, 该通道最小发送量为{min_send}条每次!')
        if mget(f'is_have_job_{user_id}') is not None:
            return api.handle_httpresponse('提交速度过快, 30秒之后再次尝试!')
        else:
            mset(f'is_have_job_{user_id}', 'yes', 30)
        threading.Thread(target=api.file_to_db, args=(user_id, sms_text, channel_id, phone_list, domain)).start()
        return api.handle_httpresponse('上传完成', 0)
    else:
        return api.handle_httpresponse("错误的文件格式, 只支持xlsx")


# --------------------------------------------------------
# 短信的模板接口
# --------------------------------------------------------
@app.route('/api/search/templateChannel')
@login.login_required
@api.handle_api_zsq('/api/search/templateChannel', 'GET')
def get_need_template_channel_by_plateform():
    return api.handle_httpresponse(api.get_need_template_channel_by_plateform(), 0)


@app.route('/api/search/templates', methods=['post'])
@login.login_required
@api.handle_api_zsq('/api/search/templates', 'POST')
def show_template_by_plateform():
    user_id = login.get_cur_user_id()
    page, channel_id = request.form.get('page', None), request.form.get('channel_id')
    page = int(page) - 1 if page not in ['null', None, '', 0, '0'] else 0
    if channel_id not in ['null', None, '', 0, '0']:
        resp = api.get_template_by_channel(channel_id, user_id)
    else:
        resp = api.get_all_template_info(page, user_id)
    return api.handle_httpresponse(resp, 0)


@app.route('/api/create/template', methods=['post'])
@login.login_required
@api.handle_api_zsq('/api/create/template', 'POST')
def create_template_by_plateform():
    user_id = login.get_cur_user_id()
    channel_id, channel_type, template = request.form['channel_id'], request.form['channel_type'], request.form['template']
    resp = api.create_template(channel_id, template, channel_type, user_id=user_id)
    return api.handle_httpresponse(resp, 0 if resp == '创建成功!' else -1)


@app.route('/api/delete/templates', methods=['post'])
@login.login_required
@api.handle_api_zsq('/api/delete/templates', 'POST')
def delete_template_by_plateform():
    user_id = login.get_cur_user_id()
    template_id_list = request.form['templates_id']
    template_id_list = template_id_list.split(',')
    resp = api.delete_template_by_plateform(template_id_list, user_id)
    return api.handle_httpresponse('删除成功!' if resp else '删除失败!', 0 if resp else -1)


# --------------------------------------------------------
# 短信的回调接口
# --------------------------------------------------------
@app.route('/api/callback/<channel>', methods=['post'])
@api.handle_api_zsq('/api/callback', 'post')
def callback(channel):
    data = request.data.decode()
    threading.Thread(target=api.handel_callback, args=(data, channel)).start()
    return 'ok'


@app.route("/<_id>")
@api.handle_api_zsq('/', 'get')
def index(_id):
    to, url = api.is_click(_id)
    if to is not None:
        if url[:4] == 'http':
            return redirect(url)
        return redirect(f'http://{url}')
    return render_template('404.html'), 404


# --------------------------------------------------------
# 总后台的接口
# --------------------------------------------------------
@app.route('/backstage/login', methods=['post'])
@api.handle_api_zsq('/backstage/login', 'POST')
def backstage_login():
    # 登录
    usr, pwd = request.form['user'], request.form['password']
    user_id = api.super_login(usr, pwd)
    if user_id != -1:
        login.login(user_id)
        return api.handle_httpresponse('登陆成功!', 0)
    return api.handle_httpresponse('账户或密码错误!')


@app.route('/backstage/userInfo', methods=['post'])
@login.login_required
@api.is_superuser_zsq
@api.handle_api_zsq('/backstage/userInfo', 'POST')
def all_user():
    # 获取所有用户信息
    plid = request.form['plateform_id']
    return api.handle_httpresponse(api.backstage_get_user_by_plid(plid), 0)


@app.route('/backstage/useradd', methods=['post'])
@login.login_required
@api.is_superuser_zsq
@api.handle_api_zsq('/backstage/useradd', 'POST')
def user_add():
    # 添加用户
    usr, pwd, plid, auth = request.form['user'], request.form['password'], request.form['plateform_id'], request.form['auth']
    resp = api.backstage_add_user(usr, pwd, auth, plid)
    return api.handle_httpresponse(resp, 0 if resp == '添加成功!' else -1)


@app.route('/backstage/userdel', methods=['post'])
@login.login_required
@api.is_superuser_zsq
@api.handle_api_zsq('/backstage/userdel', 'POST')
def user_del():
    # 删除用户
    user_id = request.form['user_id']
    resp = api.backstage_del_user_by_id(user_id)
    return api.handle_httpresponse(resp, 0 if resp == '成功删除!' else -1)


@app.route('/backstage/newpassword', methods=['post'])
@login.login_required
@api.is_superuser_zsq
@api.handle_api_zsq('/backstage/newpassword', 'POST')
def user_update():
    # 修改用户密码
    user_id, newpassword = request.form['user_id'], request.form['password']
    resp = api.backstage_newpassword_by_id(user_id, newpassword)
    return api.handle_httpresponse('删除成功!' if resp else '删除失败!', 0 if resp else -1)


@app.route('/backstage/plateformInfo', methods=['post'])
@login.login_required
@api.is_superuser_zsq
@api.handle_api_zsq('/backstage/plateformInfo', 'POST')
def all_plateform():
    # 获取所有平台信息
    plateform_name = request.form.get('plateform_name', None)
    plateform_name = plateform_name if plateform_name not in ['null', None, ''] else None
    page, need_all = request.form.get('page', None), request.form.get('need_all', None)
    page = int(page) - 1 if page not in ['null', None, '', 0, '0'] else 0
    need_all = int(need_all) if need_all not in ['null', None, '', 0, '0'] else 0
    return api.handle_httpresponse(api.get_all_plateform_info(page, need_all, plateform_name), 0)


@app.route('/backstage/recharge', methods=['post'])
@login.login_required
@api.is_superuser_zsq
@api.handle_api_zsq('/backstage/recharge', 'POST')
def recharge():
    # 给平台充值
    amount, plateform_id = request.form['amount'], request.form['plateform_id']
    resp = api.backstage_recharge(round(float(amount), 2), plateform_id)
    return api.handle_httpresponse('充值成功!' if resp else '充值失败!', 0 if resp else -1)


@app.route('/backstage/createPlateform', methods=['post'])
@login.login_required
@api.is_superuser_zsq
@api.handle_api_zsq('/backstage/createPlateform', 'POST')
def create_plateform():
    # 创建平台
    name, domain = request.form['name'], request.form['domain']
    resp = api.backstage_create_plateform(name, domain)
    return api.handle_httpresponse('添加成功!' if resp else '添加失败!', 0 if resp else -1)


@app.route('/backstage/updatePlateform', methods=['post'])
@login.login_required
@api.is_superuser_zsq
@api.handle_api_zsq('/backstage/updatePlateform', 'POST')
def update_plateform():
    # 修改平台信息   平台名/平台绑定域名/开启关闭平台/平台的通道费率
    plid, name, domain = request.form['plateform_id'], request.form['name'], request.form['domain']
    is_active, rate_list = request.form['is_active'], request.form['rate_list']
    resp = api.backstage_update_plateform_by_id(plid, name, domain, is_active, rate_list)
    return api.handle_httpresponse('更改成功!' if resp else '更改失败!', 0 if resp else -1)


@app.route('/backstage/channelInfo')
@login.login_required
@api.is_superuser_zsq
@api.handle_api_zsq('/backstage/channelInfo', 'GET')
def all_channel():
    # 获取所有通道信息
    return api.handle_httpresponse(api.get_all_channel_info(), 0)


@app.route('/backstage/updateChannel', methods=['post'])
@login.login_required
@api.is_superuser_zsq
@api.handle_api_zsq('/backstage/updateChannel', 'POST')
def update_channel():
    channel_id, name = request.form['channel_id'], request.form['name']
    des, is_active = request.form['description'], request.form['is_active']
    resp = api.backstage_update_channel_by_id(channel_id, name, des, int(is_active))
    return api.handle_httpresponse('修改成功!' if resp else '修改失败!', 0 if resp else -1)


@app.route('/backstage/changeWhitelist', methods=['post'])
@login.login_required
@api.is_superuser_zsq
@api.handle_api_zsq('/backstage/changeWhitelist', 'POST')
def change_whitelist():
    plid, status = request.form['plateform_id'], request.form['status']
    resp = api.backstage_change_whitelist_by_plid(plid, int(status))
    return api.handle_httpresponse('更改成功!' if resp else '更改失败!', 0 if resp else -1)


@app.route('/backstage/whitelist', methods=['post'])
@login.login_required
@api.is_superuser_zsq
@api.handle_api_zsq('/backstage/whitelist', 'POST')
def whitelist():
    plid, page = request.form['plateform_id'], request.form.get('page', None)
    page = int(page) - 1 if page not in ['null', None, '', 0, '0'] else 0
    return api.handle_httpresponse(api.backstage_get_whitelist_by_plid(plid, page), 0)


@app.route('/backstage/addWhitelist', methods=['post'])
@login.login_required
@api.is_superuser_zsq
@api.handle_api_zsq('/backstage/addWhitelist', 'POST')
def add_whitelist():
    ip, memo, plateform_id = request.form['ip'], request.form['memo'], request.form['plateform_id']
    resp = api.backstage_add_whitelist(ip, memo, plateform_id)
    return api.handle_httpresponse(resp, 0 if resp == '添加成功!' else -1)


@app.route('/backstage/delWhitelist', methods=['post'])
@login.login_required
@api.is_superuser_zsq
@api.handle_api_zsq('/backstage/delWhitelist', 'POST')
def del_whitelist():
    whitelist_id = request.form['whitelist_id']
    resp = api.backstage_del_whitelist_by_id(whitelist_id)
    return api.handle_httpresponse('删除成功!' if resp else '删除失败!', 0 if resp else -1)


@app.route('/backstage/getManual')
@login.login_required
@api.is_superuser_zsq
@api.handle_api_zsq('/backstage/getManual', 'GET')
def get_manual():
    message_id = request.args.get('message_id', None)
    file_path, file_name = api.get_all_manual(message_id)
    if message_id not in ['null', None, '']:
        response = make_response(send_file(file_path))
        response.headers["Content-Disposition"] = f"p_w_upload; filename={file_name};"
        return response
    return api.handle_httpresponse(file_path, 0)


@app.route('/backstage/updataManual', methods=['post'])
@login.login_required
@api.is_superuser_zsq
@api.handle_api_zsq('/backstage/updataManual', 'POST')
def update_manual():
    file, message_id = request.files.get('file'), request.form['message_id']
    if file and '.xlsx' in file.filename:
        save_path = f'{Upload.upload_phone_file_path}{int(time.time())}.xlsx'
        file.save(save_path)
        # 解析xlsx
        el = Excel(filename=save_path)
        ct = []
        for row in el.rows():
            ct.append(tuple([str(cell.value).replace('"', '') for cell in row]))
        phone_list = []
        for r in ct:
            if r[0] != 'None':
                phone_list.append((r[0], r[1].upper()))
        threading.Thread(target=api.update_manual_by_phone, args=(phone_list, message_id)).start()
        return api.handle_httpresponse('上传成功', 0)
    else:
        return api.handle_httpresponse("错误的文件格式,只支持xlsx")


@app.route('/backstage/showTemplates', methods=['post'])
@login.login_required
@api.is_superuser_zsq
@api.handle_api_zsq('/backstage/showTemplates', 'POST')
def show_templates():
    page = request.form.get('page', None)
    page = int(page) - 1 if page not in ['null', None, '', 0, '0'] else 0
    return api.handle_httpresponse(api.get_all_template_info(page), 0)


@app.route('/backstage/getTemplateChannel')
@login.login_required
@api.is_superuser_zsq
@api.handle_api_zsq('/backstage/getTemplateChannel', 'GET')
def get_need_template_channel():
    return api.handle_httpresponse(api.get_need_template_channel(), 0)


@app.route('/backstage/addTemplates', methods=['post'])
@login.login_required
@api.is_superuser_zsq
@api.handle_api_zsq('/backstage/addTemplates', 'POST')
def add_template():
    channel_id, plateform_id,  = request.form['channel_id'], request.form['plateform_id']
    template, channel_type = request.form['template'], request.form['channel_type']
    resp = api.create_template(channel_id, template, channel_type, plateform_id=plateform_id)
    return api.handle_httpresponse(resp, 0 if resp == '创建成功!' else -1)


@app.route('/backstage/delTemplates', methods=['post'])
@login.login_required
@api.is_superuser_zsq
@api.handle_api_zsq('/backstage/delTemplates', 'POST')
def del_templates():
    templates_id = request.form['templates_id']
    resp = api.delete_template_by_id(templates_id)
    return api.handle_httpresponse('删除成功!' if resp else '删除失败!', 0 if resp else -1)


@app.route('/backstage/showSensitive', methods=['post'])
@login.login_required
@api.is_superuser_zsq
@api.handle_api_zsq('/backstage/showSensitive', 'POST')
def show_sensitive():
    channel_id, page = request.form.get('channel_id'), request.form.get('page')
    page = int(page) - 1 if page not in ['null', None, '', 0, '0'] else 0
    channel_id = channel_id if channel_id not in ['null', None, '', 0, '0'] else None
    return api.handle_httpresponse(api.get_sentitive_words(channel_id, page), 0)


@app.route('/backstage/createSensitive', methods=['post'])
@login.login_required
@api.is_superuser_zsq
@api.handle_api_zsq('/backstage/createSensitive', 'POST')
def create_sensitive():
    channel_id, sensitive = request.form['channel_id'], request.form['sensitive']
    resp = api.create_sensitive_words(channel_id, sensitive)
    return api.handle_httpresponse('创建成功!' if resp else '创建失败!', 0 if resp else -1)


@app.route('/backstage/delSensitive', methods=['post'])
@login.login_required
@api.is_superuser_zsq
@api.handle_api_zsq('/backstage/delSensitive', 'POST')
def delete_sensitive():
    sensitive_id = request.form['sensitive_id']
    resp = api.delete_sensitive_words(sensitive_id)
    return api.handle_httpresponse('删除成功!' if resp else '删除失败!', 0 if resp else -1)


@app.route('/backstage/showRecharge')
@login.login_required
@api.is_superuser_zsq
@api.handle_api_zsq('/backstage/showRecharge', 'GET')
def show_recharge():
    plateform_id, page = request.args.get('plateform_id', None), request.args.get('page', None)
    start, end, need_excel = request.args.get('start', None), request.args.get('end', None), request.args.get('excel', None)
    plateform_id, page, start, end, need_excel = [i if i not in ['null', None, ''] else None for i in [plateform_id, page, start, end, need_excel]]
    page = int(page) - 1 if page is not None else page
    need_excel = int(need_excel) if need_excel is not None else need_excel
    file_path, file_name = api.search_recharge(start, end, page, plateform_id=plateform_id, need_excel=need_excel)
    if need_excel == 0:
        response = make_response(send_file(file_path))
        response.headers["Content-Disposition"] = f"p_w_upload; filename={file_name};"
        return response
    return api.handle_httpresponse(file_path, 0)


# Main
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8888, threaded=True)

