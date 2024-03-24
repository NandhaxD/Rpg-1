import asyncio
import logging
import importlib
from pyrogram import *
from apscheduler.schedulers.background import BackgroundScheduler

from Aasf import app
from Aasf.Database import *
from Aasf.plugins import *

FORMAT = "%(message)s"

async def main():
    logging.basicConfig(
        handlers=[logging.FileHandler("logs.txt"), logging.StreamHandler()],
        level=logging.DEBUG,
        format=FORMAT,
        datefmt="[%X]",
    )
    logging.getLogger("pyrogram").setLevel(logging.INFO)
    for module in ALL_MODULES:
      importlib.import_module("Aasf.plugins." + module)
    await idle()
    scheduler = BackgroundScheduler()
    scheduler.add_job(check_inactive_users, "interval", seconds=0.1, args=[app])
    scheduler.start()
    await asyncio.get_event_loop().run_forever()

if __name__ == "__main__":
    asyncio.run(main())
