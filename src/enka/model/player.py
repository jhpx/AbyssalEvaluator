# player.py

from dataclasses import dataclass
from typing import List

from src.enka.model.character import Character


@dataclass
class Player:
    """玩家类"""
    # uid
    uid: int
    # 名称
    nickname: str
    # 等级
    level: int
    # 世界等级
    world_level: int
    # 名片
    name_card_id: int
    # 名片路径
    name_card: str
    # 图标
    profile_icon_id: int
    # 图标路径
    profile_icon: str
    # 成就数
    finish_achievement_num: int
    # 深境螺旋层数
    abyss_floor_index: int | None
    # 深境螺旋间数
    abyss_level_index: int | None
    # 深境螺旋星数
    abyss_star_index: int | None

    # v5.0 新增
    # 幻想真境剧诗幕数
    theater_act_index: int | None
    # 幻想真境剧诗星数
    theater_star_index: int | None

    # v5.7 新增
    # 幽境危战难度
    stygian_difficulty: int | None
    # 幽境危战时间
    stygian_clear_time: int | None
    # 满好感角色
    max_friendship_character_count: int

    # 角色
    characters: List[Character]
