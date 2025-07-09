from dataclasses import dataclass
from typing import List


@dataclass
class ArtifactSetInfo:
    # 套装ID
    id: int
    # 套装的图标
    icon: str
    # 稀有度
    ranks: List[int]
    # 套装的英文名称
    name_en: str
    # 套装的简体中文名称
    name_chs: str
    # 套装的日文名称
    name_jp: str
    # 套装的韩文名称
    name_kr: str
    # 套装效果的英文描述
    desc_en: List[str]
    # 套装效果的简体中文描述
    desc_chs: List[str]
    # 套装效果的日文描述
    desc_jp: List[str]
    # 套装效果的韩文描述
    desc_kr: List[str]