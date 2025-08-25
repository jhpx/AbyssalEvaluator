from src.core.duckdb.duckdb_engine import DuckDBSession
from src.enka.model.character_meta import CharacterMeta
from src.core.util.duckdb_util import sync_dict_to_duckdb, sync_list_to_duckdb, rows_into_model_dict


class EnkaAssetSynchronizer:
    # 表名常量定义
    TABLE_LOC = "ods_enka_loc"
    TABLE_NAME_CARD = "ods_enka_name_card"
    TABLE_PFP = "ods_enka_pfp"
    TABLE_CHARACTER_META = "ods_enka_character_meta"

    @classmethod
    def sync_loc(cls, data: dict[str, str], db: DuckDBSession):
        sync_dict_to_duckdb(data, cls.TABLE_LOC, db, overwrite=False)

    @classmethod
    def sync_name_card(cls, data: dict[int, str], db: DuckDBSession):
        sync_dict_to_duckdb(data, cls.TABLE_NAME_CARD, db, overwrite=False)

    @classmethod
    def sync_pfp(cls, data: dict[int, str], db: DuckDBSession):
        sync_dict_to_duckdb(data, cls.TABLE_PFP, db, overwrite=False)

    @classmethod
    def sync_character_meta(cls, data: list[CharacterMeta], db: DuckDBSession):
        sync_list_to_duckdb(data, cls.TABLE_CHARACTER_META, db, overwrite=False)

    @classmethod
    def sync(cls, name: str, data, db: DuckDBSession):
        sync_dict = {
            "character": cls.sync_character_meta,
            "name_card": cls.sync_name_card,
            "pfp": cls.sync_pfp,
            "loc": cls.sync_loc,
        }
        return sync_dict[name](data, db)

    @classmethod
    def get_loc(cls, db: DuckDBSession) -> dict[str, str]:
        return rows_into_model_dict(db.extract_table(cls.TABLE_LOC), str)

    @classmethod
    def get_name_card(cls, db: DuckDBSession) -> dict[int, str]:
        return rows_into_model_dict(db.extract_table(cls.TABLE_NAME_CARD), str)

    @classmethod
    def get_pfp(cls, db: DuckDBSession) -> dict[int, str]:
        return rows_into_model_dict(db.extract_table(cls.TABLE_PFP), str)

    @classmethod
    def get_character_meta(cls, db: DuckDBSession) -> dict[int, CharacterMeta]:
        return rows_into_model_dict(db.extract_table(cls.TABLE_CHARACTER_META), CharacterMeta)

    @classmethod
    def get(cls, name: str, db: DuckDBSession):
        get_dict = {
            "character": cls.get_character_meta,
            "name_card": cls.get_name_card,
            "pfp": cls.get_pfp,
            "loc": cls.get_loc,
        }
        return get_dict[name](db)
