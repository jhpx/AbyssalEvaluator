from dataclasses import dataclass
from typing import List

from src.models.enum.position import Position
# artifact.py

from src.models.enum.stat import Stat, StatType


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
    # 评分
    score: float = 0

    def quality(self) -> int:
        """获取圣遗物品质"""
        return len(self.sub_stat_ids) - self.level // 4

    def matrix(self):
        """返回圣遗物矩阵"""
        result = {}
        for stat_type in StatType:
            result[stat_type.name] = 0
        result[self.main_stat.stat_type.name] = self.main_stat.stat_value
        for sub_stat in self.sub_stats:
            result[sub_stat.stat_type.name] = sub_stat.stat_value
        return result

