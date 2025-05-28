import os
from utils.datetime_utils import get_time_text
def parse_file_path(file_path):
    # 获取完整文件名
    full_name = os.path.basename(file_path)
    
    # 手动分割文件名
    parts = full_name.split('.')
    
    # 最后一个部分是扩展名
    ext_name = "." + parts[-1] if len(parts) > 1 else ""
    
    # 剩余部分是基础名称
    base_name = ".".join(parts[:-1]) if len(parts) > 1 else full_name
    
    return {
        "full_name": full_name,
        "base_name": base_name,
        "ext_name": ext_name
    }

def gen_timed_file_name(file_path):
    file_info = parse_file_path(file_path)
    return f"{file_info['base_name']}_{get_time_text()}.{file_info['ext_name']}"