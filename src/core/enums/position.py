# position.py

from src.core.enums.mvenum import MVEnum


class Position(MVEnum):
    """
    该枚举类表示圣遗物的各种位置。
    每个枚举成员代表一种位置，包含两个值：
    - 第一个值是Enka使用的位置标识符（如 "EQUIP_BRACER"）
    - 第二个值是mona使用的位置标识符（如 "flower"）
    """
    FLOWER = "EQUIP_BRACER", "flower"  # 生之花
    PLUME = "EQUIP_NECKLACE", "feather"  # 死之羽
    SANDS = "EQUIP_SHOES", "sand"  # 时之沙
    GOBLET = "EQUIP_RING", "cup"  # 空之杯
    CIRCLET = "EQUIP_DRESS", "head"  # 理之冠
