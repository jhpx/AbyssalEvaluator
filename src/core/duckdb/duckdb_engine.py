import os
import uuid
from pathlib import Path
from typing import Any, Dict

import duckdb


class DuckDBSession:
    """
    DuckDB 会话管理器，用于执行 SQL 查询与数据操作
    支持从 CSV 加载数据，执行 SQL 脚本，导出结果
    """

    def __init__(self, environment: str = "dev"):
        """
        初始化 DuckDB 会话

        :param environment: 环境标识符，默认为 dev
        """
        db_path = Path(__file__).parent.parent.parent.parent / "data" / "main.db"
        os.makedirs(db_path.parent, exist_ok=True)
        self.__conn = duckdb.connect(str(db_path))

    def load_csv(self,
                 file_path: str | Path,
                 table_name: str,
                 timestamp_format: str,
                 specified_types: Dict[str, str] = None,
                 ignore_errors: bool = True,
                 nullstr: str = None) -> duckdb.DuckDBPyConnection:
        """
        将 CSV 文件加载到 DuckDB 中

        :param file_path: CSV 文件路径
        :param table_name: 目标表名
        :param timestamp_format: 时间戳格式
        :param specified_types: 指定列类型
        :param ignore_errors: 是否忽略错误
        :param nullstr: NULL 值字符串
        :return: DuckDB 连接对象
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

        return self.__conn.execute(sql)

    def load_database(self,
                      db: Dict[str, Any],
                      query_template: str,
                      table_name: str) -> duckdb.DuckDBPyConnection:
        """
        MySQL/PGSQL 数据加载到 DuckDB 中

        :param db: 数据库连接信息字典
        :param query_template: 查询模板
        :param table_name: 目标表名
        :return: DuckDB 连接对象
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

    def register_table(self, table_object: Any, table_name: str) -> duckdb.DuckDBPyConnection:
        """
        将 pandas Dataframe/pyArrow Table 注册为 DuckDB 表

        :param table_object: pandas DataFrame 或 pyArrow Table
        :param table_name: 表名
        :return: DuckDB 连接对象
        """
        return self.__conn.register(table_name, table_object)

    def persist_table(self, source_table_name: str, target_table_name: str,
                      pk_column: str = "id") -> duckdb.DuckDBPyConnection:
        """
        将A表复制到B表

        :param source_table_name: 源表名
        :param target_table_name: 目标表名
        :return: DuckDB 连接对象
        """
        self.__conn.execute(
            f"CREATE OR REPLACE TABLE {target_table_name} AS SELECT * FROM {source_table_name}")
        try:
            self.__conn.execute(f"ALTER TABLE {target_table_name} ADD PRIMARY KEY ({pk_column})")
        except duckdb.CatalogException:
            pass
        return self.__conn

    def table_exists(self, table_name: str) -> bool:
        """
        检查表是否存在

        :param table_name: 表名
        :return: 表是否存在
        """
        result = self.__conn.execute(
            f"SELECT EXISTS(SELECT 1 FROM information_schema.tables WHERE table_name='{table_name}')").fetchone()
        return result[0]

    def primary_key_exists(self, table_name: str) -> bool:
        result = self.__conn.execute(f"PRAGMA table_info('{table_name}')").fetchall()
        for col in result:
            if len(col) >= 6 and col[5] == 1:  # 第6列是 'pk' 字段
                return True
        return False

    def save_table(self, table_object: Any, table_name: str) -> duckdb.DuckDBPyConnection:
        """
        把数据覆盖存入 DuckDB 表

        :param table_object: pandas DataFrame 或 pyArrow Table
        :param table_name: 表名
        :return: DuckDB 连接对象
        """
        self.register_table(table_object, "temp_df")
        return self.persist_table("temp_df", table_name)

    def upsert_table(self, table_object: Any, table_name: str, pk_column: str) -> duckdb.DuckDBPyConnection:
        """
        把数据追加存入 DuckDB 表

        :param pk_column:
        :param table_object: pandas DataFrame 或 pyArrow Table
        :param table_name: 表名
        :return: DuckDB 连接对象
        """
        self.register_table(table_object, "temp_df")
        if self.table_exists(table_name):
            if not self.primary_key_exists(table_name):
                self.__conn.execute(f"ALTER TABLE {table_name} ADD PRIMARY KEY ({pk_column})")
            return self.__conn.execute(
                f"INSERT INTO {table_name} SELECT * FROM temp_df ON CONFLICT({pk_column}) DO NOTHING")
        else:
            return self.persist_table("temp_df", table_name, pk_column)

    def execute_sql(self, sql: str, parameters=None) -> duckdb.DuckDBPyConnection:
        """
        执行 SQL 查询并返回结果

        :param parameters:
        :param sql: SQL 查询语句
        :return: DuckDB 连接对象
        """
        return self.__conn.execute(sql, parameters)

    def execute_sql_file(self, file_path: str | Path) -> duckdb.DuckDBPyConnection:
        """
        执行 SQL 脚本文件

        :param file_path: SQL 文件路径
        :return: DuckDB 连接对象
        """
        with open(file_path, 'r', encoding='utf-8') as f:
            sql_script = f.read()
        return self.__conn.execute(sql_script)

    def extract_table(self, table_name: str) -> duckdb.DuckDBPyRelation:
        """
        执行 SQL 查询以提取表内容

        :param table_name: 表名
        :return: DuckDB 连接对象
        """
        if self.table_exists(table_name):
            return self.__conn.table(table_name)
        else:
            return self.__conn.sql("SELECT 1 WHERE 1<>1")

    def sql(self, sql, *args, **kwargs) -> duckdb.DuckDBPyRelation:
        """
        执行 SQL 查询并返回结果
        :param sql: SQL 查询语句
        :return: DuckDB 连接对象
        """
        return self.__conn.sql(sql, *args, **kwargs)

    def close(self) -> None:
        """
        关闭 DuckDB 连接
        """
        self.__conn.close()
