# weapon.py

from dataclasses import dataclass
from typing import List

from src.models.artifact import Artifact
from src.models.stat import Stat
from src.models.weapon import Weapon


@dataclass
class Character:
    """角色类"""
    # id
    avatarId: int
    # 等级
    level: int
    # 稀有度
    rank: int
    # 天赋
    talent: List[Stat]
    # 好感度
    friendship: int
    # 武器
    weapon: Weapon
    # 圣遗物
    artifact_flower: Artifact
    artifact_plume: Artifact
    artifact_sands: Artifact
    artifact_goblet: Artifact
    artifact_circlet: Artifact
    # 名称
    name: str = ""
    # 图标
    icon: str = ""
    # 描述
    description: str = ""
