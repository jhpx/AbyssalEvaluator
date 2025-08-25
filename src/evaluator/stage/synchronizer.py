from src.core.duckdb.duckdb_engine import DuckDBSession
from src.core.util.duckdb_util import sync_list_to_duckdb, rows_into_model_dict
from src.evaluator.model.character_stat_weight import CharacterStatWeight


class LeanCloudSynchronizer:
    # 表名常量定义
    TABLE_CHARACTER_STAT_WEIGHT_XZS = "ods_character_stat_weight_xzs"
    TABLE_CHARACTER_STAT_WEIGHT_YM = "ods_character_stat_weight_ym"

    @staticmethod
    def sync_character_stat_weight_xzs(data: list[CharacterStatWeight], db: DuckDBSession):
        sync_list_to_duckdb(data, LeanCloudSynchronizer.TABLE_CHARACTER_STAT_WEIGHT_XZS, db, overwrite=False)

    @staticmethod
    def sync_character_stat_weight_ym(data: list[CharacterStatWeight], db: DuckDBSession):
        sync_list_to_duckdb(data, LeanCloudSynchronizer.TABLE_CHARACTER_STAT_WEIGHT_YM, db, overwrite=False)

    @classmethod
    def get_character_stat_weight_xzs(cls, db: DuckDBSession) -> dict[int, CharacterStatWeight]:
        return rows_into_model_dict(db.extract_table(cls.TABLE_CHARACTER_STAT_WEIGHT_XZS), CharacterStatWeight)

    @classmethod
    def get_character_stat_weight_ym(cls, db: DuckDBSession) -> dict[int, CharacterStatWeight]:
        return rows_into_model_dict(db.extract_table(cls.TABLE_CHARACTER_STAT_WEIGHT_YM), CharacterStatWeight)
