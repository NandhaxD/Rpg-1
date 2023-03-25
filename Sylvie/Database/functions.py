import asyncio
from Sylvie import *
from motor.motor_asyncio import AsyncIOMotorClient as async_mongo
from config import *

async_mongo_client = async_mongo(MONGO_URI)
db = async_mongo_client.Sylvie

def get_item_by_name(name):
    item = db.items.find_one({"name": name})
    return item

def get_location_by_name(name):
    location = db.locations.find_one({"location_name": name})
    return location

def get_mob_by_name(name):
    mob = db.mobs.find_one({"mob_name": name})
    return mob

def create_item(item_data):
    result = db.items.insert_one(item_data)
    return result

def create_location(location_data):
    result = db.locations.insert_one(location_data)
    return result

def create_mob(mob_data):
    result = db.mobs.insert_one(mob_data)
    return result

async def go_loc(user_id, loc_id, message):
    user = await db.persons.find_one({"user_id": user_id})
    user['location_id'] = loc_id
    await db.persons.replace_one({"user_id": user_id}, user)
    if loc_id > 0:
        cur_place = (await db.locations.find_one({"location_id": loc_id}))['location_type']
        if cur_place == "town":
            await get_town(message)
        elif cur_place == "dungeon":
            await get_dungeon(message)


async def get_town(message):
    cur_town_id = (await db.persons.find_one({"user_id": message.from_user.id}))['location_id']
    cur_town = (await db.locations.find_one({"location_id": cur_town_id}))['location_name']
    player = await db.persons.find_one({"user_id": message.from_user.id})
    player['cur_hp'] = player['hp']
    await bot.edit_message_text(chat_id=message.chat.id, message_id=message.id,
                                text=f"You Are In The City: 🏰 *{cur_town}*", reply_markup=bot.town_markup, parse_mode="Markdown")


async def get_dungeon(message):
    cur_dungeon_id = (await db.persons.find_one({"user_id": message.from_user.id}))['location_id']
    cur_dungeon = (await db.locations.find_one({"location_id": cur_dungeon_id}))['location_name']
    await bot.edit_message_text(chat_id=message.chat.id, message_id=message.id,
                                text=f"You Are In The Dungeon: ⛰️ *{cur_dungeon}*", reply_markup=bot.dungeon_gate_markup,
                                parse_mode="Markdown")


async def get_map(message):
    cur_town_id = (await db.persons.find_one({"user_id": message.from_user.id}))['location_id']
    cur_town_x = (await db.locations.find_one({"location_id": cur_town_id}))['x_coord']
    cur_town_y = (await db.locations.find_one({"location_id": cur_town_id}))['y_coord']
    destinations = db.locations.find()
    text = "*Available Locations:*\n\n"
    async for el in destinations:
        dist = round(count_distance(cur_town_x, cur_town_y, el['x_coord'], el['y_coord']))
        if 0 < dist <= 10:
            text += f"{el['location_name']} - {dist} Km 🛣️\n\n"
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
    return ((x1 - x2) ** 2 + (y1 - y2) ** 2) ** (1 / 2)
