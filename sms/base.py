# coding: utf-8
#
# SMS抽象基类
#

from abc import ABCMeta, abstractmethod


class SmsBase(metaclass=ABCMeta):

    @abstractmethod
    def get_balance(self, channel_type: str):
        pass

    @abstractmethod
    def send(self, seq: str, to_number: str, text: str) -> dict:
        pass
