from src.enka.config.prop_stat import SUB_STAT_ID_MAP


class LeanCloudParser:

    @staticmethod
    def parse_character_weight(data: dict) -> dict:
        list_character_weights = data.get("results")

        field_to_stat_type = {
            stat_type.value.removeprefix("FIGHT_PROP_").lower(): stat_type
            for stat_type in SUB_STAT_ID_MAP.values()
        }

        character_weights_map = {}
        for character_weight in list_character_weights:
            character_id = int(character_weight.get("id"))

            # 使用字典推导式简化权重字典的构建
            weights = {
                stat_type: character_weight.get(field_name)
                for field_name, stat_type in field_to_stat_type.items()
                if character_weight.get(field_name) is not None
            }

            character_weights_map[character_id] = weights
        return character_weights_map
