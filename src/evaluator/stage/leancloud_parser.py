from src.evaluator.model.character_stat_weight import CharacterStatWeight


class LeanCloudParser:

    @staticmethod
    def parse_character_weight(data: dict) -> list[CharacterStatWeight]:
        lean_cloud_weights = data.get("results")

        character_stat_weights = [CharacterStatWeight(
            id=int(cdata.get("id")),
            name=str(cdata.get("character")),
            hp_percent=cdata.get("hp_percent"),
            attack_percent=cdata.get("attack_percent"),
            defense_percent=cdata.get("defense_percent"),
            critical=cdata.get("critical"),
            critical_hurt=cdata.get("critical_hurt"),
            element_mastery=cdata.get("element_mastery"),
            charge_efficiency=cdata.get("charge_efficiency"),
            hp=cdata.get("hp"),
            attack=cdata.get("attack"),
            defense=cdata.get("defense"),
        ) for cdata in lean_cloud_weights]
        return character_stat_weights
