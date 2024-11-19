from flask import Flask, request, abort
import os
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
    # 確認請求來源是否合法
    signature = request.headers['X-Line-Signature']
    body = request.get_data(as_text=True)
    try:
        handler.handle(body, signature)
    except InvalidSignatureError:
        abort(400)
    return 'OK'


# 處理訊息事件
@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
    try:
        # 回應用戶的訊息
        reply_text = f"你說了: {event.message.text}"
        line_bot_api.reply_message(event.reply_token, TextSendMessage(text=reply_text))
    except Exception as e:
        print(f"Error handling message: {e}")


if __name__ == "__main__":
    http_server = WSGIServer(('0.0.0.0', int(LISTEN_PORT)), app)
    print('★★★★★★ 啟動Flask... port num : ' + LISTEN_PORT)
    http_server.serve_forever()
