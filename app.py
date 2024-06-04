import psycopg2.pool
from db.execute_sql import ExecuteSQL
from sql.sql_creator import SqlCreator
from flask_cors import CORS
import configparser
import os
import errno
from psycopg2.sql import Identifier, Literal
from psycopg2.sql import SQL

from flask import Flask, jsonify, request

from log.logger import logger

app = Flask(__name__)


###参考サイト
# https://www.geeksforgeeks.org/python-postgresql-connection-pooling-using-psycopg2/
# https://qiita.com/nekobake/items/4a6c1464889be2b53a63
# https://resanaplaza.com/2021/09/15/%E3%80%90-%E3%82%B3%E3%83%94%E3%83%9A%E3%81%A7ok%E3%80%91%EF%BC%99%E5%89%B2%E3%81%AE%E6%A9%9F%E8%83%BD%E3%82%92%E7%B6%B2%E7%BE%85%EF%BC%81pyton%E3%81%8B%E3%82%89postgresql%E3%82%92%E6%89%B1%E3%81%86/
# https://qiita.com/kg1/items/597684fc1b98ca686a5d

#あとで並列にリクエストを処理できるようにする
# https://qiita.com/5zm/items/251be97d2800bf67b1c6


@app.after_request
def after_request(response):
    allowed_origins = ["http://localhost:5173", "https://localhost:5173/select/data", "https://localhost:5173", "http://localhost"]
    origin = request.headers.get('Origin')
    if origin in allowed_origins:
        logger.info("アクセスが許可されています" + origin)
        response.headers.add('Access-Control-Allow-Origin', origin)
    response.headers.add('Access-Control-Allow-Headers', 'Content-Type')
    response.headers.add('Access-Control-Allow-Headers', 'Authorization')
    response.headers.add('Access-Control-Allow-Methods', 'GET, POST, OPTIONS')
    response.headers.add('Access-Control-Allow-Credentials', 'true')
    return response

@app.route("/tmp", methods=["GET"])
def get_tmp():
    print("tmp_select")
    db = ExecuteSQL(pool)
    try:
        sql = f"""
                INSERT INTO "fridge_system".user_table
                (name_user, mail)
                    VALUES (%s, %s);    
        """
        db.execute_query(sql, bind_var=("nova-tarou", "25"))
        db.commit()
        db.__del__
    except Exception as e:
        print(e)
        db.rollback()
        db.__del__
        print("ロールバックを実行しました。")
        return jsonify({'status':300, 'data':3})



@app.route("/get/units", methods=["GET", "POST"])
def get_units_table():
    print("tmp_select")
    db = ExecuteSQL(pool)
    try:
        sql = f"""
            SELECT
                id_unit, name_unit
	        FROM "fridge_system".unit_table;
        """
        list_units = db.execute_query(sql)
        print("unitテーブル取得結果", list_units)
        db.commit()
        db.__del__
        return jsonify({'status':200, 'units':list_units})
    except Exception as e:
        print(e)
        db.rollback()
        db.__del__
        print("ロールバックを実行しました。")
        return jsonify({'status':300, 'data':3})

@app.route("/select/data", methods=["GET", "POST"])
def get_table_data():
    try:
        request_data = request.get_json()
        print("request_data", request_data)
        table = request_data["table"]
        columns = request_data["columns"]
        print("テーブル名", table)
    except Exception as e:
        print(e)
        print("リクエストの取得に失敗しました。")
    
    db = ExecuteSQL(pool)
    
    try:
        list_units = db.execute_query_column(table=table, bind_var=tuple(columns))
        print("unitテーブル取得結果", list_units)
        db.commit()
        db.__del__
        return jsonify({'status':200, 'data':list_units})
    except Exception as e:
        print(e)
        db.rollback()
        db.__del__
        print("ロールバックを実行しました。")
        return jsonify({'status':300, 'data':3})
        
        
    
