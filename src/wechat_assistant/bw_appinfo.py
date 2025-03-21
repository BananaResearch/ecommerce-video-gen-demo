from typing import TypedDict
import os
import time

# 答疑助手
APP_FAQ_ASSISTANT='faq_assistant'

class AppInfo(TypedDict):
    app_id: str
    corp_id: str
    agent_id: str
    secret: str
    token: str
    aes_key: str

app_infos = {}
access_tokens = {}

def init_app_info():
    corp_id = os.getenv('WECHAT_CORP_ID', '')

    info = {
        'app_id': APP_FAQ_ASSISTANT,
        'corp_id': corp_id,
        'agent_id': os.getenv('FAQ_ASSISTANT_AGENT_ID', ''),
        'secret': os.getenv('FAQ_ASSISTANT_SECRET', ''),
        'token': os.getenv('FAQ_ASSISTANT_TOKEN', ''),
        'aes_key': os.getenv('FAQ_ASSISTANT_AES_KEY', ''),
    }

    app_infos[APP_FAQ_ASSISTANT] = info

def get_app_info(app_id: str) -> AppInfo | None:
    return app_infos.get(app_id, None)

def get_access_token_api(app_id: str):
    pass

def get_access_token_refresh(app_id: str):
    new_token = get_access_token_api(app_id)

    access_tokens[app_id] = {
        'token': new_token,
        'expires_at': int(time.time()) + 7000,
    }

    return new_token

def get_access_token(app_id: str):
    token_info = access_tokens.get(app_id, None)
    if not token_info or token_info['expires_at'] < int(time.time()):
        return get_access_token_refresh(app_id)
    else:
        return token_info['token']