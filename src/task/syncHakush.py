from dataclasses import asdict, dataclass
from typing import List
import pyarrow as pa
import httpx
import anyio

from src.core.duckdb.duckdb_engine import DuckDBSession
from src.service.hakush.api import HakushApi
from src.service.hakush.parser import HakushParser
from src.util.http_util import fetch_http_json, fetch_local_json
from src.util.logger import logger


async def sync_weapon(client: httpx.AsyncClient):
    url = HakushApi.get_weapon_list_url()
    # raw_data = await fetch_http_json(client, url)
    raw_data = await fetch_local_json(
        "F:\\Workspace-Private\\workspace-python\\DataProcess\\AbyssalEvaluator\\test\\hakush\\json\\weapon.json")

    if not raw_data:
        logger.error(f"无法获取武器数据，请检查网络连接是否正确")
        return

    duckdb_session = DuckDBSession()
    weapon_list = []
    try:
        weapon_list = HakushParser.parse_weapon_infos(raw_data)
    except Exception as e:
        logger.error(f"解析武器数据失败: {e}")

    sync_duckdb(weapon_list, "ods_weapon_info", duckdb_session)

    pass


async def sync_artifact(client: httpx.AsyncClient):
    pass


async def sync_character(client: httpx.AsyncClient):
    url = HakushApi.get_character_list_url()
    # raw_data = await fetch_http_json(client, url)
    raw_data = await fetch_local_json(
        "F:\\Workspace-Private\\workspace-python\\DataProcess\\AbyssalEvaluator\\test\\hakush\\json\\character.json")

    if not raw_data:
        logger.error(f"无法获取角色数据，请检查网络连接是否正确")
        return

    duckdb_session = DuckDBSession()
    character_list = []
    try:
        character_list = HakushParser.parse_character_infos(raw_data)
    except Exception as e:
        logger.error(f"解析角色数据失败: {e}")

    sync_duckdb(character_list, "ods_character_info", duckdb_session)
    pass

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
            tg.start_soon(sync_artifact, client)
            tg.start_soon(sync_character, client)


if __name__ == "__main__":
    anyio.run(main)
