from pyrogram import *
from pyrogram.types import *

from Sylvie import *
from Sylvie.Database import *

@app.on_message(filters.command("start"))
async def start(_, message):
    player = await get_player(message.from_user.id)
    town_markup = InlineKeyboardMarkup(
    inline_keyboard=[
        [InlineKeyboardButton("Leave The City 🚶‍♂️", callback_data="leave_city")],
        [InlineKeyboardButton("Inventory 💼", callback_data="inventory")],
        [InlineKeyboardButton("Local Store 🛍️", callback_data="shop")],
        [InlineKeyboardButton("Character Stats 👤", callback_data="stats")]
    ])
    dungeon_gate_markup = InlineKeyboardMarkup(
    inline_keyboard=[
        [InlineKeyboardButton("Enter The Dungeon ⚔️", callback_data="enter_dungeon"), InlineKeyboardButton("Character Stats 👤", callback_data="stats")],
        [InlineKeyboardButton("Back 🔙", callback_data="leave_city")]
    ])
    if not player:
        name = await message.chat.ask("**Send Me Your Name:**", parse_mode=enums.ParseMode.MARKDOWN)
        new_player = await create_player(user_id=message.from_user.id, name=name.text)
        cur_loc = await get_location(1)
        await answer.sent_message.delete()
        await app.send_message(message.chat.id, f"**You Have Successfully Registered. Welcome To The Game, {message.from_user.mention}!**")
        await app.send_message(message.chat.id, f"`You Are In The City:` 🏰 **{cur_loc["location_name"]}**", reply_markup=town_markup, parse_mode=enums.ParseMode.MARKDOWN)
    else:
        if player["location_id"] = -1:
            pass
        else:
            cur_loc = await get_location(player["location_id"])
            if cur_loc["location_type"] == "town":
                await app.send_message(message.chat.id, f"`You Are In The City:` 🏰 **{cur_loc["location_name"]}**", reply_markup=town_markup,
                                       parse_mode=enums.ParseMode.MARKDOWN)
            elif cur_loc["location_type"] == "dungeon":
                await app.send_message(message.chat.id, f"`You Are In The Dungeon:` ⛰️ **{cur_loc["location_name"]}**", reply_markup=dungeon_gate_markup,
                                       parse_mode=enums.ParseMode.MARKDOWN)
