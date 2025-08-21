import httpx

from src.core.util.http_util import fetch_and_parse
from src.evaluator.config.constants import APP_ID, APP_KEY, CLASS_CHARACTER_STAT_WEIGHT, LEANCLOUD_BASE_URL
from src.evaluator.stage.leancloud_parser import LeanCloudParser


class BaseEvaluator:

    def __init__(self):
        self.character_weights_map = {}

    async def fetch_character_weights(self):
        if self.character_weights_map:
            return None

        headers = {
            "X-LC-Id": APP_ID,
            "X-LC-Key": APP_KEY,
            "Content-Type": "application/json"
        }

        url = f"{LEANCLOUD_BASE_URL}/1.1/classes/{CLASS_CHARACTER_STAT_WEIGHT}"

        self.character_weights_map = await fetch_and_parse(
            client=httpx.AsyncClient(proxy="http://127.0.0.1:4081"),
            url=url,
            parser=LeanCloudParser.parse_character_weight,
            headers=headers
        )
        return None
