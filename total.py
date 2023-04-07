import pygsheets
import json
from export import export_total

with open("new.json", "r") as f:
    new = json.load(f)


def update_total():
    key = pygsheets.authorize(service_file='credentials.json')
    linkou = key.open_by_url('https://docs.google.com/spreadsheets/d/1FLEjEXlhYzobw6JhJWQuw7OUfkq2GAx1xVrv87x7ugo/')
    wks_total = linkou.worksheet_by_title('統整')
    y = 2
    for i in new:
        print(i['name'])
        wks_linkou = linkou.worksheet_by_title(i['name'] + '-實價登錄')
        linkou_list = wks_linkou.get_all_records()
        num = len(linkou_list)
        total = [i['name'], num, i['total'], i['total'] - num, num / i['total']]
        wks_total.update_values('A' + str(y), [total])
        y += 1
        export_total()
    return '成功'


if __name__ == "__main__":
    update_total()
