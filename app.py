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

line_bot_api = LineBotApi('hDEXigBx3q22MD9N4c4k9h/7ql08sBMCUTAuhBAevphGCcbIJb65W0nik3BePY6w68ZBPb9dkjc/s+2znFz26qZrSiOSKCghglNRZJCnQe7NUHi+RGMIExGa0r+A3HGYMAVFZwctBTmuqyTyp2aDAAdB04t89/1O/w1cDnyilFU=')
handler = WebhookHandler('bc1445fa31789d24b3cebe96a69b5010')


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
def handle_message(event):
    line_bot_api.reply_message(
        event.reply_token,
        TextSendMessage(text=event.message.text))


if __name__ == "__main__":
    app.run()