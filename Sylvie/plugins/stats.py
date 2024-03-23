from pyrogram import *
from pyrogram.types import *

from Sylvie import *
from Sylvie.Database import *

@app.on_callback_query(filters.regex("stats"))
async def stats_c(client: Client, cq: CallbackQuery):
    player = await get_player(cq.from_user.id)
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
    await cq.edit_message_text(f"🧝 **Your Character""s Statistics:**\n\n"
                                    f"**name:** `{name}`\n\n"
                                    f"**level:** `{level}` (`{100 - exp}` **To Sl.**)\n\n"
                                    f"**Health:** `{cur_hp}`/`{hp}`\n\n"
                                    f"**Damage:** `{attack}` ⚔️  `{m_attack}` 🪄\n\n"
                                    f"**Armor:** `{armour}` 🛡️  `{m_armour}` 🔮\n\n"
                                    f"**Balance:** `{balance}` 💎", reply_markup=back_markup,
                            parse_mode=enums.ParseMode.MARKDOWN)
    
@app.on_message(filters.command("stats"))
async def stats(_, message):
    player = await get_player(message.from_user.id)
    if not player:
        if message.chat.type == enums.ChatType.PRIVATE:
            return await message.reply_text("`You've Not Registered Yet Use /start To Get Register`")
        else:
            return await message.reply_text("`You've Not Registered Yet Use /start To Get Register`\n\n`Click The Below Button To Get Registered`", reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton(text="hi", url="https://telegram.me/AracadianStarBot?start=True")]]))
    else:   
        name = player['name']
        level = player['level'] 
        hp = player['hp'] 
        cur_hp = player['cur_hp']
        attack = player['attack']
        magic_attack = player['magic_attack']
        armour = player['armour']
        magic_armour = player['magic_armour']
        exp = player['exp']
        balance = player['money']
        stats_text = "👤 **Your Character's Statistics:**\n\n"
        stats_text += f"**Name:** `{name}`\n"
        stats_text += f"**Level:** `{level}` (`{level*10 - exp}` **To Next Level**)\n"
        stats_text += f"**Health:** `{cur_hp}`/`{hp}`\n"
        stats_text += f"**Attack:** `{attack}` ⚔️  `{magic_attack}` 🪄\n"
        stats_text += f"**Defense:** `{armour}` 🛡️  `{magic_armour}` 🔮\n"
        stats_text += f"**Balance:** `{balance}` 💎\n"
        await message.reply_text(stats_text, parse_mode=enums.ParseMode.MARKDOWN)
