import random
import asyncio

from pyrogram import *
from pyrogram.types import *

from Aasf import app, db
from Aasf.Database import *

# stats callback
@app.on_callback_query(filters.regex("stats"))
async def stats_cq(_, cq):
    user_id = int(cq.data.split("_")[1])
    if not cq.from_user.id == user_id:
        return await cq.answer("This Wasn't Requested By You")
    else:
        inv_markup = InlineKeyboardMarkup([[InlineKeyboardButton("Inventory 💼", callback_data=f"inventory_{cq.from_user.id}")]])
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
        stats_text = "**👤 Your Character's Statistics:**\n\n"
        stats_text += f"**Name:** `{name}`\n\n"
        stats_text += f"**Level:** `{level}` (`{level*10 - exp}` **To Next Level**)\n\n"
        stats_text += f"**Health:** `{cur_hp}`/`{hp}`\n\n"
        stats_text += f"**Attack:** `{attack}` ⚔️  `{m_attack}` 🪄\n\n"
        stats_text += f"**Defense:** `{armour}` 🛡️  `{m_armour}` 🔮\n\n"
        stats_text += f"**Balance:** `{balance}` 💎\n\n"
        await cq.edit_message_text(stats_text, reply_markup=inv_markup, parse_mode=enums.ParseMode.MARKDOWN)

# shop callback
@app.on_callback_query(filters.regex("close"))
async def close_cq(client: Client, cq: CallbackQuery):
    user_id = int(cq.data.split("_")[1])
    if cq.from_user.id == user_id:
        await cq.message.delete()
    else:
        await cq.answer("This Wasn't Requested By You")

@app.on_callback_query(filters.regex("buy"))
async def buy_cq(client: Client, cq: CallbackQuery):
    user_id = int(cq.data.split("_")[1])
    item_id = int(cq.data.split("_")[2])
    back_reply = InlineKeyboardButton("Back 🔙", callback_data=f"backshop_{user_id}")
    back_shop = InlineKeyboardMarkup([[back_reply]])
    if cq.from_user.id == user_id:
        player = await get_player(cq.from_user.id)
        item = items.get(item_id)
        if player['money'] < item['cost']:
            await cq.message.edit_text("`Not Enough Coins.`", reply_markup=back_shop, parse_mode=enums.ParseMode.MARKDOWN)
        else:
            player['money'] -= item['cost']
            await update_player(cq.from_user.id, player)
            is_already = await get_item(cq.from_user.id, item_id)
            if not is_already:
                await add_item(cq.from_user.id, item_id)
            else:
                await increase_item(cq.from_user.id, item_id)
            await cq.message.edit_text(f"**You Bought An Item** `{item['name']}`. **You Now Have Them In Your Inventory** .", reply_markup=back_shop, parse_mode=enums.ParseMode.MARKDOWN)

@app.on_callback_query(filters.regex("show"))
async def show_items_by_type_cq(client: Client, cq: CallbackQuery):
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
                    InlineKeyboardButton(f"{item['name']} - {item['cost']} coins", callback_data=f"buy_{user_id}_{get_key(item, items)}")
                ])
            buttons.append([back_shop])
            await cq.message.edit_text(f"**Items of type {item_type}:**", reply_markup=InlineKeyboardMarkup(buttons))
    else:
        await cq.answer("This Wasn't Requested By You")

@app.on_callback_query(filters.regex("backshop"))
async def back_shop_cq(client: Client, cq: CallbackQuery):
    user_id = int(cq.data.split("_")[1])
    if not cq.from_user.id == user_id:
        return await cq.answer("This Wasn't Requested By You")
    else:
        close_shop = InlineKeyboardButton("Close 🚫", callback_data=f"close_{user_id}")
        cur_loc = (await get_player(cq.from_user.id))['location_id']
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

# inventory callback
@app.on_callback_query(filters.regex("wear"))
async def wear_cq(_, cq):
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
                        await update_inventory(cq.from_user.id, item_to_wear, found_item)
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
async def inventory_cq(_, cq):
    player_id = int(cq.data.split("_")[1])
    if not cq.from_user.id == player_id:
        return await cq.answer("This Wasn't Requested By You")
    else:
        stats_markup = InlineKeyboardMarkup([[InlineKeyboardButton("Back 🔙", callback_data=f"stats_{cq.from_user.id}")]])
        cur_inv = await get_inventory(cq.from_user.id)
        if not cur_inv:
            return await cq.edit_message_text("`No Inventory Found`", reply_markup=stats_markup)
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

