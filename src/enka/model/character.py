# character.py

from dataclasses import dataclass
from decimal import Decimal

from src.enka.config.constants import Element
from src.enka.config.prop_stat import FightPropType
from src.enka.model.artifact import Artifact
from src.enka.model.weapon import Weapon


@dataclass
class Character:
    """角色类"""
    # id
    id: int
    # 名称
    name: str
    # 图标
    _side_avatar_icon: str
    # 等级
    level: int
    # 经验值
    exp: int
    # 突破
    promote_level: int
    # 稀有度
    rank: int
    # 属性
    element: Element
    # 命座
    talent_ids: list[int]
    # 主动天赋名称
    skill_names: dict[str, str]
    # 主动天赋等级
    skill_level_map: dict[str, int]
    # 主动天赋等级增强
    skill_level_ext: dict[str, int]
    # 好感度
    friendship: int
    # 武器
    weapon: Weapon
    # 圣遗物
    artifacts: list[Artifact]
    # 面板
    fight_prop: dict[FightPropType, Decimal]

    def side_avatar_icon(self) -> str:
        """获取侧脸图标"""
        return self.side_avatar_icon

    def front_avatar_icon(self) -> str:
        """获取头像图标"""
        return self.side_avatar_icon

    def gacha_image(self) -> str:
        """获取全身像"""
        return self.side_avatar_icon
