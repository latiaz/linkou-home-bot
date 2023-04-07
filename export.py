import requests
import popdf


url = 'https://docs.google.com/spreadsheets/d/1FLEjEXlhYzobw6JhJWQuw7OUfkq2GAx1xVrv87x7ugo/pdf?id' \
      '=1FLEjEXlhYzobw6JhJWQuw7OUfkq2GAx1xVrv87x7ugo&esid=77b1093f9f27a54e'


def export_linkou(case):
    form_data = {'a': 'true', 'gf': '[]', 'lds': '[]', 'pc': case['linkou']}

    r = requests.post(url, data=form_data)
    with open("./static/linkou/" + case['tag'] + "/export.pdf", 'wb') as f:
        f.write(r.content)

    popdf.pdf2imgs(
        pdf_path='./static/linkou/' + case['tag'] + '/export.pdf',
        out_dir='./static/linkou/' + case['tag']
    )
    return '成功'


def export_price(case):
    form_data = {'a': 'true', 'gf': '[]', 'lds': '[]', 'pc': case['price']}

    r = requests.post(url, data=form_data)
    with open("./static/price/" + case['tag'] + "/export.pdf", 'wb') as f:
        f.write(r.content)

    popdf.pdf2imgs(
        pdf_path='./static/price/' + case['tag'] + '/export.pdf',
        out_dir='./static/price/' + case['tag']
    )
    return '成功'


def export_total():
    form_data = {
        'a': 'true', 'gf': '[]', 'lds': '[]',
        'pc': '[null,null,null,null,null,null,null,null,null,0,[["373118791"]],10000000,null,null,null,null,null,'
              'null,null,null,null,null,null,null,null,null,45023.70489784722,null,null,[1,null,0,0,0,0,0,0,1,1,2,1,'
              'null,null,1,1],["A4",0,2,1,[0.75,0.75,0.7,0.7]],null,0]',
    }
    r = requests.post(url, data=form_data)
    with open("./static/total/total.pdf", 'wb') as f:
        f.write(r.content)

    popdf.pdf2imgs(
        pdf_path='./static/total/total.pdf',
        out_dir='./static/total'
    )
    return '成功'


if __name__ == "__main__":
    export_total()
