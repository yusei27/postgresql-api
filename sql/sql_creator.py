from psycopg2.sql import Identifier
from psycopg2.sql import SQL

import os
class SqlCreator:
    """
    SQL文を作成するクラス
    """

    def select_query(table: str, columns:list):
        query = "SELECT"
        sql = SQL("SELECT {field} FROM {schema}.{table}").format(
        field = SQL(',').join([Identifier(column) for column in columns]),
        schema = Identifier('fridge_system') ,
        table = Identifier(table)
    )
    
    def get_query_from_file(filename: str, dict_values:dict):
        print(dict_values)
        #filepath = "./sql/sql_extensiosn/" + filename
        with open("./sql/sql_extension/" + filename, "r") as f:
            print("@@@@@@@", f.read().format(dict_values))
        return