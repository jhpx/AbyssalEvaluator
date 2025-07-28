class EnkaAssetParser:

    @staticmethod
    def parse_loc(data: dict, lang: str) -> dict:
        """解析单个语言的词汇表"""
        return data.get(lang, {})


    @staticmethod
    def parse_namecard(data: dict) -> dict:
        """解析名片图标的词汇表"""
        return {key: value['icon'] for key, value in data.items()}

    @staticmethod
    def parse_pfp(data: dict) -> dict:
        """解析头像图标的词汇表"""
        return {key: value['iconPath'] for key, value in data.items()}