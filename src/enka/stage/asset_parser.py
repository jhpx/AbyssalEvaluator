class EnkaAssetParser:

    @staticmethod
    def parse_loc(data: dict, lang: str) -> dict:
        """解析单个语言的词汇表"""
        return data.get(lang, {})