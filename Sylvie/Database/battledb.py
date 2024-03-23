import time
import random 
import datetime

from Sylvie import *
from pyrogram import *
from pyrogram.types import*

async def on_battle(user_id: int):
  is_battling = await db.find_one({"player": user_id})
  if is_battling:
    return True
  else:
    return False
    
async def create_battle(user_id: int, enemy, cq):
  start = time.time()
  current_time = datetime.datetime.now()
  unique_code = current_time.strftime("%Y%m%d%H%M%S") + str(random.randint(1000, 9999))
  is_battling = await on_battle(user_id)
  if is_battling:
    return False
  else:
      await db.battle.insert_one({"battle_id": unique_code, "player": user_id, "enemy": enemy, "time": time.time(), "message_id": cq.message.id})
      return unique_code

async def end_battle(user_id: int):
  is_battling = await on_battle(user_id)
  if not is_battling:
    return False
  else:
    await db.battle.delete_one({"player": user_id})
    return True
    
async def check_inactive_users(app):
    async for x in db.battle.find():
        if time.time() - float(x["time"]) > 60:
                death_markup = InlineKeyboardMarkup([[InlineKeyboardButton("Be Reborn", callback_data="revive")]])
                await app.edit_message.text(chat_id=x["player"], message_id=x["message_id"], "`You Fell Asleep On The Battlefield And Became An Easy Target For The Enemy.`\n\n"
                                         f"**You Perished! :(**", reply_markup=death_markup,
                                    parse_mode=enums.ParseMode.MARKDOWN)
                await end_battle(x["player"]) 
