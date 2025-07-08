import uuid

import duckdb
import os
from pathlib import Path


class DuckDBSession:
    """
    DuckDB 会话管理器，用于执行 SQL 查询与数据操作
    支持从 CSV 加载数据，执行 SQL 脚本，导出结果
    """

    def __init__(self, environment="dev"):
        """
        初始化 DuckDB 会话

        :param db_path: DuckDB 数据库存储路径，默认为 data/main.db
        """

        db_path = Path(__file__).parent.parent.parent.parent / "data" / "main.db"
        os.makedirs(db_path.parent, exist_ok=True)
        self.__conn = duckdb.connect(str(db_path))

    def load_csv(self, file_path, table_name, timestamp_format, specified_types: dict = None, ignore_errors=True,
                 nullstr=None):
        """
        将 CSV 文件加载到 DuckDB 中

        :param timestamp_format:
        :param ignore_errors: 是否忽略错误
        :param specified_types: 指定列类型
        :param file_path: CSV 文件路径
        :param table_name: 生成表名
        """
        # 构造类型声明
        column_clause = ""
        if specified_types:
            columns_str = ", ".join([f"'{col}':'{dtype}'" for col, dtype in specified_types.items()])
            column_clause = f", COLUMNS={{ {columns_str} }}"

        # 忽略错误声明
        reject_clause = null_clause = ""
        if ignore_errors:
            reject_clause = ", store_rejects = true"
        if nullstr is not None:
            null_clause = f", nullstr='{nullstr}'"
        # 构建 SQL 语句
        sql = f"""
            CREATE TABLE IF NOT EXISTS {table_name} AS 
            SELECT * FROM read_csv_auto('{file_path}', timestampformat='{timestamp_format}', header=True{null_clause}{column_clause}{reject_clause})
        """

        self.__conn.execute(sql)

    def load_database(self, db, query_template, table_name):
        """
        MySQL/PGSQL数据 加载到 DuckDB 中
        """
        if not db['type'] in ['mysql', 'postgres']:
            raise ValueError(f"不支持的数据库类型：{db['type']}")

        self.__conn.execute(f"INSTALL {db['type']};")
        self.__conn.execute(f"LOAD {db['type']};")

        # 生成唯一别名
        external_db_alias = f"external_db_{uuid.uuid4().hex}"  # 使用 UUID 避免冲突

        # 构建 连库SQL 语句
        attach_sql = (f"ATTACH 'dbname={db['database']} "
                      f"user={db['user']} password={db['password']} "
                      f"host={db['host']} port={db['port']}' "
                      f"AS {external_db_alias} (TYPE {db['type']}, READ_ONLY);")
        self.__conn.execute(attach_sql)

        # 替换查询模板中的别名占位符
        actual_query = query_template.replace("${external_db}", external_db_alias)

        # 构建 建表SQL 语句
        sql = f"""
            CREATE TABLE IF NOT EXISTS {table_name} AS 
            FROM ({actual_query});
        """
        return self.__conn.execute(sql)

    def execute_sql(self, sql):
        """
        执行 SQL 查询并返回结果

        :param sql: SQL 查询语句
        """
        return self.__conn.execute(sql)

    def register_table(self, table_object, table_name):
        """
        将 pandas Dataframe/pyArrow Table 注册为 DuckDB 表

        :param table_object: pandas Dataframe/pyArrow Table
        :param table_name: 表名
        """
        self.__conn.register(table_name, table_object)

    def persist_table(self, source_table_name, target_table_name):
        """
        将A表复制到B表
        """
        self.__conn.execute(f"CREATE OR REPLACE TABLE {target_table_name} AS SELECT * FROM {source_table_name}")

    def save_table(self, table_object, table_name):
        """
        把数据存入 DuckDB 表
        """
        self.register_table(table_object, "temp_df")
        self.persist_table("temp_df", table_name)

    def execute_sql_file(self, file_path):
        """
        执行 SQL 脚本文件

        :param file_path: SQL 文件路径
        """
        with open(file_path, 'r', encoding='utf-8') as f:
            sql_script = f.read()
        return self.__conn.execute(sql_script)

    def extract_table(self, table_name):
        """
        执行 SQL 脚本文件

        :param file_path: SQL 文件路径
        """
        return self.__conn.execute(f"SELECT * FROM {table_name}").df()

    def close(self):
        """
        关闭 DuckDB 连接
        """
        self.__conn.close()