# battle callback
@app.on_callback_query(filters.regex("back_town"))
async def btown_cq(_, cq):
    user_id = int(cq.data.split("_")[1])
    cur_loc = (await get_player(user_id))["location_id"]
    if ((await get_location(cur_loc))["location_type"]) == "dungeon":
        await get_dungeon(cq)
    else:
        await get_town(cq)

@app.on_callback_query(filters.regex("back_dungeon"))
async def bdungeon_cq(_, cq):
    await get_dungeon(cq)

@app.on_callback_query(filters.regex("leave_city"))
async def leave_city_cq(_, cq):
    await get_map(cq)

@app.on_callback_query(filters.regex("revive"))
async def revive_cq(_, cq):
    await end_battle(cq.from_user.id)
    player = await get_player(cq.from_user.id)
    player['location_id'] = 1
    player['cur_hp'] = player['hp']
    await get_town(cq)
    await update_player(cq.from_user.id, player)

@app.on_callback_query(filters.regex("check"))
async def check_cq(_, cq):
    battle = await get_battle(cq.from_user.id)
    enemy = battle['enemy']
    check_markup = InlineKeyboardMarkup(
    inline_keyboard=[
        [InlineKeyboardButton("Attack", callback_data="attack")]
    ])

    await cq.edit_message_text(f"**{enemy['name']}**:\n\n" + f"**Health:** `{enemy['hp']}/{(mobs.get(get_key(enemy['name'], mobs))[battle['probability']])["hp"]}`\n" + f"**Attack:** `{enemy['attack']}` {'⚔️' if enemy['attack_type'] == 'phys' else '🪄'}\n" + f"**Protection:** `{enemy['armour']}` 🛡️ `{enemy['magic_armour']}` 🔮",
                                reply_markup=check_markup, parse_mode=enums.ParseMode.MARKDOWN)


@app.on_callback_query(filters.regex("enter_dungeon"))
async def edungeon_cq(_, cq):
    player = await get_player(cq.from_user.id)
    options = [0, 1, 2, 3, 4]
    probabilities = [0.4, 0.3, 0.2, 0.09, 0.01]
    enemy_id = random.choices(options, probabilities)[0]
    one = int(player["location_id"])
    two = int(enemy_id)
    enem = mobs.get(one)
    enemy = enem[two]
    enemy_name = enemy['name']
    battle_markup = InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton("Estimate 🧮", callback_data="check")],
            [InlineKeyboardButton("Attack 🗡️", callback_data="attack")],
            [InlineKeyboardButton("Drink The Potion ⚱️", callback_data="heal")]
    ])
    await cq.message.delete()
    await app.send_photo(cq.message.chat.id, photo=enemy["mob_img"], caption=f"`{enemy_name}` `{random.choice(['Got In The Way!', 'Jumped Out Of The Corner!', 'Crept Unnoticed!'])}`",
                                reply_markup=battle_markup)
    await create_battle(cq.from_user.id, enemy, probabilities, cq)


