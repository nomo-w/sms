# coding: utf-8
#
# setup : pip install plivo
#

from sms.base import SmsBase
from db.channel import ChannelDB
from util.common import is_10086, is_10000
from sms.clickatell import Clickatell
from sms.plivos import Plivo
from sms.hk import Hk
from sms.axflix import Axflix


class Choice(SmsBase):
    def __init__(self):
        pass

    def get_balance(self, channel_type):
        # 并没有正常调用余额，以后需要的时候补上即可
        # return {'value': '自动预充值', 'autoReload': False}
        # return {'value': 10, 'autoReload': False}
        return Axflix().get_balance(channel_type)

    def send(self, _id, to_number, text):
        """
        智能选择哪个运营商的号码走哪个通道
        """
        # if is_10000(to_number):
        #    return dict(message_id='0', to_number=to_number, price='0', err='99', err_text='【电信】到达率太低,暂时跳过')

        # return Hk().send(seq, to_number, text)
        return Axflix().send(_id, to_number, text)
