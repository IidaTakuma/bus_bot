import settings
import json

from typing import (Optional,)
from fastapi import (FastAPI, Header, HTTPException, Request,)

from linebot import (WebhookParser,)
from linebot.exceptions import (InvalidSignatureError, LineBotApiError,)
from text_send_message_custom import (Message, TextSendMessageCustom)
from line_bot_api_custom import LineBotApiCustom
from utility import TimeTableUtility


CHANNEL_ACCESS_TOKEN = settings.CAT
CHANNEL_SECRET = settings.CS

app = FastAPI()
line_bot_api = LineBotApiCustom(CHANNEL_ACCESS_TOKEN)
webhock_parser = WebhookParser(CHANNEL_SECRET)


@app.get("/echo")
async def echo():
    return {'status': 'success'}


@app.post("/callback")
async def callback(
        request: Request,
        x_line_signature: Optional[str] = Header(None)):

    body = await request.body()

    try:
        events = webhock_parser.parse(body.decode('utf-8'), x_line_signature)
    except InvalidSignatureError:
        raise HTTPException(status_code=401, detail="Invalid signature error")
    except LineBotApiError:
        raise HTTPException(status_code=400, detail="Line bot api error")

    # モードは "TakatsukiToKansai","TondaToKansai","KansaiToTakatsuki","KansaiToTonda"のいずれか
    for event in events:
        mode = json.loads(str(event))['postback']['data']
        if mode is not None:
            timeTable_utility = TimeTableUtility(mode)
            messages = list()
            all_timeTable_message = Message(
                timeTable_utility.make_all_timeTable_text())
            messages.append(all_timeTable_message)
            next_three_bus_message = Message(
                timeTable_utility.make_response_text())
            messages.append(next_three_bus_message)
            line_bot_api.reply_message(
                event.reply_token,
                TextSendMessageCustom(_messages=messages)
            )

    return {'status': 'success'}
