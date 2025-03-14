import io
import PIL.Image
import base64

BASE64_PREAMBLE = "data:image/png;base64,"


# 定义处理函数，将图片转化为base64编码
def img_to_base64(img: PIL.Image.Image):
    byte_arr = io.BytesIO()
    img.save(byte_arr, format='PNG')
    byte_arr = byte_arr.getvalue()
    encoded_string = base64.b64encode(byte_arr).decode('utf-8')
    return f"{BASE64_PREAMBLE}{encoded_string}"