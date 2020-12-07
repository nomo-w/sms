# coding: utf-8

import hashlib


def is_10086(phone):
    """是否移动的电话号码"""
    segs_10086 = ['134', '135', '136', '137', '138', '139', '147', '148', '150', '151', '152', '157', '158', '159',
                  '178', '182', '183', '184', '187', '188']
    for seg in segs_10086:
        if phone.startswith(seg):
            return True
    return False


def is_10000(phone):
    """是否电信的电话号码"""
    segs_10000 = ['133', '153', '180', '181', '189', '177', '1700']
    for seg in segs_10000:
        if phone.startswith(seg):
            return True
    return False


def is_right_china_number(num):
    """判断是否中国手机号码"""
    return len(num) == 11 and num[0] == '1'


def md5(_str):
    """32bit md5 encode"""
    h = hashlib.md5()
    h.update(_str.encode('utf-8'))
    return h.hexdigest()


def sign_(data, charset='utf-8'):
    '''
    私钥签名,使用utf-8编码
    :param message: 需要签名的数据
    :param private_key_file: rsa私钥文件的位置
    :return: 签名后的字符串
    '''
    signature = hashlib.md5(data.encode(charset)).hexdigest()
    return signature


def verify_(signature, data, charset='utf-8'):
    '''
    公钥验签,使用utf-8编码
    :param signature: 经过签名处理的数据
    :param data: 需要验证的数据
    :param publickey_path: rsa公钥文件的位置
    :return: bool值
    '''
    sign = sign_(data, charset)
    return [False, True][sign == signature]


if __name__ == '__main__':
    print(sign_('sdfsdfeee22222'))
    print(md5('sdfsdfeee22222'))