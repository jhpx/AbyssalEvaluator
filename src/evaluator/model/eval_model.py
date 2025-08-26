from decimal import Decimal

from src.enka.model.artifact import Artifact
from src.enka.model.character import Character
from src.enka.model.stat import StatType
from src.evaluator.model.genre import Genre


class ArtifactEval(Artifact):
    def __init__(self, artifact: Artifact, score: Decimal = Decimal(0)):
        # 复制父类的所有属性
        super().__init__(**artifact.__dict__)
        # 添加新的字段
        self.score = score
        self.effective_rolls_dict: dict[StatType, Decimal] = dict()

    @property
    def effective_rolls(self) -> Decimal:
        return sum(self.effective_rolls_dict.values(), Decimal(0))

    def effective_rolls_clac(self, genre: Genre) -> Decimal:
        """
        计算加权的有效次数总和
        使用genre的clac_stat_weight方法作为权重
        """
        weight_values = [rolls * genre.clac_stat_weight(stat_type)
                         for stat_type, rolls in self.effective_rolls_dict.items()]
        return sum(weight_values, Decimal(0))


class CharacterEval(Character):
    def __init__(self, character: Character, total_score: Decimal = Decimal(0)):
        # 复制父类的所有属性
        super().__init__(**character.__dict__)
        # 添加新的字段
        self.genre = None
        self.total_score = total_score
        self.total_effective_rolls = Decimal(0)
