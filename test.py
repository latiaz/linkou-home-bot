import pygsheets
import requests
import json
import re
import cn2an
from export import export_linkou

with open("new.json", "r", encoding="utf-8") as f:
    new = json.load(f)
    new = [item for item in new if item['name'] != '森聯摩天41']


def update_linkou():
    # key = pygsheets.authorize(service_file='credentials.json')
    # linkou = key.open_by_url('https://docs.google.com/spreadsheets/d/1FLEjEXlhYzobw6JhJWQuw7OUfkq2GAx1xVrv87x7ugo/')
    # wks_flower = linkou.worksheet_by_title(i['name'] + '-實價登錄')
    # wks_price = linkou.worksheet_by_title(i['name'] + '-銷售登錄')
    message = 'update 11205 19 20'
    parts = message.split(' ')
    keyword = parts[0]
    month = parts[1]
    days = parts[2:]
    day_values = [int(month + day.zfill(2)) for day in days]
    param = {'month': month, 'day': day_values}
    r = requests.get('https://i.land.ntpc.gov.tw/landwa2/api/RPB_Alls/search3?RPTOWN1=%E6%9E%97%E5%8F%A3%E5%8D%80'
                     '&xmax=4000000&xmin=20000&ymax=40000000&ymin=200000&RPBUILD5=all&RPTYPE2=%E5%BB%BA%2B%E5%9C'
                     '%B0%2F%E5%9C%B0%2B%E5%BB%BA%2B%E8%BB%8A%2F&YMS=' + month + '&YME=11601&CA1=0&CA2=100000&FA1=0&FA2'
                     '=100000&MPS=0&MPE=10000000&TPS=0&TPE=900000000&FAGEmin=0&FAGEmax=100&RPLEVEL=%E5%B1%A4'
                     '&RPSECT=&RPROAD=&RPUSE=&RPZONE=&SPCASE=特殊-&BUILD1=999&BUILD2=999'
                     '&BUILD3=999&P1MA_TYPEB_1=&P1MA_TYPEB_2=')
    data = r.json()
    print(param)
    return '成功'


if __name__ == "__main__":
    update_linkou()
