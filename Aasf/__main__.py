import asyncio
from pyrogram import *

from Aasf import app
from Aasf.Database import *
from Aasf.plugins import *

FORMAT = "%(message)s"

async def check_inactive_users_loop():
    while True:
        await check_inactive_users(app)
        await asyncio.sleep(0.1)

if __name__ == "__main__":
    logging.basicConfig(
        handlers=[logging.FileHandler("logs.txt"), logging.StreamHandler()],
        level=logging.DEBUG,
        format=FORMAT,
        datefmt="[%X]",
    )
    logging.getLogger("pyrogram").setLevel(logging.INFO)
    for module in ALL_MODULES:
        importlib.import_module("Aasf.plugins." + module)
    idle()
    asyncio.create_task(check_inactive_users_loop())
    while True:
        await asyncio.sleep(1)
