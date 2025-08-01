from logging import raiseExceptions

from src.enka.config.prop_stat import SUB_STAT_ID_MAP
from src.enka.model.artifact import Artifact
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
            f"\n===== {character.name} {'★' * character.rank} (Lv.{character.level} Exp.{character.exp}) {character.element} ♥{character.friendship}=====",
            f"Talents: " + ",".join(f'T{t}' for t in character.talent_ids)
        ]

        # 添加天赋信息
        skills = []
        for skill_id, skill_name in character.skill_names.items():
            skill_level_str = str(character.skill_level_map.get(skill_id, 1))
            skill_level_ext = character.skill_level_ext.get(skill_id, 0)
            if skill_level_ext > 0:
                skill_level_str += f"+{skill_level_ext}"
            skills.append(f"{skill_name}: {skill_level_str}")

        info_parts.append("Skills:\n  " + ", ".join(skills))

        # 添加武器信息
        info_parts.append(EnkaTextDisplayer.display_weapon(character.weapon, loc_map))

        # 添加圣遗物信息
        info_parts.append("Artifacts:")
        for aft in character.artifacts:
            info_parts.append(EnkaTextDisplayer.display_artifact(aft, loc_map))

        # 添加总评分
        info_parts.append(
            f"Total Score:" + f" {character.total_score:.1f}" if hasattr(character, 'total_score') else "", )
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
            f"Weapon: {weapon.name} {'★' * weapon.rank} (Lv.{weapon.level}) R{weapon.refine}",
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
    def display_artifact(aft: Artifact, loc_map: dict) -> str:
        """
        显示圣遗物信息
        :param aft: 圣遗物对象
        :param loc_map: 国际化字典
        :return: 圣遗物信息字符串
        """
        if not aft:
            return "  No artifact"

        # 构建圣遗物信息
        info_parts = [

            f"  {aft.equipment_type.mv_value(1)}: {aft.set_name} {'★' * aft.rank} (Lv.{aft.level})"
            + f" | Score: {aft.score:.1f}" if hasattr(aft, 'score') else "",
        ]

        # 添加主属性
        main_stat_name = loc_map.get(aft.main_stat.stat_type.value)

        # 添加副属性
        sub_stat_appends = [SUB_STAT_ID_MAP.get(sid // 10) for sid in aft.sub_stat_ids]
        sub_stats = [
            f"{loc_map.get(stat.stat_type.value)} {stat.stat_value_str} (+{sub_stat_appends.count(stat.stat_type) - 1})"
            for stat in aft.sub_stats]

        info_parts.append(f"  Stats: {main_stat_name} {aft.main_stat.stat_value_str}, " + ", ".join(sub_stats))

        return "\n".join(info_parts)
