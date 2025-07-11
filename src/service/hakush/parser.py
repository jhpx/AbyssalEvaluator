from typing import List, Dict

from src.models.meta.artifact_info import ArtifactInfo
from src.models.meta.artifact_set_info import ArtifactSetInfo
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
            id=int(cid.replace("-", "")),
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

    @classmethod
    def parse_artifact_set_infos(cls, data: Dict[str, Dict]) -> List[ArtifactSetInfo]:
        artifactSetInfos = []
        for aid, adata in data.items():
            effect = adata.get("set", {})
            name_translations = {"EN": "", "CHS": "", "JP": "", "KR": ""}
            desc_translations = {lang: [] for lang in ["EN", "CHS", "JP", "KR"]}

            for e_id, e_data in effect.items():
                name_json = e_data.get("name", {})
                desc_json = e_data.get("desc", {})

                for lang in ["EN", "CHS", "JP", "KR"]:
                    if not name_translations[lang]:
                        name_translations[lang] = name_json.get(lang, "")
                    desc_translations[lang].append(desc_json.get(lang, ""))

            if len(desc_translations) > 1:
                effect_need = [2, 4]
            else:
                effect_need = [1]
            artifactSetInfos.append(ArtifactSetInfo(
                id=int(aid),
                icon=adata.get("icon", ""),
                ranks=adata.get("rank", []),
                effect_need=effect_need,
                name_en=name_translations["EN"],
                name_chs=name_translations["CHS"],
                name_jp=name_translations["JP"],
                name_kr=name_translations["KR"],
                effect_desc_en=desc_translations["EN"],
                effect_desc_chs=desc_translations["CHS"],
                effect_desc_jp=desc_translations["JP"],
                effect_desc_kr=desc_translations["KR"]
            ))

        return artifactSetInfos

    @classmethod
    def parse_artifact_set_info_single(cls, data: Dict[str, Dict], lang: str) -> List[ArtifactInfo]:
        """
        解析单个圣遗物套装详细数据（如 artifact-15003.json）
        :param data: 包含圣遗物信息的字典
        :param lang: 当前补完的语言
        :return: 一套5个的ArtifactInfo 列表
        """
        artifactInfos = []

        # 从 Parts 提取各个部位
        parts = data.get("Parts", {})
        for part_key, part_data in parts.items():
            # 将 part_key 映射到 Position 枚举
            artifactInfos.append(ArtifactInfo(
                icon=part_data.get("Icon", ""),
                set_id=data.get("Id", 0),
                lang=lang,
                name=part_data.get("Name", ""),
                desc=part_data.get("Desc", ""),
            ))

        return artifactInfos
