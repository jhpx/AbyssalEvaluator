from src.core.duckdb.duckdb_engine import DuckDBSession
from src.util.duckdb_util import rows_into_model_dict
from src.models.meta.character_info import CharacterInfo
from src.models.meta.weapon_info import WeaponInfo
from src.models.player import Player
from src.util.logger import logger
import httpx
import anyio

from src.service.enka.api import EnkaApi
from src.service.enka.parser import EnkaParser
from src.util.http_util import fetch_local_json


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
        character_info_rows = duckdb_session.extract_table("ods_character_info")
        character_dict = rows_into_model_dict(character_info_rows, CharacterInfo)
        # 关联武器
        weapon_info_rows = duckdb_session.extract_table("ods_weapon_info")
        weapon_dict = rows_into_model_dict(weapon_info_rows, WeaponInfo)
        # # 关联圣遗物
        # artifact_info_rows = duckdb_session.extract_table("ods_artifact_info")
        # artifact_dict = rows_into_model_dict(artifact_info_rows, ArtifactInfo)
        for character in player.characters:
            weapon_info = weapon_dict.get(character.weapon.id, None)
            character_info = character_dict.get(character.avatarId, None)
            character.name = character_info.name_chs if character_info else "未知角色"
            character.icon = character_info.icon if character_info else "未知图标"
            character.weapon.name = weapon_info.name_chs if weapon_info else "未知武器"
            character.weapon.type = weapon_info.type if weapon_info else "未知武器类型"

        print_player(player)


def print_player(player: Player):
    print(f"\n[UID={player.uid}]{player.nickname} 的角色信息如下：")
    print(f"等级: {player.level}")
    print(f"世界等级: {player.world_level}")
    print(f"成就数量: {player.finish_achievement_num}")
    print(f"深境螺旋: 第{player.tower_floor_index}层 第{player.tower_level_index}间")
    print(f"满好感角色数量: {player.full_friendship_num}")
    for idx, character in enumerate(player.characters, 1):
        print(f"\n{idx}. {character.name}(ID: {character.avatarId}|{character.icon})")
        print(f"   等级: {character.level}")
        print(f"   好感度: {character.friendship}")
        wp = character.weapon
        print(
            f"   武器: {wp.name}(ID: {wp.id}|{wp.icon}) (类型: {wp.type}) (等级: {wp.level}) (精炼: {wp.refine}) (效果: {wp.weapon_stats})")
        for aft in [character.artifact_flower, character.artifact_plume, character.artifact_sands,
                    character.artifact_goblet, character.artifact_circlet]:
            if aft:
                print(
                    f"   圣遗物{aft.position}(套装:{aft.set_name}): {aft.name}({aft.id}|{aft.icon}) (等级: {aft.level}) (效果: {aft.main_stat},{aft.sub_stats})")


async def main():
    uid = "101242308"
    async with httpx.AsyncClient(proxy="http://127.0.0.1:4081") as client:
        async with anyio.create_task_group() as tg:
            tg.start_soon(sync_player, client, uid)
