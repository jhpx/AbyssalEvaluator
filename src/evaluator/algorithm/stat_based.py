# sbe.py

from types import MappingProxyType

from src.enka.config.prop_stat import FightPropType
from src.enka.model.artifact import Artifact
from src.enka.model.character import Character
from src.enka.model.stat import StatType, FIX_STAT_TYPES
from src.evaluator.model.eval_model import CharacterEval, ArtifactEval
from src.evaluator.model.genre import Genre


class YSINAlgorithm:
    """词条统计法实现圣遗物评分：如YSIN

    YSIN的词条评分算法是：圣遗物得分 = 目前圣遗物词条数 / 默认圣遗物词条数 * 100
    词条标准收益
    """
    REMOTE_WEIGHT_TABLE = "CharacterStatWeight_XZS"

    # 定义每个圣遗物词条的标准收益（默认）
    __SUB_STAT_BENEFIT = MappingProxyType({
        StatType.CRIT_RATE: 3.3,  # 暴击率
        StatType.CRIT_DMG: 6.6,  # 暴击伤害
        StatType.ATK_PERCENT: 4.975,  # 攻击百分比
        StatType.HP_PERCENT: 4.975,  # 生命百分比
        StatType.DEF_PERCENT: 6.2,  # 防御百分比
        StatType.ELEMENTAL_MASTERY: 19.75,  # 元素精通
        StatType.ELEMENTAL_CHARGE: 5.5,  # 充能效率
    })

    def evaluate_artifact(self, artifact: Artifact, character: Character,
                          genre: Genre) -> ArtifactEval:
        """
        根据预设的权重计算圣遗物的总评分。

        参数:
            artifact (Artifact): 一个包含圣遗物信息的对象。
        返回:
            float: 圣遗物的总评分。
        """
        result = ArtifactEval(artifact)

        # 副词条收益统计
        for sub_stat in artifact.sub_stats:
            clac_type = sub_stat.stat_type
            # 固定词条折算成百分比词条
            if clac_type in FIX_STAT_TYPES:
                prop_type = FightPropType.from_name(clac_type.value.replace("PROP_", "PROP_BASE_"))
                base_prop = character.fight_prop.get(prop_type) / 100.0
                # 利用名称构造枚举
                clac_type = StatType.from_name(clac_type.name + "_PERCENT")
            else:
                base_prop = 1
            # 计算有效词条数
            if clac_type in self.__SUB_STAT_BENEFIT.keys() and clac_type in genre.effective_stats:
                weight = genre.effective_stat_weight(clac_type)
                effective_roll = sub_stat.stat_value * weight / base_prop / self.__SUB_STAT_BENEFIT[clac_type]
            else:
                effective_roll = 0.0
            result.effective_rolls_dict[sub_stat.stat_type] = round(effective_roll, 2)

        return result

    def evaluate_character(self, character: Character, weights: dict[StatType, int]) -> CharacterEval:

        result = CharacterEval(character)
        result.genre = Genre.from_weights(weights)
        artifact_evals = [self.evaluate_artifact(aft, character, result.genre)
                          for aft in character.artifacts]
        result.total_effective_rolls = sum(aft.effective_rolls for aft in artifact_evals)
        total_effective_rolls_clac = sum(aft.effective_rolls_clac(result.genre) for aft in artifact_evals)

        # 计算总分
        result.total_score = round(total_effective_rolls_clac * 100 / result.genre.default_effective_rolls(), 2)
        result.artifacts = artifact_evals
        return result
