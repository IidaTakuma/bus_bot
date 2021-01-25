import settings

# 検証用
import base64
import hashlib
import hmac
import json

from typing import (
    Dict,
    List,
    Optional,
)
from fastapi import (
    FastAPI,
    Header,
    HTTPException,
)
from pydantic import (
    BaseModel
)

from starlette.responses import (
    Response
)

from starlette.status import (
    HTTP_200_OK
)

CHANNEL_ACCESS_TOKEN = settings.CAT
CHANNEL_SECRET = settings.CS

app = FastAPI()


def signatureVerification(x_line_signature, request_body):
    hash = hmac.new(CHANNEL_SECRET.encode('utf-8'),
                    request_body.encode('utf-8'), hashlib.sha256).digest()
    signature = base64.b64encode(hash)

    # print(request_body)

    if x_line_signature == signature:
        return True
    else:
        return False


@app.get("/echo")
async def echo():
    return {"message": "hello!!"}


@app.post("/callback", status_code=200)
async def callback(
        response: Response,
        body_data: Dict,
        x_line_signature: Optional[str] = Header(None)):

    print("x_line_signature:", x_line_signature)
    print("body_data:", body_data)

    json_body = json.dumps(body_data)
    if signatureVerification(x_line_signature, json.dumps(json_body)):
        response.status_code = HTTP_200_OK
        return {"text": "OK!"}
    else:
        raise HTTPException(status_code=404, detail="Verification failed!!")
