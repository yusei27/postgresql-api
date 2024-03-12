import psycopg2.pool
from db.execute_sql import ExecuteSQL
from flask_cors import CORS
import configparser
import os
import errno

from flask import Flask, jsonify, request

app = Flask(__name__)

###参考サイト
# https://www.geeksforgeeks.org/python-postgresql-connection-pooling-using-psycopg2/
# https://qiita.com/nekobake/items/4a6c1464889be2b53a63


#あとで並列にリクエストを処理できるようにする
# https://qiita.com/5zm/items/251be97d2800bf67b1c6
@app.route("/tmp", methods=["GET"])
def get_tmp():
    print("tmp_select")
    try:
        db = ExecuteSQL(pool)
        sql = f"""
                INSERT INTO "fridge-system".user_table
                (name_user, mail)
                    VALUES (%s, %s);    
        """
        db.execute_query(sql, bind_var=("nova-tarou", "25"))
        db.commit()
    except Exception as e:
        print(e)
        db.rollback()
        print("ロールバックを実行しました。")
        return jsonify({'status':300, 'data':3})



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
      
      #特定のオリジンだけを許可する
      cors = CORS(app, resources={r"/*":{"origin": ["http://localhost:5173"]}})
      app.run(host='0.0.0.0', port=3333, debug=True, threaded=True)
      pool = connect_postgresql()