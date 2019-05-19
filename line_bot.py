from flask import Flask, request, abort
from linebot import (LineBotApi, WebhookHandler)
from linebot.exceptions import (InvalidSignatureError)
from linebot.models import (MessageEvent, TextMessage, TextSendMessage,)
from pcc import tender

app = Flask(__name__)
line_bot_api = LineBotApi('W6zpUfcms1ytidHlMmZhAktnhgsvND+2yIfvV5vcEagCrbe8i/bVJ2dV9Oxz006p+S20SQKy26XsnvsMJVS2aPdVnnMKz3EFw4EWKRd5vbeHJwctRXjYCRkOPCB2/+aRLn9FJI1Jo8sZQer1ltu5CAdB04t89/1O/w1cDnyilFU=')
handler = WebhookHandler('4516396bb160573c5800a111047ca918')

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

#===============================================#
@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
    td = tender(event.message.text) #搜尋關鍵字
    try:
        line_bot_api.reply_message(event.reply_token,TextSendMessage(td.message(td.search())))
    except:
        line_bot_api.reply_message(event.reply_token,TextSendMessage("從政府電子採購網爬蟲失敗..."))    

#===============================================#
if __name__ == "__main__":
    app.run()