from pyrogram import *
from pyrogram.types import *
from Sylvie import *
from Sylvie.plugins.callback import *
from Sylvie.Database import *

# cities buttons
town_markup = InlineKeyboardMarkup(
    inline_keyboard=[
        [InlineKeyboardButton("Leave The City", callback_data="leave_city")],
        [InlineKeyboardButton("Inventory", callback_data="inventory")],
        [InlineKeyboardButton("Local Store", callback_data="shop")],
        [InlineKeyboardButton("Character Stats", callback_data="stats")]
    ])

# stats buttons
stats_markup = InlineKeyboardMarkup(
    inline_keyboard=[
        [InlineKeyboardButton("Back", callback_data="back_town")]
    ])

# battle buttons
battle_markup = InlineKeyboardMarkup(
    inline_keyboard=[
        [InlineKeyboardButton("Estimate", callback_data="check")],
        [InlineKeyboardButton("attack", callback_data="attack")],
        [InlineKeyboardButton("Drink The Potion", callback_data="heal")]
    ])

# evaluation buttons
check_markup = InlineKeyboardMarkup(
    inline_keyboard=[
        [InlineKeyboardButton("attack", callback_data="attack")]
    ])

# dungeon buttons
dungeon_gate_markup = InlineKeyboardMarkup(
    inline_keyboard=[
        [InlineKeyboardButton("Go To The Dungeon!", callback_data="enter_dungeon"), InlineKeyboardButton("Character Stats", callback_data="stats")],
        [InlineKeyboardButton("Back", callback_data="leave_city")]
    ])

# victory buttons
win_markup = InlineKeyboardMarkup(
    inline_keyboard=[
        [InlineKeyboardButton("Back", callback_data="leave_city")],
        [InlineKeyboardButton("Keep Going", callback_data="enter_dungeon")]
    ])

# death buttons
death_markup = InlineKeyboardMarkup(
    inline_keyboard=[
        [InlineKeyboardButton("Be Reborn", callback_data="revive")]
    ])

# no money buttons
no_money_markup = InlineKeyboardMarkup(
    inline_keyboard=[
        [InlineKeyboardButton("Back", callback_data="inventory")]
    ])

# deal buttons
after_deal_markup = InlineKeyboardMarkup(
    inline_keyboard=[
        [InlineKeyboardButton("Back", callback_data="inventory")]
    ])
