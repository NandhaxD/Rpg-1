import asyncio
from math import floor

from Aasf import app
from Aasf.Database.playerdb import *
from Aasf.Database.__init__ import get_location, locations

from pyrogram import *
from pyrogram.types import * 

def count_distance(x1, y1, x2, y2):
    return ((x1 - x2) ** 2 + (y1 - y2) ** 2) ** (1 / 2)

async def get_town(message):
    player = await get_player(message.from_user.id)
    cur_town = await get_location(player['location_id'])
    player['cur_hp'] = player['hp']
    await update_player(message.from_user.id, player)
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
    cur_dungeon = await get_location(player['location_id'])
    dungeon_gate_markup = InlineKeyboardMarkup(
    inline_keyboard=[
        [InlineKeyboardButton("Enter The Dungeon ⚔️", callback_data="enter_dungeon"), InlineKeyboardButton("Character Stats 👤", callback_data="stats")],
        [InlineKeyboardButton("Back 🔙", callback_data="leave_city")]
    ])
    await app.edit_message_text(chat_id=message.chat.id, message_id=message.id,
                                text=f"`You Are In The Dungeon:` **⛰️ {cur_dungeon['location_name']}**", reply_markup=dungeon_gate_markup,
                                parse_mode=enums.ParseMode.MARKDOWN)
    
async def go_loc(user_id, loc_id, cq):
    player = await get_player(user_id)
    player['location_id'] = loc_id
    await update_player(user_id, player)
    if loc_id > 0:
        cur_place = await get_location(loc_id)
        if cur_place['location_type'] == "town":
            await get_town(cq)
        elif cur_place['location_type'] == "dungeon":
            await get_dungeon(cq)

async def get_map(message):
    player = await get_player(message.from_user.id)
    cur_town = await get_location(player['location_id'])
    cur_town_x = cur_town['x_coord']
    cur_town_y = cur_town['y_coord']
    text = "**Available Locations:**\n\n"
    choose_location_markup = []
    for el in locations.values():
        if el["location_id"] != player['location_id']:
            dist = round(count_distance(cur_town_x, cur_town_y, el['x_coord'], el['y_coord']))
            if 0 < dist <= 10:
                text += f"`{el['location_name']}` **-** `{dist}` **Km 🛣️**\n\n"
                if el["location_type"] == "town":
                    back_location = InlineKeyboardButton("Back 🔙", callback_data="back_town")
                if el["location_type"] == "dungeon":
                    back_location = InlineKeyboardButton("Back 🔙", callback_data="back_dungeon")
                choose_location_markup.append([InlineKeyboardButton(f"Go: {el['location_name']} 🚶‍♂️", callback_data=f"go_{el['location_id']}")])
                choose_location_markup.append([back_location])
    await app.send_message(message.message.chat.id, text=text, reply_markup=InlineKeyboardMarkup(choose_location_markup), parse_mode=enums.ParseMode.MARKDOWN)

@app.on_callback_query(filters.regex("go"))
async def gogo(_, cq):
    player = await get_player(cq.from_user.id)
    cur_loc = await get_location(player["location_id"])
    if player["level"] < (await get_location(int(cq.data.split("_")[1])))["req_level"]:
        return await cq.edit_message_text(f"`Your Level Was Too Low To Travel This Location`\n\n**Required Level:** {(await get_location(int(cq.data.split('_')[1])))['req_level']}")   
    else:
        aim_x = await get_location(int(cq.data.split("_")[1]))['x_coord']
        aim_y = await get_location(int(cq.data.split("_")[1]))['y_coord']
        delay = count_distance(cur_loc['x_coord'], cur_loc['y_coord'], aim_x, aim_y)
        await go_loc(cq.from_user.id, -1, cq)
        ticks = floor(delay / 0.6)
        for i in range(1, ticks):
            await cq.edit_message_text(f"**On My Way**" + "." * (i % 4),
                                        parse_mode=enums.ParseMode.Markdown)

            await asyncio.sleep(0.6)
        await go_loc(cq.from_user.id, int(cq.data.split("_")[1]), cq)
