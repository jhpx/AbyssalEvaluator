# character_meta.py

from dataclasses import dataclass
from typing import List


@dataclass
class CharacterMeta:
    # 角色ID
    id: int
    # 角色名称Hash
    name_text_hash: str
    # 角色属性
    element: str
    # 角色侧脸图标
    side_avatar_icon: str
    # 角色稀有度
    rank: int
    # 角色武器种类
    weapon_type: str
    # 角色衣装
    costume: str
    # 技能顺序
    skill_order: List[int]

