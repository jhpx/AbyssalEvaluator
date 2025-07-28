from typing import Optional

import httpx

from src.core.duckdb.duckdb_engine import DuckDBSession
from src.enka.api import EnkaApi
from src.enka.config.constants import Language
from src.enka.model.character import Character
from src.enka.model.player import Player
from src.enka.stage.api_parser import EnkaParser
from src.enka.stage.asset_parser import EnkaAssetParser
from src.enka.stage.synchronizer import EnkaAssetSynchronizer
from src.enka.test_api import TestEnkaApi
from src.models.meta.character_info import CharacterInfo
from src.util.duckdb_util import rows_into_model_dict
from src.util.http_util import fetch_and_parse


class EnkaClient:
    def __init__(self, lang: Language | str, proxy: str = None):
        self._client = httpx.AsyncClient(proxy=proxy)
        self._lang = self._convert_lang(lang)
        self._db = DuckDBSession()
        self._asset_map = {}
        self._player = None

    def _convert_lang(self, lang: Language | str) -> Language:
        """针对不支持的语言报错"""
        if not lang in Language:
            raise ValueError(f"Invalid language: {lang}")
        return lang

    async def __aenter__(self):
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        await self._client.aclose()

    async def fetch_assets(self):
        """从enka获取最新的静态资源"""
        loc = await fetch_and_parse(
            client=self._client,
            url=TestEnkaApi.get_loc_json(),
            parser=lambda data: EnkaAssetParser.parse_loc(data, self._lang)
        )
        EnkaAssetSynchronizer.sync_loc(loc, self._db)
        self._asset_map["loc"] = rows_into_model_dict(self._db.extract_table("loc"), str)

        namecard = await fetch_and_parse(
            client=self._client,
            url=TestEnkaApi.get_namecard_json(),
            parser=EnkaAssetParser.parse_namecard
        )
        EnkaAssetSynchronizer.sync_namecard(namecard, self._db)
        self._asset_map["namecard"] = rows_into_model_dict(self._db.extract_table("namecard"), str)

        pfp = await fetch_and_parse(
            client=self._client,
            url=TestEnkaApi.get_pfp_json(),
            parser=EnkaAssetParser.parse_pfp
        )
        EnkaAssetSynchronizer.sync_pfp(pfp, self._db)
        self._asset_map["pfp"] = rows_into_model_dict(self._db.extract_table("pfp"), str)

        return self._asset_map

    async def get_asset(self, name):
        """从本地数据库获取静态资源"""
        if name in self._asset_map.keys():
            if name != "character":
                self._asset_map[name] = rows_into_model_dict(self._db.extract_table(name), str)
            else:
                self._asset_map[name] = rows_into_model_dict(self._db.extract_table(name), CharacterInfo)
        return self._asset_map[name]

    async def fetch_player(self, uid: str) -> Optional[Player]:
        """
        从enka获取最新的玩家信息

        :param uid: 玩家 UID
        :return: Player 实例 或 None
        """
        player = await fetch_and_parse(
            client=self._client,
            url=EnkaApi.get_player_url(uid),
            parser=lambda data: EnkaParser.parse_player(data, self._asset_map)
        )
        return player

    async def get_player(self, uid: str, lang: str = 'zh') -> Optional[Player]:
        """
        从本地数据库获取玩家信息

        :param uid: 玩家 UID
        :param lang: 语言（默认为 'zh'）
        :return: Player 实例 或 None
        """
        if not self._player:
            self._player = rows_into_model_dict(self._db.extract_table("player"), Player)
        return self._player