@app.route("/register/recipe", methods=["POST"])
def register_recipe():
# {
#     name_recipe: '肉じゃが', 
#     serving_size: 3, 
#     method: '感覚的', 
#     ingredient_alredy_exist: [{id_ingredient: 1, num: 2, id_unit: 3, id_genre: 4},{id_ingredient: 2, num: 2, id_unit: 1, id_genre: 1}], 
#     ingredient_not_exist: {ingredient_name: 'しょうゆ', num: 2, id_unit: 2, id_genre: 5}
# }
#nextvalのシーケンスの払い出しはロールバックしても戻らない。そのため、ロールバックすると主キーの番号が飛び飛びになる
    print("レシピ登録")
    try:
        request_data = request.get_json()
        print("request_data", request_data)
        name_recipe = request_data["name_recipe"]
        serving_size = request_data["serving_size"]
        method = request_data["method"]
        list_ingredient_alredy_exist = request_data["ingredient_alredy_exist"]
        list_ingredient_not_exist= request_data["ingredient_not_exist"]
    except Exception as e:
        print(e)
        print("リクエストの取得に失敗しました。")
    try:
        db = ExecuteSQL(pool)
        
        
        if len(list_ingredient_not_exist) != 0:
            #材料テーブルに新規データを挿入するとき
            #材料テーブルの新規シーケンス番号を挿入レコード分取得
            sqls = ["SELECT nextval('fridge_system.id_ingredient_id_ingredient_seq');"] * len(list_ingredient_not_exist)
            nextvals = db.execute_multiple_query(sqls=sqls)
            print("取得したnextvals", nextvals)

            print("追加材料",list_ingredient_not_exist)
            sqls = []
            for index, ingredient in enumerate(list_ingredient_not_exist):
                #db.execute_non_query("""LOCK TABLE "fridge_system".ingredient_table ROW EXCLUSIVE""")
                
                nextval_ingredient = nextvals[index]["nextval"]
                list_ingredient_not_exist[index]["id_ingredient"] = nextval_ingredient
                sql = SQL("""INSERT INTO {schema}.{table}
                            (id_ingredient, name_ingredient, fk_id_unit, fk_id_genre)VALUES
                            ({id_ingredient}, {name_ingredient}, {fk_id_unit}, {fk_id_genre})""").format(
                                schema=Identifier("fridge_system"),
                                table = Identifier("ingredient_table"),
                                id_ingredient = Literal(nextval_ingredient),
                                name_ingredient = Literal(ingredient["ingredient_name"]),
                                fk_id_unit = Literal(ingredient["id_unit"]),
                                fk_id_genre = Literal(ingredient["id_genre"])
                )
                print("SQL作成", sql)
                sqls.append(sql)
            db.execute_multiple_non_query(sqls=sqls)

        #レシピ登録
        sql = "SELECT nextval('fridge_system.recipe_table_id_recipe_seq');"
        list_nextval_scalor = db.execute_query(sql=sql)
        nextval_recipe = list_nextval_scalor[0]["nextval"]
        sql = SQL("""INSERT INTO {schema}.{table}
                    (id_recipe, name_recipe, serving_size, method)VALUES
                    ({id_recipe}, {name_recipe}, {serving_size}, {method})""").format(
                        schema=Identifier("fridge_system"),
                        table = Identifier("recipe_table"),
                        id_recipe = Literal(nextval_recipe),#単一の値を取得するsqlメソッドをあとで作成
                        name_recipe = Literal(name_recipe),
                        serving_size = Literal(serving_size),
                        method = Literal(method)
        )
        print("レシピ登録SQL", sql.as_string)
        db.execute_non_query(sql=sql)


        #レシピと材料テーブルにデータ登録
        list_ingredient = list_ingredient_alredy_exist + list_ingredient_not_exist
        for ingredient in list_ingredient:
            sqls = []
            sql = SQL("""INSERT INTO {schema}.{table}(
                        fk_id_recipe, fk_id_ingredient, amount)
                        VALUES({fk_id_recipe}, {fk_id_ingredient}, {amount})""").format(
                            schema=Identifier("fridge_system"),
                            table = Identifier("recipe_ingredient_table"),
                            fk_id_recipe = Literal(nextval_recipe),
                            fk_id_ingredient = Literal(ingredient["id_ingredient"]),
                            amount = Literal(ingredient["num"]),
            )
            sqls.append(sql)
            db.execute_multiple_non_query(sqls=sqls)
        
        db.commit()
        return jsonify({'status':200})

    except Exception as e:
        print(e)
        db.rollback()
        db.__del__
        print("ロールバックを実行しました。")
        return jsonify({'status':300})
    
@app.route("/get/ingredients/from/recipe", methods=["POST"])
def getRecipeingredients():
    try:
        request_data = request.get_json()
        print("request_data", request_data)
        id_recipe = request_data["id_recipe"]

    except Exception as e:
        print(e)
        print("リクエストの取得に失敗しました。")
    
    db = ExecuteSQL(pool)

    try:
        print("レシピ材料テーブルから材料IDを取得")
        sql_values = {"schema":"fridge_system", "id_recipe":str(id_recipe)}
        sql = SqlCreator.get_query_from_file("getRecipeIngredients.sql", sql_values)
        list_recipe_detail = db.execute_query(sql)
        print("レシピ詳細取得結果", list_recipe_detail)
        return jsonify({'status':200, 'data':list_recipe_detail})
    
    except Exception as e:
        print(e)
        db.rollback()
        db.__del__
        print("ロールバックを実行しました。")
        return jsonify({'status':300})


def connect_postgresql():
        # コンフィグファイルからデータを取得
        # config_db = configparser.ConfigParser()
        # config_ini_path = "./config/dbconfig.ini"

        # # 指定したiniファイルが存在しない場合、エラー発生
        # if not os.path.exists(config_ini_path):
        #     raise FileNotFoundError(errno.ENOENT, os.strerror(errno.ENOENT), config_ini_path)
        # config_db.read(config_ini_path)
        pool = psycopg2.pool.SimpleConnectionPool(
            minconn=2,
            maxconn=6,
            user = os.environ.get("db_user"),
            password = os.environ.get("db_password"),
            host = os.environ.get("host"),
            port = os.environ.get("db_port"),
            dbname = os.environ.get("db_name")
        )
        print("プール作成")
        logger.info("デバック出力成功") 
        return pool

pool = connect_postgresql()


if __name__== '__main__':
      #特定のオリジンだけを許可する
      #cors = CORS(app, resources={r"/*":{"origin": ["http://localhost:5173", "https://localhost:5173"]}})
      #app.run(host='0.0.0.0', port=3334, debug=True, threaded=True, ssl_context=('network/server.crt', 'network/server.key'))
      #app.run(debug=True, threaded=True, ssl_context=('network/server.crt', 'network/server.key'))
      app.run(debug=True, threaded=True)
