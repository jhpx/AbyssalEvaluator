from dataclasses import dataclass


@dataclass
class WeaponInfo:
    # 武器的唯一标识符
    id: int

    # 武器的图标
    icon: str

    # 武器的稀有度
    rank: int

    # 武器的类型，如单手剑、长柄武器等
    type: str

    # 武器的英文名称
    name_en: str

    # 武器的简体中文名称
    name_chs: str

    # 武器的日文名称
    name_jp: str

    # 武器的韩文名称
    name_kr: str
