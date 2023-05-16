from flask import Flask, request, abort
from linebot import LineBotApi, WebhookHandler
from linebot.exceptions import InvalidSignatureError
from linebot.models import *
import os
import shutil
import json
import threading
import requests
import time
from key import channel_access_token, channel_secret
from linkou import update_linkou
from price import update_price
from total import update_total
from export import export_linkou, export_price, export_total

app = Flask(__name__)

line_bot_api = LineBotApi(channel_access_token())
handler = WebhookHandler(channel_secret())

url = 'https://linkou-home-bot.onrender.com'

with open("new.json", "r", encoding="utf-8") as f:
    new = json.load(f)

for i in new:
    os.makedirs('./static/linkou/' + i['tag'], exist_ok=True)
    os.makedirs('./static/price/' + i['tag'], exist_ok=True)
os.makedirs('./static/total', exist_ok=True)
shutil.move('/opt/render/project/src/floor', './static/floor')


def wake():
    while 1 == 1:
        res = requests.get(url + '/wakeup')
        if res.status_code == 200:
            print('繼續賣肝')
        else:
            print('肝不動了')
        time.sleep(10 * 60)


threading.Thread(target=wake).start()


@app.route("/wakeup")
def wake_up():
    return "十萬青年十萬肝，加入輪班救台灣"


@app.route("/callback", methods=['POST'])
def callback():
    signature = request.headers['X-Line-Signature']
    body = request.get_data(as_text=True)
    app.logger.info("Request body: " + body)
    try:
        handler.handle(body, signature)
    except InvalidSignatureError:
        abort(400)
    return 'OK'


@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
    if event.message.text == 'update linkou':
        result = update_linkou()
        line_bot_api.reply_message(event.reply_token, TextSendMessage(text=result))
    if event.message.text == 'update price':
        result = update_price()
        line_bot_api.reply_message(event.reply_token, TextSendMessage(text=result))
    if event.message.text == 'update total':
        result = update_total()
        line_bot_api.reply_message(event.reply_token, TextSendMessage(text=result))
    if event.message.text == 'export linkou':
        for case in new:
            export_linkou(case)
        result = '實價登錄：成功'
        line_bot_api.reply_message(event.reply_token, TextSendMessage(text=result))
    if event.message.text == 'export price':
        for case in new:
            export_price(case)
        result = '銷售登錄表：成功'
        line_bot_api.reply_message(event.reply_token, TextSendMessage(text=result))
    if event.message.text == 'export total':
        export_total()
        result = '統整：成功'
        line_bot_api.reply_message(event.reply_token, TextSendMessage(text=result))
    if event.message.text == 'export all':
        for case in new:
            export_linkou(case)
            export_price(case)
        export_total()
        result = '匯出：成功'
        line_bot_api.reply_message(event.reply_token, TextSendMessage(text=result))

    if event.message.text == '實價登錄':
        flex = json.load(open('flex-linkou.json', 'r', encoding='utf-8'))
        for item in new:
            data = {"type": "box", "layout": "baseline",
                    "contents": [
                        {"type": "icon", "size": "lg",
                         "url": "https://scdn.line-apps.com/n/channel_devcenter/img/fx/review_gold_star_28.png"},
                        {"type": "text", "text": item['name'], "size": "lg", "align": "end",
                         "action": {"type": "postback", "label": "action", "data": '實價登錄/' + item['tag']}}]}
            flex['body']['contents'][1]['contents'].append(data)
        line_bot_api.reply_message(event.reply_token, FlexSendMessage(alt_text='新建案の實價登錄', contents=flex))

    if event.message.text == '銷售登錄表':
        flex = json.load(open('flex-price.json', 'r', encoding='utf-8'))
        for item in new:
            data = {"type": "box", "layout": "baseline",
                    "contents": [
                        {"type": "icon", "size": "lg",
                         "url": "https://scdn.line-apps.com/n/channel_devcenter/img/fx/review_gold_star_28.png"},
                        {"type": "text", "text": item['name'], "size": "lg", "align": "end",
                         "action": {"type": "postback", "label": "action", "data": '銷售登錄表/' + item['tag']}}]}
            flex['body']['contents'][1]['contents'].append(data)
        line_bot_api.reply_message(event.reply_token, FlexSendMessage(alt_text='新建案の銷售登錄表', contents=flex))

    if event.message.text == '統整':
        # flex = json.load(open('development.json', 'r', encoding='utf-8'))
        reply = []
        num = len(os.listdir('./static/total')) - 1
        for n in range(num):
            reply.append(ImageSendMessage(
                original_content_url=url + "/static/total/images_" + str(n) + ".png",
                preview_image_url=url + "/static/total/images_" + str(n) + ".png"))
        line_bot_api.reply_message(event.reply_token, reply)

    if event.message.text == '平面圖':
        flex = json.load(open('flex-floor.json', 'r', encoding='utf-8'))
        for item in new:
            data = {"type": "box", "layout": "baseline",
                    "contents": [
                        {"type": "icon", "size": "lg",
                         "url": "https://scdn.line-apps.com/n/channel_devcenter/img/fx/review_gold_star_28.png"},
                        {"type": "text", "text": item['name'], "size": "lg", "align": "end",
                         "action": {"type": "postback", "label": "action", "data": '平面圖/' + item['tag']}}]}
            flex['body']['contents'][1]['contents'].append(data)
        line_bot_api.reply_message(event.reply_token, FlexSendMessage(alt_text='新建案の平面圖', contents=flex))


@handler.add(PostbackEvent)
def post_back(event):
    back = event.postback.data.split("/")
    tag = back[1]
    reply = []
    if back[0] == '實價登錄':
        num = len(os.listdir('./static/linkou/' + tag)) - 1
        for n in range(num):
            reply.append(ImageSendMessage(
                original_content_url=url + "/static/linkou/" + tag + "/images_" + str(n) + ".png",
                preview_image_url=url + "/static/linkou/" + tag + "/images_" + str(n) + ".png"))
        line_bot_api.reply_message(event.reply_token, reply)
    elif back[0] == '銷售登錄表':
        num = len(os.listdir('./static/price/' + tag)) - 1
        for n in range(num):
            reply.append(ImageSendMessage(
                original_content_url=url + "/static/price/" + tag + "/images_" + str(n) + ".png",
                preview_image_url=url + "/static/price/" + tag + "/images_" + str(n) + ".png"))
        line_bot_api.reply_message(event.reply_token, reply)
    elif back[0] == '平面圖':
        line_bot_api.reply_message(event.reply_token, ImageSendMessage(
            original_content_url=url + "/static/floor/" + tag + ".png",
            preview_image_url=url + "/static/floor/" + tag + ".png"))
    else:
        print('TEST')


if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000)
