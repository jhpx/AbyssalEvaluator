from dataclasses import dataclass

from src.enka.model.stat import StatType


@dataclass
class CharacterStatWeight:
    # 角色ID
    id: int
    # 角色名称
    character: str
    # 属性
    hp_percent: int
    attack_percent: int
    defense_percent: int
    critical: int
    critical_hurt: int
    element_mastery: int
    charge_efficiency: int
    hp: int
    attack: int
    defense: int

    def to_dict(self):
        return {
            StatType.ATK_PERCENT: self.attack_percent,
            StatType.HP_PERCENT: self.hp_percent,
            StatType.DEF_PERCENT: self.defense_percent,
            StatType.CRIT_RATE: self.critical,
            StatType.CRIT_DMG: self.critical_hurt,
            StatType.ELEMENTAL_MASTERY: self.element_mastery,
            StatType.ELEMENTAL_CHARGE: self.charge_efficiency,
            StatType.HP: self.hp,
            StatType.ATK: self.attack,
            StatType.DEF: self.defense,
        }
