import settings
import json

from typing import (
    Optional,
)
from fastapi import (
    FastAPI,
    Header,
    HTTPException,
    Request,
)

from linebot import (LineBotApi, WebhookParser,)
from linebot.exceptions import (InvalidSignatureError, LineBotApiError,)
from linebot.models import (MessageEvent, TextSendMessage,)

from utility import make_response_text


CHANNEL_ACCESS_TOKEN = settings.CAT
CHANNEL_SECRET = settings.CS

app = FastAPI()

line_bot_api = LineBotApi(CHANNEL_ACCESS_TOKEN)
webhock_parser = WebhookParser(CHANNEL_SECRET)


@app.get("/echo")
async def echo():
    return {"message": "hello!!"}


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

    for event in events:
        mode = json.loads(str(event))['postback']['data']
        print(mode)
        if mode is not None:
            # モードは「TakatsukiToKansai」「TondaToKansai」「KansaiToTakatsuki」「KansaiToTonda」のどれか
            ret_text = make_response_text(mode)
            line_bot_api.reply_message(
                event.reply_token,
                TextSendMessage(text=ret_text)
            )

    return {'status': 'success'}
