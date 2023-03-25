from pyrogram import *
from pyrogram.types import *

from Sylvie import *
from Sylvie.Database import *
from Sylvie.plugins.buttons import *

cur_fights = dict()
class State:
    answered = False

@bot.callback_query()
async def handle(_, cq):
    async def wait(cq, state):
        for i in range(300):
            if state.answered:
                break
            await asyncio.sleep(0.2)
        if not state.answered:
            state.answered = True
            await cq.edit_message_text("`You Fell Asleep On The Battlefield And Became An Easy Target For The Enemy.`\n\n"
                                             f"**You Perished! :(**", reply_markup=death_markup,
                                        parse_mode=enums.ParseMode.MARKDOWN)

    cur_loc = (await db.persons.find_one({"user_id": message.from_user.id}))["LocationID"]
    cur_loc_x = (await db.locations.find_one({"LocationID": cur_loc}))["XCoord"]
    cur_loc_y = (await db.locations.find_one({"LocationID": cur_loc}))["YCoord"]
    if cq.data == "shop":
        if cur_loc == 1:
            await cq.edit_message_text("🛒 **Welcome To Shop!**", reply_markup=shop_markup_1,
                                        parse_mode=enums.ParseMode.MARKDOWN)
        elif cur_loc == 2:
            await cq.edit_message_text("🛒 **Welcome To Shop!**", reply_markup=shop_markup_2,
                                        parse_mode=enums.ParseMode.MARKDOWN)

    elif cq.data == "stats":
        user_id = cq.from_user.id
        uwu = await db.persons.find_one({"user_id": user_id})
        name = uwu["Name"]
        level = uwu["Level"] 
        hp = uwu["HP"] 
        cur_hp = uwu["CurHP"]
        attack = uwu["Attack"]
        m_attack = uwu["MagicAttack"]
        armour = uwu["Armour"]
        m_armour = uwu["MagicArmour"]
        xp = uwu["XP"]
        balance = uwu["Money"]
        await cq.edit_message_text(f"🧝 **Your Character's Statistics:**\n\n"
                                         f"**Name:** `{name}`\n\n"
                                         f"**Level:** `{level}` (`{100 - xp}` **To Sl.**)\n\n"
                                         f"**Health:** `{cur_hp}`/`{hp}`\n\n"
                                         f"**Damage:** `{attack}` ⚔️  `{m_attack}` 🪄\n\n"
                                         f"**Armor:** `{armour}` 🛡️  `{m_armour}` 🔮\n\n"
                                         f"**Balance:** `{balance}` 💎", reply_markup=stats_markup,
                                    parse_mode=enums.ParseMode.MARKDOWN")
    elif cq.data == "back_town":
        if cur_loc >= 3:  # will break when naively adding new locks, you need to carefully
            await get_dungeon(cq)
        else:
            await get_town(cq)
    elif cq.data == "back_dungeon":
        await get_dungeon(cq)
    elif cq.data == "leave_city":
        await get_map(cq)
    elif cq.data[0:2] == "go":
        aim_x = (await db.locations.find_one({"LocationID": cq.data[3:]}))["XCoord"]
        aim_y = (await db.locations.find_one({"LocationID": cq.data[3:]}))["YCoord"]
        delay = count_distance(cur_loc_x, cur_loc_y, aim_x, aim_y)
        await go_loc(cq.from_user.id, -1, cq)
        ticks = floor(delay / 0.6)
        for i in range(1, ticks):
            await cq.edit_message_text(f"**On My Way**" + "." * (i % 4),
                                        parse_mode=enums.ParseMode.Markdown)

            await asyncio.sleep(0.6)
        await go_loc(cq.from_user.id, int(cq.data[3:]), cq)
    elif cq.data == 'enter_dungeon':
        if cur_loc == 3:
            options = [1, 2]
            probabilities = [0.8, 0.2]
            enemy_id = random.choices(options, probabilities)[0]
        elif cur_loc == 4:
            options = [3, 4, 5]
            probabilities = [0.6, 0.3, 0.1]
            enemy_id = random.choices(options, probabilities)[0]
        enemy = Enemy(enemy_id)
        enemy_name = enemy["Name"]
        player = await db.persons.find_one({"user_id": cq.from_user.id})
        await cq.edit_message_text(f"`{enemy_name}` {random.choice(['`Got In The Way!`', '`Jumped Out Of The Corner!`', '`Crept Unnoticed!`'])}",
                                    reply_markup=battle_markup)
        player["LocationID"] = -2
        await db.persons.replace_one({"user_id": cq.from_user.id}, player)
        state = State()
        cur_fights[player["Name"]] = [enemy, player, cur_loc, state]
        await wait(cq, state)
    elif cq.data == 'attack':
        cur_fights[cq.from_user.id][3].answered = True
        enemy = cur_fights[cq.from_user.id][0]
        player = cur_fights[cq.from_user.id][1]
        damage = player["Attack"] * 1.5 if random.random() < 0.2 else player["Attack"]
        enemy["HP"] -= max(damage - enemy["Armour"], 0)
        crit = f"**Attack On** `{damage}` **Damage!**"
        if damage > player["Attack"]:
            crit = f"**Critical Attack On** `{damage}` **Damage!**"
        if enemy["HP"] <= 0:
            lup = ""
            new_xp = player["XP"] + enemy["XP"]
            if new_xp >= 100:
                player["Level"] += 1
                player["HP"] += 10
                player["XP"] = new_xp - 100
                lup = f"\n\n**Level Up! Now Your Level:** `{player["Level"]}`"
            else:
                player["XP"] = new_xp
            player["Money"] += enemy["Money"]
            await cq.edit_message_text(f"{crit}\n\n**You Won! Received** `{enemy["XP"]}` **Experience And** `{enemy["Money"]}` **Coins.**"
                                             f"{lup}",
                                        reply_markup=win_markup, parse_mode=enums.ParseMode.MARKDOWN)
            player["XP"] += enemy["XP"]
            player["Money"] += enemy["Money"]
            player["LocationID"] = cur_fights[player["Name"]][2]
            cur_fights.pop(player["Name"])
        else:
            for i in range(0, 4):
                await cq.edit_message_text(f"{crit}\n**The Enemy Has** `{enemy["HP"]}` **Health.**\n\n"
                                                 f"`The Enemy Is Attacking`" + "." * (i % 4), parse_mode=enums.ParseMode.Markdown)
                await asyncio.sleep(0.6)
            if enemy["AttackType"] == 'phys':
                enemy_damage = random.choices([enemy["Attack"], enemy["Attack"] * 1.5], weights=[0.8, 0.2])[0]
                player["CurHP"] -= max((enemy_damage - player["Armour"]), 0)
                if player["CurHP"] <= 0:
                    await cq.edit_message_text(f"**Opponent** {random.choice(['`Hit`', '`Wounded`', '`Scratched`'])} **You On** `{max((enemy_damage - player["Armour"]), 0)}` **Damage.**\n\n"
                                                     f"**You Perished! :(**",
                                                reply_markup=death_markup, parse_mode=enums.ParseMode.Markdown)
                else:
                    await cq.edit_message_text(f"**Opponent** {random.choice(['`Hit`', '`Wounded`', '`Scratched`'])} **You On** `{max((enemy_damage - player["Armour"]), 0)}` **Damage.**\n\n"
                                                     f"**You Have Left** `{player["CurHP"]}` **Health.**",
                                                reply_markup=battle_markup, parse_mode=enums.ParseMode.MARKDOWN)
                    state = State()
                    cur_fights[cq.from_user.id][3] = state
                    await wait(cq, state)
            elif enemy["AttackType"] == 'mag':
                enemy_damage = random.choices([enemy["Attack"], enemy["Attack"] * 1.5], weights=[0.8, 0.2])[0]
                player["CurHP"] -= max((enemy_damage - player["MagicArmour"]), 0)
                if player["CurHP"] <= 0:
                    await cq.edit_message_text(f"**Opponent** {random.choice(['`Hit`', '`Hurt`', '`Scratched`'])} **You On** `{max((enemy_damage - player["MagicArmour"]), 0)}` **Damage.**\n\n"
                                                     f"**You Perished ! :(**",
                                                reply_markup=death_markup, parse_mode=enums.ParseMode.MARKDOWN)
                else:
                    await cq.edit_message_text(f"**Opponent** {random.choice(['`Cast A Spell`', '`Fireball Launched`', '`Cast A Spell`'])} **And Wounded You On** `{max((enemy_damage - player["MagicArmour"]), 0)}` **Damage.**\n\n"
                                                    f"**You Have Left** `{player["CurHP"]}` **Health.**",
                                                reply_markup=battle_markup, parse_mode=enums.ParseMode.MARKDOWN)
                    state = State()
                    cur_fights[cq.from_user.id][3] = state
                    await wait(cq, state)
        await db.persons.replace_one({"user_id": cq.from_user.id}, player)
    elif cq.data == 'check':
        print(cur_fights)
        enemy = cur_fights[cq.from_user.id][0]
        await cq.edit_message_text(f"**{enemy["Name"]}**:\n\n"
                                         f"**Health:** `{enemy["HP"]}`/`{(await db.mobs.find_one({'MobName': name}))["Name"]}`\n"
                                         f"**Attack:** `{enemy["Attack"]}` {'⚔️' if enemy["AttackType"] == 'phys' else '🪄'}\n"
                                         f"**Protection:** `{enemy["Armour"]}` 🛡️ `{enemy["MagicArmour"]}` 🔮",
                                    reply_markup=check_markup, parse_mode=enums.ParseMode.MARKDOWN")
    elif cq.data == 'revive':
        player = cur_fights[cq.from_user.id][1]
        cur_fights.pop(cq.from_user.id)
        player["LocationID"] = 1
        player["CurHP"] = player["HP"]
        await get_town(cq)
        await db.persons.replace_one({"user_id": cq.from_user.id}, player)
    elif cq.data[0:3] == 'buy':
        player = await db.persons.find_one({"user_id": cq.from_user.id})
        item = await db.items.find_one({"_id": int(cq.data[4:])})
        if player["Money"] < item["Cost"]:
            if player["LocationID"] == 1:
                await cq.edit_message_text("`Not Enough Coins.`", reply_markup=no_money_markup,
                                            parse_mode=enums.ParseMode.Markdown)
            elif player["LocationID"] == 2:
                await cq.edit_message_text("`Not Enough Coins.`", reply_markup=no_money_markup,
                                            parse_mode=enums.ParseMode.Markdown)
        else:
            player["Money"] -= item["Cost"]
            await db.persons.replace_one({"user_id": cq.from_user.id}, player)
            item_in_inv = await db.inventory.find_one({'user_id': cq.from_user.id, 'item_id': item["ItemID"]})
            if item_in_inv is None:
                print('aaa')    
                new_data = Inventory(user_id=cq.from_user.id, Name=player["Name"], ItemID=int(cq.data[4:]), Quantity=0))
                await db.inventory.insert_one(new_data)
            item_in_inv_changeable = await db.inventory.find_one({'user_id': cq.from_user.id, 'item_id': item["ItemID"]})
            if item_in_inv_changeable['Quantity'] <= 0:
                item_in_inv_changeable['Quantity'] -= 1
            else:
                item_in_inv_changeable['Quantity'] += 1
            await db.inventory.replace_one({"user_id": cq.from_user.id, 'item_id': item["ItemID"]}, item_in_inv_changeable)
            if player["LocationID"] == 1:
                await cq.edit_message_text(f"**You Bought An Item** `{item["Name"]}`. **You Now Have Them In Your Inventory** `{abs(amt)+1}`.",
                                            reply_markup=shop_markup_1, parse_mode=enums.ParseMode.Markdown)
            elif player["LocationID"] == 2:
                await cq.edit_message_text(f"**You Bought An Item** `{item["Name"]}`. **You Now Have Them In Your Inventory** `{abs(amt) + 1}`.",
                                            reply_markup=shop_markup_2, parse_mode=enums.ParseMode.Markdown)
    elif cq.data == 'inventory':
        inventory_markup = []
        cur_inv = await db.inventory.find_one({'user_id': cq.from_user.id})
        text = ''
        for item in cur_inv:
            item_doc = await db.items.find_one({'ItemID': item['ItemID']})
            name = item_doc['Name']
            quantity = item['Quantity']
            item_type = item_doc['ItemType']
            if quantity != 0:
                if quantity < 0 and item_type != 'potion':
                    inventory_markup.append(InlineKeyboardButton(
                        f"Put On {name}",
                        callback_data=f'wear_{item["ItemID"]}'))
                text += f'{name} - {abs(quantity)} PC. {"✅" if quantity > 0 else ""}\n'
                inventory_markup.append(InlineKeyboardButton(
                    f"Sell {name} ({item_doc['CostToSale']} 💎)",
                    callback_data=f'sell_{item["ItemID"]}'))
        await cq.edit_message_text(f"**Your Inventory:**\n\n"
                                         f"{'`Empty`!' if text == '' else `text`}",
                                    reply_markup=InlineKeyboardMarkup(inventory_markup), parse_mode=enums.ParseMode.Markdown)
    elif cq.data[0:3] == 'sel':
        item_to_sell = int(cq.data[5:])
        item_in_inv = await db.inventory.find_one({'user_id': cq.from_user.id, 'item_id': item_to_sell})
        if item_in_inv["Quantity"] < 0:
            item_in_inv["Quantity"] += 1
        elif item_in_inv["Quantity"] > 0:
            item_in_inv["Quantity"] -= 1
        user = await db.persons.find_one({'user_id': cq.from_user.id})
        item_cost = await db.items.find_one({"ItemID": item_to_sell})
        user["Money"] += item_cost["CostToSale"]
        await db.persons.replace_one({"user_id": cq.from_user.id}, user)
        await db.inventory.replace_one({"user_id": cq.from_user.id, 'item_id': item_to_sell}, item_in_inv)
        await cq.edit_message_text(f"**You Sold** {item_cost["Name"]}",
                                    reply_markup=after_deal_markup, parse_mode=enums.ParseMode.Markdown)
    elif cq.data[0:3] == 'wea':
        user = await db.persons.find_one({'user_id': cq.from_user.id})
        item_to_wear = int(cq.data[5:])
        item_to_wear_inst = await db.items.find_one({"ItemID": item_to_wear})
        item_type = item_to_wear_inst["ItemType"]
        print(item_type)
        if item_to_wear_inst["ReqLevel"] > user["Level"]:
            await cq.edit_message_text(f"`You Are Too Small, To Wear This Item.`",
                                        reply_markup=after_deal_markup, parse_mode=enums.ParseMode.Markdown)
        else:
            player_inv = await db.inventory.find_one({'user_id': cq.from_user.id})
            for item in player_inv:
                inv_item_type = await db.items.find_one({"ItemID": item["Inventory"]["ItemID"]})
                if inv_item_type == item_type:
                    found_item = await db.inventory.find_one({'user_id': cq.from_user.id, 'item_id': item["Inventory"]["ItemID"]})
                    found_item_inst = await db.items.find_one({"ItemID": item["Inventory"]["ItemID"]})
                    if found_item["Quantity"] > 0:
                        found_item["Quantity"] *= -1
                        user = await db.persons.find_one({'user_id': cq.from_user.id})
                        user["HP"] -= found_item_inst["HP"]
                        user["Attack"] -= found_item_inst["Attack"]
                        user["MagicAttack"] -= found_item_inst["MagicAttack"]
                        user["Armour"] -= found_item_inst["Armour"]
                        user["MagicArmour"] -= found_item_inst["MagicArmour"]
                        await db.persons.replace_one({"user_id": cq.from_user.id}, user)
                        await db.inventory.replace_one({"user_id": cq.from_user.id, 'item_id': item["Inventory"]["ItemID"]}, found_item)
            stmt = await db.inventory.find_one({'user_id': cq.from_user.id, 'item_id': item_to_wear})
            stmt["Quantity"] *= -1
            user = await db.persons.find_one({'user_id': cq.from_user.id})
            user["HP"] += item_to_wear_inst["HP"]
            user["Attack"] += item_to_wear_inst["Attack"]
            user["MagicAttack"] += item_to_wear_inst["MagicAttack"]
            user["Armour"] += item_to_wear_inst["Armour"]
            user["MagicArmour"] += item_to_wear_inst["MagicArmour"]
            await db.persons.replace_one({"user_id": cq.from_user.id}, user)
            await db.inventory.replace_one({"user_id": cq.from_user.id, 'item_id': item_to_wear}, stmt)
            await cq.edit_message_text(f"**You Put On** `{(await db.items.find_one({"ItemID": item_to_wear}))["Name"]}`",
                                    reply_markup=after_deal_markup, parse_mode=enums.ParseMode.Markdown)
    elif cq.data == 'heal':
        cur_fights[cq.from_user.id][3].answered = True
        enemy = cur_fights[cq.from_user.id][0]
        player = cur_fights[cq.from_user.id][1]
        stmt = select(Inventory).where(Inventory.Nickname == cq.from_user.id).where(Inventory.ItemID == 9)
        if session.scalars(stmt).one().Quantity != 0:
            stmt1 = select(Persons).where(Persons.Nickname == cq.from_user.id)
            if session.scalars(stmt).one().Quantity > 0:
                session.scalars(stmt).one().Quantity -= 1
            else:
                session.scalars(stmt).one().Quantity += 1
            session.scalars(stmt1).one().CurHP = min((session.scalars(stmt1).one().CurHP + 5), session.scalars(stmt1).one().HP)
            session.commit()
            for i in range(0, 4):
                await bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.id,
                                            text=f"You Drank A Health Potion! Restored 5 Hp. Current Health: {session.scalars(stmt1).one().CurHP}\n\n"
                                                 f"The Enemy Is Attacking" + "." * (i % 4), parse_mode=enums.ParseMode.Markdown)
                await asyncio.sleep(0.6)
        else:
            for i in range(0, 4):
                await bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.id,
                                            text=f"You Reached Into Your Backpack For A Potion, But He Wasn't There!\n\n"
                                                 f"The Enemy Is Attacking" + "." * (i % 4), parse_mode=enums.ParseMode.Markdown)
                await asyncio.sleep(0.6)
        if enemy["AttackType"] == 'phys':
            enemy_damage = numpy.random.choice([enemy["Attack"], enemy["Attack"] * 1.5], p=[0.8, 0.2])
            player["CurHP"] -= max((enemy_damage - player["Armour"]), 0)
            if player["CurHP"] <= 0:
                await bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.id,
                                            text=f"Opponent {random.choice(['Hit', 'Wounded', 'Scratched'])} You On {max((enemy_damage - player["Armour"]), 0)} Damage.\n\n"
                                                 f"*You Perished! :(*",
                                            reply_markup=death_markup, parse_mode=enums.ParseMode.Markdown)
            else:
                await bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.id,
                                            text=f"Opponent {random.choice(['Hit', 'Wounded', 'Scratched'])} You On {max((enemy_damage - player["Armour"]), 0)} Damage.\n\n"
                                                 f"You Have Left {player["CurHP"]} Health.",
                                            reply_markup=battle_markup, parse_mode=enums.ParseMode.Markdown)
                state = State()
                cur_fights[cq.from_user.id][3] = state
                await wait(cq, state)
        elif enemy["AttackType"] == 'mag':
            enemy_damage = numpy.random.choice([enemy["Attack"], enemy["Attack"] * 1.5], p=[0.8, 0.2])
            player["CurHP"] -= max((enemy_damage - player["MagicArmour"]), 0)
            if player["CurHP"] <= 0:
                await bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.id,
                                            text=f"Opponent {random.choice(['Hit', 'Hurt', 'Scratched'])} You On {max((enemy_damage - player["MagicArmour"]), 0)} Damage.\n\n"
                                                 f"*You Perished ! :(*",
                                            reply_markup=death_markup, parse_mode=enums.ParseMode.Markdown)
            else:
                await bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.id,
                                            text=f"Opponent {random.choice(['Cast A Spell', 'Fireball Launched', 'Cast A Spell'])} And Wounded You On {max((enemy_damage - player["MagicArmour"]), 0)} Damage.\n\n"
                                                 f"You Have Left {player["CurHP"]} Health.",
                                            reply_markup=battle_markup, parse_mode=enums.ParseMode.Markdown)
                state = State()
                cur_fights[cq.from_user.id][3] = state
                await wait(cq, state)
    await bot.answer_callback_query(cq.id)
