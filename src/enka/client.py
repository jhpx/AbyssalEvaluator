from typing import Optional

import httpx

from src.enka.api import EnkaApi
from src.enka.config.constants import Language
from src.enka.model.player import Player
from src.enka.stage.api_parser import EnkaParser
from src.enka.stage.asset_parser import EnkaAssetParser
from src.enka.stage.synchronizer import EnkaAssetSynchronizer
from src.enka.test_api import TestEnkaApi
from src.util.http_util import fetch_and_parse


class EnkaClient:
    def __init__(self, lang: Language | str, proxy: str = None):
        self._client = httpx.AsyncClient(proxy=proxy)
        self._lang = self._convert_lang(lang)

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
        EnkaAssetSynchronizer.sync_loc(loc)

    async def get_assets(self):
        """从本地数据库获取静态资源"""
        self._text_map = {}

    async def fetch_player(self, uid: str) -> Optional[Player]:
        """
        从enka获取最新的玩家信息

        :param uid: 玩家 UID
        :return: Player 实例 或 None
        """
        return await fetch_and_parse(
            client=self._client,
            url=EnkaApi.get_player_url(uid),
            parser=EnkaParser.parse_player
        )

    async def get_player(self, uid: str, lang: str = 'zh') -> Optional[Player]:
        """
        从本地数据库获取玩家信息

        :param uid: 玩家 UID
        :param lang: 语言（默认为 'zh'）
        :return: Player 实例 或 None
        """
        player = await self.get_player(uid)
        if player:
            # 假设 compose_player 已被导入或移入合适模块
            from src.task.sync_enka import compose_player
            await compose_player(player, lang)

            import pickle
            with open(f"data\\player\\{player.uid}.pkl", "wb") as f:
                pickle.dump(player, f)
        return player
