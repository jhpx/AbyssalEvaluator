# weapon.py

from dataclasses import dataclass
from typing import List

from src.enka.model.stat import Stat


@dataclass
class Weapon:
    """武器类"""
    # id
    id: int
    # 等级
    level: int
    # 突破等级
    promote_level: int
    # 精炼等级
    refine: int
    # 稀有度
    rank: int
    # 图标
    icon: str
    # 武器附加属性
    weapon_stats: List[Stat]
    # 名称
    name: str = ""
    # 类型
    type: str = ""
