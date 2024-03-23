from pyrogram import *
from pyrogram.types import *

from Sylvie import *
from Sylvie.Database important*

@app.on_message(filters.command("stats"))
async def stats(_, message):
    player = await get_player(message.from_user.id)
    if not player and enums.ChatType.PRIVATE:
        return await message.reply_text("`You've Not Registered Yet Use /start To Get Register`")
    if not player and not enums.ChatType.PRIVATE:
        return await message.reply_text("`You've Not Registered Yet Use /start To Get Register`\n\n`Click The Below Button To Get Registered`", reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton(text="hi", url="https://telegram.me/AracadianStarBot?start=True")]]))
    else:   
        name = user_data['name']
        level = user_data['level'] 
        hp = user_data['hp'] 
        cur_hp = user_data['cur_hp']
        attack = user_data['attack']
        magic_attack = user_data['magic_attack']
        armour = user_data['armour']
        magic_armour = user_data['magic_armour']
        exp = user_data['exp']
        balance = user_data['money']
        stats_text = "👤 **Your Character's Statistics:**\n\n"
        stats_text += f"**Name:** `{name}`\n"
        stats_text += f"**Level:** `{level}` (`{level*10 - exp}` **To Next Level**)\n"
        stats_text += f"**Health:** `{cur_hp}`/`{hp}`\n"
        stats_text += f"**Attack:** `{attack}` ⚔️  `{magic_attack}` 🪄\n"
        stats_text += f"**Defense:** `{armour}` 🛡️  `{magic_armour}` 🔮\n"
        stats_text += f"**Balance:** `{balance}` 💎\n"
        await message.reply_text(stats_text, parse_mode=enums.ParseMode.MARKDOWN)
