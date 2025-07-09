from typing import Type, Dict, TypeVar, List

from duckdb import DuckDBPyConnection

# 泛型定义
T = TypeVar('T')


def rows_into_model_dict(dbc: DuckDBPyConnection, model_class: Type[T]) -> Dict[int, T]:
    """
    将查询结果映射为指定类型的对象字典

    :param dbc: DuckDB 连接对象
    :param model_class: 映射的目标类（需为 dataclass）
    :return: 对象字典
    """
    model_rows = dbc.fetchall()
    return {r[0]: model_class(*r) for r in model_rows}


def rows_into_model_list(dbc: DuckDBPyConnection, model_class: Type[T]) -> List[T]:
    """
    将查询结果映射为指定类型的对象列表

    :param dbc: DuckDB 连接对象
    :param model_class: 映射的目标类（需为 dataclass）
    :return: 对象列表
    """
    model_rows = dbc.fetchall()
    return [model_class(*r) for r in model_rows]