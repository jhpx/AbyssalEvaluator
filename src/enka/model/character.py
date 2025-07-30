# character.py

from dataclasses import dataclass
from typing import List, Optional

from src.enka.model.artifact import Artifact
from src.enka.model.stat import Stat
from src.enka.model.weapon import Weapon


@dataclass
class Character:
    """角色类"""
    # id
    avatarId: int
    # 名称
    name: str
    # 图标
    _side_avatar_icon: str
    # 等级
    level: int
    # 经验值
    exp:int
    # 突破
    promote_level: int
    # 稀有度
    rank: int
    # 属性
    element: str
    # 天赋
    talent_levels: dict[int,int]
    # 好感度
    friendship: int
    # 武器
    weapon: Weapon
    # 圣遗物
    artifact_flower: Optional[Artifact]
    artifact_plume: Optional[Artifact]
    artifact_sands: Optional[Artifact]
    artifact_goblet: Optional[Artifact]
    artifact_circlet: Optional[Artifact]

    def side_avatar_icon(self) -> str:
        """获取侧脸图标"""
        return self.side_avatar_icon

    def front_avatar_icon(self) -> str:
        """获取头像图标"""
        return self.side_avatar_icon

    def gacha_image(self) -> str:
        """获取全身像"""
        return self.side_avatar_icon