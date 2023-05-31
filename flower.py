import pygsheets
import requests
import json
import re
import cn2an
from export import export_linkou

# with open("new.json", "r", encoding="utf-8") as f:
#     new = json.load(f)


def update_linkou():
    key = pygsheets.authorize(service_file='credentials.json')
    linkou = key.open_by_url('https://docs.google.com/spreadsheets/d/1FLEjEXlhYzobw6JhJWQuw7OUfkq2GAx1xVrv87x7ugo/')
    i = {
        "name": "福樺中央大樓",
        "height": 30,
        "total": 65,
        "table": {"A": "B", "B": "C", "C": "D"},
        "tag": "flower",
        "linkou": "[null,null,null,null,null,null,null,null,null,0,[[\"1936289523\"]],10000000,null,null,null,null,null,null,null,null,null,null,null,null,null,null,45043.596773275465,null,null,[1,null,0,0,0,0,0,0,1,1,2,1,null,null,2,1],[\"A4\",1,2,1,[0.19685039370078738,0.19685039370078738,0.7,0.7]],null,0,[]]",
        "price": "[null,null,null,null,null,null,null,null,null,0,[[\"208471879\"]],10000000,null,null,null,null,null,null,null,null,null,null,null,null,null,null,45043.60954690972,null,null,[1,null,0,0,0,0,0,0,1,1,2,1,null,null,2,1],[\"A4\",1,4,1,[0.75,0.75,0.7,0.7]],null,0,[]]"
      }

    print(i['name'])
    wks_flower = linkou.worksheet_by_title(i['name'] + '-實價登錄')
    wks_price = linkou.worksheet_by_title(i['name'] + '-銷售登錄')

    r = requests.get('https://i.land.ntpc.gov.tw/landwa2/api/RPB_Alls/search3?RPTOWN1=%E6%9E%97%E5%8F%A3%E5%8D%80'
                     '&xmax=4000000&xmin=20000&ymax=40000000&ymin=200000&RPBUILD5=all&RPTYPE2=%E5%BB%BA%2B%E5%9C'
                     '%B0%2F%E5%9C%B0%2B%E5%BB%BA%2B%E8%BB%8A%2F&YMS=11001&YME=11601&CA1=0&CA2=100000&FA1=0&FA2'
                     '=100000&MPS=0&MPE=10000000&TPS=0&TPE=900000000&FAGEmin=0&FAGEmax=100&RPLEVEL=%E5%B1%A4'
                     '&RPSECT=&RPROAD=&RPUSE=&RPZONE=&SPCASE=特殊-&BUILD1=999&BUILD2=999'
                     '&BUILD3=999&P1MA_TYPEB_1=' + i['name'] + '&P1MA_TYPEB_2=')

    data = r.json()
    real_price = []
    price = []

    for status in data:
        if status['P1MA_STATUS'] != '4':
            if status['P1MA_BUILD5'] == '住宅大樓' or status['P1MA_BUILD5'] == '辦公商業大樓':
                real_price.append(status)

    for data in real_price:
        if data['P1MA_TYPEB_5'] == 'Ａ':
            real = [
                data['P1MA_TYPEB_1'],  # 建案
                'A',  # 棟
                re.sub('\\D', '', data['P1MA_TYPEB_6']),  # 號
                float(data['P1MA_TOTPRICE']) / 10000,  # 總價
                float(data['P1MA_PARKPRICE']) / 10000,  # 車位
                (float(data['P1MA_BUILD6']) - float(data['P1PA_PARKAREA'])) * 0.3025,  # 坪數
                float(data['MeanPrice']) / 10000,  # 單價
                data['P1MA_BUILD5'],  # 類型
                data['P1MA_SPECIAL'],  # 備註
                data['P1LA_SEQNOTE'],
                data['P1MA_DATE'],  # 日期
            ]
        else:
            real = [
                data['P1MA_TYPEB_1'],  # 建案
                data['P1MA_TYPEB_5'],  # 棟
                re.sub('\\D', '', data['P1MA_TYPEB_6']),  # 號
                float(data['P1MA_TOTPRICE']) / 10000,  # 總價
                float(data['P1MA_PARKPRICE']) / 10000,  # 車位
                (float(data['P1MA_BUILD6']) - float(data['P1PA_PARKAREA'])) * 0.3025,  # 坪數
                float(data['MeanPrice']) / 10000,  # 單價
                data['P1MA_BUILD5'],  # 類型
                data['P1MA_SPECIAL'],  # 備註
                data['P1LA_SEQNOTE'],
                data['P1MA_DATE'],  # 日期
            ]
        price.append(real)
    price.sort(key=lambda arr: (arr[1], int(arr[2])))
    wks_flower.update_values('A2', price)

    table = i['table']
    linkou_list = wks_flower.get_all_records()
    for data in linkou_list:
        building = data['棟']
        floor = data['號']
        total_price = data['總價']
        mean_price = data['單價']
        park_price = data['車位']
        p = data['坪數']
        x = table[building]
        y = 2 * (i['height'] - int(floor)) + 2
        wks_price.update_values(x + str(y), [[str(total_price) + ' (' + str(park_price) + ')'],
                                             [str(mean_price) + ' (' + str(p) + ')']])
    return '成功'


if __name__ == "__main__":
    update_linkou()
