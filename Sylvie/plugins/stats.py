from pyrogram import *
from pyrogram.types import *

from Sylvie import *

@app.on_message(filters.command("stats"))
async def stats(_, message):
    user_data = await db.persons.find_one({'user_id': message.from_user.id})
    name = user_data['name']
    level = user_data['level'] 
    hp = user_data['hp'] 
    cur_hp = user_data['cur_hp']
    attack = user_data['attack']
    magic_attack = user_data['magic_attack']
    armour = user_data['armour']
    magic_armour = user_data['magic_armour']
    xp = user_data['xp']
    balance = user_data['money']
    stats_text = "👤 **Your Character's Statistics:**\n\n"
    stats_text += f"**Name:** `{name}`\n\n"
    stats_text += f"**Level:** `{level}` (`{level*10 - xp}` **To Next Level**)\n\n"
    stats_text += f"**Health:** `{cur_hp}`/`{hp}`\n\n"
    stats_text += f"**Attack:** `{attack}` ⚔️  `{magic_attack}` 🪄\n\n"
    stats_text += f"**Defense:** `{armour}` 🛡️  `{magic_armour}` 🔮\n\n"
    stats_text += f"**Balance:** `{balance}` 💎\n\n"
    await message.reply_text(stats_text, parse_mode=enums.ParseMode.MARKDOWN)
