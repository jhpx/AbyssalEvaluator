from typing import List, Dict

from src.models.meta.character_info import CharacterInfo
from src.models.meta.weapon_info import WeaponInfo


class HakushParser:

    @classmethod
    def parse_weapon_infos(cls, data: Dict[str, Dict]) -> List[WeaponInfo]:
        return [WeaponInfo(
            id=int(wid),
            icon=wdata.get("icon", ""),
            rank=wdata.get("rank", 0),
            type=wdata.get("type", ""),
            name_en=wdata.get("EN", ""),
            name_chs=wdata.get("CHS", ""),
            name_jp=wdata.get("JP", ""),
            name_kr=wdata.get("KR", ""),
        ) for wid, wdata in data.items()]

    @classmethod
    def parse_character_infos(cls, data: Dict[str, Dict]) -> List[CharacterInfo]:
        str_to_rank = {
            "QUALITY_ORANGE": 5,
            "QUALITY_PURPLE": 4,
        }
        return [CharacterInfo(
            id=int(cid.replace("-","")),
            icon=cdata.get("icon", ""),
            rank=str_to_rank.get(cdata.get("rank", ""), 0),
            weapon=cdata.get("weapon", ""),
            element=cdata.get("element", ""),
            birth=cdata.get("birth", []),
            release=cdata.get("release", ""),
            name_en=cdata.get("EN", ""),
            name_chs=cdata.get("CHS", ""),
            name_jp=cdata.get("JP", ""),
            name_kr=cdata.get("KR", ""),
        ) for cid, cdata in data.items()]
