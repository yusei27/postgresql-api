#元となるDockerイメージの指定
FROM python:3.12.1
#作成者
LABEL maintainer "yusei-hashimoto"

#デフォルトでDebianが入る、下記のコマンドで余計なものを削除してコンテナサイズを落とす
# 「&&（複数コマンドが書ける）」と「 \（改行して書ける）」
# https://dev.classmethod.jp/articles/apt-get-magic-spell-in-docker/
# RUN apt-get update && apt-get install -y \
#     xxx \
#     && apt-get clean \
#     && rm -rf /var/lib/apt/lists/*

#pipenvをインストール
RUN pip install --upgrade pip && \
    pip install pipenv

#API起動
#CMD ["python", "./app.py"]