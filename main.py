import anyio
from pathlib import Path

from src.enka.client import EnkaClient

from src.evaluator.algorithm.stat_based import YSINAlgorithm
from src.evaluator.algorithm.weight_based import XZSAlgorithm
from src.evaluator.evaluator import Evaluator


# from src.evaluator.artifact_evaluator import WeightBasedArtifactEvaluator as WAE
# from src.enka.model.character import Character
# from src.enka.model.stat import StatType
# from src.enka.model.player import Player
# from src.task import sync_hakush, sync_enka


async def main() -> None:
    async with EnkaClient("zh-cn", proxy="socks5h://127.0.0.1:4080") as api:
        # Update assets
        # 只有在 data/main.db 不存在时才执行 fetch_assets()
        if not Path("data/main.db").exists():
            await api.fetch_assets()
        # print(await api.get_asset("loc"))
        # print(await api.get_asset("namecard"))
        # print(await api.get_asset("pfp"))
        # print(await api.get_asset("character"))
        player = await api.fetch_player("101242308")
        ev = Evaluator(api, YSINAlgorithm())
        #ev = Evaluator(api, XZSAlgorithm())
        await ev.fetch_character_weights()
        # ev.refresh_weights()
        ev.evaluate_player(player)
        print(api.info_player())
        # player.characters[5] = ev.evaluate_character(player.characters[5])
        # print(api.info_character("神里绫华"))
    return None


# async def run_tasks():
#     await sync_hakush.main()
#     player = await sync_enka.main()
#     print_player(player)


if __name__ == "__main__":
    anyio.run(main)
    # # 从文件读取