# player.py

from dataclasses import dataclass
from typing import List

from src.models.character import Character


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
    # 成就数
    finish_achievement_num: int
    # 深渊层数
    tower_floor_index: int
    # 深渊间数
    tower_level_index: int
    # 星数
    tower_star_index: int
    # 图标
    profile_icon_id: int
    # 满好感角色
    full_friendship_num: int
    # 角色
    characters: List[Character]
