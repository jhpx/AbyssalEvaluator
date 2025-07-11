from dataclasses import dataclass
from typing import List

from src.models.enum.position import Position
# artifact.py

from src.models.enum.stat import Stat


@dataclass
class Artifact:
    """圣遗物类"""
    # ID
    id: int
    # 套装ID
    set_id: int
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
    # 名称
    name: str = ""
    # 套装名称
    set_name: str = ""
