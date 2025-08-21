# genre.py

from dataclasses import dataclass

from src.enka.model.stat import StatType


@dataclass
class Genre:
    # 流派名称
    name: str
    # 有效属性类型列表
    effective_stats: set[StatType]

    def effective_stat_weights(self) -> dict[StatType, int]:
        """获取所有属性的权重字典，有效属性为100，无效属性为0"""
        return {stat_type: 100 for stat_type in self.effective_stats}

    def default_effective_rolls(self) -> float:
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
    name="双爆",
    effective_stats={
        StatType.CRIT_RATE,
        StatType.CRIT_DMG,
    }
)

GENRE_ATK_CRIT = Genre(
    name="攻双爆",
    effective_stats={
        StatType.ATK,
        StatType.ATK_PERCENT,
        StatType.CRIT_RATE,
        StatType.CRIT_DMG,
    }
)

GENRE_ATK_EC_CRIT = Genre(
    name="攻充双爆",
    effective_stats={
        StatType.ATK,
        StatType.ATK_PERCENT,
        StatType.ELEMENTAL_CHARGE,
        StatType.CRIT_RATE,
        StatType.CRIT_DMG,
    }
)

GENRE_ATK_EM_CRIT = Genre(
    name="攻精双爆",
    effective_stats={
        StatType.ATK,
        StatType.ATK_PERCENT,
        StatType.ELEMENTAL_MASTERY,
        StatType.CRIT_RATE,
        StatType.CRIT_DMG,
    }
)

GENRE_ATK_HP_EM_CRIT = Genre(
    name="攻生精双爆",
    effective_stats=[
        StatType.ATK,
        StatType.ATK_PERCENT,
        StatType.HP,
        StatType.HP_PERCENT,
        StatType.ELEMENTAL_MASTERY,
        StatType.CRIT_RATE,
        StatType.CRIT_DMG,
    ]
)

GENRE_DEFAULT = GENRE_ATK_EC_CRIT
