from dataclasses import dataclass, asdict
from typing import Type, Dict, TypeVar, List, Any

import pyarrow
from duckdb.duckdb import DuckDBPyRelation

from src.core.duckdb.duckdb_engine import DuckDBSession

# 泛型定义
T = TypeVar('T')


def rows_into_model_dict(db_relation: DuckDBPyRelation, model_class: Type[T]) -> Dict[Any, T]:
    """
    将查询结果映射为指定类型的对象字典

    :param db_relation: DuckDB 连接对象
    :param model_class: 映射的目标类（需为 dataclass）
    :return: 对象字典
    """
    model_rows = db_relation.fetchall()
    if model_class in {str, int}:
        return {r[0]: r[1] for r in model_rows}
    else:
        return {r[0]: model_class(*r) for r in model_rows}


def rows_into_model_list(db_relation: DuckDBPyRelation, model_class: Type[T]) -> List[T]:
    """
    将查询结果映射为指定类型的对象列表

    :param db_relation: DuckDB 连接对象
    :param model_class: 映射的目标类（需为 dataclass）
    :return: 对象列表
    """
    model_rows = db_relation.fetchall()
    if model_class in {str, int}:
        return [r[1] for r in model_rows]
    return [model_class(*r) for r in model_rows]


def sync_dict_to_duckdb(data_dict: dict[int | str, str], table_name: str, duckdb_session: DuckDBSession,
                        pk_column: str = "id",
                        overwrite: bool = False):
    """
    将实体类列表同步到 DuckDB 表中

    :param pk_column: 主键
    :param overwrite: 是否覆盖
    :param data_dict: 实体类对象列表（支持 dataclass 或 pydantic 模型）
    :param table_name: DuckDB 中目标表名
    :param duckdb_session: 已有的 DuckDB 会话实例
    """
    if not data_dict:
        return
    if overwrite:
        duckdb_session.save_table(data_dict, table_name)
    else:
        duckdb_session.upsert_table(data_dict, table_name, pk_column)


def sync_list_to_duckdb(items: List[dataclass], table_name: str, duckdb_session: DuckDBSession,
                        pk_column: str = "id",
                        overwrite: bool = True):
    """
    将实体类列表同步到 DuckDB 表中

    :param pk_column: 主键
    :param overwrite: 是否覆盖
    :param items: 实体类对象列表（支持 dataclass 或 pydantic 模型）
    :param table_name: DuckDB 中目标表名
    :param duckdb_session: 已有的 DuckDB 会话实例
    """
    if not items:
        return

    # 转换为字典列表
    df = pyarrow.Table.from_pylist([asdict(item) for item in items])
    if overwrite:
        duckdb_session.save_table(df, table_name)
    else:
        duckdb_session.upsert_table(df, table_name, pk_column)
