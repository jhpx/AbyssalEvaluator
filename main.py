import anyio

from src.task import syncHakush, syncEnka

async def run_tasks():
    await syncHakush.main()
    # await syncEnka.main()

if __name__ == "__main__":
    anyio.run(run_tasks)