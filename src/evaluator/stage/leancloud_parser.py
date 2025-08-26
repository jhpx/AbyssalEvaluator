import dacite
from dacite import Config

from src.evaluator.model.character_stat_weight import CharacterStatWeight


class LeanCloudParser:

    @staticmethod
    def parse_character_weight(data: dict) -> list[CharacterStatWeight]:
        lean_cloud_weights = data.get("results")

        return [
            dacite.from_dict(data_class=CharacterStatWeight,
                             data=cdata, config=Config(cast=[int]))
            for cdata in lean_cloud_weights
        ]
