import psycopg2.pool
from flask_cors import CORS
import configparser
import os
import errno

from flask import Flask, jsonify, request

###参考サイト
# https://qiita.com/nekobake/items/4a6c1464889be2b53a63
# https://qiita.com/nekobake/items/4a6c1464889be2b53a63

def connect_postgresql():
        # コンフィグファイルからデータを取得
        config_db = configparser.ConfigParser()
        config_ini_path = "./config/dbconfig.ini"

        # 指定したiniファイルが存在しない場合、エラー発生
        if not os.path.exists(config_ini_path):
            raise FileNotFoundError(errno.ENOENT, os.strerror(errno.ENOENT), config_ini_path)
        config_db.read(config_ini_path)
        pool = psycopg2.pool.SimpleConnectionPool(
            minconn=2,
            maxconn=4,
            user=config_db["POSTGRESSQL_DB_SERVER"]["user"],
            password = config_db["POSTGRESSQL_DB_SERVER"]["password"],
            host = config_db["POSTGRESSQL_DB_SERVER"]["host"],
            port = config_db["POSTGRESSQL_DB_SERVER"]["port"],
            database = config_db["POSTGRESSQL_DB_SERVER"]["dbname"]
        )
        print("プール作成")


if __name__== '__main__':
      app = Flask(__name__)
      #特定のオリジンだけを許可する
      cors = CORS(app, resources={r"/*":{"origin": ["http://localhost:5173"]}})
      app.run(host='0.0.0.0', port=3333, debug=True)
      connect_postgresql()