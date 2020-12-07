from util.api import my_requests
from config import LDY
from db.channel import ChannelDB


class LingDaoYi:
    @staticmethod
    def send(_id, to_number, text):
        data = {
            'tjpc': _id,
            'usr': LDY.user,
            'pwd': LDY.password,
            'mobile': to_number,
            'msg': text
        }
        resp = my_requests(LDY.send_url, 'post', data)
        return resp

    @staticmethod
    def get_balance():
        params = {'usr': LDY.user, 'pwd': LDY.password}
        resp = my_requests(LDY.balance_url, 'get', params)
        if resp is not None:
            if str(resp) != LDY.balance_resp_err_code:
                with ChannelDB() as db:
                    db.update_balance(resp, channel_type='http_ldy')
        return resp

    @staticmethod
    def get_result():
        resp = my_requests(LDY.status_url, 'post', {'usr': LDY.user, 'pwd': LDY.password})
        return resp if isinstance(resp, list) else []
