from pyrogram import *
from pyrogram.types import *

from Sylvie import *
from Sylvie.Database import *

@app.on_callback_query(filters.regex("wear"))
async def wear(_, cq):
    user_id = int(cq.data.split("_")[1])
    item_to_wear = int(cq.data.split("_")[2])
    if not cq.from_user.id == user_id:
        return await cq.answer("This Wasn't Requested By You.")
    else:
        back_inv = InlineKeyboardMarkup([[InlineKeyboardButton("Back 🔙", callback_data=f"inventory_{cq.from_user.id}")]])
        player = await get_player(cq.from_user.id)
        item_to_wear_inst = items.get(item_to_wear)
        if item_to_wear_inst['req_level'] > player['level']:
            return await cq.edit_message_text(f"`You Are Too Small To Wear This Item.`",
                                        reply_markup=back_inv)
        else:
            player_inv = await get_inventory(cq.from_user.id)
            for item in player_inv:
                if item['item_id'] == item_to_wear:
                    found_item = await get_item(cq.from_user.id, item['item_id'])
                    if not found_item['quantity'] == 0:
                        found_item_inst = items.get(item_to_wear)
                        found_item['quantity'] -= 1
                        player['hp'] += found_item_inst['hp']
                        player['attack'] += found_item_inst['attack']
                        player['magic_attack'] += found_item_inst['magic_attack']
                        player['armour'] += found_item_inst['armour']
                        player['magic_armour'] += found_item_inst['magic_armour']
                        await update_player(cq.from_user.id, player)
                        await update_inventory(cq.from_user.id, item_to_sell, item_in_inv)
                        return await cq.edit_message_text(f"**You Put On** `{(items.get(item_to_wear))['name']}`.",
                                                    reply_markup=back_inv)
                    else:
                        return await cq.edit_message_text("`You Don't Have This Item In Your Inventory.`",
                                                    reply_markup=back_inv)
            if not found_item:
                return await cq.edit_message_text("`You Don't Have This Item In Your Inventory.`",
                                            reply_markup=back_inv)

@app.on_callback_query(filters.regex("sell"))
async def sell(_, cq):
    player_id = int(cq.data.split("_")[1])
    item_to_sell = int(cq.data.split("_")[2])
    if not cq.from_user.id == player_id:
        return await cq.answer("This Wasn't Requested By You")
    else:
        after_deal_markup = InlineKeyboardMarkup([[InlineKeyboardButton("Back 🔙", callback_data=f"inventory_{cq.from_user.id}")]])
        item_in_inv = await get_item(cq.from_user.id, item_to_sell)
        if not item_in_inv:
            return await cq.answer("You Don't Have This Item")
        item_in_inv['quantity'] -= 1
        player = await get_player(cq.from_user.id)
        item_cost = items.get(item_to_sell)
        player['money'] += item_cost['sell_cost']
        await update_player(cq.from_user.id, player)
        await update_inventory(cq.from_user.id, item_to_sell, item_in_inv)
        await cq.edit_message_text(f"**You Sold** `{item_cost['name']}` **And Got** `{item_cost['sell_cost']}`",
                                    reply_markup=after_deal_markup, parse_mode=enums.ParseMode.MARKDOWN)
@app.on_callback_query(filters.regex("inventory"))
async def inventory_c(_, cq):
    player_id = int(cq.data.split("_")[1])
    if not cq.from_user.id == player_id:
        return await cq.answer("This Wasn't Requested By You")
    else:
        stats_markup = InlineKeyboardMarkup([[InlineKeyboardButton("Back 🔙", callback_data=f"stats_{cq.from_user.id}")]])
        cur_inv = await get_inventory(cq.from_user.id)
        if not cur_inv:
            return await cq.edit_message_text("`No Inventory Found`")
        else:
            inventory_markup = []
            text = ""
            num = 0
            row_buttons = []
            for item in cur_inv:
                item_doc = items.get(int(item['item_id']))
                name = item_doc['name']
                quantity = item['quantity']
                item_type = item_doc['item_type']
                if not quantity == 0:
                    if item_type == 'potion':
                        row_buttons.append(InlineKeyboardButton(
                            f"Sell {name} ({item_doc['sell_cost']} 💎)",
                            callback_data=f"sell_{cq.from_user.id}_{int(item['item_id'])}"))
                        inventory_markup.append(row_buttons)
                        row_buttons = []
                        num += 1
                        text += "`{}`. `{}` ×`{}` (**`{}/{}`**)**\n".format(num, name, abs(quantity), item_doc['cost'], item_doc['sell_cost'])
                    else:
                        row_buttons.append(InlineKeyboardButton(
                            f"Sell {name} ({item_doc['sell_cost']} 💎)",
                            callback_data=f"sell_{cq.from_user.id}_{int(item['item_id'])}"))
                        row_buttons.append(InlineKeyboardButton(
                             f"Wear {name} {item_doc['item_symbol']}",
                             callback_data=f"wear_{cq.from_user.id}_{item['item_id']}"))
                        if len(row_buttons) == 2:
                            inventory_markup.append(row_buttons)
                            row_buttons = []
                        num += 1
                        text += "`{}`. `{}` ×`{}` (**`{}/{}`**)**\n".format(num, name, abs(quantity), item_doc['cost'], item_doc['sell_cost'])
            if row_buttons:
                inventory_markup.append(row_buttons)
            inventory_markup.append([InlineKeyboardButton(
                f"Statistics ✨",
                callback_data=f"stats_{cq.from_user.id}")])
            if not text:
                return await cq.edit_message_text("`Your Inventory Is Empty`", reply_markup=stats_markup)
            await cq.edit_message_text(
                "**Your Inventory:**\n\n" + "{}".format(text),
                reply_markup=InlineKeyboardMarkup(inventory_markup),
                parse_mode=enums.ParseMode.MARKDOWN
            )
            
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
