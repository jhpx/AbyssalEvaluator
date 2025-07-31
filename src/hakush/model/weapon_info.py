from dataclasses import dataclass


@dataclass
class WeaponInfo:
    # 武器的唯一标识符
    id: int
    # 武器的图标
    icon: str
    # 武器的稀有度
    rank: int
    # 武器的类型，如单手剑、长柄武器等
    type: str
    # 武器的英文名称
    name_en: str
    # 武器的简体中文名称
    name_zh: str
    # 武器的日文名称
    name_ja: str
    # 武器的韩文名称
    name_ko: str

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
