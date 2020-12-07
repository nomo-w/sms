from util.api import my_requests
from config import DCY
from db.channel import ChannelDB


class DiChiYun:
    @staticmethod
    def send(_id, to_number, text):
        data = {
            'appid': DCY.appid,
            'secret': DCY.secret,
            'mobile': to_number,
            'content': text,
            "genre": DCY.yingxiao_code
        }
        resp = my_requests(DCY.send_url, 'post', data, need_json_params=True)
        return resp if resp is not None else {}

    @staticmethod
    def get_balance():
        data = {'appid': DCY.appid, 'secret': DCY.secret, 'genre': DCY.balance_code}
        resp = my_requests(DCY.balance_url, 'post', data, need_json_params=True)
        if resp is not None:
            with ChannelDB() as db:
                db.update_balance(resp['data']['sur_num'], channel_type='http_dcy')
        return resp

    # @staticmethod
    # def get_result():
    #     resp = my_requests(LDY.status_url, {'usr': LDY.user, 'pwd': LDY.password})
    #     return resp
