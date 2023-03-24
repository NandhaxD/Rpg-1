import asyncio
from Database.classes import *
from Sylvie import *

async def go_loc(user_id, loc_id, message):
    user = await db.persons.find_one({"user_id": user_id})
    user["LocationID"] = loc_id
    await db.persons.replace_one({"user_id": user_id}, user)
    if loc_id > 0:
        cur_place = (await db.locations.find_one({"LocationID": loc_id}))["LocationType"]
        if cur_place == 'town':
            await get_town(message)
        elif cur_place == 'dungeon':
            await get_dungeon(message)


async def get_town(message):
    cur_town_id = (await db.persons.find_one({"user_id": message.from_user.id}))["LocationID"]
    cur_town = (await db.locations.find_one({"LocationID": cur_town_id}))["LocationName"]
    player = await db.persons.find_one({"user_id": message.from_user.id})
    player["CurHP"] = player["HP"]
    await bot.edit_message_text(chat_id=message.chat.id, message_id=message.id,
                                text=f"You Are In The City: 🏰 *{cur_town}*", reply_markup=bot.town_markup, parse_mode="Markdown")


async def get_dungeon(message):
    cur_dungeon_id = (await db.persons.find_one({"user_id": message.from_user.id}))["LocationID"]
    cur_dungeon = (await db.locations.find_one({"LocationID": cur_dungeon_id}))["LocationName"]
    await bot.edit_message_text(chat_id=message.chat.id, message_id=message.id,
                                text=f"You Are In The Dungeon: ⛰️ *{cur_dungeon}*", reply_markup=bot.dungeon_gate_markup,
                                parse_mode="Markdown")


async def get_map(message):
    cur_town_id = (await db.persons.find_one({"user_id": message.from_user.id}))["LocationID"]
    cur_town_x = (await db.locations.find_one({"LocationID": cur_town_id}))["XCoord"]
    cur_town_y = (await db.locations.find_one({"LocationID": cur_town_id}))["YCoord"]
    destinations = db.locations.find()
    text = '*Available Locations:*\n\n'
    async for el in destinations:
        dist = round(count_distance(cur_town_x, cur_town_y, el["XCoord"], el["YCoord"]))
        if 0 < dist <= 10:
            text += f"{el['LocationName']} - {dist} Km 🛣️\n\n"
    if cur_town_id == 1:
        await bot.edit_message_text(chat_id=message.chat.id, message_id=message.id,
                                    text=text, reply_markup=bot.choose_location_1_markup,
                                    parse_mode="Markdown")
    elif cur_town_id == 2:
        await bot.edit_message_text(chat_id=message.chat.id, message_id=message.id,
                                    text=text, reply_markup=bot.choose_location_2_markup,
                                    parse_mode="Markdown")
    elif cur_town_id == 3:
        await bot.edit_message_text(chat_id=message.chat.id, message_id=message.id,
                                    text=text, reply_markup=bot.choose_location_3_markup,
                                    parse_mode="Markdown")
    elif cur_town_id == 4:
        await bot.edit_message_text(chat_id=message.chat.id, message_id=message.id,
                                    text=text, reply_markup=bot.choose_location_4_markup,
                                    parse_mode="Markdown")

def count_distance(x1, y1, x2, y2):
    return ((x1 - x2) ** 2 + (y1 - y2) ** 2) ** (1 / 2))
