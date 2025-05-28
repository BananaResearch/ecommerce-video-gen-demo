import os
from cozepy import COZE_CN_BASE_URL
from cozepy import Coze, TokenAuth, Message, ChatStatus, MessageContentType  # noqa

def coze_asr(audio_file_path: str):
    '''
    调用 coze 的 asr 接口，将音频文件转换为文本 。
    '''

    # Get an access_token through personal access token or oauth.
    coze_api_token = os.getenv('COZE_CN_API_TOKEN', '')
    # The default access is api.coze.com, but if you need to access api.coze.cn,
    # please use base_url to configure the api endpoint to access
    coze_api_base = COZE_CN_BASE_URL
    # Init the Coze client through the access_token.
    coze = Coze(auth=TokenAuth(token=coze_api_token), base_url=coze_api_base)

    result = coze.audio.transcriptions.create(file=open(audio_file_path, 'rb'))

    print(result.text)

    return result