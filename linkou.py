import pygsheets
import requests
import json
import re
from export import export_linkou
from surprise import upup_price, village_price, x1_x7_price, meet_price, mei_price, insight_price, cian_price

with open("new.json", "r", encoding="utf-8") as f:
    new = json.load(f)
    new = [item for item in new if item['name'] == '築禾琢玥']


def update_linkou():
    key = pygsheets.authorize(service_file='credentials.json')
    linkou = key.open_by_url('https://docs.google.com/spreadsheets/d/1FLEjEXlhYzobw6JhJWQuw7OUfkq2GAx1xVrv87x7ugo/')

    for i in new:
        print(i['name'])
        wks_linkou = linkou.worksheet_by_title(i['name'] + '-實價登錄')

        headers = {
            'Host': 'i.land.ntpc.gov.tw',
            'Referer': 'https://i.land.ntpc.gov.tw/webgis/index.html?fun=realprice'
        }

        r = requests.get('https://i.land.ntpc.gov.tw/landwa2/api/RPB_Alls/search3?RPTOWN1=%E6%9E%97%E5%8F%A3%E5%8D%80'
                         '&xmax=4000000&xmin=20000&ymax=40000000&ymin=200000&RPBUILD5=all&RPTYPE2=%E5%BB%BA%2B%E5%9C'
                         '%B0%2F%E5%9C%B0%2B%E5%BB%BA%2B%E8%BB%8A%2F&YMS=10001&YME=11601&CA1=0&CA2=100000&FA1=0&FA2'
                         '=100000&MPS=0&MPE=10000000&TPS=0&TPE=900000000&FAGEmin=0&FAGEmax=100&RPLEVEL=%E5%B1%A4'
                         '&RPSECT=&RPROAD=&RPUSE=&RPZONE=&SPCASE=特殊-&BUILD1=999&BUILD2=999'
                         '&BUILD3=999&P1MA_TYPEB_1=' + i['name'] + '&P1MA_TYPEB_2=', headers=headers, verify=False)

        data = r.json()
        real_price = []
        price = []

        for status in data:
            if status['P1MA_STATUS'] != '4':
                if status['P1MA_BUILD5'] == '住宅大樓' or status['P1MA_BUILD5'] == '辦公商業大樓' or status['P1MA_BUILD5'] == '華廈':
                    real_price.append(status)

        for data in real_price:
            if data['P1MA_TYPEB_1'] == '亞昕森匯·天匯(森匯)' or data['P1MA_TYPEB_1'] == '亞昕森匯·天匯(天匯)' or data['P1MA_TYPEB_1'] == '森鉅M-林境' or data['P1MA_TYPEB_1'] == '森鉅M-逸境':
                real = upup_price(data)
                price.append(real)
            elif data['P1MA_TYPEB_1'] == '長耀里' or data['P1MA_TYPEB_1'] == '小·學堂':
                real = village_price(data)
                price.append(real)
            elif data['P1MA_TYPEB_1'] == '群祥謙':
                real = cian_price(data)
                price.append(real)
            elif data['P1MA_TYPEB_1'] == '聿德觀璟' or data['P1MA_TYPEB_1'] == '聿翔沐風' or data['P1MA_TYPEB_1'] == '和洲艾美':
                real = x1_x7_price(data)
                price.append(real)
            elif data['P1MA_TYPEB_1'] == '敘日':
                real = x1_x7_price(data)
                price.append(real)
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
                    data['P1MA_DATE'],  # 日期
                ]
                price.append(real)
        filtered_data = [item for item in price if (item[0] == '聚美家') or not (
                    item[1].startswith('S') or item[2] == '1' or item[2] == '01' or item[2] == 1)]
        filtered_repeat = []
        for item in filtered_data:
            if not any(x[1] == item[1] and x[2] == item[2] and int(x[9]) > int(item[9]) for x in filtered_data):
                filtered_repeat.append(item)
        filtered_repeat.sort(key=lambda arr: (arr[1], int(arr[2])))
        wks_linkou.update_values('A2', filtered_repeat)
        export_linkou(i)
    return '成功'


if __name__ == "__main__":
    update_linkou()
