#!/bin/bash

# 遍历当前文件夹中所有的 .mp4 文件
for video_file in *.mp4; do
  # 检查是否找到 .mp4 文件
  if [ -e "$video_file" ]; then
    # 提取文件名（不带扩展名）
    base_name="${video_file%.*}"
    
    # 输出 mp3 文件名
    audio_file="${base_name}.mp3"
    
    # 使用 ffmpeg 提取音频
    echo "正在处理: $video_file -> $audio_file"
    ffmpeg -i "$video_file" -q:a -1 -map a "$audio_file"
  else
    echo "未找到任何 .mp4 文件。"
  fi
done

echo "处理完成！"
