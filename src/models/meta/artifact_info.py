from dataclasses import dataclass
from typing import List

from src.models.meta.artifact_set_info import ArtifactSetInfo
from src.models.position import Position


@dataclass
class ArtifactInfo:
    # 圣遗物ID
    id: int
    # 圣遗物的图标
    icon: str
    # 稀有度
    ranks: List[int]
    # 效果条件
    effect_need: List[int]
    # 圣遗物的英文名称
    name_en: str
    # 圣遗物的简体中文名称
    name_chs: str
    # 圣遗物的日文名称
    name_jp: str
    # 圣遗物的韩文名称
    name_kr: str
    # 圣遗物的位置
    position: Position
    # 圣遗物套装
    artifact_set: ArtifactSetInfo