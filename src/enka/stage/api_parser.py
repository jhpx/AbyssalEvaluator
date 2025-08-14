# parser.py

from src.enka.config.constants import EquipmentType, Element
from src.enka.config.prop_stat import FightPropType
from src.enka.model.artifact import Artifact
from src.enka.model.character import Character
from src.enka.model.player import Player
from src.enka.model.stat import Stat, StatType
from src.enka.model.weapon import Weapon


class EnkaParser:

    @staticmethod
    def parse_weapon(data: dict, asset_map: dict) -> Weapon:
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
        return Weapon(
            id=data.get("itemId", 0),
            name=asset_map["loc"].get(flat_data.get("nameTextMapHash")),
            level=weapon_data.get("level", 1),
            promote_level=weapon_data.get("promoteLevel", 0),
            refine=refine + 1,
            rank=flat_data.get("rankLevel", 0),
            icon=flat_data.get("icon", ""),
            weapon_stats=weapon_stats
        )

    @staticmethod
    def parse_artifact(data: dict, asset_map: dict) -> Artifact:
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
        sub_stats = [
            Stat(StatType(sub.get("appendPropId")), stat_value=sub.get("statValue", 0.0))
            for sub in flat_data.get("reliquarySubstats", [])
        ]

        # 构造参数字典
        return Artifact(
            id=data.get("itemId", 0),
            # 默认的loc查不到此名称
            name="TextHash_" + flat_data.get("nameTextMapHash"),
            level=reliquary_data.get("level", 1) - 1,
            equipment_type=EquipmentType(flat_data.get("equipType")),
            rank=flat_data.get("rankLevel", 0),
            set_id=flat_data.get("setId", 0),
            set_name=asset_map["loc"].get(flat_data.get("setNameTextMapHash")),
            icon=flat_data.get("icon", ""),
            main_stat_id=reliquary_data.get("mainPropId"),
            sub_stat_ids=reliquary_data.get("appendPropIdList"),
            main_stat=main_stat,
            sub_stats=sub_stats
        )

    @staticmethod
    def parse_equip_item(data: dict, asset_map: dict) -> Artifact | Weapon | None:
        """解析圣遗物装备或武器装备"""
        if data.get("reliquary"):
            return EnkaParser.parse_artifact(data, asset_map)
        elif data.get("weapon"):
            return EnkaParser.parse_weapon(data, asset_map)
        else:
            return None

    @staticmethod
    def parse_character(data: dict, asset_map: dict) -> Character:
        """
        解析角色信息
        :param asset_map: 国际化字典
        :param data: 包含角色信息的字典
        :return: Character 对象
        """

        # 基础属性
        avatar_id = data.get("avatarId")
        character_meta = asset_map["character"].get(avatar_id)

        # 等级、经验值、突破
        prop_map = data.get("propMap")
        level_data = prop_map.get("4001")  # 等级信息键是 "4001"
        level = int(level_data.get("val"))
        exp_data = prop_map.get("1001")  # 经验值信息键是 "1001"
        exp = int(exp_data.get("val", exp_data.get("ival")))
        promote_level_data = prop_map.get("1002", {})  # 突破信息键是 "1002"
        promote_level = int(promote_level_data.get("val"))

        # 解析战斗面板
        fight_prop_map = {
            FightPropType(int(k)): v
            for k, v in data.get("fightPropMap", {}).items()
        }

        # 命座
        talent_ids = data.get("talentIdList", [])
        # 天赋等级
        skill_level_map = data.get("skillLevelMap")
        proud_skill_extraL_level_map = data.get("proudSkillExtraLevelMap", {})
        skill_level_ext = {k: proud_skill_extraL_level_map.get(str(v), 0) for k, v in
                           character_meta.proud_map.items()}
        # 好感度
        friendship_level = data.get("fetterInfo").get("expLevel")

        # 装备信息
        equip_list = data.get("equipList", [])

        # 解析武器与圣遗物
        weapon = None
        artifact_list: list[Artifact | None] = [None] * 5

        for equip in equip_list:
            parsed_item = EnkaParser.parse_equip_item(equip, asset_map)
            if isinstance(parsed_item, Weapon):
                weapon = parsed_item
            elif isinstance(parsed_item, Artifact):
                # 按EquipmentType定义顺序构造圣遗物列表：花、羽、沙、杯、冠
                index = list(EquipmentType).index(parsed_item.equipment_type)
                artifact_list[index] = parsed_item
                pass

        # 构造参数字典
        return Character(
            id=avatar_id,
            name=asset_map["loc"].get(character_meta.name_text_hash),
            _side_avatar_icon=character_meta.side_avatar_icon,
            level=level,
            exp=exp,
            promote_level=promote_level,
            rank=character_meta.rank,
            element=Element.from_name(character_meta.element),
            talent_ids=talent_ids,
            skill_names=character_meta.skill_names,
            skill_level_map=skill_level_map,
            skill_level_ext=skill_level_ext,
            friendship=friendship_level,
            weapon=weapon,
            artifacts=artifact_list,
            fight_prop=fight_prop_map
        )

    @staticmethod
    def parse_player(data: dict, asset_map: dict) -> Player:
        """解析玩家信息"""
        player_data = data.get("playerInfo", {})

        # 解析角色列表
        characters_data = data.get("avatarInfoList", [])
        characters = []
        for character_data in characters_data:
            characters.append(EnkaParser.parse_character(character_data, asset_map))

        name_card_id = player_data.get("nameCardId", 0)

        profile_icon_id = player_data.get("profilePicture", {}).get("id", 100000)

        # 构造Player对象
        return Player(
            uid=int(data.get("uid", 0)),
            nickname=player_data.get("nickname", ""),
            level=player_data.get("level", 1),
            world_level=player_data.get("worldLevel", 0),
            name_card_id=name_card_id,
            name_card=asset_map["namecard"].get(name_card_id),
            profile_icon_id=profile_icon_id,
            profile_icon=asset_map["pfp"].get(profile_icon_id),
            finish_achievement_num=player_data.get("finishAchievementNum", 0),
            abyss_floor_index=player_data.get("towerFloorIndex", 0),
            abyss_level_index=player_data.get("towerLevelIndex", 0),
            abyss_star_index=player_data.get("towerStarIndex", 0),
            theater_act_index=player_data.get("theaterActIndex", 0),
            theater_star_index=player_data.get("theaterStarIndex", 0),
            stygian_difficulty=player_data.get("stygianIndex", 0),
            stygian_clear_time=player_data.get("stygianSeconds", 0),
            max_friendship_character_count=player_data.get("fetterCount", 0),
            characters=characters
        )
