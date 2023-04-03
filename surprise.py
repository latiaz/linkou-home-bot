import cn2an


def x7_price(data):
    real = [
        data['P1MA_TYPEB_1'],  # 建案
        data['P1MA_TYPEB_5'] + data['P1MA_TYPEB_6'],  # 棟
        cn2an.cn2an(data['P1MA_BUILD10_1'][:-1], 'smart'),  # 號
        float(data['P1MA_TOTPRICE']) / 10000,  # 總價
        float(data['MeanPrice']) / 10000,  # 單價
        float(data['P1MA_PARKPRICE']) / 10000,  # 車位
        data['P1MA_DATE'],  # 日期
        data['P1MA_BUILD5']  # 類型
    ]
    return real
