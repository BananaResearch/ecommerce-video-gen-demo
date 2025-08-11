import logging
import os
from logging.handlers import RotatingFileHandler

def setup_logger(name: str = 'ecommerce_video_gen') -> logging.Logger:
    """设置日志记录器

    Args:
        name: 日志记录器名称

    Returns:
        配置好的日志记录器
    """
    # 创建日志记录器
    logger = logging.getLogger(name)
    logger.setLevel(logging.INFO)

    # 避免重复添加处理器
    if logger.handlers:
        return logger

    # 创建控制台处理器
    console_handler = logging.StreamHandler()
    console_handler.setLevel(logging.INFO)

    # 创建格式化器
    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    console_handler.setFormatter(formatter)

    # 添加处理器到记录器
    logger.addHandler(console_handler)

    # 如果需要文件日志，可以取消下面的注释
    # log_dir = 'logs'
    # if not os.path.exists(log_dir):
    #     os.makedirs(log_dir)
    # file_handler = RotatingFileHandler(
    #     os.path.join(log_dir, 'app.log'),
    #     maxBytes=1024 * 1024 * 5,  # 5MB
    #     backupCount=5,
    #     encoding='utf-8'
    # )
    # file_handler.setLevel(logging.INFO)
    # file_handler.setFormatter(formatter)
    # logger.addHandler(file_handler)

    return logger