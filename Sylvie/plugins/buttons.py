from pyrogram import *
from pyrogram.types import *

from Sylvie import *
from Sylvie.plugins.callback import *
from Sylvie.Database import *

# cities buttons
town_markup = InlineKeyboardMarkup([
    [InlineKeyboardButton("Leave The City", callback_data="leave_city")],
    [InlineKeyboardButton("Inventory", callback_data="inventory")],
    [InlineKeyboardButton("Local Store", callback_data="shop")],
    [InlineKeyboardButton("Character Stats", callback_data="stats")]
])

# stats buttons
stats_markup = InlineKeyboardMarkup([[InlineKeyboardButton("Back", callback_data="back_town")]])

# battle buttons
battle_markup = InlineKeyboardMarkup([
    [InlineKeyboardButton("Estimate", callback_data="check")],
    [InlineKeyboardButton("attack", callback_data="attack")],
    [InlineKeyboardButton("Drink The Potion", callback_data="heal")]
])

# evaluation buttons
check_markup = InlineKeyboardMarkup([[InlineKeyboardButton("attack", callback_data="attack")]])

# dungeon buttons
dungeon_gate_markup = InlineKeyboardMarkup([[InlineKeyboardButton("Go To The Dungeon!", callback_data="enter_dungeon"),InlineKeyboardButton("Character Stats", callback_data="stats")],[InlineKeyboardButton("Back", callback_data="leave_city")]])

# victory buttons
win_markup = InlineKeyboardMarkup([[InlineKeyboardButton("Back", callback_data="leave_city")], [InlineKeyboardButton("Keep Going", callback_data="enter_dungeon")]])

# death buttons
death_markup = InlineKeyboardMarkup([[InlineKeyboardButton("Be Reborn", callback_data="revive")]])

# no money buttons
no_money_markup = InlineKeyboardMarkup([[InlineKeyboardButton("Back", callback_data="back_town")]])

# deal buttons
after_deal_markup = InlineKeyboardMarkup([[InlineKeyboardButton("Back", callback_data="inventory")]])
