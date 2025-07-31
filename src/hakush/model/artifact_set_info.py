from dataclasses import dataclass
from typing import List


class Postion:
    pass


@dataclass
class ArtifactSetInfo:
    # 套装ID
    id: int
    # 套装的图标
    icon: str
    # 稀有度
    ranks: List[int]
    # 效果条件
    effect_need: List[int]
    # 套装的英文名称
    name_en: str
    # 套装的简体中文名称
    name_zh: str
    # 套装的日文名称
    name_ja: str
    # 套装的韩文名称
    name_ko: str
    # 套装效果的英文描述
    effect_desc_en: List[str]
    # 套装效果的简体中文描述
    effect_desc_zh: List[str]
    # 套装效果的日文描述
    effect_desc_ja: List[str]
    # 套装效果的韩文描述
    effect_desc_ko: List[str]

    def name(self, lang: str) -> str:
        if lang == "en":
            return self.name_en
        elif lang == "zh":
            return self.name_zh
        elif lang == "ja":
            return self.name_ja
        elif lang == "ko":
            return self.name_ko
        else:
            return self.name_en

    def effect_desc(self, lang: str) -> str:
        if lang == "en":
            return self.name_en
        elif lang == "zh":
            return self.name_zh
        elif lang == "ja":
            return self.name_ja
        elif lang == "ko":
            return self.name_ko
        else:
            return self.name_en