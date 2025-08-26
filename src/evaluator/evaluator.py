from src.core.util.http_util import fetch_and_parse
from src.enka.client import EnkaClient
from src.enka.model.character import Character
from src.enka.model.player import Player
from src.evaluator.algorithm.stat_based import YSINAlgorithm
from src.evaluator.algorithm.weight_based import XZSAlgorithm
from src.evaluator.config.constants import APP_ID, APP_KEY, LEANCLOUD_BASE_URL
from src.evaluator.model.character_stat_weight import CharacterStatWeight
from src.evaluator.model.genre import GENRE_DEFAULT
from src.evaluator.stage.leancloud_parser import LeanCloudParser
from src.evaluator.stage.synchronizer import LeanCloudSynchronizer


class Evaluator:
    # 算法
    algorithm: YSINAlgorithm | XZSAlgorithm

    def __init__(self, client: EnkaClient, algorithm: YSINAlgorithm | XZSAlgorithm):
        self.algorithm = algorithm
        self._enka_client = client
        self._character_weights_map = {}

    async def fetch_character_weights(self):
        # 从LeanCloud获取数据
        headers = {
            "X-LC-Id": APP_ID,
            "X-LC-Key": APP_KEY,
            "Content-Type": "application/json"
        }

        url = f"{LEANCLOUD_BASE_URL}/1.1/classes/{self.algorithm.REMOTE_WEIGHT_TABLE}"

        character_stat_weights = await fetch_and_parse(
            client=self._enka_client.client,
            url=url,
            parser=LeanCloudParser.parse_character_weight,
            headers=headers
        )
        # 同步入库并从数据库重新载入缓存
        algorithm_name = self.algorithm.__class__.__name__
        LeanCloudSynchronizer.sync(algorithm_name, character_stat_weights, self._enka_client.db)
        self._character_weights_map = LeanCloudSynchronizer.get(algorithm_name, self._enka_client.db)

        return self._character_weights_map

    def refresh_weights(self):
        algorithm_name = self.algorithm.__class__.__name__
        data = LeanCloudSynchronizer.get(algorithm_name, self._enka_client.db)
        if data:
            self._character_weights_map = data
        return

    def evaluate_player(self, player: Player):
        """计算玩家角色携带的所有圣遗物"""
        self.refresh_weights()
        player.characters = [self.evaluate_character(c) for c in player.characters]
        return

    def evaluate_character(self, character: Character):
        """计算角色携带的所有圣遗物"""
        if character.id in self._character_weights_map:
            weights = self._character_weights_map.get(character.id).to_dict()
        elif self._character_weights_map:
            weights = GENRE_DEFAULT.effective_stat_weights()
        else:
            raise ValueError("没有找到角色权重")

        return self.algorithm.evaluate_character(character, weights)
