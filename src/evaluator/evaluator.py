from src.core.util.http_util import fetch_and_parse
from src.enka.client import EnkaClient
from src.enka.model.player import Player
from src.evaluator.algorithm.stat_based import YSINAlgorithm
from src.evaluator.algorithm.weight_based import XZSAlgorithm
from src.evaluator.config.constants import APP_ID, APP_KEY, CLASS_CHARACTER_STAT_WEIGHT, LEANCLOUD_BASE_URL
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

        url = f"{LEANCLOUD_BASE_URL}/1.1/classes/{CLASS_CHARACTER_STAT_WEIGHT}"

        character_stat_weights = await fetch_and_parse(
            client=self._enka_client.client,
            url=url,
            parser=LeanCloudParser.parse_character_weight,
            headers=headers
        )
        # 同步入库并从数据库重新载入缓存
        LeanCloudSynchronizer.sync_character_stat_weight_xzs(character_stat_weights, self._enka_client.db)
        self._character_weights_map = LeanCloudSynchronizer.get_character_stat_weight_xzs(self._enka_client.db)

        return self._character_weights_map

    def evaluate_player(self, player: Player):
        return self.algorithm.evaluate_player(player, self._character_weights_map)
