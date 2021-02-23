import json
from linebot.api import LineBotApi
from custom_text_send_message import (Message, CustomTextSendMessage)


class LineBotApiCustom(LineBotApi):
    def reply_message(self,
                      reply_token,
                      messages: CustomTextSendMessage,
                      notification_disabled=False,
                      timeout=None):
        if not isinstance(messages, (list, tuple)):
            messages = [messages]

        data = {
            'replyToken': reply_token,
            'messages': [message.messages.as_json_dict() for message in messages],
            'notificationDisabled': notification_disabled,
        }

        self._post(
            '/v2/bot/message/reply', data=json.dumps(data), timeout=timeout
        )