@app.on_callback_query(filters.regex("heal"))
async def heal_cq(_, cq):
    battle = await get_battle(cq.from_user.id)
    enemy = battle['enemy']
    await update_time(cq.from_user.id)
    player = await get_player(cq.from_user.id)
    stmt = await update_inventory(cq.from_user.id, 10)
    death_markup = InlineKeyboardMarkup(
                    inline_keyboard=[
                        [InlineKeyboardButton("Be Reborn 💞", callback_data="revive")]
                    ])
    battle_markup = InlineKeyboardMarkup(
                    inline_keyboard=[
                        [InlineKeyboardButton("Estimate 🧮", callback_data="check")],
                        [InlineKeyboardButton("Attack 🗡️", callback_data="attack")],
                        [InlineKeyboardButton("Drink The Potion ⚱️", callback_data="heal")]
    ])
    if stmt['quantity'] != 0:
        stmt1 = await get_player(cq.from_user.id)
        if stmt['quantity'] > 0:
                stmt['quantity'] -= 1
        else:
            stmt['quantity'] += 1
        stmt1['cur_hp'] = min((stmt1['cur_hp'] + 5), stmt1['hp'])
        await update_player(cq.from_user.id, stmt1)
        await update_inventory(cq.from_user.id, 10, stmt)
        for i in range(0, 4):
            await cq.edit_message_caption(f"**You Drank A Health Potion! Restored 5 hp. Current Health:** {stmt1['cur_hp']}\n\n`The Enemy Is attacking`" + "." * (i % 4), parse_mode=enums.ParseMode.Markdown)
            await asyncio.sleep(0.6)
    else:
        for i in range(0, 4):
            await cq.edit_message_caption(f"**You Reached Into Your Backpack For A Potion, But He Wasn''t There!**\n\n`The Enemy Is Attacking`" + "." * (i % 4), parse_mode=enums.ParseMode.Markdown)
            await asyncio.sleep(0.6)
    if enemy['attack_type'] == 'phys':
        enemy_damage = random.choices([enemy['attack'], enemy['attack'] * 1.5], weights=[0.8, 0.2])[0]
        player['cur_hp'] -= max((enemy_damage - player['armour']), 0)
        await db.persons.replace_one({'user_id': cq.from_user.id}, player)
        if player['cur_hp'] <= 0:
            await cq.edit_message_caption(f"**Opponent** `{random.choice(['Hit', 'Wounded', 'Scratched'])}` **You On** `{max((enemy_damage - player['armour']), 0)}` **Damage.**\n\n**You Perished! :(**",
                                        reply_markup=death_markup, parse_mode=enums.ParseMode.Markdown)
            await end_battle(cq.from_user.id)
        else:
            await cq.edit_message_caption(f"**Opponent** `{random.choice(['Hit', 'Wounded', 'Scratched'])}` **You On** `{max((enemy_damage - player['armour']), 0)}` **Damage.**\n\n**You Have Left** `{player['cur_hp']}` **Health.**",
                                        reply_markup=battle_markup, parse_mode=enums.ParseMode.Markdown)
            await update_time(cq.from_user.id)
    elif enemy['attack_type'] == 'mag':
        enemy_damage = enemy['attack'] * 1.5 if random.random() < 0.2 else enemy['attack']
        player['cur_hp'] -= max((enemy_damage - player['magic_armour']), 0)
        await update_player(cq.from_user.id, player)
        if player['cur_hp'] <= 0:
            await cq.edit_message_caption(f"**Opponent** `{random.choice(['Hit', 'Hurt', 'Scratched'])}` **You On** `{max((enemy_damage - player['magic_armour']), 0)}` **Damage.**\n\n"
                                            f"**You Perished ! :(**",
                                        reply_markup=death_markup, parse_mode=enums.ParseMode.MARKDOWN)
            await end_battle(cq.from_user.id)
        else:
            await cq.edit_message_caption(f"**Opponent** `{random.choice(['Cast A Spell', 'Fireball Launched', 'Cast A Spell'])}` **And Wounded You On** `{max((enemy_damage - player['magic_armour']), 0)}` **Damage.**\n\n"
                                            f"**You Have Left** `{player['cur_hp']}` **Health.**",
                                        reply_markup=battle_markup, parse_mode=enums.ParseMode.MARKDOWN)
            await update_time(cq.from_user.id)

    

