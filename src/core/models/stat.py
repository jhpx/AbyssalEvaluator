# stat.py

from dataclasses import dataclass

from src.core.enums.stat_type import StatType


@dataclass
class Stat:
    """属性类"""
    # 属性字符串
    stat_type: StatType
    # 属性值
    stat_value: float
