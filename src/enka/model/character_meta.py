# character_meta.py

from dataclasses import dataclass

@dataclass
class CharacterMeta:
    # 角色ID
    id: int
    # 角色名称Hash
    name_text_hash: str
    # 角色属性
    element: str
    # 角色侧脸图标
    side_avatar_icon: str
    # 角色稀有度
    rank: int
    # 角色武器种类
    weapon_type: str
    # 角色衣装
    costume: str
    # 天赋顺序
    skill_order: list[int]
    # 天赋名称
    skill_names: dict[str, str]
    # 固定天赋
    proud_map: dict[str, int]

    @classmethod
    def default(cls, id) -> 'CharacterMeta':
        """创建一个默认的CharacterMeta实例"""
        return cls(
            id=id,
            name_text_hash="",
            element="unknown",
            side_avatar_icon="",
            rank=0,
            weapon_type="",
            costume="",
            skill_order=[],
            skill_names={},
            proud_map={}
        )