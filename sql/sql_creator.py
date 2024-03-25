from psycopg2.sql import Identifier
from psycopg2.sql import SQL

class SqlCreator:
    """
    SQL文を作成するクラス
    """

    def select_query(table: str, columns:list):
        query = "SELECT"
        sql = SQL("SELECT {field} FROM {schema}.{table}").format(
        field = SQL(',').join([Identifier(bind) for bind in bind_var]),
        schema = Identifier('fridge_system') ,
        table = Identifier(table)
    )