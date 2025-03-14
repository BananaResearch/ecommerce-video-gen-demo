from datetime import datetime

def generate_timestamp_filename():
    now = datetime.now()
    timestamp = now.strftime("%Y%m%d-%H%M%S-%f")[:-3]  # 获取毫秒并截取前三位
    return timestamp