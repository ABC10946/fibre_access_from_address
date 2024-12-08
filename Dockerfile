# ベースイメージとしてPython 3.9を使用
FROM python:3.10-slim

# 作業ディレクトリを設定
WORKDIR /app

# 依存関係ファイルをコピー
COPY requirements.txt requirements.txt

# 依存関係をインストール
RUN pip install --no-cache-dir -r requirements.txt

# アプリケーションのソースコードをコピー
COPY . .

# ポート5000を公開
EXPOSE 5000

# サーバーを起動
CMD ["python", "server.py"]