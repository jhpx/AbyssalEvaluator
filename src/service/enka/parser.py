# parser.py

from typing import Dict

from dacite import from_dict

from src.models.artifact import Artifact
from src.models.character import Character
from src.models.player import Player
from src.models.enum.position import Position
from src.models.enum.stat import Stat, StatType
from src.models.weapon import Weapon


class EnkaParser:

    @staticmethod
    def parse_weapon(data: Dict) -> Weapon:
        """解析武器装备"""
        weapon_data = data.get("weapon", {})
        flat_data = data.get("flat", {})

        # 解析精炼等级
        refine = 0
        if "affixMap" in weapon_data and weapon_data["affixMap"]:
            refine = list(weapon_data["affixMap"].values())[0]

        # 解析武器属性（主词条和副词条）
        weapon_stats_data = flat_data.get("weaponStats", [])
        weapon_stats = [
            Stat(StatType(st.get("appendPropId")), st.get("statValue", 0.0))
            for st in weapon_stats_data
        ]

        # 构造参数字典
        weapon_dict = {
            "id": data.get("itemId", 0),
            "level": weapon_data.get("level", 1),
            "promote_level": weapon_data.get("promoteLevel", 0),
            "refine": refine + 1,
            "rank": flat_data.get("rankLevel", 0),
            "icon": flat_data.get("icon", ""),
            "weapon_stats": weapon_stats
        }

        return from_dict(data_class=Weapon, data=weapon_dict)

    @staticmethod
    def parse_artifact(data: Dict) -> Artifact:
        """解析圣遗物装备"""
        reliquary_data = data.get("reliquary", {})
        flat_data = data.get("flat", {})

        # 解析主属性
        main_stat_data = flat_data.get("reliquaryMainstat", {})
        main_stat = Stat(
            StatType(main_stat_data.get("mainPropId")),
            stat_value=main_stat_data.get("statValue", 0.0)
        )

        # 解析副属性
        sub_stats_data = flat_data.get("reliquarySubstats", [])
        sub_stats = [
            Stat(StatType(sub.get("appendPropId")), stat_value=sub.get("statValue", 0.0))
            for sub in sub_stats_data
        ]

        # 构造参数字典
        artifact_dict = {
            "id": data.get("itemId", 0),
            "level": reliquary_data.get("level", 1) - 1,
            "position": Position(flat_data.get("equipType", "")),
            "rank": flat_data.get("rankLevel", 0),
            "set_id": flat_data.get("setId", 0),
            "icon": flat_data.get("icon", ""),
            "main_stat_id": reliquary_data.get("mainPropId"),
            "sub_stat_ids": reliquary_data.get("appendPropIdList"),
            "main_stat": main_stat,
            "sub_stats": sub_stats
        }

        return from_dict(data_class=Artifact, data=artifact_dict)

    @staticmethod
    def parse_equip_item(data: Dict) -> Artifact | Weapon | None:
        """解析圣遗物装备或武器装备"""
        if data.get("reliquary"):
            return EnkaParser.parse_artifact(data)
        elif data.get("weapon"):
            return EnkaParser.parse_weapon(data)
        else:
            return None

    @staticmethod
    def parse_character(data: Dict) -> Character:
        """
        解析角色信息
        :param data: 包含角色信息的字典
        :return: Character 对象
        """

        # 基础属性
        avatar_id = data.get("avatarId", 0)
        prop_map = data.get("propMap", {})
        level_data = prop_map.get("4001", {})  # 等级信息键是 "4001"
        level = int(level_data.get("val", 1)) if level_data else 1

        # 好感度
        friendship_level = data.get("fetterInfo", {}).get("expLevel", 0)

        # 天赋等级（可选）
        talent_id_list = data.get("talentIdList", [])
        talent_level_map = data.get("skillLevelMap", {})

        # 装备信息
        equip_list = data.get("equipList", [])

        # 解析武器与圣遗物
        weapon = None
        artifact_map = {}

        for equip in equip_list:
            parsed_item = EnkaParser.parse_equip_item(equip)

            if isinstance(parsed_item, Weapon):
                weapon = parsed_item
            elif isinstance(parsed_item, Artifact):
                artifact_map[parsed_item.position] = parsed_item

        # 构造参数字典
        character_dict = {
            "avatarId": avatar_id,
            "level": level,
            "rank": data.get("rankLevel", 5),
            "talent": [],
            "friendship": friendship_level,
            "weapon": weapon,
            "artifact_flower": artifact_map[Position.FLOWER],
            "artifact_plume": artifact_map[Position.PLUME],
            "artifact_sands": artifact_map[Position.SANDS],
            "artifact_goblet": artifact_map[Position.GOBLET],
            "artifact_circlet": artifact_map[Position.CIRCLET],
        }

        return from_dict(data_class=Character, data=character_dict)

    @staticmethod
    def parse_player(data: Dict) -> Player:
        """解析玩家信息"""
        player_data = data.get("playerInfo", {})

        # 解析角色列表
        characters_data = data.get("avatarInfoList", [])
        characters = []
        for character_data in characters_data:
            characters.append(EnkaParser.parse_character(character_data))

        # 构造Player对象
        player_dict = {
            "uid": int(data.get("uid", 0)),
            "nickname": player_data.get("nickname", ""),
            "level": player_data.get("level", 1),
            "world_level": player_data.get("worldLevel", 0),
            "finish_achievement_num": player_data.get("finishAchievementNum", 0),
            "tower_floor_index": player_data.get("towerFloorIndex", 0),
            "tower_level_index": player_data.get("towerLevelIndex", 0),
            "tower_star_index": player_data.get("towerStarIndex", 0),
            "profile_icon_id": player_data.get("profilePicture").get("id", 100000),
            "full_friendship_num": player_data.get("fetterCount", 0),
            "characters": characters
        }

        return from_dict(data_class=Player, data=player_dict)
