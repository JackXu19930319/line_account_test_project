
# 使用官方的 Python 基礎映像檔
FROM python:3.9-slim

# 設定工作目錄
WORKDIR /app

# 複製當前目錄的內容到工作目錄
COPY . /app

# 安裝所需的 Python 套件
RUN pip install --no-cache-dir -r requirements.txt

# 設定環境變數
ENV PORT=8080

# 暴露應用程式埠
EXPOSE 8080

# 執行應用程式
CMD ["python", "main.py"]