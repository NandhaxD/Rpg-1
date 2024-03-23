from pyrogram import *
from pyrogram.types import *

from Aasf import app
from Aasf.Database import *
       
@app.on_message(filters.command("inventory"))
async def inventory(_, message):
    stats_markup = InlineKeyboardMarkup([[InlineKeyboardButton("Back 🔙", callback_data=f"stats_{message.from_user.id}")]])
    cur_inv = await get_inventory(message.from_user.id)
    if not cur_inv:
        return await message.reply_text("`No Inventory Found`")
    else:
        inventory_markup = []
        text = ""
        num = 0
        for item in cur_inv:
            item_doc = items.get(int(item['item_id']))
            name = item_doc['name']
            quantity = item['quantity']
            item_type = item_doc['item_type']
            if not quantity == 0:
                row_buttons = []
                if item_type == 'potion':
                    row_buttons.append(InlineKeyboardButton(
                        f"Sell {name} ({item_doc['sell_cost']} 💎)",
                        callback_data=f"sell_{message.from_user.id}_{int(item['item_id'])}"))
                else:
                    row_buttons.append(InlineKeyboardButton(
                        f"Sell {name} ({item_doc['sell_cost']} 💎)",
                        callback_data=f"sell_{message.from_user.id}_{int(item['item_id'])}"))
                    row_buttons.append(InlineKeyboardButton(
                        f"Wear {name} {item_doc['item_symbol']}",
                        callback_data=f"wear_{message.from_user.id}_{item['item_id']}"))
                inventory_markup.append(row_buttons)
                num += 1
                text += "`{}`. `{}` ×`{}` (**`{}/{}`**)**\n".format(num, name, abs(quantity), item_doc['cost'], item_doc['sell_cost'])
        if not text:
            return await message.reply_text("`Your Inventory Is Empty`", reply_markup=stats_markup)
        row_buttons = [InlineKeyboardButton(
            f"Statistics ✨",
            callback_data=f"stats_{message.from_user.id}")]
        inventory_markup.append(row_buttons)
        await message.reply_text(
            "**Your Inventory:**\n\n" + "{}".format(text),
            reply_markup=InlineKeyboardMarkup(inventory_markup),
            parse_mode=enums.ParseMode.MARKDOWN
        )
