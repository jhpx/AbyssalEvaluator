# wbe.py
from decimal import Decimal
from types import MappingProxyType

from src.enka.model.artifact import Artifact
from src.enka.model.character import Character
from src.enka.model.stat import StatType
from src.evaluator.model.eval_model import CharacterEval, ArtifactEval


class XZSAlgorithm:
    """权重系数法实现圣遗物评分：如提瓦特小助手

    小助手的评分算法是：副词条得分 = 数值 * 均衡乘数 * 角色收益权重，圣遗物得分为副词条得分之和，如果头冠是暴击/爆伤，加20分
    """
    REMOTE_WEIGHT_TABLE = "CharacterStatWeight_XZS"

    # 定义每个圣遗物词条的系数（小助手公式）
    __XZS_ARTIFACT_STAT_FACTORS = MappingProxyType({
        StatType.CRIT_RATE: Decimal(2.0),  # 暴击率
        StatType.CRIT_DMG: Decimal(1.0),  # 暴击伤害
        StatType.ATK_PERCENT: Decimal(1.33),  # 攻击百分比
        StatType.HP_PERCENT: Decimal(1.33),  # 生命百分比
        StatType.DEF_PERCENT: Decimal(1.06),  # 防御百分比
        StatType.ATK: Decimal(0.398) * Decimal(0.5),  # 攻击力 0.199
        StatType.HP: Decimal(0.026) * Decimal(0.66),  # 生命值 0.01716
        StatType.DEF: Decimal(0.335) * Decimal(0.66),  # 防御力 0.2211
        StatType.ELEMENTAL_MASTERY: Decimal(0.33),  # 元素精通
        StatType.ELEMENTAL_CHARGE: Decimal(1.1979),  # 充能效率
    })

    # 定义每个圣遗物词条的系数（刻晴办公桌公式）
    __KEQING_ARTIFACT_STAT_FACTORS = MappingProxyType({
        StatType.CRIT_RATE: Decimal(2.0),  # 暴击率
        StatType.CRIT_DMG: Decimal(1.0),  # 暴击伤害
        StatType.ATK_PERCENT: Decimal(1.331429),  # 攻击百分比
        StatType.HP_PERCENT: Decimal(1.331429),  # 生命百分比
        StatType.DEF_PERCENT: Decimal(1.066362),  # 防御百分比
        StatType.ATK: Decimal(0.199146),  # 攻击力
        StatType.HP: Decimal(0.012995),  # 生命值
        StatType.DEF: Decimal(0.162676),  # 防御力
        StatType.ELEMENTAL_MASTERY: Decimal(0.332857),  # 元素精通
        StatType.ELEMENTAL_CHARGE: Decimal(1.197943),  # 充能效率
    })

    def __init__(self):
        self.factor_dict = self.__XZS_ARTIFACT_STAT_FACTORS

    def evaluate_artifact(self, artifact: Artifact, character: Character,
                          weights: dict[StatType, int]) -> ArtifactEval:
        """
        根据预设的权重计算圣遗物的总评分。

        参数:
            artifact (Artifact): 一个包含圣遗物信息的对象。
        返回:
            Decimal: 圣遗物的总评分。
        """
        result = ArtifactEval(artifact)

        # 副词条评分
        for sub_stat in artifact.sub_stats:
            if sub_stat.stat_type in self.factor_dict.keys():
                result.score +=  round(sub_stat.stat_value * self.factor_dict[sub_stat.stat_type] * weights.get(sub_stat.stat_type, 0) / 100, 1)

        result.score = round(result.score, 0)
        if artifact.main_stat.stat_type in [StatType.CRIT_DMG, StatType.CRIT_RATE]:
            result.score += 20

        return result

    def evaluate_character(self, character: Character, weights: dict[StatType, int]) -> CharacterEval:
        result = CharacterEval(character)
        artifact_evals = [self.evaluate_artifact(aft, character, weights)
                          for aft in character.artifacts]
        result.total_score = sum(aft.score for aft in artifact_evals)
        result.artifacts = artifact_evals
        return result
