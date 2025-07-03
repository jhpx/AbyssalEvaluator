from dataclasses import dataclass
from typing import List

from src.core.enums.position import Position
# artifact.py

from src.core.models.stat import Stat


@dataclass
class Artifact:
    """圣遗物类"""
    # ID
    id: int
    # 名称
    name: str
    # 系列ID
    set_id: int
    # 系列Name
    set_name: str
    # 等级
    level: int
    # 装备位置
    position: Position
    # 稀有度
    rank: int
    # 图标
    icon: str
    # 主属性ID
    main_stat_id: int
    # 副属性ID
    sub_stat_ids: List[int]
    # 主属性
    main_stat: Stat
    # 副属性
    sub_stats: List[Stat]
