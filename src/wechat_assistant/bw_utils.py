from wechat_assistant.bw_appinfo import get_app_info 
from wechat_assistant.WXBizMsgCrypt import WXBizMsgCrypt
def verify_signature(signature: str, app_id: str, timestamp: str, nonce: str, msg_encrypt: str):
    app_info = get_app_info(app_id)
    if not app_info:
        raise Exception('app_id not found')

    token = app_info['token']
    aes_key = app_info['aes_key']
    corp_id = app_info['corp_id']

    crypt = WXBizMsgCrypt(token, aes_key, corp_id)

    return crypt.VerifyURL(signature, timestamp, nonce, msg_encrypt)

def decrypt_msg(app_id: str, timestamp: str, nonce: str, msg_encrypt: str):
    pass
    
