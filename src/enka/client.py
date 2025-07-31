from typing import Optional

import httpx

from src.core.duckdb.duckdb_engine import DuckDBSession
from src.enka.config.constants import Language
from src.enka.model.player import Player
from src.enka.stage.api_parser import EnkaParser
from src.enka.stage.asset_parser import EnkaAssetParser
from src.enka.stage.synchronizer import EnkaAssetSynchronizer
from src.enka.stage.text_displayer import EnkaTextDisplayer
from src.enka.test_api import TestEnkaApi
from src.core.util.duckdb_util import rows_into_model_dict
from src.core.util.http_util import fetch_and_parse


class EnkaClient:

    def __init__(self, lang: Language | str, proxy: str = None):
        self._client = httpx.AsyncClient(proxy=proxy)
        self._lang = self._convert_lang(lang)
        self._db = DuckDBSession()
        self._asset_map = {}
        self._player = None
        # 定义资源配置
        self._asset_configs = {
            "loc": {
                "name": "loc",
                "url": TestEnkaApi.get_loc_json(),
                "parser": lambda data: EnkaAssetParser.parse_loc(data, self._lang),
                "sync_func": EnkaAssetSynchronizer.sync_loc,
                "get_func": EnkaAssetSynchronizer.get_loc
            },
            "namecard": {
                "name": "namecard",
                "url": TestEnkaApi.get_name_card_json(),
                "parser": EnkaAssetParser.parse_name_card,
                "sync_func": EnkaAssetSynchronizer.sync_name_card,
                "get_func": EnkaAssetSynchronizer.get_name_card
            },
            "pfp": {
                "name": "pfp",
                "url": TestEnkaApi.get_pfp_json(),
                "parser": EnkaAssetParser.parse_pfp,
                "sync_func": EnkaAssetSynchronizer.sync_pfp,
                "get_func": EnkaAssetSynchronizer.get_pfp
            },
            "character": {
                "name": "character",
                "url": TestEnkaApi.get_character_json(),
                "parser": EnkaAssetParser.parse_character_meta,
                "sync_func": EnkaAssetSynchronizer.sync_character_meta,
                "get_func": EnkaAssetSynchronizer.get_character_meta
            }
        }

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

        for name, config in self._asset_configs.items():
            data = await fetch_and_parse(
                client=self._client,
                url=config["url"],
                parser=config["parser"]
            )
            config["sync_func"](data, self._db)
            self._asset_map[name] = config["get_func"](self._db)

        return self._asset_map

    async def refresh_asset(self, name):
        """从本地数据库获取静态资源"""
        if name not in self._asset_map.keys():
            self._asset_map[name] = self._asset_configs[name]["get_func"](self._db)
        return

    async def refresh_assets(self):
        """从本地数据库获取静态资源"""
        await self.refresh_asset("loc")
        await self.refresh_asset("namecard")
        await self.refresh_asset("pfp")
        await self.refresh_asset("character")
        return

    async def fetch_player(self, uid: str) -> Optional[Player]:
        """
        从enka获取最新的玩家信息

        :param uid: 玩家 UID
        :return: Player 实例 或 None
        """
        await self.refresh_assets()
        self._player = await fetch_and_parse(
            client=self._client,
            url=TestEnkaApi.get_player_url(uid),
            parser=lambda data: EnkaParser.parse_player(data, self._asset_map)
        )
        return self._player

    async def refresh_player(self):
        """
        从本地数据库获取玩家信息

        :return: Player 实例 或 None
        """
        if not self._player:
            self._player = rows_into_model_dict(self._db.extract_table("player"), Player)
        return

    def info_player(self) -> str:
        """
        返回一个支持国际化的玩家信息字符串表示

        :return: 本地化的字符串表示
        """
        return EnkaTextDisplayer.display_player(self._player,self._asset_map["loc"])

