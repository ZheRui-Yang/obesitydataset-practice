from flask import Flask, request, abort
from linebot import LineBotApi, WebhookHandler
from linebot.exceptions import InvalidSignatureError
from linebot.models import MessageEvent, TextMessage, TextSendMessage
from . import settings
from . import model


app = Flask(__name__)

# create line-bot instance
line_bot_api = LineBotApi(settings.LINE_CHANNEL_ACCESS_TOKEN)
handler = WebhookHandler(settings.LINE_CHANNEL_SECRET)

# our mechine learning model
md = model.Model()
md.load_fit()

question_id = 0  # global step indicator, 0 for not in progress
questionnaire = {}  # container of user replies

keylabels = settings.LABELS  # 使用者選項字典的鍵值
question_text = settings.QUESTION_DESC  # 問卷說明文字
choice_text = settings.CHOICES  # 選項文字
ctt = settings.CHOICE_TRANSFORMATION_TABLE  # 用來轉換成 model 能懂的形式


@app.route("/bmibot", methods=['POST'])
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
        print("Invalid signature. Please check your channel access "
              "token/channel secret.")
        abort(400)

    return 'OK'


@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
    global question_id
    global questionnaire

    msg_in = event.message.text.lower()

    if msg_in.lower() in ['說明', 'help', '幫助']:
        reply = '這是說明文字'
    elif msg_in in ["go", "start", "開始"]:
        question_id = 1
        questionnaire = {}
        reply = make_question_text('問卷開始！請輸入選項前的數字答題')
    elif msg_in in ["重來", "restart"]:
        question_id = 1
        questionnaire = {}
        reply = make_question_text('問卷重來')
    elif msg_in in ["結束", "stop", "over"]:
        question_id = 0
        questionnaire = {}
        reply = '問卷結束'
    else:
        key = keylabels[question_id - 1]
        try:
            choice = int(msg_in)
        except ValueError:
            choice = msg_in

        try:
            questionnaire[key] = ctt[question_id - 1][choice]
            question_id += 1

            if not question_id > len(keylabels):
                reply = make_question_text()
        except KeyError:
            reply = make_question_text('您選了不存在的選項，請再選一次')

    if question_id > len(keylabels):
        result = md.transform_predict(questionnaire)
        suggestion = settings.SUGGETIONS[result]
        reply = '結果： ' + result.replace('_', ' ') + '\n' + suggestion

        question_id = 0
        questionnaire = {}

    line_bot_api.reply_message(  # reply plain text
        event.reply_token,
        TextSendMessage(text=reply))


def make_question_text(text=None):
    text = '' if text is None else text

    choice = ''
    for i, v in enumerate(choice_text[question_id - 1]):
        choice += str(i + 1) + '. ' + v + '\n'

    return (text + '\n\n'
            + question_text[question_id - 1] + '\n'
            + choice).strip()


if __name__ == "__main__":
    app.run()
