from src.enka.model.artifact import Artifact
from src.enka.model.character import Character


class ArtifactEval(Artifact):
    def __init__(self, artifact: Artifact, score: float = 0.0):
        # 复制父类的所有属性
        super().__init__(**artifact.__dict__)
        # 添加新的字段
        self.score = score


class CharacterEval(Character):
    def __init__(self, character: Character, total_score: float = 0.0):
        # 复制父类的所有属性
        super().__init__(**character.__dict__)
        # 添加新的字段
        self.total_score = total_score
