import settings

# 検証用
import base64
import hashlib
import hmac

from typing import (
    Dict,
    List,
    Optional,
)
from fastapi import (
    FastAPI,
    Header,
    HTTPException,
    Request,
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


def signatureVerification(x_line_signature, body):
    hash = hmac.new(CHANNEL_SECRET.encode('utf-8'),
                    body, hashlib.sha256).digest()
    signature = base64.b64encode(hash).decode('utf-8')

    print("x_line_signature:", x_line_signature)
    print("signature:", signature)

    if x_line_signature == signature:
        return True
    else:
        return False


@app.get("/echo")
async def echo():
    return {"message": "hello!!"}


@app.post("/callback")
async def callback(
        request: Request,
        response: Response,
        x_line_signature: Optional[str] = Header(None)):
    body = await request.body()
    if signatureVerification(x_line_signature, body):
        response.status_code = HTTP_200_OK
        return {"text": "OK!"}
    else:
        raise HTTPException(status_code=404, detail="Verification failed!!")

# @app.post("/callback", status_code=200)
# async def callback(
#         response: Response,
#         dict_body: Dict,
#         x_line_signature: Optional[str] = Header(None)):

#     json_body = json.dumps(dict_body)
#     print("dict_body:", dict_body)
#     print("json_body:", json_body)
#     if signatureVerification(x_line_signature, json_body):
#         response.status_code = HTTP_200_OK
#         return {"text": "OK!"}
#     else:
#         raise HTTPException(status_code=404, detail="Verification failed!!")
