# 使用Python 3.11作为基础镜像
FROM python:3.11-alpine

# 设置工作目录
WORKDIR /app

# 复制依赖文件
COPY requirements.txt .

# 配置阿里云源
RUN pip config set global.index-url https://mirrors.aliyun.com/pypi/simple/

# 安装Python依赖
RUN pip install -r requirements.txt

# 复制项目文件
COPY . .

# 安装当前项目
RUN pip install -e .

# 暴露端口（Gradio默认使用7860）
EXPOSE 7860

# 启动命令
CMD ["python", "src/app.py"]