from pyrogram import *
from pyrogram.types import *

from Aasf import app
from Aasf.Database import get_player, items

@app.on_message(filters.command("shop"))
async def shop(client: Client, message: Message):
    close_shop = InlineKeyboardButton("Close 🚫", callback_data=f"close_{message.from_user.id}")
    cur_loc = await get_player(message.from_user.id)['location_id']
    y = {}
    for x in items.values():
        if not x.get("item_type") in y:
            y[x.get("item_type")] = x.get("item_symbol")
        else:
            pass

    type_buttons = [
        InlineKeyboardButton(
            f"Buy {item_type[0].capitalize()}{ 's' if item_type[0][-1]!='s' else ''} {item_type[1]}",
            callback_data=f"show_{message.from_user.id}_{item_type[0]}_{cur_loc}"
        ) for item_type in y.items()
    ]

    buttons = [type_buttons[i:i+2] for i in range(0, len(type_buttons), 2)]
    markup = InlineKeyboardMarkup([[button for button in row] for row in buttons])
    markup.inline_keyboard.append([close_shop])
    await message.reply_text(
        "🛒 **Welcome To Shop!**", 
        reply_markup=markup, 
        parse_mode=enums.ParseMode.MARKDOWN
          )
