from dataclasses import dataclass


@dataclass
class CharacterInfo:
    # 角色的唯一标识符
    id: int
    # 角色的图标
    icon: str
    # 角色的稀有度
    rank: int
    # 角色的武器类型，如单手剑、长柄角色等
    weapon: str
    # 角色的属性
    element: str
    # 生日
    birth: list[int]
    # 角色的发布时间
    release: str
    # 角色的英文名称
    name_en: str
    # 角色的简体中文名称
    name_chs: str
    # 角色的日文名称
    name_jp: str
    # 角色的韩文名称
    name_kr: str
    pass
