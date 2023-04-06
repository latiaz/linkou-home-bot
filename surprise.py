import cn2an
import re


def upup_price(data):
    real = [
        data['P1MA_TYPEB_1'],  # 建案
        data['P1MA_TYPEB_5'][0] + str(int(re.sub('\\D', '', data['P1MA_TYPEB_5']))),  # 棟
        re.sub('\\D', '', data['P1MA_TYPEB_6']),  # 號
        float(data['P1MA_TOTPRICE']) / 10000,  # 總價
        float(data['MeanPrice']) / 10000,  # 單價
        float(data['P1MA_PARKPRICE']) / 10000,  # 車位
        data['P1MA_DATE'],  # 日期
        data['P1MA_BUILD5'] + '(' + data['P1MA_SPECIAL'] + ')'  # 類型 / 特殊交易
    ]
    return real


def village_price(data):
    split = data['P1MA_TYPEB_6'].split("-")
    real = [
        data['P1MA_TYPEB_1'],  # 建案
        split[0],  # 棟
        re.sub('\\D', '', split[1]),  # 號
        float(data['P1MA_TOTPRICE']) / 10000,  # 總價
        float(data['MeanPrice']) / 10000,  # 單價
        float(data['P1MA_PARKPRICE']) / 10000,  # 車位
        data['P1MA_DATE'],  # 日期
        data['P1MA_BUILD5'] + '(' + data['P1MA_SPECIAL'] + ')'  # 類型 / 特殊交易
    ]
    return real


def x1_x7_price(data):
    real = [
        data['P1MA_TYPEB_1'],  # 建案
        data['P1MA_TYPEB_5'] + data['P1MA_TYPEB_6'],  # 棟
        cn2an.cn2an(data['P1MA_BUILD10_1'][:-1], 'smart'),  # 號
        float(data['P1MA_TOTPRICE']) / 10000,  # 總價
        float(data['MeanPrice']) / 10000,  # 單價
        float(data['P1MA_PARKPRICE']) / 10000,  # 車位
        data['P1MA_DATE'],  # 日期
        data['P1MA_BUILD5'] + '(' + data['P1MA_SPECIAL'] + ')'  # 類型 / 特殊交易
    ]
    return real


def meet_price(data):
    split = data['P1MA_TYPEB_6'].split("-")
    real = [
        data['P1MA_TYPEB_1'],  # 建案
        data['P1MA_TYPEB_5'] + split[0],  # 棟
        re.sub('\\D', '', split[1]),  # 號
        float(data['P1MA_TOTPRICE']) / 10000,  # 總價
        float(data['MeanPrice']) / 10000,  # 單價
        float(data['P1MA_PARKPRICE']) / 10000,  # 車位
        data['P1MA_DATE'],  # 日期
        data['P1MA_BUILD5'] + '(' + data['P1MA_SPECIAL'] + ')'  # 類型 / 特殊交易
    ]
    return real
