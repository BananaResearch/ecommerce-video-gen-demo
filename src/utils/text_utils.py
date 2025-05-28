def format_text(text: str, max_length: int = 300) -> str:
    """格式化文本，超过指定长度则截断并添加...
    
    Args:
        text: 要格式化的文本
        max_length: 最大允许长度，默认为100
        
    Returns:
        格式化后的文本
    """
    if len(text) > max_length:
        return text[:max_length] + "..."
    return text