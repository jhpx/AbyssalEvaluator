from logging import raiseExceptions

from src.enka.model.character import Character
from src.enka.model.player import Player
from src.enka.model.weapon import Weapon


class EnkaTextDisplayer:

    @staticmethod
    def display_player(player: Player, loc_map: dict) -> str:
        """
        显示玩家信息
        :param loc_map: 国际化字典
        :param player: 玩家对象
        :return: 玩家信息字符串
        """
        if not player:
            raise ValueError("Player not found")
        if not loc_map:
            raise ValueError("Loc map not found")

        # 获取本地化标签
        level_label = loc_map.get("level", "Lv.")
        abyss_label = loc_map.get("abyss", "Spiral Abyss")
        achievements_label = loc_map.get("achievements", "Total Achievements")

        # 构建基础信息
        info_parts = [
            f"{player.nickname}(uid:{player.uid})",
            f"{level_label}: {player.level}",
            f"{achievements_label}: {player.finish_achievement_num}"
        ]

        # 添加深境螺旋信息
        abyss_info = f"{abyss_label}: {player.abyss_floor_index or '?'}-{player.abyss_level_index or '?'}"
        abyss_info += f" ({player.abyss_star_index or '?'}★)"
        info_parts.append(abyss_info)

        # 添加幻想真境剧诗信息
        theater_info = f"Theater: Act {player.theater_act_index or '?'}"
        theater_info += f" ({player.theater_star_index or '?'}★)"
        info_parts.append(theater_info)

        # 添加幽境危战信息（如果存在）
        stygian_info = f"Stygian: Difficulty {player.stygian_difficulty or '?'}"
        if player.stygian_clear_time is not None:
            # 将秒转换为分钟和秒的格式
            minutes = player.stygian_clear_time // 60
            seconds = player.stygian_clear_time % 60
            stygian_info += f" ({minutes}m {seconds}s)"
        else:
            stygian_info += " (Not Cleared)"
        info_parts.append(stygian_info)

        # 添加满好感角色数
        info_parts.append(f"Max Friendship Characters: {player.max_friendship_character_count}")
        #
        # 添加角色信息
        for character in player.characters:
            info_parts.append(EnkaTextDisplayer.display_character(character, loc_map))

        return "\n".join(info_parts)

    @staticmethod
    def display_character(character: Character, loc_map: dict) -> str:
        """
        显示角色信息
        :param character: 角色对象
        :param loc_map: 国际化字典
        :return: 角色信息字符串
        """
        if not character:
            return "Invalid character"


        # 构建角色基本信息
        info_parts = [
            f"\n=== {character.name} (Lv.{character.level} Exp.{character.exp}) ===",
            f"Rarity: {'★' * character.rank}",
            f"Element: {character.element}",
            f"Friendship Level: {character.friendship}"
        ]

        # 添加天赋信息
        talents = []
        for talent_id, talent_level in character.talent_levels.items():
            talent_name = loc_map.get(talent_id, f"(SKILL {talent_id})")
            talents.append(f"{talent_name} {talent_level}")
        if talents:
            info_parts.append("Talents: " + ", ".join(talents))

        # 添加武器信息
        if character.weapon:
            info_parts.append(EnkaTextDisplayer.display_weapon(character.weapon, loc_map))

        # # 添加圣遗物信息
        # if character.artifacts:
        #     for artifact in character.artifacts:
        #         info_parts.append(EnkaTextDisplayer.display_artifact(artifact, loc_map))

        return "\n".join(info_parts)

    @staticmethod
    def display_weapon(weapon: Weapon, loc_map: dict) -> str:
        """
        显示武器信息
        :param weapon: 武器对象
        :param loc_map: 国际化字典
        :return: 武器信息字符串
        """
        if not weapon:
            return "No weapon"

        # 构建武器信息
        info_parts = [
            f"Weapon: {weapon.name} (Lv.{weapon.level}) {'★' * weapon.rank} R{weapon.refine}",
        ]

        # 添加武器属性
        if weapon.weapon_stats:
            stats = []
            for stat in weapon.weapon_stats:
                stats.append(f"{loc_map.get(stat.stat_type, stat.stat_type.name)}: {stat.stat_value_str}")
            if stats:
                info_parts.append("  Stats: " + ", ".join(stats))

        return "\n".join(info_parts)

    @staticmethod
    def display_artifact(artifact, loc_map: dict) -> str:
        """
        显示圣遗物信息
        :param artifact: 圣遗物对象
        :param loc_map: 国际化字典
        :return: 圣遗物信息字符串
        """
        if not artifact:
            return "No artifact"

        # 获取圣遗物名称和套装名称
        artifact_name = loc_map.get(str(artifact.id), artifact.name)
        set_name = loc_map.get(str(artifact.set_id), artifact.set_name)

        # 构建圣遗物信息
        info_parts = [
            f"\nArtifact: {artifact_name} (+{artifact.level - 1})",
            f"Set: {set_name}",
            f"Rarity: {'★' * artifact.rank}",
            f"Type: {artifact.type}"
        ]

        # 添加主属性
        if artifact.main_stat:
            main_stat_name = loc_map.get(artifact.main_stat.prop_id, artifact.main_stat.prop_id)
            info_parts.append(f"Main Stat: {main_stat_name} +{artifact.main_stat.value}")

        # 添加副属性
        if artifact.sub_stats:
            sub_stats = []
            for stat in artifact.sub_stats:
                stat_name = loc_map.get(stat.prop_id, stat.prop_id)
                sub_stats.append(f"{stat_name} +{stat.value}")
            if sub_stats:
                info_parts.append("Sub Stats: " + ", ".join(sub_stats))

        return "\n".join(info_parts)
