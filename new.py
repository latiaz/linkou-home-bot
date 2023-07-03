import pygsheets
import requests
import json
import re
from surprise import upup_price, village_price, x1_x7_price, meet_price

with open("new.json", "r", encoding="utf-8") as f:
    new = json.load(f)
    new = [item for item in new if item['name'] != '森聯摩天41']

price = []
count = 0
previous = ''
today = {"new": {}, "update": {}}

message = 'update 11206 01 02 03'
parts = message.split(' ')
keyword = parts[0]
month = parts[1]
days = parts[2:]
day_values = [int(month + day.zfill(2)) for day in days]
param = {'month': month, 'day': day_values}


def update(param):
    key = pygsheets.authorize(service_file='credentials.json')
    linkou = key.open_by_url('https://docs.google.com/spreadsheets/d/1FLEjEXlhYzobw6JhJWQuw7OUfkq2GAx1xVrv87x7ugo/')

    global price, count, previous, today
    r = requests.get('https://i.land.ntpc.gov.tw/landwa2/api/RPB_Alls/search3?RPTOWN1=%E6%9E%97%E5%8F%A3%E5%8D%80'
                     '&xmax=4000000&xmin=20000&ymax=40000000&ymin=200000&RPBUILD5=all&RPTYPE2=%E5%BB%BA%2B%E5%9C'
                     '%B0%2F%E5%9C%B0%2B%E5%BB%BA%2B%E8%BB%8A%2F&YMS=' + param['month'] + '&YME=11601&CA1=0&CA2=100000&FA1=0&FA2'
                     '=100000&MPS=0&MPE=10000000&TPS=0&TPE=900000000&FAGEmin=0&FAGEmax=100&RPLEVEL=%E5%B1%A4'
                     '&RPSECT=&RPROAD=&RPUSE=&RPZONE=&SPCASE=特殊-&BUILD1=999&BUILD2=999'
                     '&BUILD3=999&P1MA_TYPEB_1=&P1MA_TYPEB_2=')
    data = r.json()
    filtered_day = [item for item in data if item['P1MA_DATE'] in [str(day) for day in param['day']]]
    filtered_case = [item for item in filtered_day if any(case['name'] in item['P1MA_TYPEB_1'] for case in new)]
    real_price = []

    for status in filtered_case:
        if status['P1MA_STATUS'] != '4':
            if status['P1MA_BUILD5'] == '住宅大樓' or status['P1MA_BUILD5'] == '辦公商業大樓' or status['P1MA_BUILD5'] == '華廈':
                real_price.append(status)
    if len(real_price) == 0:
        return 'none'
    real_price.sort(key=lambda x: x['P1MA_TYPEB_1'])

    for index, data in enumerate(real_price):
        if count == 0:
            if data['P1MA_TYPEB_1'] == '森聯上上謙-森越社區':
                previous = '森聯上上謙-森越'
                count += 1
            else:
                previous = data['P1MA_TYPEB_1']
                count += 1
        elif count != 0 and data['P1MA_TYPEB_1'] == previous:
            count += 1
        elif count != 0 and data['P1MA_TYPEB_1'] != previous:
            update_new(linkou)
            if data['P1MA_TYPEB_1'] == '森聯上上謙-森越社區':
                previous = '森聯上上謙-森越'
                count = 1
            else:
                previous = data['P1MA_TYPEB_1']
                count = 1
        if data['P1MA_TYPEB_1'] == '森聯上上謙-森越' or data['P1MA_TYPEB_1'] == '森聯上上謙-森越社區' or data['P1MA_TYPEB_1'] == '森聯上上謙-森治社區':
            real = upup_price(data)
            price.append(real)
        elif data['P1MA_TYPEB_1'] == '長耀里':
            real = village_price(data)
            price.append(real)
        elif data['P1MA_TYPEB_1'] == '侘壹' or data['P1MA_TYPEB_1'] == '侘極' or data['P1MA_TYPEB_1'] == '侘極\\' or data['P1MA_TYPEB_1'] == '九揚華都' or data['P1MA_TYPEB_1'] == '聿德觀璟':
            real = x1_x7_price(data)
            price.append(real)
        elif data['P1MA_TYPEB_1'] == '遇見' or data['P1MA_TYPEB_1'] == '頤昌松琚' or data['P1MA_TYPEB_1'] == '頤昌柏舍' or data['P1MA_TYPEB_1'] == '潤鴻日麗':
            real = meet_price(data)
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
        if index == len(real_price) - 1:
            update_new(linkou)
    # formatted = json.dumps(today, indent=4, ensure_ascii=False)
    # print(str(formatted))
    result = today
    today = {"new": {}, "update": {}}
    return result


def update_new(google):
    global price, count, previous
    # print(previous, count)
    wks_price = google.worksheet_by_title(previous + '-實價登錄')
    price_list = wks_price.get_all_records()
    converted_data = [[
        str(d['建案名稱']),
        str(d['棟']),
        int(d['號']),
        str(d['總價']),
        float(d['車位']),
        float(d['坪數']),
        float(d['單價']),
        str(d['類型']),
        str(d['備註']),
        str(d['交易日期'])
    ] for d in price_list]
    price.sort(key=lambda arr: (arr[1], int(arr[2])))
    for n in price:
        found = False
        for i, o in enumerate(converted_data):
            if str(n[1]) == str(o[1]) and int(n[2]) == int(o[2]):
                converted_data[i] = n
                found = True
                today_new(n, 'update')
                break
        if not found:
            converted_data.append(n)
            today_new(n, 'new')
    new_data = [item for item in converted_data if (item[0] == '聚美家') or not (item[1].startswith('S') or item[2] == '1' or item[2] == '01' or item[2] == 1)]
    new_data.sort(key=lambda arr: (arr[1], int(arr[2])))
    wks_price.update_values('A2', new_data)
    price_new(google)
    price = []


def price_new(google):
    global price, previous
    price = [item for item in price if (item[0] == '聚美家') or not (item[1].startswith('S') or item[2] == '1' or item[2] == '01' or item[2] == 1)]
    wks_price = google.worksheet_by_title(previous + '-銷售登錄')
    target = next((item for item in new if item['name'] == previous), None)
    height = target['height']
    table = target['table']
    for data in price:
        building = data[1]
        floor = data[2]
        total_price = '{:,.0f}'.format(data[3])
        mean_price = round(data[6], 1)
        park_price = int(data[4])
        p = round(data[5], 2)
        x = table[building]
        y = 2 * (height - int(floor)) + 2
        wks_price.update_values(x + str(y), [[str(total_price) + ' (' + str(park_price) + ')'], [str(mean_price) + ' (' + str(p) + ')']])


def today_new(case, status):
    global today
    name = case[0]
    code = case[1] + '-' + str(int(case[2]))

    if name not in today[status]:
        today[status][name] = {'count': 1, 'case': [code]}
    else:
        today[status][name]['count'] += 1
        today[status][name]['case'].append(code)


if __name__ == "__main__":
    update(param)
