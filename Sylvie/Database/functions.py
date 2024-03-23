import asyncio

from Sylvie import *
from Sylvie.Database import *

from pyrogram import *
from pyrogram.types import * 

def count_distance(x1, y1, x2, y2):
    return ((x1 - x2) ** 2 + (y1 - y2) ** 2) ** (1 / 2)
    
async def go_loc(user_id, loc_id, message):
    player = await get_player(user_id)
    player['location_id'] = loc_id
    await update_player(user_id, player)
    if loc_id > 0:
        cur_place = await get_location(loc_id)
        if cur_place['location_type'] == "town":
            await get_town(message)
        elif cur_place['location_type'] == "dungeon":
            await get_dungeon(message)

async def get_town(message):
    player = await get_player(message.from_user.id)
    cur_town = (await get_location(player['location_id'])
    player['cur_hp'] = player['hp']
    await update_player(user_id, player)
    town_markup = InlineKeyboardMarkup(
    inline_keyboard=[
        [InlineKeyboardButton("Leave The City 🚶‍♂️", callback_data="leave_city")],
        [InlineKeyboardButton("Inventory 💼", callback_data="inventory")],
        [InlineKeyboardButton("Local Store 🛍️", callback_data="shop")],
        [InlineKeyboardButton("Character Stats 👤", callback_data="stats")]
    ])
    await app.edit_message_text(chat_id=message.chat.id, message_id=message.id,
                                text=f"You Are In The City: 🏰 *{cur_town['location_name']}*", reply_markup=town_markup, parse_mode=enums.ParseMode.MARKDOWN)

async def get_dungeon(message):
    player = await get_player(message.from_user.id)
    cur_dungeon = (await get_location(player['location_id'])
    dungeon_gate_markup = InlineKeyboardMarkup(
    inline_keyboard=[
        [InlineKeyboardButton("Enter The Dungeon ⚔️", callback_data="enter_dungeon"), InlineKeyboardButton("Character Stats 👤", callback_data="stats")],
        [InlineKeyboardButton("Back 🔙", callback_data="leave_city")]
    ])
    await app.edit_message_text(chat_id=message.chat.id, message_id=message.id,
                                text=f"`You Are In The Dungeon:` **⛰️ {cur_dungeon['location_name']}**", reply_markup=dungeon_gate_markup,
                                parse_mode=enums.ParseMode.MARKDOWN)

async def get_map(message):
    player = await get_player(message.from_user.id)
    cur_town = await get_location(player['location_id'])
    cur_town_x = cur_town['x_coord']
    cur_town_y = cur_town['y_coord']
    text = "**Available Locations:**\n\n"
    choose_location_markup = []
    async for el in locations.values():
        if el["location_id"] != player['location_id']:
            dist = round(count_distance(cur_town_x, cur_town_y, el['x_coord'], el['y_coord']))
            if 0 < dist <= 10:
                text += f"`{el['location_name']}` **-** `{dist}` **Km 🛣️**\n\n"
                if x["location_type"] == "town":
                    back_location = InlineKeyboardButton("Back 🔙", callback_data="back_town")
                if x["location_type"] == "dungeon":
                    back_location = InlineKeyboardButton("Back 🔙", callback_data="back_dungeon")
                choose_location_markup.append([InlineKeyboardButton(f"Go: {el["location_name"]} 🚶‍♂️", callback_data=f"go_{el["location_id"]}")])
                choose_location_markup.append([back_location])
    await app.send_message(message.chat.id, text=text, reply_markup=choose_location_markup, parse_mode=enums.ParseMode.MARKDOWN)
