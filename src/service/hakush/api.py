class HakushApi:
    @staticmethod
    def get_character_list_url() -> str:
        """
        获取玩家信息
        :param avatarId: 玩家 UID
        """
        return f"https://api.hakush.in/gi/data/character.json"


    @staticmethod
    def get_weapon_list_url() -> str:
        """
        获取玩家信息
        :param id: 玩家 UID
        """
        return f"https://api.hakush.in/gi/data/weapon.json"


    @staticmethod
    def get_artifact_list_url(set_id: str) -> str:
        """
        获取玩家信息
        :param set_id: 玩家 UID
        """
        return f"https://api.hakush.in/gi/data/artifact.json"

    @staticmethod
    def get_artifact_single_url(set_id: str) -> str:
        """
        获取玩家信息
        :param set_id: 玩家 UID
        """
        return f"https://api.hakush.in/gi/data/zh/artifact/{set_id}.json"
