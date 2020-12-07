from util.api import my_requests
from db.channel import ChannelDB
from config import JK
import xmltodict


class JieKe:
    @staticmethod
    def _xmltojson(xmldata):
        if xmldata is not None:
            try:
                return xmltodict.parse(xmldata)
            except Exception as e:
                return {}
        return {}

    @classmethod
    def send(cls, _id, to_number, text, is_qunfa):
        param = {
            'UserName': JK.username,
            'PassWord': JK.password,
            'Caller': JK.caller,
            'Callee': to_number,
            'CharSet': JK.charset,
            'DCS': JK.dsc,
            'Text': text
        }
        resp = my_requests(JK.qunfa_send_url if is_qunfa else JK.danfa_send_url, 'get', param, need_json_resp=False)
        return cls._xmltojson(resp)

    @classmethod
    def get_result(cls):
        resp = cls._xmltojson(my_requests(JK.status_url, 'get', {'UserName': JK.username, 'PassWord': JK.password}, need_json_resp=False))
        if resp and str(resp['Message']['Head']['Status']) == '0':
            report = resp['Message']['Body']['Report'] if resp['Message']['Body'] else []
            if report:
                return [report] if isinstance(report, dict) else report
        return []

    @classmethod
    def get_balance(cls):
        # {"Message": {"Head": {"MessageID": "QueryClientBalanceAck", "Status": "0"}, "Body": {"Balance": "100.0000", "Credit": "2.0000"}}}
        resp = cls._xmltojson(my_requests(JK.balance_url, 'get', {'UserName': JK.username, 'PassWord': JK.password}, need_json_resp=False))
        if resp and str(resp['Message']['Head']['Status']) == '0':
            with ChannelDB() as db:
                db.update_balance(resp['Message']['Body']['Balance'], channel_type='http_jk')

