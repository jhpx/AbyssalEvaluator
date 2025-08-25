class EnkaApi:
    ENKA_API_BASE = "https://enka.network/api"
    ENKA_API_DOCS_BASE = "https://raw.githubusercontent.com/EnkaNetwork/API-docs/master/store"

    @classmethod
    def get_player_url(cls, uid: str) -> str:
        """
        获取玩家信息
        :param uid: 玩家 UID
        """
        return cls.ENKA_API_BASE + f"/uid/{uid}"

    @classmethod
    def get_affix_json(cls):
        """
        获取affix本地化json
        :return:
        """
        return cls.ENKA_API_DOCS_BASE + "/affixes.json"

    @classmethod
    def get_loc_json(cls):
        """
        获取loc本地化json
        :return:
        """
        return cls.ENKA_API_DOCS_BASE + "/loc.json"

    @classmethod
    def get_character_json(cls):
        """
        获取character本地化json
        :return:
        """
        return cls.ENKA_API_DOCS_BASE + "/characters.json"

    @classmethod
    def get_name_card_json(cls):
        """
        获取name_card本地化json
        :return:
        """
        return cls.ENKA_API_DOCS_BASE + "/namecards.json"

    @classmethod
    def get_pfp_json(cls):
        """
        获取pfp本地化json
        :return:
        """
        return cls.ENKA_API_DOCS_BASE + "/pfps.json"

    @classmethod
    def get_url(cls, name: str) -> str:
        url_dict = {
            "character": cls.get_character_json,
            "name_card": cls.get_name_card_json,
            "pfp": cls.get_pfp_json,
            "loc": cls.get_loc_json,
            "affix": cls.get_affix_json
        }
        return url_dict[name]()
