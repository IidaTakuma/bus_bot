from linebot.models.send_messages import SendMessage


class TextSendMessageCustom(SendMessage):
    """ 複数メッセージを一度のレスポンスで送信するためのクラス """

    def __init__(self, _messages=None, quick_reply=None, **kwargs):

        super(TextSendMessageCustom, self).__init__(
            quick_reply=quick_reply, **kwargs)

        self.messages = _messages


class Message():
    def __init__(self, _text):
        self.type = 'text'
        self.text = _text
