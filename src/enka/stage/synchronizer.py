from src.core.duckdb.duckdb_engine import DuckDBSession
from src.util.duckdb_util import sync_dict_to_duckdb


class EnkaAssetSynchronizer:

    @staticmethod
    def sync_loc(data: dict, db: DuckDBSession):
        sync_dict_to_duckdb(data, "loc", db)

    @staticmethod
    def sync_namecard(data: dict, db: DuckDBSession):
        sync_dict_to_duckdb(data, "namecard", db)

    @staticmethod
    def sync_pfp(data: dict, db: DuckDBSession):
        sync_dict_to_duckdb(data, "pfp", db)
