import requests
import popdf
import json


url = 'https://docs.google.com/spreadsheets/d/1FLEjEXlhYzobw6JhJWQuw7OUfkq2GAx1xVrv87x7ugo/pdf?id' \
      '=1FLEjEXlhYzobw6JhJWQuw7OUfkq2GAx1xVrv87x7ugo&esid=547ee5c50b863ca2'


def export_linkou(case):
    form_data = {'a': 'true', 'gf': '[]', 'lds': '[]', 'pc': case['linkou']}

    r = requests.post(url, data=form_data)
    with open("./old/linkou/" + case['tag'] + "/export.pdf", 'wb') as f:
        f.write(r.content)

    popdf.pdf2imgs(
        pdf_path='./old/linkou/' + case['tag'] + '/export.pdf',
        out_dir='./old/linkou/' + case['tag']
    )
    return '成功'


def export_price(case):
    form_data = {'a': 'true', 'gf': '[]', 'lds': '[]', 'pc': case['price']}

    r = requests.post(url, data=form_data)
    with open("./old/price/" + case['tag'] + "/export.pdf", 'wb') as f:
        f.write(r.content)

    popdf.pdf2imgs(
        pdf_path='./old/price/' + case['tag'] + '/export.pdf',
        out_dir='./old/price/' + case['tag']
    )
    return '成功'


def export_all():
    old = json.load(open('old.json', 'r', encoding='utf-8'))
    for case in old:
        export_linkou(case)
        export_price(case)
    return '成功'


if __name__ == "__main__":
    export_all()
