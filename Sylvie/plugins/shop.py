from pyrogram import *
from pyrogram.types import *

from Sylvie import *
from Sylvie.Database import *

@app.on_callback_query(filters.regex("close"))
async def close(client: Client, cq: CallbackQuery):
    user_id = int(cq.data.split("_")[1])
    if cq.from_user.id == user_id:
        await cq.message.delete()
    else:
        await cq.answer("This Wasn't Requested By You")

@app.on_callback_query(filters.regex("buy"))
async def buy(client: Client, cq: CallbackQuery):
    user_id = int(cq.data.split("_")[1])
    item_id = int(cq.data.split("_")[2])
    back_reply = InlineKeyboardButton("Back 🔙", callback_data=f"backshop_{user_id}")
    back_shop = InlineKeyboardMarkup([[back_reply]])
    if cq.from_user.id == user_id:
        player = await get_player(cq.from_user.id)
        item = await get_item(item_id)
        if player['money'] < item['cost']:
            await cq.message.edit_text("`Not Enough Coins.`", reply_markup=back_shop, parse_mode=enums.ParseMode.MARKDOWN)
        else:
            player['money'] -= item['cost']
            await update_player(cq.from_user.id, player)
            await add_item(cq.from_user.id, item_id)
            await update_item(cq.from_user.id, item_id)
            await cq.message.edit_text(f"**You Bought An Item** `{item['name']}`. **You Now Have Them In Your Inventory** .", reply_markup=back_shop, parse_mode=enums.ParseMode.MARKDOWN)

@app.on_callback_query(filters.regex("show"))
async def show_items_by_type(client: Client, cq: CallbackQuery):
    user_id = int(cq.data.split("_")[1])
    item_type = cq.data.split("_")[2]
    cur_loc = cq.data.split("_")[3]
    back_shop = InlineKeyboardButton("Back 🔙", callback_data=f"backshop_{cq.from_user.id}")
    if cq.from_user.id == user_id:
        items_list = [item for item in items.values() if item.get("item_type") == str(item_type) and item.get("availability") == int(cur_loc)]
        if not items_list:
            await cq.message.edit_text("`No items to show.`", reply_markup=InlineKeyboardMarkup([[back_shop]]))
        else:
            buttons = []
            for item in items_list:
                buttons.append([
                    InlineKeyboardButton(f"{item['name']} - {item['cost']} coins", callback_data=f"buy_{user_id}_{item['id']}")
                ])
            buttons.append([back_shop])
            await cq.message.edit_text(f"**Items of type {item_type}:**", reply_markup=InlineKeyboardMarkup(buttons))
    else:
        await cq.answer("This Wasn't Requested By You")

@app.on_message(filters.command("shop"))
async def shop(client: Client, message: Message):
    close_shop = InlineKeyboardButton("Close 🚫", callback_data=f"close_{message.from_user.id}")
    cur_loc = (await db.persons.find_one({'user_id': message.from_user.id}))['location_id']

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

@app.on_callback_query(filters.regex("backshop"))
async def back_shop(client: Client, cq: CallbackQuery):
    user_id = int(cq.data.split("_")[1])
    if not cq.from_user.id == user_id:
        return await cq.answer("This Wasn't Requested By You")
    else:
        close_shop = InlineKeyboardButton("Close 🚫", callback_data=f"close_{user_id}")
        cur_loc = (await db.persons.find_one({'user_id': user_id}))['location_id']

        y = {}
        for x in items.values():
            if not x.get("item_type") in y:
                y[x.get("item_type")] = x.get("item_symbol")
            else:
                pass

        type_buttons = [
            InlineKeyboardButton(
                f"Buy {item_type[0].capitalize()}{ 's' if item_type[0][-1]!='s' else ''} {item_type[1]}",
                callback_data=f"show_{user_id}_{item_type[0]}_{cur_loc}"
            ) for item_type in y.items()
        ]

        buttons = [type_buttons[i:i+2] for i in range(0, len(type_buttons), 2)]
        markup = InlineKeyboardMarkup([[button for button in row] for row in buttons])
        markup.inline_keyboard.append([close_shop])
        await cq.edit_message_text(
            "🛒 **Welcome To Shop!**", 
            reply_markup=markup, 
            parse_mode=enums.ParseMode.MARKDOWN
  )
