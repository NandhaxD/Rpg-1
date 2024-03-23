from pyrogram import *
from pyrogram.types import *

from Aasf import app
from Aasf.Database import *
 
@app.on_message(filters.command("stats"))
async def stats(_, message):
    inv_markup = InlineKeyboardMarkup([[InlineKeyboardButton("Inventory 💼", callback_data=f"inventory_{message.from_user.id}")]])
    player = await get_player(message.from_user.id)
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
    await message.reply_text(stats_text, reply_markup=inv_markup, parse_mode=enums.ParseMode.MARKDOWN)
