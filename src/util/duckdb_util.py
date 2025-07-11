from typing import Type, Dict, TypeVar, List, Any

from duckdb import DuckDBPyConnection
from duckdb.duckdb import DuckDBPyRelation

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
    return {r[0]: model_class(*r) for r in model_rows}


def rows_into_model_list(db_relation: DuckDBPyRelation, model_class: Type[T]) -> List[T]:
    """
    将查询结果映射为指定类型的对象列表

    :param db_relation: DuckDB 连接对象
    :param model_class: 映射的目标类（需为 dataclass）
    :return: 对象列表
    """
    model_rows = db_relation.fetchall()
    return [model_class(*r) for r in model_rows]