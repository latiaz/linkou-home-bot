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

url = 'https://linkou-home-bot.onrender.com'

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

    # if event.message.text == '實價登錄':
    #     result = export_sunny()
    #     if result == '成功':
    #         line_bot_api.reply_message(event.reply_token, [ImageSendMessage(
    #             original_content_url=url + "/static/sunny/images_0.png",
    #             preview_image_url=url + "/static/sunny/images_0.png"),
    #             ImageSendMessage(
    #                 original_content_url=url + "/static/sunny/images_1.png",
    #                 preview_image_url=url + "/static/sunny/images_1.png")])
    # if event.message.text == '銷售登錄表':
    #     result = export_price()
    #     if result == '成功':
    #         line_bot_api.reply_message(event.reply_token, ImageSendMessage(
    #             original_content_url=url + "/static/price/images_0.png",
    #             preview_image_url=url + "/static/price/images_0.png"))
    # if event.message.text == '統整':
    #     result = export_total()
    #     if result == '成功':
    #         line_bot_api.reply_message(event.reply_token, ImageSendMessage(
    #             original_content_url=url + "/static/total/images_0.png",
    #             preview_image_url=url + "/static/total/images_0.png"))


if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000)
