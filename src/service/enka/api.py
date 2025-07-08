class EnkaApi:
    @staticmethod
    def get_player_url(uid: str) -> str:
        """
        获取玩家信息
        :param uid: 玩家 UID
        """
        return f"https://enka.network/api/uid/{uid}"
