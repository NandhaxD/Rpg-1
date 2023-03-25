from pyrogram import *
from pyrogram.types import *

from Sylvie import *
from Sylvie.plugins.buttons import *
from Database import *

@bot.on_messge(filters.command("start"))
async def start(_, message):
    nickname = await db.persons.find_one({"user_id": user_id})
    if nickname is None:
        answer await message.chat.ask("**Send Me Your name:**", parse_mode=enums.ParseMode.MARKDOWN)
        new_one = Persons(user_id=message.from_user.id, name=answer.text, level=1, hp=10, cur_hp=10, money=50, attack=1, magic_attack=0,
                    xp=0, armour=0, magic_armour=0, location_id=1)
        await db.persons.insert_one(new_one)
        await answer.request.delete()
        await bot.send_message(message.chat.id,
                               f"**You Have Successfully Registered. Welcome To The Game, {message.from_user.mention}!**")
        cur_town_id = (await db.persons.find_one({"user_id": message.from_user.id}))["location_id"]
        cur_town = (await db.locations.find_one({"location_id": cur_loc_id}))["location_name"]
        await bot.send_message(message.chat.id, f"`You Are In The City:` 🏰 **{cur_town}**", reply_markup=town_markup,
                               parse_mode=enums.ParseMode.MARKDOWN)
    else:
        cur_loc_id = (await db.persons.find_one({"user_id": message.from_user.id}))["location_id"]
        if cur_loc_id == -1:
            pass
        else:
            cur_loc_type = (await db.locations.find_one({"location_id": cur_loc_id}))["location_type"]
            if cur_loc_type == "town":
                cur_town = (await db.locations.find_one({"location_id": cur_loc_id}))["location_name"]
                await bot.send_message(message.chat.id, f"`You Are In The City:` 🏰 **{cur_town}**", reply_markup=town_markup,
                                       parse_mode=enums.ParseMode.MARKDOWN)
            elif cur_loc_type == "dungeon":
                cur_dungeon = (await db.locations.find_one({"location_id": cur_loc_id}))["location_name"]
                await bot.send_message(message.chat.id, f"`You Are In The Dungeon:` ⛰️ **{cur_dungeon}**", reply_markup=town_markup,
                                       parse_mode=enums.ParseMode.MARKDOWN)
