from config import LDY, DCY, WB, JK, TELEHOO, SMS123
from sms.lingdaoyi_api import LingDaoYi
from sms.dichiyun_api import DiChiYun
from sms.telehoo_api import Telehoo
from sms.sms123_api import Sms123
from sms.weibo_api import WeiBo
from sms.jieke import JieKe
from sms import Sms


class Dispatcher:
    @staticmethod
    def send(_type, _id, to_number, text, is_qunfa=False):
        if _type == 'socket_axflix_china':
            ret = Sms().send(_id, to_number+':socket_axflix_china', text)
            ret, status = '', True
        elif _type == 'socket_axflix_vietnam':
            ret = Sms().send(_id, to_number+':socket_axflix_vietnam', text)
            ret, status = '', True
        elif _type == 'http_ldy':
            ret = LingDaoYi.send(_id, ','.join(to_number) if is_qunfa else to_number, text)
            status = True if str(ret) == LDY.return_success_code else False
            ret = ''
        elif _type == 'http_dcy':
            ret = DiChiYun.send(_id, ','.join(to_number) if is_qunfa else to_number, text)
            status = True if str(ret.get('code', '')) == DCY.return_success_code else False
            ret = ret['data']['taskcode'] if str(ret.get('code', '')) == DCY.return_success_code else ret.get('message', 'failed')
        elif _type == 'http_wb':
            ret = WeiBo.send(_id, ','.join(to_number) if is_qunfa else to_number, text)
            status = True if ret.get('result', '') == WB.return_success_code else False
            ret = ret['msgid'] if ret.get('result', '') == WB.return_success_code else ret.get('desc', 'failed')
        elif _type == 'http_jk':
            ret = JieKe.send(_id, ','.join(to_number) if is_qunfa else to_number, text, is_qunfa)
            status = True if ret and str(ret['Message']['Head']['Status']) == JK.return_success_code else False
            ret = ret['Message']['Body']['MsgID'] if ret and str(ret['Message']['Head']['Status']) == JK.return_success_code else ret
        elif _type == 'http_telehoo':
            ret = Telehoo.send(_id, ','.join(to_number) if is_qunfa else to_number, text, is_qunfa)
            status = True if ret and ret['mtstat'] == TELEHOO.success_mtstat else False
            ret = ret['mtmsgid'] if ret and ret['mtstat'] == TELEHOO.success_mtstat else ret['mtmsgid']
        elif _type == 'http_sms123':
            ret = Sms123.send(_id, ';'.join(to_number) if is_qunfa else to_number, text)
            status = True if ret and ret['status'] == SMS123.send_return_success_status else False
            ret = ''
        else:
            ret, status = '', False
        return ret, status

    @staticmethod
    def balance(_type):
        if 'socket_axflix' in _type:
            Sms().get_balance(channel_type=_type)
        elif _type == 'http_ldy':
            LingDaoYi.get_balance()
        elif _type == 'http_dcy':
            DiChiYun.get_balance()
        elif _type == 'http_wb':
            WeiBo.get_balance()
        elif _type == 'http_jk':
            JieKe.get_balance()
        elif _type == 'http_sms123':
            Sms123.get_balance()
