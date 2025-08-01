# artifact_weight.py

from types import MappingProxyType

from src.enka.model.artifact import Artifact
from src.enka.model.character import Character
from src.enka.model.player import Player
from src.enka.model.stat import StatType
from src.evaluator.model.eval_model import CharacterEval, ArtifactEval

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

    def fetch_character_weights(self):
        self.character_weights_map = {}

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
                result.score += sub_stat.stat_value * factor_dict[sub_stat.stat_type] * weights.get(sub_stat.stat_type,
                                                                                                    0)
        if algorithm == "xzs" and artifact.main_stat.stat_type in [StatType.CRIT_DMG, StatType.CRIT_RATE]:
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
