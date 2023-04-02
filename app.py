from flask import Flask, request, abort
from linebot import LineBotApi, WebhookHandler
from linebot.exceptions import InvalidSignatureError
from linebot.models import *
import os
import json
from key import channel_access_token, channel_secret
from linkou import update_linkou
from price import update_price
from total import update_total
from export import export_linkou, export_price, export_total

app = Flask(__name__)

line_bot_api = LineBotApi(channel_access_token())
handler = WebhookHandler(channel_secret())

# url = 'https://linkou-home-bot.onrender.com'
url = 'https://855d-218-172-106-50.ngrok.io'

with open("new.json", "r") as f:
    new = json.load(f)

for i in new:
    os.makedirs('./static/linkou/' + i['tag'], exist_ok=True)
    os.makedirs('./static/price/' + i['tag'], exist_ok=True)
os.makedirs('./static/total', exist_ok=True)


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
    if event.message.text == 'update實價登錄':
        result = update_linkou()
        line_bot_api.reply_message(event.reply_token, TextSendMessage(text=result))
    if event.message.text == 'update銷售登錄表':
        result = update_price()
        line_bot_api.reply_message(event.reply_token, TextSendMessage(text=result))
    if event.message.text == 'update統整':
        result = update_total()
        line_bot_api.reply_message(event.reply_token, TextSendMessage(text=result))

    if event.message.text == '實價登錄':
        flex = json.load(open('flex-linkou.json', 'r', encoding='utf-8'))
        for item in new:
            data = {"type": "box", "layout": "baseline",
                    "contents": [
                        {"type": "icon", "size": "lg",
                         "url": "https://scdn.line-apps.com/n/channel_devcenter/img/fx/review_gold_star_28.png"},
                        {"type": "text", "text": item['name'], "size": "lg", "align": "end",
                         "action": {"type": "postback", "label": "action", "data": '實價登錄-' + item['name']}}]}
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
                         "action": {"type": "postback", "label": "action", "data": '銷售登錄表-' + item['name']}}]}
            flex['body']['contents'][1]['contents'].append(data)
        line_bot_api.reply_message(event.reply_token, FlexSendMessage(alt_text='新建案の銷售登錄表', contents=flex))

    if event.message.text == '統整':
        flex = json.load(open('development.json', 'r', encoding='utf-8'))
        line_bot_api.reply_message(event.reply_token, FlexSendMessage(alt_text='努力趕工中', contents=flex))


@handler.add(PostbackEvent)
def post_back(event):
    requests = event.postback.data.split("-")
    item = [element for element in new if element['name'] == requests[1]][0]
    reply = []
    if requests[0] == '實價登錄':
        num = len(os.listdir('./static/linkou/' + item['tag'])) - 1
        for n in range(num):
            reply.append(ImageSendMessage(
                original_content_url=url + "/static/linkou/" + item['tag'] + "/images_" + str(n) + ".png",
                preview_image_url=url + "/static/linkou/" + item['tag'] + "/images_" + str(n) + ".png"))
        line_bot_api.reply_message(event.reply_token, reply)
    elif requests[0] == '銷售登錄表':
        num = len(os.listdir('./static/price/' + item['tag'])) - 1
        for n in range(num):
            reply.append(ImageSendMessage(
                original_content_url=url + "/static/price/" + item['tag'] + "/images_" + str(n) + ".png",
                preview_image_url=url + "/static/price/" + item['tag'] + "/images_" + str(n) + ".png"))
        line_bot_api.reply_message(event.reply_token, reply)
    else:
        print('TEST')


if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5877)
