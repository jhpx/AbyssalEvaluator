from enum import StrEnum
from typing import Literal

from src.core.misc.mvenum import MVEnum


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


class EquipmentType(MVEnum):
    """圣遗物类型"""

    FLOWER = "EQUIP_BRACER", "🌺"
    PLUME = "EQUIP_NECKLACE","🪶"
    SANDS = "EQUIP_SHOES","⏳"
    GOBLET = "EQUIP_RING","🏆"
    CIRCLET = "EQUIP_DRESS","👑"


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

class Element(StrEnum):
    """元素类型"""

    ICE = "🧊"
    FIRE = "🔥"
    WATER = "💧"
    ELECTRIC = "⚡️"
    ROCK = "🪨"
    WIND = "🍃"
    GRASS = "🌱"