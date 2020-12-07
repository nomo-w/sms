from util.api import my_requests
from db.channel import ChannelDB
from config import SMS123


class Sms123:
    @staticmethod
    def send(_id, to_number, text):
        # {'status': 'error', 'msgCode': 'BE00036', 'statusMsg': 'The message is not allowed to send without whitelisting. Kindly submit your content for approval. '}
        # {'status': 'ok', 'msgCode': 'E00001', 'statusMsg': 'Completed successfully.', 'referenceID': ['q5f0d78a85c160'], 'balance': 3960.00004, 'data': [{'recipients': '8613031046676', 'referenceID': 'q5f0d78a85c160', 'msgCode': 'E00001'}]}
        # {'status': 'ok', 'msgCode': 'E00001', 'statusMsg': 'Completed successfully.', 'referenceID': ['q5f0d7a146d0b4', 'q5f0d7a146d109'], 'balance': 3946.66672, 'data': [{'recipients': '8613031046676', 'referenceID': 'q5f0d7a146d0b4', 'msgCode': 'E00001'}, {'recipients': '8613717994977', 'referenceID': 'q5f0d7a146d109', 'msgCode': 'E00001'}]}
        data = {
            'apiKey': SMS123.apikey,
            'recipients': to_number,
            'messageContent': text,
            'referenceID': _id
        }
        resp = my_requests(SMS123.send_url, 'get', params=data)
        # print(resp)
        return resp

    @staticmethod
    def get_balance():
        data = {
            'apiKey': SMS123.apikey,
            'email': SMS123.email,
        }
        resp = my_requests(SMS123.balance_url, 'get', params=data)
        if resp is not None and resp['msgCode'] == SMS123.balance_return_success_code:
            with ChannelDB() as db:
                db.update_balance(resp['balance'].replace(',', ''), channel_type='http_sms123')
        # print(resp)
        return resp


