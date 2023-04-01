import pygsheets
import numpy as np


def update_total():
    key = pygsheets.authorize(service_file='credentials.json')
    turtle = key.open_by_url('https://docs.google.com/spreadsheets/d/1UMUFc1FHYFbYBseO8ShmTDyb9555oYBSe3WY83IWP_M/')

    wks_price = turtle.worksheet_by_title('銷售登錄')
    wks_member = turtle.worksheet_by_title('已購群組')
    wks_total = turtle.worksheet_by_title('TOTAL')

    types = ['A1', 'A2', 'A3', 'A5', 'A6', 'B1', 'B2', 'B3', 'B5', 'B6', 'B7']
    member = 0
    price = 0
    price_array = []
    member_array = []

    price_list = wks_price.get_all_records()
    for item in price_list:
        if item['銷售登錄'] != '':
            for type in types:
                if item[type] != '':
                    price += 1
                    price_array.append(type + '-' + str(item['銷售登錄']))

    member_list = wks_member.get_all_records()
    for item in member_list:
        if item['已購群組'] != '':
            for type in types:
                if item[type] != '':
                    member += 1
                    member_array.append(type + '-' + str(item['已購群組']))

    price_diff = np.setdiff1d(price_array, member_array)
    member_diff = np.setdiff1d(member_array, price_array)

    wks_total.update_value('A2', price)
    wks_total.update_value('B2', member)
    wks_total.update_value('A5', len(price_diff))
    wks_total.update_value('B5', len(member_diff))
    wks_total.update_values('A6', [[''] * 2 for _ in range(100)])
    wks_total.update_values('A7', np.array(price_diff).reshape(len(price_diff), 1).tolist())
    wks_total.update_values('B7', np.array(member_diff).reshape(len(member_diff), 1).tolist())
    return '成功'


if __name__ == "__main__":
    update_total()
