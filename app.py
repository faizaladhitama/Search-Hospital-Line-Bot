# encoding: utf-8
from flask import Flask, request, abort

from linebot import (
    LineBotApi, WebhookHandler
)
from linebot.exceptions import (
    InvalidSignatureError
)
from linebot.models import (
    MessageEvent, TextMessage, TextSendMessage,
)

app = Flask(__name__)

#Your Channel Access Token
line_bot_api = LineBotApi("vfKILEFUN3oaz79OgC4XOrPQ9jXbgBrKMdjkuFpEf/Fu9mjOKrR5+ZHEKHW1Qv+ha/vkMjZO2Y5eNcyTmtT7fhdgPhQ6ctgoTL2WeyrZzyUvVaYwduEdAXZ2kH06tHOGjNo7eRezf0puW+tyXc20LgdB04t89/1O/w1cDnyilFU=") 
#Your Channel Secret
handler = WebhookHandler("fb698ed6c00c04a7ced40856bddd6890")

@app.route("/callback", methods=['POST'])
def callback():
    # get X-Line-Signature header value
    signature = request.headers['X-Line-Signature']

    # get request body as text
    body = request.get_data(as_text=True)
    app.logger.info("Request body: " + body)

    # handle webhook body
    try:
        handler.handle(body, signature)
    except InvalidSignatureError:
        abort(400)

    return 'OK'

@handler.add(MessageEvent, message=TextMessage)
def handle_text_message(event):
    text = event.message.text #message from user

    line_bot_api.reply_message(
        event.reply_token,
        TextSendMessage(text=text)) #reply the same message from user
    

import os
if __name__ == "__main__":
    app.run(host='0.0.0.0',port=int(os.environ['PORT']))
