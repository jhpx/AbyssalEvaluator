# genre.py

from dataclasses import dataclass
from decimal import Decimal

from src.enka.model.stat import StatType


@dataclass
class Genre:
    def __init__(self, name: str, effective_stats: set[StatType]):
        """初始化"""
        self.name = name
        self.effective_stats = effective_stats

    @classmethod
    def from_weights(cls, weights: dict[StatType, int]):
        """从权重字典创建Genre实例"""
        effective_stats = set(stat_type for stat_type, weight in weights.items() if weight > 0)
        name = cls._generate_name_from_stats(effective_stats)
        return cls(name, effective_stats)

    @staticmethod
    def _generate_name_from_stats(effective_stats) -> str:
        """根据有效属性生成名称"""
        name_parts = []
        # 检查攻击相关属性
        if any(stat in effective_stats for stat in [StatType.ATK, StatType.ATK_PERCENT]):
            name_parts.append("攻")
        # 检查生命值相关属性
        if any(stat in effective_stats for stat in [StatType.HP, StatType.HP_PERCENT]):
            name_parts.append("生")
        # 检查防御力相关属性
        if any(stat in effective_stats for stat in [StatType.DEF, StatType.DEF_PERCENT]):
            name_parts.append("防")
        # 检查元素精通
        if StatType.ELEMENTAL_MASTERY in effective_stats:
            name_parts.append("精")
        # 检查双爆属性
        if StatType.CRIT_RATE in effective_stats:
            name_parts.append("暴")
        if StatType.CRIT_DMG in effective_stats:
            name_parts.append("爆")
        # 检查元素充能效率
        if StatType.ELEMENTAL_CHARGE in effective_stats:
            name_parts.append("充")

        return "".join(name_parts)

    def effective_stat_weight(self, stat_type: StatType) -> int:
        """获取所有属性的权重字典，有效属性为100，无效属性为0"""
        return 1 if stat_type in self.effective_stats else 0

    def clac_stat_weight(self, stat_type: StatType) -> Decimal:
        """获取所有属性的权重字典，有效属性为1，无效属性为0"""
        if stat_type in {StatType.ELEMENTAL_CHARGE, StatType.ELEMENTAL_MASTERY}:
            return Decimal(0.5)
        elif stat_type in self.effective_stats:
            return Decimal(1.0)
        else:
            return Decimal(0.0)

    def default_effective_rolls(self) -> int:
        """获取所有属性的默认有效次数"""
        count_stat_set = {
            StatType.HP_PERCENT,
            StatType.ATK_PERCENT,
            StatType.DEF_PERCENT,
            StatType.ELEMENTAL_CHARGE,
            StatType.ELEMENTAL_MASTERY,
            StatType.CRIT_RATE,
            StatType.CRIT_DMG,
        }

        effective_stats = len(self.effective_stats & count_stat_set)

        return {2: 18, 3: 22, 4: 25, 5: 28, 6: 31, 7: 34}[effective_stats]

    pass


GENRE_CRIT = Genre(
    name="暴爆",
    effective_stats={
        StatType.CRIT_RATE,
        StatType.CRIT_DMG,
    }
)

GENRE_ATK_CRIT = Genre(
    name="攻暴爆",
    effective_stats={
        StatType.ATK,
        StatType.ATK_PERCENT,
        StatType.CRIT_RATE,
        StatType.CRIT_DMG,
    }
)

GENRE_ATK_EC_CRIT = Genre(
    name="攻暴爆充",
    effective_stats={
        StatType.ATK,
        StatType.ATK_PERCENT,
        StatType.ELEMENTAL_CHARGE,
        StatType.CRIT_RATE,
        StatType.CRIT_DMG,
    }
)

GENRE_ATK_EM_CRIT = Genre(
    name="攻精暴爆",
    effective_stats={
        StatType.ATK,
        StatType.ATK_PERCENT,
        StatType.ELEMENTAL_MASTERY,
        StatType.CRIT_RATE,
        StatType.CRIT_DMG,
    }
)

GENRE_ATK_HP_EM_CRIT = Genre(
    name="攻生精暴爆",
    effective_stats={
        StatType.ATK,
        StatType.ATK_PERCENT,
        StatType.HP,
        StatType.HP_PERCENT,
        StatType.ELEMENTAL_MASTERY,
        StatType.CRIT_RATE,
        StatType.CRIT_DMG,
    }
)

GENRE_DEFAULT = GENRE_ATK_EC_CRIT
