from dataclasses import asdict, dataclass
from functools import partial
from typing import List, TypeVar, Callable, Type
import pyarrow as pa
import httpx
import anyio

from src.core.duckdb.duckdb_engine import DuckDBSession
from src.models.meta.artifact_info import ArtifactInfo
from src.models.meta.artifact_set_info import ArtifactSetInfo
from src.models.meta.character_info import CharacterInfo
from src.models.meta.weapon_info import WeaponInfo
from src.service.hakush.api import HakushApi
from src.service.hakush.parser import HakushParser
from src.util.http_util import fetch_http_json, fetch_local_json
from src.util.logger import logger

T = TypeVar("T")


async def sync_generic(
        client: httpx.AsyncClient,
        url_getter: Callable[[], str],
        parser: Callable[[dict], List[T]],
        table_name: str,
        model_class: Type[T],
        use_local: bool = True,
        local_file_path: str = None):
    """
    通用同步函数，用于同步武器/角色等基础数据到 DuckDB

    :param client: HTTP 客户端
    :param url_getter: 获取 API 地址的函数
    :param parser: 数据解析函数
    :param table_name: DuckDB 表名
    :param model_class: 对象类型
    :param use_local: 是否使用本地文件替代网络请求
    :param local_file_path: 本地文件路径（如果 use_local=True）
    """
    url = url_getter()

    # 判断是否使用本地文件
    if use_local and local_file_path:
        raw_data = await fetch_local_json(local_file_path)
    else:
        raw_data = await fetch_http_json(client, url)

    if not raw_data:
        logger.error(f"无法获取 {model_class} 数据，请检查网络连接是否正确")
        return

    duckdb_session = DuckDBSession()
    items = None
    try:
        items = parser(raw_data)
    except Exception as e:
        logger.error(f"解析 {model_class} 数据失败: {e}")
    if items:
        try:
            sync_duckdb(items, table_name, duckdb_session)
        except Exception as e:
            logger.error(f"{table_name} 写入数据失败: {e}")


async def sync_weapon(client: httpx.AsyncClient):
    await sync_generic(
        client=client,
        url_getter=HakushApi.get_weapon_list_url,
        parser=HakushParser.parse_weapon_infos,
        table_name="ods_weapon_info",
        model_class=WeaponInfo,
        use_local=True,
        local_file_path="test/hakush/json/weapon.json"
    )


async def sync_artifact_set(client: httpx.AsyncClient):
    await sync_generic(
        client=client,
        url_getter=HakushApi.get_artifact_set_list_url,
        parser=HakushParser.parse_artifact_set_infos,
        table_name="ods_artifact_set_info",
        model_class=ArtifactSetInfo,
        use_local=True,
        local_file_path="test/hakush/json/artifact.json"
    )
    set_id = 15003
    await sync_generic(
        client=client,
        url_getter=lambda: HakushApi.get_artifact_set_single_url(set_id, 'zh'),
        parser=HakushParser.parse_artifact_set_info_single,
        table_name="ods_artifact_info",
        model_class=ArtifactInfo,
        use_local=True,
        local_file_path=f"test/hakush/json/artifact-{set_id}.json"
    )


async def sync_character(client: httpx.AsyncClient):
    await sync_generic(
        client=client,
        url_getter=HakushApi.get_character_list_url,
        parser=HakushParser.parse_character_infos,
        table_name="ods_character_info",
        model_class=CharacterInfo,
        use_local=True,
        local_file_path="test/hakush/json/character.json"
    )


def sync_duckdb(items: List[dataclass], table_name: str, duckdb_session: DuckDBSession):
    """
    将实体类列表同步到 DuckDB 表中

    :param items: 实体类对象列表（支持 dataclass 或 pydantic 模型）
    :param table_name: DuckDB 中目标表名
    :param duckdb_session: 已有的 DuckDB 会话实例
    """
    if not items:
        return

    # 转换为字典列表
    df = pa.Table.from_pylist([asdict(item) for item in items])
    duckdb_session.save_table(df, table_name)


async def main():
    async with httpx.AsyncClient(proxy="http://127.0.0.1:4081") as client:
        async with anyio.create_task_group() as tg:
            tg.start_soon(sync_weapon, client)
            tg.start_soon(sync_character, client)
            tg.start_soon(sync_artifact_set, client)
