from src.core.duckdb.duckdb_engine import DuckDBSession
from src.models.meta.artifact_info import ArtifactInfo
from src.util.duckdb_util import rows_into_model_dict
from src.models.meta.character_info import CharacterInfo
from src.models.meta.weapon_info import WeaponInfo
from src.models.player import Player
from src.util.logger import logger
import httpx
import anyio

from src.service.enka.api import EnkaApi
from src.service.enka.parser import EnkaParser
from src.util.http_util import fetch_local_json, fetch_and_parse


async def sync_player(client: httpx.AsyncClient, uid: str):
    """
    获取并解析玩家信息，输出到控制台

    :param client: httpx.AsyncClient 实例
    :param uid: 玩家 UID
    """
    player = await fetch_and_parse(
        client=client,
        url=EnkaApi.get_player_url(uid),
        parser=EnkaParser.parse_player,
        use_local=True,
        local_file_path="test\\enka\\json\\player.json"
    )

    if player:
        await compose_player(player,'ko')
        print_player(player)


async def compose_player(player: Player, lang: str):
    duckdb_session = DuckDBSession()
    # 关联角色
    character_info_rows = duckdb_session.extract_table("ods_character_info")
    character_dict = rows_into_model_dict(character_info_rows, CharacterInfo)
    # 关联武器
    weapon_info_rows = duckdb_session.extract_table("ods_weapon_info")
    weapon_dict = rows_into_model_dict(weapon_info_rows, WeaponInfo)
    # 关联圣遗物
    artifact_info_rows = duckdb_session.sql(f"SELECT * from ods_artifact_info WHERE lang = '{lang}'")
    artifact_dict = rows_into_model_dict(artifact_info_rows, ArtifactInfo)
    for character in player.characters:
        weapon_info = weapon_dict.get(character.weapon.id, None)
        character_info = character_dict.get(character.avatarId, None)
        artifact_info_flower = artifact_dict.get(character.artifact_flower.icon, None)
        artifact_info_plume = artifact_dict.get(character.artifact_plume.icon, None)
        artifact_info_sands = artifact_dict.get(character.artifact_sands.icon, None)
        artifact_info_goblet = artifact_dict.get(character.artifact_goblet.icon, None)
        artifact_info_circlet = artifact_dict.get(character.artifact_circlet.icon, None)
        character.name = character_info.name(lang) if character_info else "UNKNOWN"
        character.icon = character_info.icon if character_info else "UNKNOWN"
        character.weapon.name = weapon_info.name(lang) if weapon_info else "UNKNOWN"
        character.weapon.type = weapon_info.type if weapon_info else "UNKNOWN"
        character.artifact_flower.name = artifact_info_flower.name if artifact_info_flower else "UNKNOWN"
        character.artifact_plume.name = artifact_info_plume.name if artifact_info_plume else "UNKNOWN"
        character.artifact_sands.name = artifact_info_sands.name if artifact_info_sands else "UNKNOWN"
        character.artifact_goblet.name = artifact_info_goblet.name if artifact_info_goblet else "UNKNOWN"
        character.artifact_circlet.name = artifact_info_circlet.name if artifact_info_circlet else "UNKNOWN"


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
