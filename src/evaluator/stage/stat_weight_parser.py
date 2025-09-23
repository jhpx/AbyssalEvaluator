import csv
from io import StringIO

import dacite
from dacite import Config

from src.evaluator.model.character_stat_weight import CharacterStatWeight


class StatWeightParser:

    @staticmethod
    def parse_character_weight(data: str) -> list[CharacterStatWeight]:
        """
        从CSV文件中解析角色权重数据
        Returns:
            CharacterStatWeight对象列表
        """
        reader = csv.DictReader(StringIO(data))
        return [
            dacite.from_dict(data_class=CharacterStatWeight,
                             data=cdata, config=Config(cast=[int]))
            for cdata in reader
        ]

