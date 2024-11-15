import pygsheets
import json
import numpy as np
np.seterr(divide='ignore', invalid='ignore')
from export import export_total


def update_total():
    with open("new.json", "r", encoding="utf-8") as f:
        new = json.load(f)

    # old = json.load(open('old.json', 'r', encoding='utf-8'))
    total = new
    key = pygsheets.authorize(service_file='credentials.json')
    linkou = key.open_by_url('https://docs.google.com/spreadsheets/d/1FLEjEXlhYzobw6JhJWQuw7OUfkq2GAx1xVrv87x7ugo/')
    wks_total = linkou.worksheet_by_title('統整')
    wks_average = linkou.worksheet_by_title('單價統整')
    y = 3
    summary_each = [0] * 19
    summary_total = [0] * 3
    summary_average = [0] * 19
    for i in total:
        each = [0] * 19
        average = [0] * 19
        print(i['name'])
        wks_linkou = linkou.worksheet_by_title(i['name'] + '-實價登錄')
        linkou_list = wks_linkou.get_all_records()
        for case in linkou_list:
            date = str(case['交易日期'])[:5]
            if date == '11101' or date == '11102' or date == '11103':
                each[1] += 1
                average[1] += case['單價']
            elif date == '11104' or date == '11105' or date == '11106':
                each[2] += 1
                average[2] += case['單價']
            elif date == '11107' or date == '11108' or date == '11109':
                each[3] += 1
                average[3] += case['單價']
            elif date == '11110' or date == '11111' or date == '11112':
                each[4] += 1
                average[4] += case['單價']
            elif date == '11201' or date == '11202' or date == '11203':
                each[5] += 1
                average[5] += case['單價']
            elif date == '11204' or date == '11205' or date == '11206':
                each[6] += 1
                average[6] += case['單價']
            elif date == '11207' or date == '11208' or date == '11209':
                each[7] += 1
                average[7] += case['單價']
            elif date == '11210' or date == '11211' or date == '11212':
                each[8] += 1
                average[8] += case['單價']
            elif date == '11301':
                each[9] += 1
                average[9] += case['單價']
            elif date == '11302':
                each[10] += 1
                average[10] += case['單價']
            elif date == '11303':
                each[11] += 1
                average[11] += case['單價']
            elif date == '11304':
                each[12] += 1
                average[12] += case['單價']
            elif date == '11305':
                each[13] += 1
                average[13] += case['單價']
            elif date == '11306':
                each[14] += 1
                average[14] += case['單價']
            elif date == '11307':
                each[15] += 1
                average[15] += case['單價']
            elif date == '11308':
                each[16] += 1
                average[16] += case['單價']
            elif date == '11309':
                each[17] += 1
                average[17] += case['單價']
            elif date == '11310':
                each[18] += 1
                average[18] += case['單價']
            else:
                each[0] += 1
                average[0] += case['單價']
        name = [i['name']]
        num = len(linkou_list)
        total = [num, i['total'], i['total'] - num, num / i['total']]
        result = name + each + total
        average_price_np = np.nan_to_num(np.divide(average, each), nan=0)
        average_price = average_price_np.tolist()
        result_price = name + average_price
        result_price.append(sum(average_price) / len(average_price_np[average_price_np != 0]))
        wks_total.update_values('A' + str(y), [[data if data != 0 else '' for data in result]])
        wks_average.update_values('A' + str(y), [[data if data != 0 else '' for data in result_price]])
        y += 1
        summary_each = np.sum([each, summary_each], axis=0).tolist()
        summary_total = np.sum([total[:3], summary_total], axis=0).tolist()
        summary_average = np.sum([average, summary_average], axis=0).tolist()
    result_average = np.divide(summary_average, summary_each).tolist()
    summary_each.insert(0, '總計')
    summary_each += summary_total
    result_average.append(sum(result_average) / len(result_average))
    result_average.insert(0, '總計')
    wks_total.update_values('A' + str(y), [summary_each])
    wks_average.update_values('A' + str(y), [result_average])
    export_total()
    return '成功'


if __name__ == "__main__":
    update_total()
