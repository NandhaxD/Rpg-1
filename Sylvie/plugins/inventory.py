from Sylvie import *
from Sylvie.Database import *
from pyrogram import *
from pyrogram.types import *

@app.on_callback_query(filters.regex("sell"))
async def sell(_, cq):
    user_id = int(cq.data.split("_")[1])
    item_to_sell = int(cq.data.split("_")[2])
    if not cq.from_user.id == user_id:
        return await cq.answer("This Wasn't Requested By You")
    else:
        after_deal_markup = InlineKeyboardMarkup([[InlineKeyboardButton("Back", callback_data=f"inventory_{cq.from_user.id}")]])
        item_in_inv = await get_item(cq.from_user.id, item_to_sell)
        if not item_in_inv:
            return await cq.answer("You Don't Have This Item")
        item_in_inv['quantity'] -= 1
        user = await db.persons.find_one({'user_id': cq.from_user.id})
        item_cost = items.get(item_to_sell)
        user['money'] += item_cost['sell_cost']
        await db.persons.replace_one({'user_id': cq.from_user.id}, user)
        await db.inventory.replace_one({'user_id': cq.from_user.id, 'item_id': item_to_sell}, item_in_inv)
        await cq.edit_message_text(f"**You Sold** `{item_cost['name']}` **And Got** `{item_cost['sell_cost']}`",
                                    reply_markup=after_deal_markup, parse_mode=enums.ParseMode.MARKDOWN)

@app.on_message(filters.command("inventory"))
async def inventory(_, message):
    cur_inv = await get_inventory(message.from_user.id)
    if not cur_inv:
        return await message.reply_text("`No Inventory Found`")
    else:
        inventory_markup = []
        text = ""
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
                        callback_data=f"wear_{item['item_id']}"))
                inventory_markup.append(row_buttons)
                text += "`{}` **-** `{}` **PC.** {}\n".format(name, abs(quantity), '✅' if quantity > 0 else '')
        if not text:
            return await message.reply_text("`Your Inventory Is Empty`")
        await message.reply_text(
            "**Your Inventory:**\n\n" + "{}".format(text),
            reply_markup=InlineKeyboardMarkup(inventory_markup),
            parse_mode=enums.ParseMode.MARKDOWN
        )
