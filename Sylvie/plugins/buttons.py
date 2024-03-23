from pyrogram import *
from pyrogram.types import *
from Sylvie import *
from Sylvie.plugins.callback import *
from Sylvie.Database import *

# cities button
town_markup = InlineKeyboardMarkup(
    inline_keyboard=[
        [InlineKeyboardButton("Leave The City", callback_data="leave_city")],
        [InlineKeyboardButton("Inventory", callback_data="inventory")],
        [InlineKeyboardButton("Local Store", callback_data="shop")],
        [InlineKeyboardButton("Character Stats", callback_data="stats")]
    ])

# back button
back_markup = InlineKeyboardMarkup(
    inline_keyboard=[
        [InlineKeyboardButton("Back", callback_data="back_town")]
    ])

# battle button
battle_markup = InlineKeyboardMarkup(
    inline_keyboard=[
        [InlineKeyboardButton("Estimate", callback_data="check")],
        [InlineKeyboardButton("Attack", callback_data="attack")],
        [InlineKeyboardButton("Drink The Potion", callback_data="heal")]
    ])

# evaluation button
check_markup = InlineKeyboardMarkup(
    inline_keyboard=[
        [InlineKeyboardButton("Attack", callback_data="attack")]
    ])

# dungeon button
dungeon_gate_markup = InlineKeyboardMarkup(
    inline_keyboard=[
        [InlineKeyboardButton("Go To The Dungeon!", callback_data="enter_dungeon"), InlineKeyboardButton("Character Stats", callback_data="stats")],
        [InlineKeyboardButton("Back", callback_data="leave_city")]
    ])

# victory button
win_markup = InlineKeyboardMarkup(
    inline_keyboard=[
        [InlineKeyboardButton("Back", callback_data="leave_city")],
        [InlineKeyboardButton("Keep Going", callback_data="enter_dungeon")]
    ])

# death button
death_markup = InlineKeyboardMarkup(
    inline_keyboard=[
        [InlineKeyboardButton("Be Reborn", callback_data="revive")]
    ])

# no money button
no_money_markup = InlineKeyboardMarkup(
    inline_keyboard=[
        [InlineKeyboardButton("Back", callback_data="inventory")]
    ])

# deal button
after_deal_markup = InlineKeyboardMarkup(
    inline_keyboard=[
        [InlineKeyboardButton("Back", callback_data="inventory")]
    ])
