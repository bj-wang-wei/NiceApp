FROM python:3.11-slim-bookworm

# 创建工作目录
WORKDIR /usr/src/app

# 复制依赖文件并安装依赖
COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

# 复制应用程序代码
COPY . .

# 使用非 root 用户运行
RUN useradd -m appuser
USER appuser

# 设置默认启动命令
CMD ["python3", "./main.py"]