# stat_type.py

from src.core.misc.mvenum import MVEnum


class StatType(MVEnum):
    """
    该枚举类表示各种属性类型。
    每个枚举成员代表一种属性类型，包含两个值：
    - 第一个值是Enka使用的属性标识符（如 "FIGHT_PROP_HP"）
    - 第二个值是mona使用的属性标识符（如 "lifeStatic"）
    """

    # 生命值相关
    HP = "FIGHT_PROP_HP", "lifeStatic"  # 固定生命值
    HP_PERCENT = "FIGHT_PROP_HP_PERCENT", "lifePercentage"  # 生命值百分比加成

    # 攻击力相关
    ATK_BASE = "FIGHT_PROP_BASE_ATTACK", "attackBase"  # 基础攻击力
    ATK = "FIGHT_PROP_ATTACK", "attackStatic"  # 固定攻击力
    ATK_PERCENT = "FIGHT_PROP_ATTACK_PERCENT", "attackPercentage"  # 攻击力百分比加成

    # 防御力相关
    DEF = "FIGHT_PROP_DEFENSE", "defendStatic"  # 固定防御力
    DEF_PERCENT = "FIGHT_PROP_DEFENSE_PERCENT", "defendPercentage"  # 防御力百分比加成

    # 暴击与伤害相关
    CRIT_RATE = "FIGHT_PROP_CRITICAL", "critical"  # 暴击率
    CRIT_DMG = "FIGHT_PROP_CRITICAL_HURT", "criticalDamage"  # 暴击伤害加成

    # 元素伤害加成
    PYRO_DMG_BONUS = "FIGHT_PROP_FIRE_ADD_HURT", "fireBonus"  # 火元素伤害加成
    ELECTRO_DMG_BONUS = "FIGHT_PROP_ELEC_ADD_HURT", "thunderBonus"  # 雷元素伤害加成
    CRYO_DMG_BONUS = "FIGHT_PROP_ICE_ADD_HURT", "iceBonus"  # 冰元素伤害加成
    HYDRO_DMG_BONUS = "FIGHT_PROP_WATER_ADD_HURT", "waterBonus"  # 水元素伤害加成
    GEO_DMG_BONUS = "FIGHT_PROP_ROCK_ADD_HURT", "rockBonus"  # 岩元素伤害加成
    ANEMO_DMG_BONUS = "FIGHT_PROP_WIND_ADD_HURT", "windBonus"  # 风元素伤害加成
    DENDRO_DMG_BONUS = "FIGHT_PROP_GRASS_ADD_HURT", "dendroBonus"  # 草元素伤害加成
    PHYSICAL_DMG_BONUS = "FIGHT_PROP_PHYSICAL_ADD_HURT", "physicalBonus"  # 物理伤害加成

    # 其他
    ENERGY_RECHARGE = "FIGHT_PROP_CHARGE_EFFICIENCY", "recharge"  # 元素充能效率
    ELEMENTAL_MASTERY = "FIGHT_PROP_ELEMENT_MASTERY", "elementalMastery"  # 元素精通
    HEALING_BONUS = "FIGHT_PROP_HEAL_ADD", "cureEffect"  # 治疗效果加成
