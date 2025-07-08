from typing import Optional

from src.core.duckdb.duckdb_engine import DuckDBSession
from src.models.meta.character_info import CharacterInfo
from src.models.meta.weapon_info import WeaponInfo
from src.models.player import Player
from src.util.logger import logger
import httpx
import anyio

from src.service.enka.api import EnkaApi
from src.service.enka.parser import EnkaParser
from src.util.http_util import fetch_http_json, fetch_local_json


async def sync_player(client: httpx.AsyncClient, uid: str):
    """
    获取并解析玩家信息，输出到控制台

    :param client: httpx.AsyncClient 实例
    :param uid: 玩家 UID
    """
    url = EnkaApi.get_player_url(uid)

    # raw_data = await fetch_http_json(client, url)
    raw_data = await fetch_local_json(
        "F:\\Workspace-Private\\workspace-python\\DataProcess\\AbyssalEvaluator\\test\\enka\\json\\player.json")

    if not raw_data:
        logger.error(f"无法获取玩家数据（UID={uid}），请检查网络连接或UID是否正确")
        return

    player = None
    try:
        player = EnkaParser.parse_player(raw_data)
    except Exception as e:
        logger.error(f"解析玩家数据失败（UID={uid}）: {e}")

    if player:
        duckdb_session = DuckDBSession()
        # 关联角色
        character_info_rows = duckdb_session.extract_table("ods_character_info").fetchall()
        character_dict = {r[0]: CharacterInfo(*r) for r in character_info_rows}
        # 关联武器
        weapon_info_rows = duckdb_session.extract_table("ods_weapon_info").fetchall()
        weapon_dict = {r[0]: WeaponInfo(*r) for r in weapon_info_rows}

        for character in player.characters:
            weapon_info = weapon_dict.get(character.weapon.id)
            character_info = character_dict.get(character.avatarId)
            character.name = character_info.name_chs if character_info else "未知角色"
            character.icon = character_info.icon if character_info else "未知图标"
            character.weapon.name = weapon_info.name_chs if weapon_info else "未知武器"
            character.weapon.type = weapon_info.type if weapon_info else "未知武器类型"

        print_player(player)


def print_player(player: Player):
    print(f"\n【UID={player.uid}】{player.nickname} 的角色信息如下：")
    print(f"等级: {player.level}")
    print(f"世界等级: {player.world_level}")
    print(f"成就数量: {player.finish_achievement_num}")
    print(f"深境螺旋: 第{player.tower_floor_index}层 第{player.tower_level_index}间")
    print(f"满好感角色数量: {player.full_friendship_num}")
    for idx, character in enumerate(player.characters, 1):
        print(f"\n{idx}. {character.name} (ID: {character.avatarId})")
        print(f"   等级: {character.level}")
        print(f"   好感度: {character.friendship}")

        if character.weapon:
            print(
                f"   武器: {character.weapon.name} (等级: {character.weapon.level}) (精炼: {character.weapon.refine})")

        if character.artifact_flower:
            print(f"   圣遗物花: {character.artifact_flower.name} (等级: {character.artifact_flower.level})")
            print(f"   圣遗物羽: {character.artifact_plume.name} (等级: {character.artifact_plume.level})")
            print(f"   圣遗物沙: {character.artifact_sands.name} (等级: {character.artifact_sands.level})")
            print(f"   圣遗物杯: {character.artifact_goblet.name} (等级: {character.artifact_goblet.level})")
            print(f"   圣遗物冠: {character.artifact_circlet.name} (等级: {character.artifact_circlet.level})")


async def main():
    uid = "101242308"
    async with httpx.AsyncClient(proxy="http://127.0.0.1:4081") as client:
        async with anyio.create_task_group() as tg:
            tg.start_soon(sync_player, client, uid)


if __name__ == "__main__":
    anyio.run(main)
