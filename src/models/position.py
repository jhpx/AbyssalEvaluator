# position.py

from src.core.misc.mvenum import MVEnum


class Position(MVEnum):
    """
    该枚举类表示圣遗物的各种位置。
    每个枚举成员代表一种位置，包含两个值：
    - 第一个值是Enka使用的位置标识符（如 "EQUIP_BRACER"）
    - 第二个值是mona使用的位置标识符（如 "flower"）
    """
    FLOWER = "EQUIP_BRACER", "flower", "花"  # 生之花
    PLUME = "EQUIP_NECKLACE", "feather", "羽"  # 死之羽
    SANDS = "EQUIP_SHOES", "sand", "沙"  # 时之沙
    GOBLET = "EQUIP_RING", "cup", "杯"  # 空之杯
    CIRCLET = "EQUIP_DRESS", "head", "冠"  # 理之冠
    def __str__(self):
        return f"{self._all_values[2]}"
    def __repr__(self):
        return str(self)