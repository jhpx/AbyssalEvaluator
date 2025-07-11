from dataclasses import asdict, dataclass
from typing import List, TypeVar, Callable

import anyio
import httpx
import pyarrow as pa

from src.core.duckdb.duckdb_engine import DuckDBSession
from src.models.meta.artifact_set_info import ArtifactSetInfo
from src.service.hakush.api import HakushApi
from src.service.hakush.parser import HakushParser
from src.util.duckdb_util import rows_into_model_list
from src.util.http_util import fetch_and_parse
from src.util.logger import logger

T = TypeVar("T")

async def sync_generic(
        client: httpx.AsyncClient,
        url: str,
        parser: Callable[[dict], List[T]],
        table_name: str,
        use_local: bool = True,
        local_file_path: str = None):
    """
    通用同步函数，用于同步武器/角色等基础数据到 DuckDB

    :param client: HTTP 客户端
    :param url: API 地址
    :param parser: 数据解析函数
    :param table_name: DuckDB 表名
    :param use_local: 是否使用本地文件替代网络请求
    :param local_file_path: 本地文件路径（如果 use_local=True）
    """

    items = await fetch_and_parse(
        client=client,
        url=url,
        parser=parser,
        use_local=use_local,
        local_file_path=local_file_path
    )
    if items:
        duckdb_session = DuckDBSession()
        try:
            sync_duckdb(items, table_name, duckdb_session)
        except Exception as e:
            logger.error(f"{table_name} 写入数据失败: {e}")
        duckdb_session.close()
    return items


async def sync_multi_lang_generic(
        client: httpx.AsyncClient,
        langs: List[str],
        url_resolver: Callable[[str], str],
        parser: Callable[[dict, str], List[T]],
        table_name: str,
        pk_column: str = "id",
        use_local: bool = True,
        file_path_resolver: Callable[[str], str] = None,
):
    """
    通用同步多语言资源的方法，适用于圣遗物、武器、角色等需要多语言合并的数据。

    :param pk_column: 主键
    :param client: HTTP 客户端
    :param langs: 需要同步的语言列表，如 ['zh', 'en', 'ja', 'ko']
    :param url_resolver: 获取 API 地址的函数 (接受 lang)
    :param parser: 数据解析函数 (接受 raw_data, lang)
    :param table_name: DuckDB 表名
    :param use_local: 是否使用本地文件替代网络请求
    :param file_path_resolver: 本地文件路径生成器
    """

    # 默认 merger 函数为 identity
    result_items = []
    # 并行下载并解析所有语言的数据
    for lang in langs:
        url = url_resolver(lang)
        local_file_path = file_path_resolver(lang) if file_path_resolver else None
        result_items.extend(await fetch_and_parse(
            client=client,
            url=url,
            parser=lambda data: parser(data, lang),
            use_local=use_local,
            local_file_path=local_file_path
        ))

    # 写入数据库
    if result_items:
        duckdb_session = DuckDBSession()
        try:
            sync_duckdb(result_items, table_name, duckdb_session, f'{pk_column},lang', False)
        except Exception as e:
            logger.error(f"{table_name} 写入数据失败: {e}")
        duckdb_session.close()
    return result_items


async def sync_weapon(client: httpx.AsyncClient):
    return await sync_generic(
        client=client,
        url=HakushApi.get_weapon_list_url(),
        parser=HakushParser.parse_weapon_infos,
        table_name="ods_weapon_info",
        use_local=True,
        local_file_path="test/hakush/json/weapon.json"
    )


async def sync_artifact_set(client: httpx.AsyncClient):
    await sync_generic(
        client=client,
        url=HakushApi.get_artifact_set_list_url(),
        parser=HakushParser.parse_artifact_set_infos,
        table_name="ods_artifact_set_info",
        use_local=True,
        local_file_path="test/hakush/json/artifact.json"
    )


async def sync_artifact_set_details(client: httpx.AsyncClient):
    duckdb_session = DuckDBSession()
    artifact_set_info_rows = duckdb_session.extract_table("ods_artifact_set_info")
    artifact_set_info_list = rows_into_model_list(artifact_set_info_rows, ArtifactSetInfo)
    duckdb_session.close()
    # 注意此处会强制同步大量网络数据，请谨慎使用
    for set_id in [item.id for item in artifact_set_info_list]:
        # await sync_artifact(client, set_id, False)
        pass


async def sync_artifact(client: httpx.AsyncClient, set_id, use_local: bool = True):
    return await sync_multi_lang_generic(
        client=client,
        langs=["zh", "en", "ja", "ko"],
        url_resolver=lambda lang: HakushApi.get_artifact_set_single_url(set_id, lang),
        parser=HakushParser.parse_artifact_set_info_single,
        table_name="ods_artifact_info",
        pk_column='icon',
        use_local=use_local,
        file_path_resolver=lambda lang: f"test/hakush/json/artifact-{set_id}-{lang}.json"
    )


async def sync_character(client: httpx.AsyncClient):
    return await sync_generic(
        client=client,
        url=HakushApi.get_character_list_url(),
        parser=HakushParser.parse_character_infos,
        table_name="ods_character_info",
        use_local=True,
        local_file_path="test/hakush/json/character.json"
    )


def sync_duckdb(items: List[dataclass], table_name: str, duckdb_session: DuckDBSession,
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
    df = pa.Table.from_pylist([asdict(item) for item in items])
    if overwrite:
        duckdb_session.save_table(df, table_name)
    else:
        duckdb_session.upsert_table(df, table_name, pk_column)


async def main():
    async with httpx.AsyncClient(proxy="http://127.0.0.1:4081") as client:
        async with anyio.create_task_group() as tg:
            tg.start_soon(sync_weapon, client)
            tg.start_soon(sync_character, client)
            tg.start_soon(sync_artifact_set, client)
            tg.start_soon(sync_artifact_set_details, client)
