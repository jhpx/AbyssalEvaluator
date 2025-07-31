from src.core.duckdb.duckdb_engine import DuckDBSession
from src.enka.model.character_meta import CharacterMeta
from src.util.duckdb_util import sync_dict_to_duckdb, sync_list_to_duckdb, rows_into_model_dict


class EnkaAssetSynchronizer:
    # 表名常量定义
    TABLE_LOC = "ods_enka_loc"
    TABLE_NAME_CARD = "ods_enka_name_card"
    TABLE_PFP = "ods_enka_pfp"
    TABLE_CHARACTER_META = "ods_enka_character_meta"

    @staticmethod
    def sync_loc(data: dict[str, str], db: DuckDBSession):
        sync_dict_to_duckdb(data, EnkaAssetSynchronizer.TABLE_LOC, db, overwrite=True)

    @staticmethod
    def sync_name_card(data: dict[int, str], db: DuckDBSession):
        sync_dict_to_duckdb(data, EnkaAssetSynchronizer.TABLE_NAME_CARD, db, overwrite=True)

    @staticmethod
    def sync_pfp(data: dict[int, str], db: DuckDBSession):
        sync_dict_to_duckdb(data, EnkaAssetSynchronizer.TABLE_PFP, db, overwrite=True)

    @staticmethod
    def sync_character_meta(data: list[CharacterMeta], db: DuckDBSession):
        sync_list_to_duckdb(data, EnkaAssetSynchronizer.TABLE_CHARACTER_META, db, overwrite=True)

    @staticmethod
    def get_loc(db: DuckDBSession) -> dict[str, str]:
        return rows_into_model_dict(db.extract_table(EnkaAssetSynchronizer.TABLE_LOC), str)

    @staticmethod
    def get_name_card(db: DuckDBSession) -> dict[int, str]:
        return rows_into_model_dict(db.extract_table(EnkaAssetSynchronizer.TABLE_NAME_CARD), str)

    @staticmethod
    def get_pfp(db: DuckDBSession) -> dict[int, str]:
        return rows_into_model_dict(db.extract_table(EnkaAssetSynchronizer.TABLE_PFP), str)

    @staticmethod
    def get_character_meta(db: DuckDBSession) -> dict[str, CharacterMeta]:
        return rows_into_model_dict(db.extract_table(EnkaAssetSynchronizer.TABLE_CHARACTER_META), CharacterMeta)
