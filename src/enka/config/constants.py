from enum import StrEnum
from typing import Literal


class Language(StrEnum):
    """语言代码"""

    ENGLISH = "en"
    RUSSIAN = "ru"
    VIETNAMESE = "vi"
    THAI = "th"
    PORTUGUESE = "pt"
    KOREAN = "ko"
    JAPANESE = "ja"
    INDONESIAN = "id"
    FRENCH = "fr"
    SPANISH = "es"
    GERMAN = "de"
    TRADITIONAL_CHINESE = "zh-tw"
    SIMPLIFIED_CHINESE = "zh-cn"
    ITALIAN = "it"
    TURKISH = "tr"


class EquipmentType(StrEnum):
    """圣遗物类型"""

    FLOWER = "EQUIP_BRACER"
    PLUME = "EQUIP_NECKLACE"
    SANDS = "EQUIP_SHOES"
    GOBLET = "EQUIP_RING"
    CIRCLET = "EQUIP_DRESS"


class ItemType(StrEnum):
    """装备类型"""

    WEAPON = "ITEM_WEAPON"
    ARTIFACT = "ITEM_RELIQUARY"

# 角色稀有度
CHARACTER_RARITY_MAP: dict[str, Literal[4, 5]] = {
    "QUALITY_ORANGE": 5,
    "QUALITY_ORANGE_SP": 5,
    "QUALITY_PURPLE": 4,
}

# 角色突破与等级对应关系
ASCENSION_TO_MAX_LEVEL: dict[Literal[0, 1, 2, 3, 4, 5, 6], Literal[20, 40, 50, 60, 70, 80, 90]] = {
    0: 20,
    1: 40,
    2: 50,
    3: 60,
    4: 70,
    5: 80,
    6: 90,
}
