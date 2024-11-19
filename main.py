import os
from flask import Flask, request, abort
from linebot import LineBotApi, WebhookHandler
from linebot.exceptions import InvalidSignatureError
from linebot.models import MessageEvent, TextMessage, TextSendMessage
from gevent.pywsgi import WSGIServer

# 初始化 Flask 應用
app = Flask(__name__)

# 設定 LINE API 的 Channel Access Token 和 Channel Secret
LINE_CHANNEL_ACCESS_TOKEN = os.environ.get('LINE_CHANNEL_ACCESS_TOKEN', 'YOUR_DEFAULT_ACCESS_TOKEN')
LINE_CHANNEL_SECRET = os.environ.get('LINE_CHANNEL_SECRET', 'YOUR_DEFAULT_CHANNEL_SECRET')

line_bot_api = LineBotApi(LINE_CHANNEL_ACCESS_TOKEN)
handler = WebhookHandler(LINE_CHANNEL_SECRET)

LISTEN_PORT = os.environ.get('PORT', '80')


@app.route("/")
def hello():
    return "Hello, World!"


@app.route("/callback", methods=['POST'])
def callback():
    # 確認來自 LINE 平台的請求
    signature = request.headers['X-Line-Signature']
    body = request.get_data(as_text=True)

    try:
        handler.handle(body, signature)
    except InvalidSignatureError:
        abort(400)

    return 'OK'


@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
    # 使用者傳來的訊息
    user_message = event.message.text
    # 回應訊息
    reply_message = f"{user_message} send"
    line_bot_api.reply_message(event.reply_token, TextSendMessage(text=reply_message))


if __name__ == "__main__":
    http_server = WSGIServer(('0.0.0.0', int(LISTEN_PORT)), app)
    print('★★★★★★ 啟動Flask... port num : ' + LISTEN_PORT)
    http_server.serve_forever()
