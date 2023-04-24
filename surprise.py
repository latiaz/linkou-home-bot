import cn2an
import re
import requests
import json


def upup_price(data):
    real = [
        data['P1MA_TYPEB_1'],  # 建案
        data['P1MA_TYPEB_5'][0] + str(int(re.sub('\\D', '', data['P1MA_TYPEB_5']))),  # 棟
        re.sub('\\D', '', data['P1MA_TYPEB_6']),  # 號
        float(data['P1MA_TOTPRICE']) / 10000,  # 總價
        float(data['P1MA_PARKPRICE']) / 10000,  # 車位
        (float(data['P1MA_BUILD6']) - float(data['P1PA_PARKAREA'])) * 0.3025,  # 坪數
        float(data['MeanPrice']) / 10000,  # 單價
        data['P1MA_BUILD5'],  # 類型
        data['P1MA_SPECIAL'],  # 備註
        data['P1MA_DATE'],  # 日期
    ]
    return real


def village_price(data):
    split = data['P1MA_TYPEB_6'].split("-")
    real = [
        data['P1MA_TYPEB_1'],  # 建案
        split[0],  # 棟
        re.sub('\\D', '', split[1]),  # 號
        float(data['P1MA_TOTPRICE']) / 10000,  # 總價
        float(data['P1MA_PARKPRICE']) / 10000,  # 車位
        (float(data['P1MA_BUILD6']) - float(data['P1PA_PARKAREA'])) * 0.3025,  # 坪數
        float(data['MeanPrice']) / 10000,  # 單價
        data['P1MA_BUILD5'],  # 類型
        data['P1MA_SPECIAL'],  # 備註
        data['P1MA_DATE'],  # 日期
    ]
    return real


def x1_x7_price(data):
    real = [
        data['P1MA_TYPEB_1'],  # 建案
        data['P1MA_TYPEB_5'] + data['P1MA_TYPEB_6'],  # 棟
        cn2an.cn2an(data['P1MA_BUILD10_1'][:-1], 'smart'),  # 號
        float(data['P1MA_TOTPRICE']) / 10000,  # 總價
        float(data['P1MA_PARKPRICE']) / 10000,  # 車位
        (float(data['P1MA_BUILD6']) - float(data['P1PA_PARKAREA'])) * 0.3025,  # 坪數
        float(data['MeanPrice']) / 10000,  # 單價
        data['P1MA_BUILD5'],  # 類型
        data['P1MA_SPECIAL'],  # 備註
        data['P1MA_DATE'],  # 日期
    ]
    return real


def meet_price(data):
    split = data['P1MA_TYPEB_6'].split("-")
    real = [
        data['P1MA_TYPEB_1'],  # 建案
        data['P1MA_TYPEB_5'] + split[0],  # 棟
        re.sub('\\D', '', split[1]),  # 號
        float(data['P1MA_TOTPRICE']) / 10000,  # 總價
        float(data['P1MA_PARKPRICE']) / 10000,  # 車位
        (float(data['P1MA_BUILD6']) - float(data['P1PA_PARKAREA'])) * 0.3025,  # 坪數
        float(data['MeanPrice']) / 10000,  # 單價
        data['P1MA_BUILD5'],  # 類型
        data['P1MA_SPECIAL'],  # 備註
        data['P1MA_DATE'],  # 日期
    ]
    return real


def mei_price():
    r = requests.get('https://i.land.ntpc.gov.tw/landwa2/api/RPB_Alls/search3?RPTOWN1=%E6%9E%97%E5%8F%A3%E5%8D%80'
                     '&xmax=4000000&xmin=20000&ymax=40000000&ymin=200000&RPBUILD5=all&RPTYPE2=%E5%BB%BA%2B%E5%9C'
                     '%B0%2F%E5%9C%B0%2B%E5%BB%BA%2B%E8%BB%8A%2F&YMS=11101&YME=11601&CA1=0&CA2=100000&FA1=0&FA2'
                     '=100000&MPS=0&MPE=10000000&TPS=0&TPE=900000000&FAGEmin=0&FAGEmax=100&RPLEVEL=%E5%B1%A4'
                     '&RPSECT=&RPROAD=&RPUSE=&RPZONE=&SPCASE=特殊-&BUILD1=999&BUILD2=999'
                     '&BUILD3=999&P1MA_TYPEB_1=仟葉美&P1MA_TYPEB_2=')

    data = r.json()
    for i in data:
        real = village_price(i)
        return real
