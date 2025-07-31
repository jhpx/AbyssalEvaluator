from dataclasses import dataclass


@dataclass
class ArtifactInfo:
    # 圣遗物的图标
    icon: str
    # 圣遗物套装
    set_id: id
    # 圣遗物描述语言
    lang: str
    # 圣遗物的名称
    name: str = ""
    # 圣遗物的描述
    desc: str = ""