# prop_id_map.py

from src.core.enums.position import Position
from src.core.enums.stat_type import StatType

ID_MAP = {
    # 生之花
    14001: (Position.FLOWER, StatType.HP),

    # 死之羽
    12001: (Position.PLUME, StatType.ATK),

    # 理之冠
    13002: (Position.CIRCLET, StatType.HP_PERCENT),
    13004: (Position.CIRCLET, StatType.ATK_PERCENT),
    13006: (Position.CIRCLET, StatType.DEF_PERCENT),
    13007: (Position.CIRCLET, StatType.CRIT_RATE),
    13008: (Position.CIRCLET, StatType.CRIT_DMG),
    13009: (Position.CIRCLET, StatType.HEALING_BONUS),

    # 时之沙
    10002: (Position.SANDS, StatType.HP_PERCENT),
    10004: (Position.SANDS, StatType.ATK_PERCENT),
    10006: (Position.SANDS, StatType.DEF_PERCENT),
    10007: (Position.SANDS, StatType.ENERGY_RECHARGE),

    # 空之杯
    15002: (Position.GOBLET, StatType.HP_PERCENT),
    15004: (Position.GOBLET, StatType.ATK_PERCENT),
    15006: (Position.GOBLET, StatType.DEF_PERCENT),
    15008: (Position.GOBLET, StatType.PYRO_DMG_BONUS),
    15009: (Position.GOBLET, StatType.ELECTRO_DMG_BONUS),
    15010: (Position.GOBLET, StatType.CRYO_DMG_BONUS),
    15011: (Position.GOBLET, StatType.HYDRO_DMG_BONUS),
    15012: (Position.GOBLET, StatType.DENDRO_DMG_BONUS),
    15013: (Position.GOBLET, StatType.GEO_DMG_BONUS),
    15014: (Position.GOBLET, StatType.ANEMO_DMG_BONUS),
}

SUB_ID_MAP = {
    50102: StatType.HP,
    50103: StatType.HP_PERCENT,
    50105: StatType.ATK,
    50106: StatType.ATK_PERCENT,
    50108: StatType.DEF,
    50109: StatType.DEF_PERCENT,
    50120: StatType.CRIT_RATE,
    50122: StatType.CRIT_DMG,
    50123: StatType.ENERGY_RECHARGE,
    50124: StatType.ELEMENTAL_MASTERY,
}