from flask import Flask, request, abort
from linebot import (LineBotApi, WebhookHandler)
from linebot.exceptions import (InvalidSignatureError)
from linebot.models import (MessageEvent, TextMessage, TextSendMessage,)
from pcc import tender

app = Flask(__name__)
line_bot_api = LineBotApi('') #Channel access token
handler = WebhookHandler('') #Channel secret

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