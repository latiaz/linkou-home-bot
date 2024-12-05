import pygsheets
import json
from export import export_price

with open("new.json", "r", encoding="utf-8") as f:
    new = json.load(f)
    new = [item for item in new if item['name'] == '聯虹珺玥']


def update_price():
    key = pygsheets.authorize(service_file='credentials.json')
    linkou = key.open_by_url('https://docs.google.com/spreadsheets/d/1FLEjEXlhYzobw6JhJWQuw7OUfkq2GAx1xVrv87x7ugo/')

    for i in new:
        print(i['name'])
        wks_linkou = linkou.worksheet_by_title(i['name'] + '-實價登錄')
        wks_price = linkou.worksheet_by_title(i['name'] + '-銷售登錄')

        table = i['table']

        linkou_list = wks_linkou.get_all_records()
        for data in linkou_list:
            building = data['棟']
            floor = data['號']
            total_price = data['總價']
            mean_price = data['單價']
            park_price = data['車位']
            p = data['坪數']
            x = table[building]
            y = 2 * (i['height'] - int(floor)) + 2
            wks_price.update_values(x + str(y), [[str(total_price) + ' (' + str(park_price) + ')'], [str(mean_price) + ' (' + str(p) + ')']])
        export_price(i)
    return '成功'


if __name__ == "__main__":
    update_price()
