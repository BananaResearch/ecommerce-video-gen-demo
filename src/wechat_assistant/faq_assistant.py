from fastapi.routing import APIRouter
import hashlib
from wechat_assistant.bw_utils import verify_signature 
from wechat_assistant.bw_appinfo import APP_FAQ_ASSISTANT

router = APIRouter(prefix='/faq-assistant')

app_id = APP_FAQ_ASSISTANT

# 企业微信消息回调
@router.get('/bw-callback')
def business_wechat_callback(msg_signature: str, timestamp: str, nonce: str, echostr: str):
    # dev_msg_signature = calculate_signature(token, timestamp, nonce, echostr)
    pass

@router.get('/bw-callback/verify')
def business_wechat_callback_verify(msg_signature: str, timestamp: str, nonce: str, echostr: str):
    ret, sReplyEchoStr = verify_signature(msg_signature, app_id, timestamp, nonce, echostr)

    if ret == 0:
        return sReplyEchoStr

    raise Exception('verify signature failed')
