import psycopg2
import psycopg2.extras
from psycopg2.sql import Identifier
from psycopg2.sql import SQL
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
        self.pool = pool
        self.connection = self.pool.getconn()
        self.cursor = self.connection.cursor(cursor_factory=psycopg2.extras.DictCursor)
        #self.cursor = self.con.cursor(cursor_factory=psycopg2.extras.DictCursor)
    def execute_non_query(self, sql: str, bind_var: tuple = None) -> None:
        """CREATE/INSERT/UPDATE/DELETEのSQL実行メソッド
        :param sql: 実行SQL
        :param bind_var: バインド変数
        :return: None
        """
        # SQLの実行
        print(sql)
        if bind_var is None:
            self.cursor.execute(sql)
        else:
            # バインド変数がある場合は指定して実行
            self.cursor.execute(sql, bind_var)

    def execute_multiple_non_query(self, sqls: list, bind_var: list = None) -> None:
        """CREATE/INSERT/UPDATE/DELETEのSQL実行メソッド
        :param sql: 実行SQL
        :param bind_var: バインド変数
        :return: None
        """
        print("MULTIPLE SQL", sqls)
        for sql in sqls:
            # SQLの実行
            print(sql)
            self.cursor.execute(sql)

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
            print(bind_var)
            bind_var = [Identifier(bind) for bind in bind_var]
            print(bind_var)
            self.cursor.execute(sql.format(bind_var))
        result = []
        if count == 0:
            rows = self.cursor.fetchall()
            print("rows2", rows)
            for row in rows:
                result.append(dict(row))
        else:
            # 件数指定がある場合はその件数分を取得する
            rows = self.cursor.fetchmany(count)
            for row in rows:
                result.append(dict(row))
        return result
    
    def execute_multiple_query(self, sqls: list) -> list:
        """SELECTのSQL実行メソッド
        :param sql: 実行SQL
        :param bind_var: バインド変数
        :param count: データ取得件数
        :return: 結果リスト
        """
        result = []
        # SQLの実行
        for sql in sqls:
            print(sql)
            self.cursor.execute(sql)



            rows = self.cursor.fetchall()
            print("rows", rows)
            if len(rows) >= 1:
                #取得結果が0件だったり、INSERTなど返却値がないSQLを発行したときは結果リストへの格納を行わない
                for row in rows:
                    print(row)
                    result.append(dict(row))
            
        return result

    def execute_query_column(self, table: str, bind_var: tuple = None,  count: int = 0) -> list:
        #https://qiita.com/RjChiba/items/0685111a65c31c427680
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
            sql = SQL("SELECT {field} FROM {schema}.{table}").format(
                field = SQL(',').join([Identifier(bind) for bind in bind_var]),
                schema = Identifier('fridge_system') ,
                table = Identifier(table)
            )
            print(sql.as_string(self.connection))
            # バインド変数がある場合は指定して実行
            self.cursor.execute(sql)
        result = []
        if count == 0:
            rows = self.cursor.fetchall()
            print("rows2", rows)
            for row in rows:
                result.append(dict(row))
        else:
            # 件数指定がある場合はその件数分を取得する
            rows = self.cursor.fetchmany(count)
            for row in rows:
                result.append(dict(row))
        return result
    
    def get_next_sequence(self, sequence):
        """次のシーケンス番号を吐き出す。シーケンス番号を確認するsqlではないので注意。
        :return: number
        """
        sql = SQL("SELECT nextval({schema}.{sequence}')").format(
            schema = Identifier('fridge_system'),
            sequence = Identifier(sequence)
        )
        print(sql.as_string(self.connection))
        self.cursor.execute(sql)
        nextval = self.cursor.fetchall()
        return nextval
    
    def commit(self) -> None:
        """コミット
        :return: None
        """
        self.connection.commit()
    def rollback(self) -> None:
        """ロールバック
        :return: None
        """
        self.con.rollback()
    def __del__(self) -> None:
        """デストラクタ DBとのセッションを切断する
        :return: None
        """
        self.cursor.close()
        self.connection.close()
        self.pool.putconn(self.connection)