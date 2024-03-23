import logging
import asyncio
import importlib
from pyrogram import *

from Sylvie import *
from Sylvie.Database import *
from Sylvie.plugins import *

FORMAT = "%(message)s"

def main():
    logging.basicConfig(
        handlers=[logging.FileHandler("logs.txt"), logging.StreamHandler()],
        level=logging.INFO,
        format=FORMAT,
        datefmt="[%X]",
    )
    for module in ALL_MODULES:
      importlib.import_module("Sylvie.plugins." + module)
    logging.getLogger("pyrogram").setlevel(logging.INFO)    
    idle()

    while True:
        check_inactive_users(app)
        asyncio.sleep(0.1)
    
if __name__ == "__main__":
    main()
