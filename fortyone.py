import pygsheets
import requests
import json
import re
import cn2an
from export import export_linkou

with open("new.json", "r", encoding="utf-8") as f:
    new = json.load(f)


def update_linkou():
    key = pygsheets.authorize(service_file='credentials.json')
    linkou = key.open_by_url('https://docs.google.com/spreadsheets/d/1FLEjEXlhYzobw6JhJWQuw7OUfkq2GAx1xVrv87x7ugo/')

    for i in new:
        if i['name'] == '森聯摩天41':
            print(i['name'])
            wks_41 = linkou.worksheet_by_title(i['name'] + '-實價登錄')

            r = requests.get('https://i.land.ntpc.gov.tw/landwa2/api/RPA_Alls/search3?RPTOWN1=%E6%9E%97%E5%8F%A3%E5'
                             '%8D%80&xmax=286381&xmin=286381&ymax=2773297&ymin=2773297&RPBUILD5=all&RPTYPE2=%E5%BB%BA'
                             '%2B%E5%9C%B0%2F%E5%9C%B0%2B%E5%BB%BA%2B%E8%BB%8A%2F&YMS=10404&YME=11204&CA1=0&CA2'
                             '=100000&FA1=0&FA2=100000&MPS=0&MPE=10000000&TPS=0&TPE=900000000&FAGEmin=0&FAGEmax=100'
                             '&RPLEVEL=%E5%B1%A4&RPSECT=%E5%BB%BA%E6%9E%97%E6%AE%B5&RPROAD=&RPUSE=&RPZONE=&SPCASE=%E7'
                             '%89%B9%E6%AE%8A-&BUILD1=999&BUILD2=999&BUILD3=999')

            data = r.json()
            real_price = []
            price = []
            addr = i['addr']

            for status in data:
                if status['P1MA_STATUS'] != '4':
                    if status['P1MA_BUILD5'] == '住宅大樓' or status['P1MA_BUILD5'] == '辦公商業大樓':
                        real_price.append(status)

            for data in real_price:
                split = data['THEADDR'].split("號")
                if split[1] == '':
                    hao = '1'
                else:
                    hao = cn2an.cn2an(split[1][:-1], 'smart')
                real = [
                    i['name'],  # 建案
                    addr[split[0][-2:]],  # 棟
                    hao,  # 號
                    float(data['P1MA_TOTPRICE']) / 10000,  # 總價
                    float(data['P1MA_PARKPRICE']) / 10000,  # 車位
                    (float(data['P1LA_FArea']) - float(data['P1PA_PARKAREA'])) * 0.3025,  # 坪數
                    float(data['MeanPrice']) / 10000,  # 單價
                    data['P1MA_BUILD5'],  # 類型
                    data['P1MA_SPECIAL'],  # 備註
                    data['P1MA_DATE'],  # 日期
                ]
                price.append(real)
            price.sort(key=lambda arr: (arr[1], int(arr[2])))
            wks_41.update_values('A2', price)
            export_linkou(i)
    return '成功'


if __name__ == "__main__":
    update_linkou()
