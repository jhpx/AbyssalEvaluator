from src.enka.model.artifact import Artifact
from src.enka.model.character import Character
from src.evaluator.model.genre import Genre


class ArtifactEval(Artifact):
    def __init__(self, artifact: Artifact, score: float = 0.0):
        # 复制父类的所有属性
        super().__init__(**artifact.__dict__)
        # 添加新的字段
        self.score = score
        self.effective_rolls_dict = dict()

    @property
    def effective_rolls(self) -> float:
        return sum(self.effective_rolls_dict.values())

    def effective_rolls_clac(self, genre: Genre) -> float:
        """
        计算加权的有效次数总和
        使用genre的clac_stat_weight方法作为权重
        """
        return sum(rolls * genre.clac_stat_weight(stat_type)
                   for stat_type, rolls in self.effective_rolls_dict.items())


class CharacterEval(Character):
    def __init__(self, character: Character, total_score: float = 0.0):
        # 复制父类的所有属性
        super().__init__(**character.__dict__)
        # 添加新的字段
        self.genre = None
        self.total_score = total_score
        self.total_effective_rolls = 0.0
