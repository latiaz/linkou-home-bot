import pygsheets
import json
from export import export_total

with open("new.json", "r", encoding="utf-8") as f:
    new = json.load(f)


def update_total():
    key = pygsheets.authorize(service_file='credentials.json')
    linkou = key.open_by_url('https://docs.google.com/spreadsheets/d/1FLEjEXlhYzobw6JhJWQuw7OUfkq2GAx1xVrv87x7ugo/')
    wks_total = linkou.worksheet_by_title('統整')
    y = 3
    for i in new:
        each = [0] * 9
        print(i['name'])
        wks_linkou = linkou.worksheet_by_title(i['name'] + '-實價登錄')
        linkou_list = wks_linkou.get_all_records()
        for case in linkou_list:
            date = str(case['交易日期'])[:5]
            if date == '11101' or date == '11102' or date == '11103':
                each[0] += 1
            elif date == '11104' or date == '11105' or date == '11106':
                each[1] += 1
            elif date == '11107' or date == '11108' or date == '11109':
                each[2] += 1
            elif date == '11110':
                each[3] += 1
            elif date == '11111':
                each[4] += 1
            elif date == '11112':
                each[5] += 1
            elif date == '11201':
                each[6] += 1
            elif date == '11202':
                each[7] += 1
            elif date == '11203':
                each[8] += 1
        name = [i['name']]
        num = len(linkou_list)
        total = [num, i['total'], i['total'] - num, num / i['total']]
        result = name + each + total
        wks_total.update_values('A' + str(y), [[data if data != 0 else '' for data in result]])
        y += 1
    export_total()
    return '成功'


if __name__ == "__main__":
    update_total()
