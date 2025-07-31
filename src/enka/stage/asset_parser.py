from src.enka.config.constants import CHARACTER_RARITY_MAP
from src.enka.model.character_meta import CharacterMeta


class EnkaAssetParser:

    @staticmethod
    def parse_loc(data: dict, lang: str) -> dict[str, str]:
        """解析单个语言的词汇表"""
        return data.get(lang, {})

    @staticmethod
    def parse_name_card(data: dict) -> dict[int, str]:
        """解析名片图标的词汇表"""
        return {int(key): value['icon'] for key, value in data.items()}

    @staticmethod
    def parse_pfp(data: dict) -> dict[int, str]:
        """解析头像图标的词汇表"""
        return {int(key): value['iconPath'] for key, value in data.items()}

    @staticmethod
    def parse_character_meta(data: dict) -> list[CharacterMeta]:
        """解析角色相关的词汇表"""

        return [CharacterMeta(
            id=int(cid.replace("-", "")),
            name_text_hash=str(cdata.get("NameTextMapHash")),
            element=cdata.get("Element"),
            side_avatar_icon=cdata.get("SideIconName"),
            rank=CHARACTER_RARITY_MAP.get(cdata.get("QualityType"), 0),
            weapon_type=cdata.get("WeaponType"),
            costume=str(cdata.get("Costumes")),
            skill_order=cdata.get("SkillOrder"),
            skill_names=cdata.get("Skills"),
            proud_map=cdata.get("ProudMap")
        ) for cid, cdata in data.items()]
