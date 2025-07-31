import json
from dataclasses import dataclass, asdict
from typing import Type, Dict, TypeVar, List, Any, get_type_hints

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
        result_dict = {}
        # 处理一阶字典，从json反序列化为dict
        column_names = db_relation.columns
        type_hints = get_type_hints(model_class)
        for row in model_rows:
            row_cp = list(row)
            for col, t in type_hints.items():
                if 'dict' in str(t):
                    index = column_names.index(col)
                    row_cp[index] = json.loads(row[index])
            result_dict[row[0]] = model_class(*row_cp)
        return result_dict


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
    else:
        result_list = []
        # 处理一阶字典，从json反序列化为dict
        column_names = db_relation.columns
        type_hints = get_type_hints(model_class)
        for row in model_rows:
            for k, v in type_hints.items():
                if 'dict' in str(v):
                    index = column_names.index(k)
                    row[index] = json.loads(row[index])
            result_list.append(model_class(*row))
        return result_list


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

    # 处理一阶字典，序列化为json存储
    pylist = []
    for item in items:
        pdict = asdict(item)
        for k, v in pdict.items():
            if isinstance(v, dict):
                pdict[k] = json.dumps(v, ensure_ascii=False)
        pylist.append(pdict)

    # 转换为字典列表
    pt = pyarrow.Table.from_pylist(pylist)
    if overwrite:
        duckdb_session.save_table(pt, table_name)
    else:
        duckdb_session.upsert_table(pt, table_name, pk_column)