@app.on_callback_query(filters.regex("attack"))
async def atck_cq(_, cq):
    await update_time(cq.from_user.id)
    battle = get_battle(cq.from_user.id)
    enemy = battle["enemy"]
    player = await get_player(cq.from_user.id)
    damage = player['attack'] * 1.5 if random.random() < 0.2 else player['attack']
    enemy['hp'] -= max(damage - enemy['armour'], 0)
    crit = f"**Attack On** `{damage}` **Damage!**"
    win_markup = InlineKeyboardMarkup(
            inline_keyboard=[
                [InlineKeyboardButton("Back 🔙", callback_data="leave_city")],
                [InlineKeyboardButton("Keep Going 🚶‍♂️", callback_data="enter_dungeon")]
            ])
    death_markup = InlineKeyboardMarkup(
            inline_keyboard=[
                [InlineKeyboardButton("Be Reborn 💞", callback_data="revive")]
            ])
    battle_markup = InlineKeyboardMarkup(
            inline_keyboard=[
                [InlineKeyboardButton("Estimate 🧮", callback_data="check")],
                [InlineKeyboardButton("Attack ⚔️", callback_data="attack")],
                [InlineKeyboardButton("Drink The Potion ⚱️", callback_data="heal")]
            ])
    if damage > player['attack']:
            crit = f"**Critical Attack On** `{damage}` **Damage!**"
    if enemy['hp'] <= 0:
            lup = ""
            new_xp = player['exp'] + enemy['exp']
            if new_xp >= 100:
                player['level'] += 1
                player['hp'] += 10
                player['exp'] = new_xp - 100
                lup = f"\n\n**Level Up! Now Your Level:** `{player['level']}`"
            else:
                player['exp'] = new_xp
            player['money'] += enemy['money']
            await cq.edit_message_caption(f"{crit}\n\n**You Won! Received** `{enemy['exp']}` **Experience And** `{enemy['money']}` **Coins.** {lup}",
                                        reply_markup=win_markup, parse_mode=enums.ParseMode.MARKDOWN)
            player['exp'] += enemy['exp']
            player['money'] += enemy['money']
            
            await end_battle(cq.from_user.id)
    else:
        for i in range(0, 4):
             await cq.edit_message_caption(f"{crit}\n**The Enemy Has** `{enemy['hp']}` **Health.**\n\n"
                                          f"`The Enemy Is Attacking`" + "." * (i % 4), parse_mode=enums.ParseMode.Markdown)
             await asyncio.sleep(0.6)
    if enemy['attack_type'] == 'phys':
                enemy_damage = random.choices([enemy['attack'], enemy['attack'] * 1.5], weights=[0.8, 0.2])[0]
                player['cur_hp'] -= max((enemy_damage - player['armour']), 0)
                if player['cur_hp'] <= 0:
                    await cq.edit_message_caption(f"**Opponent** `{random.choice(['Hit', 'Wounded', 'Scratched'])}` **You On** `{max((enemy_damage - player['armour']), 0)}` **Damage.**\n\n **You Perished! :(**",
                                                reply_markup=death_markup, parse_mode=enums.ParseMode.Markdown)
                    await end_battle(cq.from_user.id)
                else:
                    await cq.edit_message_caption(f"**Opponent** `{random.choice(['Hit', 'Wounded', 'Scratched'])}` **You On** `{max((enemy_damage - player['armour']), 0)}` **Damage.**\n\n"
                                                     f"**You Have Left** `{player['cur_hp']}` **Health.**",
                                                reply_markup=battle_markup, parse_mode=enums.ParseMode.MARKDOWN)
                    await update_time(cq.from_user.id)
    elif enemy['attack_type'] == 'mag':
                enemy_damage = random.choices([enemy['attack'], enemy['attack'] * 1.5], weights=[0.8, 0.2])[0]
                player['cur_hp'] -= max((enemy_damage - player['magic_armour']), 0)
                if player['cur_hp'] <= 0:
                    await cq.edit_message_caption(f"**Opponent** `{random.choice(['Hit', 'Hurt', 'Scratched'])}` **You On** `{max((enemy_damage - player['magic_armour']), 0)}` **Damage.**\n\n **You Perished ! :(**",
                                                reply_markup=death_markup, parse_mode=enums.ParseMode.MARKDOWN)
                else:
                    await cq.edit_message_caption(f"**Opponent** `{random.choice(['Cast A Spell', 'Fireball Launched', 'Cast A Spell'])}` **And Wounded You On** `{max((enemy_damage - player['magic_armour']), 0)}` **Damage.**\n\n"
                                                    f"**You Have Left** `{player['cur_hp']}` **Health.**",
                                                reply_markup=battle_markup, parse_mode=enums.ParseMode.MARKDOWN)
                    await update_time(cq.from_user.id)
    await update_player(cq.from_user.id, player)
        
