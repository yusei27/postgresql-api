import psycopg2
import psycopg2.extras
import configparser
import os
import errno

class ExecuteSQL:
    """
    Postgresqlにアクセスするための汎用クラス
    以下のサイトを参考に作成
    https://tech.nkhn37.net/python-psycopg2-postgresql-dbaccess/
    """
    def __init__(self, pool) -> None:
        """コンストラクタ
        :return: None
        """
        # カーソルを作成する
        connection = pool.get_connection()
        self.cursor = connection.cursor()
        #self.cursor = self.con.cursor(cursor_factory=psycopg2.extras.DictCursor)
    def execute_non_query(self, sql: str, bind_var: tuple = None) -> None:
        """CREATE/INSERT/UPDATE/DELETEのSQL実行メソッド
        :param sql: 実行SQL
        :param bind_var: バインド変数
        :return: None
        """
        # SQLの実行
        if bind_var is None:
            self.cursor.execute(sql)
        else:
            # バインド変数がある場合は指定して実行
            self.cursor.execute(sql, bind_var)
    def execute_query(self, sql: str, bind_var: tuple = None, count: int = 0) -> list:
        """SELECTのSQL実行メソッド
        :param sql: 実行SQL
        :param bind_var: バインド変数
        :param count: データ取得件数
        :return: 結果リスト
        """
        # SQLの実行
        if bind_var is None:
            print(sql)
            self.cursor.execute(sql)
        else:
            # バインド変数がある場合は指定して実行
            print(sql)
            self.cursor.execute(sql, bind_var)
        result = []
        if count == 0:
            rows = self.cursor.fetchall()
            for row in rows:
                result.append(dict(row))
        else:
            # 件数指定がある場合はその件数分を取得する
            rows = self.cursor.fetchmany(count)
            for row in rows:
                result.append(dict(row))
        return result
    def commit(self) -> None:
        """コミット
        :return: None
        """
        self.con.commit()
    def rollback(self) -> None:
        """ロールバック
        :return: None
        """
        self.con.rollback()
    def __del__(self) -> None:
        """デストラクタ
        :return: None
        """
        self.cursor.close()
        self.con.close()