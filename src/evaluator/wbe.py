# artifact_weight.py

from types import MappingProxyType

import httpx

from src.core.util.http_util import fetch_and_parse
from src.enka.model.artifact import Artifact
from src.enka.model.character import Character
from src.enka.model.player import Player
from src.enka.model.stat import StatType
from src.evaluator.config.constants import APP_ID, APP_KEY, CLASS_CHARACTER_STAT_WEIGHT, LEANCLOUD_BASE_URL
from src.evaluator.model.eval_model import CharacterEval, ArtifactEval
from src.evaluator.stage.leancloud_parser import LeanCloudParser

# 定义每个圣遗物词条的系数（小助手公式）
XZS_ARTIFACT_STAT_FACTORS = MappingProxyType({
    StatType.CRIT_RATE: 2.0,  # 暴击率
    StatType.CRIT_DMG: 1.0,  # 暴击伤害
    StatType.ATK_PERCENT: 1.33,  # 攻击百分比
    StatType.HP_PERCENT: 1.33,  # 生命百分比
    StatType.DEF_PERCENT: 1.06,  # 防御百分比
    StatType.ATK: 0.398 * 0.5,  # 攻击力 0.199
    StatType.HP: 0.026 * 0.66,  # 生命值 0.01716
    StatType.DEF: 0.335 * 0.66,  # 防御力 0.2211
    StatType.ELEMENTAL_MASTERY: 0.33,  # 元素精通
    StatType.ELEMENTAL_CHARGE: 1.1979,  # 充能效率
})

# 定义每个圣遗物词条的系数（刻晴办公桌公式）
KEQING_ARTIFACT_STAT_FACTORS = MappingProxyType({
    StatType.CRIT_RATE: 2.0,  # 暴击率
    StatType.CRIT_DMG: 1.0,  # 暴击伤害
    StatType.ATK_PERCENT: 1.331429,  # 攻击百分比
    StatType.HP_PERCENT: 1.331429,  # 生命百分比
    StatType.DEF_PERCENT: 1.066362,  # 防御百分比
    StatType.ATK: 0.199146,  # 攻击力
    StatType.HP: 0.012995,  # 生命值
    StatType.DEF: 0.162676,  # 防御力
    StatType.ELEMENTAL_MASTERY: 0.332857,  # 元素精通
    StatType.ELEMENTAL_CHARGE: 1.197943,  # 充能效率
})

DEFAULT_CHARACTER_WEIGHTS = {
    StatType.CRIT_RATE: 1,  # 暴击率
    StatType.CRIT_DMG: 1,  # 暴击伤害
    StatType.ATK_PERCENT: 1,  # 攻击百分比
    StatType.ATK: 1,  # 攻击力
    StatType.ELEMENTAL_CHARGE: 1,  # 充能效率
}


class WeightBasedEvaluator:
    """权重系数法实现圣遗物评分：如提瓦特小助手

    小助手的评分算法是：副词条得分 = 数值 * 均衡乘数 * 角色收益权重，圣遗物得分为副词条得分之和，如果头冠是暴击/爆伤，加20分
    """

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

    def evaluate_artifact(self, artifact: Artifact, character_id: int,
                          factor_dict: dict = XZS_ARTIFACT_STAT_FACTORS,
                          algorithm: str = "xzs") -> ArtifactEval:
        """
        根据预设的权重计算圣遗物的总评分。

        参数:
            artifact (Artifact): 一个包含圣遗物信息的对象。
        返回:
            float: 圣遗物的总评分。
        """
        result = ArtifactEval(artifact)
        weights = self.character_weights_map.get(character_id, DEFAULT_CHARACTER_WEIGHTS)

        # 副词条评分
        for sub_stat in artifact.sub_stats:
            if sub_stat.stat_type in factor_dict.keys():
                result.score += round(sub_stat.stat_value * factor_dict[sub_stat.stat_type]
                                 * weights.get(sub_stat.stat_type, 0) / 100,0)
        if algorithm == "xzs":
            result.score = round(result.score, 0)
            if artifact.main_stat.stat_type in [StatType.CRIT_DMG, StatType.CRIT_RATE]:
                result.score += 20

        return result

    def evaluate_character(self, character: Character, factor_dict: dict = XZS_ARTIFACT_STAT_FACTORS,
                           algorithm: str = "xzs") -> CharacterEval:
        result = CharacterEval(character)
        artifact_evals = [self.evaluate_artifact(aft, character.id, factor_dict, algorithm)
                          for aft in character.artifacts]
        result.total_score = sum(aft.score for aft in artifact_evals)
        result.artifacts = artifact_evals
        return result

    def evaluate_player(self, player: Player, factor_dict: dict = XZS_ARTIFACT_STAT_FACTORS,
                        algorithm: str = "xzs"):
        """计算玩家角色携带的所有圣遗物"""
        player.characters = [self.evaluate_character(c, factor_dict, algorithm) for c in player.characters]
