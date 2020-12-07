# coding: utf-8

from threading import Timer
from functools import partial


class MyTimer(object):

    def __init__(self, interval, function, args=[], kwargs={}):
        """
        定时器初始化
        """
        self.interval = interval
        self.function = partial(function, *args, **kwargs)
        self.running = False
        self._timer = None

    def __call__(self):
        """
        定时任务
        """
        self.running = False  # 标记定时器未运行
        self.start()          # 再次开启定时器
        self.function()       # 运行任务

    def start(self):
        """
        启动定时器
        """
        if self.running:
            # 判断运行状态，保证定时器只运行一次
            return

        # 创建定时器并启动，更新运行状态
        self._timer = Timer(self.interval, self)
        self._timer.start()
        self.running = True

    def stop(self):
        """
        销毁定时器
        """
        if self._timer:
            self._timer.cancel()
        self.running = False
        self._timer = None
