import json
from linebot.api import LineBotApi
from text_send_message_custom import (TextSendMessageCustom)


class LineBotApiCustom(LineBotApi):
    def reply_message(self,
                      reply_token,
                      messages: TextSendMessageCustom,
                      notification_disabled=False,
                      timeout=None):
        # if not isinstance(messages, (list, tuple)):
        #     messages = [messages]

        data = {
            'replyToken': reply_token,
            'messages': [message.as_json_dict() for message in messages.messages],
            'notificationDisabled': notification_disabled,
        }

        self._post(
            '/v2/bot/message/reply', data=json.dumps(data), timeout=timeout
        )
