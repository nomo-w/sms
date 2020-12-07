from util.api import my_requests
from config import TELEHOO


class Telehoo:
    @staticmethod
    def send(_id, to_number, text, is_qunfa):
        data = {
            'command': TELEHOO.qunfa_command if is_qunfa else TELEHOO.danfa_command,
            'cpid': TELEHOO.cpid,
            'cppwd': TELEHOO.cppwd,
            'da': to_number,
            'sm': text
        }
        resp = my_requests(TELEHOO.send_url, 'get', data, need_json_resp=False)
        data = {'mtstat': 'REJECTD', 'mtmsgid': None}
        for i in resp.split('&'):
            _ = i.split('=')
            if _[0] == 'mtstat' and TELEHOO.success_mtstat == _[1]:
                data['mtstat'] = TELEHOO.success_mtstat
            if _[0] == 'mtmsgid':
                data['mtmsgid'] = '05a8e61528b105'
        return data

    @staticmethod
    def get_result(msgid):
        resp = my_requests(TELEHOO.status_url, 'get',
                           {'cpid': TELEHOO.cpid, 'cppwd': TELEHOO.cppwd, 'msgid': msgid}, need_json_resp=False)
        return resp
