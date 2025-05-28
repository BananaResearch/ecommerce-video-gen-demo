from datetime import datetime

# 获取当前时间并格式化为字符串，精确到 3 位毫秒
def get_time_text(sep = '_'):
    now = datetime.now()
    time_str = now.strftime(f"%Y%m%d{sep}%H%M%S{sep}%f")[:-3]  # 取微秒的前 3 位作为毫秒
    return time_str