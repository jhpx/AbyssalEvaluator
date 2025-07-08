from typing import List, Dict

from src.models.meta.weapon_info import WeaponInfo


class HakushParser:
    @classmethod
    def _build_weapon_info(cls, weapon_id: str, weapon_data: Dict) -> WeaponInfo:
        return WeaponInfo(
            id=int(weapon_id),
            icon=weapon_data.get("icon", ""),
            rank=weapon_data.get("rank", 0),
            type=weapon_data.get("type", ""),
            name_en=weapon_data.get("EN", ""),
            name_chs=weapon_data.get("CHS", ""),
            name_jp=weapon_data.get("JP", ""),
            name_kr=weapon_data.get("KR", ""),
        )

    @classmethod
    def parse_weapon_infos(cls, data: Dict[str, Dict]) -> List[WeaponInfo]:
        return [cls._build_weapon_info(wid, wdata) for wid, wdata in data.items()]
