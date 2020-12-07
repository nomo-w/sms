# coding: utf-8
"""初始化log，替换print输出到文件中"""

from config import LogDefine
import traceback
import builtins
import time
import os


def my_print(print_, level=None, log_type=None, file=None):
    """
    print函数重载, 输入log到文件
    :param args:
    :return:
    """
    # new_args = (str(arg) for arg in args)
    if file:
        log_path = file
    else:
        log_path = f'{LogDefine.logpath}/{time.strftime("%Y-%m-%d", time.localtime())}.log'
    log = f'[{time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())}] [{LogDefine.log_level[level]}] [{log_type}] : ' \
          f'{print_}'
    log = log.replace('"', ' ')
    log = log.replace("'", " ")
    log = log.replace('\n', ' ')
    log = log.replace('\r\n', ' ')
    log = log.replace('`', ' ')
    os.system(f'echo "{log}" >> {log_path}')


def init():
    # 重载print
    if not os.path.exists(LogDefine.logpath):
        os.system(f'mkdir {LogDefine.logpath}')
    builtins.print = my_print
