from src.core.duckdb.duckdb_engine import DuckDBSession
from src.util.duckdb_util import sync_dict_to_duckdb


class EnkaAssetSynchronizer:

    @staticmethod
    def sync_loc(data: dict):
        sync_dict_to_duckdb(data, "loc", DuckDBSession())