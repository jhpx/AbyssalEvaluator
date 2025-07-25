# artifact_weight.py

from src.enka.model.artifact import Artifact
from src.enka.model.stat import StatType

# 定义每个圣遗物词条的系数（小助手公式）
XZS_ARTIFACT_STAT_FACTORS = {
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
}

# 定义每个圣遗物词条的系数（刻晴办公桌公式）
KEQING_ARTIFACT_STAT_FACTORS = {
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
}

CHARACTER_STAT_WEIGHTS = {
    StatType.CRIT_RATE: 1,  # 暴击率
    StatType.CRIT_DMG: 1,  # 暴击伤害
    StatType.ATK_PERCENT: 0.5,  # 攻击百分比
    StatType.DEF_PERCENT: 1,  # 防御百分比
    StatType.ATK: 0.5,  # 攻击力
    StatType.DEF: 1,  # 防御力
    StatType.ELEMENTAL_CHARGE: 0.55,  # 充能效率
}


class WeightBasedArtifactEvaluator:
    """权重系数法实现圣遗物评分：如提瓦特小助手"""

    # 小助手的评分算法是：副词条得分 = 数值 * 均衡乘数 * 收益权重，例如暴击的均衡乘数是2，收益权重是100

    @classmethod
    def evaluate(cls, artifact: Artifact,
                 factor_dict: dict = XZS_ARTIFACT_STAT_FACTORS,
                 character_weight: dict = CHARACTER_STAT_WEIGHTS,
                 algorithm: str = "xzs") -> float:
        """
        根据预设的权重计算圣遗物的总评分。

        参数:
            artifact (Artifact): 一个包含圣遗物信息的对象。

        返回:
            float: 圣遗物的总评分。
        """
        total_score = 0.0

        # 副词条评分
        for sub_stat in artifact.sub_stats:
            if sub_stat.stat_type in factor_dict.keys():
                total_score += sub_stat.stat_value * factor_dict[sub_stat.stat_type] * character_weight.get(
                    sub_stat.stat_type, 0)
        if algorithm == "xzs" and artifact.main_stat.stat_type in [StatType.CRIT_DMG, StatType.CRIT_RATE]:
            total_score += 20
        elif algorithm == "ym" and artifact.main_stat.stat_type in factor_dict.keys():
            main_stat = artifact.main_stat
            # total_score += main_stat.stat_value * factor_dict[main_stat.stat_type] * 0.013 * character_weight.get(
            #     main_stat.stat_type, 0)
        artifact.score = total_score
        return total_score
