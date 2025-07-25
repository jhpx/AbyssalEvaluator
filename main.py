import pickle

import anyio

from src.enka.client import EnkaClient
# from src.evaluator.artifact_evaluator import WeightBasedArtifactEvaluator as WAE
# from src.enka.model.character import Character
# from src.enka.model.stat import StatType
# from src.enka.model.player import Player
# from src.task import sync_hakush, sync_enka


async def main() -> None:
    async with EnkaClient("en",proxy="http://127.0.0.1:4081") as api:
        # Update assets
        await api.fetch_assets()
    return None

# async def run_tasks():
#     await sync_hakush.main()
#     player = await sync_enka.main()
#     print_player(player)





if __name__ == "__main__":
    anyio.run(main)
    # # 从文件读取

