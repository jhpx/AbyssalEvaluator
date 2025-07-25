# stat.py

from dataclasses import dataclass
from enum import StrEnum, IntEnum


class StatType(StrEnum):
    """
    该枚举类表示装备加成中的各种属性类型。
    """

    # 生命值相关
    HP = "FIGHT_PROP_HP"  # 固定生命值
    HP_PERCENT = "FIGHT_PROP_HP_PERCENT"  # 生命值百分比加成

    # 攻击力相关
    BASE_ATK = "FIGHT_PROP_BASE_ATTACK"  # 基础攻击力
    ATK = "FIGHT_PROP_ATTACK"  # 固定攻击力
    ATK_PERCENT = "FIGHT_PROP_ATTACK_PERCENT"  # 攻击力百分比加成

    # 防御力相关
    DEF = "FIGHT_PROP_DEFENSE"  # 固定防御力
    DEF_PERCENT = "FIGHT_PROP_DEFENSE_PERCENT"  # 防御力百分比加成

    # 暴击与伤害相关
    CRIT_RATE = "FIGHT_PROP_CRITICAL"  # 暴击率
    CRIT_DMG = "FIGHT_PROP_CRITICAL_HURT"  # 暴击伤害加成

    # 元素伤害加成
    FIRE_DMG_BONUS = "FIGHT_PROP_FIRE_ADD_HURT"  # 火元素伤害加成
    ELECTRO_DMG_BONUS = "FIGHT_PROP_ELEC_ADD_HURT"  # 雷元素伤害加成
    ICE_DMG_BONUS = "FIGHT_PROP_ICE_ADD_HURT"  # 冰元素伤害加成
    WATER_DMG_BONUS = "FIGHT_PROP_WATER_ADD_HURT"  # 水元素伤害加成
    ROCK_DMG_BONUS = "FIGHT_PROP_ROCK_ADD_HURT"  # 岩元素伤害加成
    WIND_DMG_BONUS = "FIGHT_PROP_WIND_ADD_HURT"  # 风元素伤害加成
    GRASS_DMG_BONUS = "FIGHT_PROP_GRASS_ADD_HURT"  # 草元素伤害加成
    PHYSICAL_DMG_BONUS = "FIGHT_PROP_PHYSICAL_ADD_HURT"  # 物理伤害加成

    # 其他
    ELEMENTAL_CHARGE = "FIGHT_PROP_CHARGE_EFFICIENCY"  # 元素充能效率
    ELEMENTAL_MASTERY = "FIGHT_PROP_ELEMENT_MASTERY"  # 元素精通
    HEALING_BONUS = "FIGHT_PROP_HEAL_ADD"  # 治疗效果加成


@dataclass
class Stat:
    """属性类"""
    # 属性字符串
    stat_type: StatType
    # 属性值
    stat_value: float

    # 属性字符串
    def __repr__(self):
        return f"{self.stat_type.name}: {self.stat_value}"
