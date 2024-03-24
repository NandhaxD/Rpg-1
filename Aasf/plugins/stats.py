from pyrogram import filters
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup

from Aasf import app
from Aasf.Database import get_player

@app.on_message(filters.command("stats"))
async def stats(_, message):
    player = await get_player(message.from_user.id)
    if not player:
        create_markup = InlineKeyboardMarkup([[InlineKeyboardButton("Register 📑", url="https://telegram.me/KishoreDXD_Bot?start=True")]])
        return await message.reply_text("`You Haven't Registered Yet!`\n\n`Click The Below Button To Get Registered 👇`", reply_markup=create_markup)

    name = player['name']
    level = player['level']
    hp = player['hp']
    cur_hp = player['cur_hp']
    attack = player['attack']
    m_attack = player['magic_attack']
    armour = player['armour']
    m_armour = player['magic_armour']
    exp = player['exp']
    balance = player['money']

    stats_text = "**👤 Your Character's Statistics:**\n\n"
    stats_text += f"**Name:** `{name}`\n\n"
    stats_text += f"**Level:** `{level}` (`{level*1000 - exp}` **To Next Level**)\n\n"
    stats_text += f"**Health:** `{cur_hp}`/`{hp}`\n\n"
    stats_text += f"**Attack:** `{attack}` ⚔️  `{m_attack}` 🪄\n\n"
    stats_text += f"**Defense:** `{armour}` 🛡️  `{m_armour}` 🔮\n\n"
    stats_text += f"**Balance:** `{balance}` 💎\n\n"

    inv_markup = InlineKeyboardMarkup([[InlineKeyboardButton("Inventory 💼", callback_data=f"inventory_{message.from_user.id}")]])
 
    await message.reply_text(stats_text, reply_markup=inv_markup, parse_mode=enums.ParseMode.MARKDOWN)
