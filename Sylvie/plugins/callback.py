import random
from pyrogram import *
from pyrogram.types import *

from Sylvie import *
from Sylvie.Database import *
from Sylvie.plugins.buttons import *

cur_fights = dict()
heal_potion = 9 # the _id of heal potion
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

    cur_loc = (await db.persons.find_one({"user_id": message.from_user.id}))["location_id"]
    cur_loc_x = (await db.locations.find_one({"location_id": cur_loc}))["x_coord"]
    cur_loc_y = (await db.locations.find_one({"location_id": cur_loc}))["y_coord"]
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
        name = uwu["name"]
        level = uwu["level"] 
        hp = uwu["hp"] 
        cur_hp = uwu["cur_hp"]
        attack = uwu["attack"]
        m_attack = uwu["magic_attack"]
        armour = uwu["armour"]
        m_armour = uwu["magic_armour"]
        xp = uwu["xp"]
        balance = uwu["money"]
        await cq.edit_message_text(f"🧝 **Your Character"s Statistics:**\n\n"
                                         f"**name:** `{name}`\n\n"
                                         f"**level:** `{level}` (`{100 - xp}` **To Sl.**)\n\n"
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
        aim_x = (await db.locations.find_one({"location_id": cq.data[3:]}))["x_coord"]
        aim_y = (await db.locations.find_one({"location_id": cq.data[3:]}))["y_coord"]
        delay = count_distance(cur_loc_x, cur_loc_y, aim_x, aim_y)
        await go_loc(cq.from_user.id, -1, cq)
        ticks = floor(delay / 0.6)
        for i in range(1, ticks):
            await cq.edit_message_text(f"**On My Way**" + "." * (i % 4),
                                        parse_mode=enums.ParseMode.Markdown)

            await asyncio.sleep(0.6)
        await go_loc(cq.from_user.id, int(cq.data[3:]), cq)
    elif cq.data == "enter_dungeon":
        if cur_loc == 3:
            options = [1, 2]
            probabilities = [0.8, 0.2]
            enemy_id = random.choices(options, probabilities)[0]
        elif cur_loc == 4:
            options = [3, 4, 5]
            probabilities = [0.6, 0.3, 0.1]
            enemy_id = random.choices(options, probabilities)[0]
        enemy = Enemy(enemy_id)
        enemy_name = enemy["name"]
        player = await db.persons.find_one({"user_id": cq.from_user.id})
        await cq.edit_message_text(f"`{enemy_name}` `{random.choice(["Got In The Way!", "Jumped Out Of The Corner!", "Crept Unnoticed!"])}`",
                                    reply_markup=battle_markup)
        player["location_id"] = -2
        await db.persons.replace_one({"user_id": cq.from_user.id}, player)
        state = State()
        cur_fights[player["name"]] = [enemy, player, cur_loc, state]
        await wait(cq, state)
    elif cq.data == "attack":
        cur_fights[cq.from_user.id][3].answered = True
        enemy = cur_fights[cq.from_user.id][0]
        player = cur_fights[cq.from_user.id][1]
        damage = player["attack"] * 1.5 if random.random() < 0.2 else player["attack"]
        enemy["hp"] -= max(damage - enemy["armour"], 0)
        crit = f"**attack On** `{damage}` **Damage!**"
        if damage > player["attack"]:
            crit = f"**Critical attack On** `{damage}` **Damage!**"
        if enemy["hp"] <= 0:
            lup = ""
            new_xp = player["xp"] + enemy["xp"]
            if new_xp >= 100:
                player["level"] += 1
                player["hp"] += 10
                player["xp"] = new_xp - 100
                lup = f"\n\n**level Up! Now Your level:** `{player["level"]}`"
            else:
                player["xp"] = new_xp
            player["money"] += enemy["money"]
            await cq.edit_message_text(f"{crit}\n\n**You Won! Received** `{enemy["xp"]}` **Experience And** `{enemy["money"]}` **Coins.**"
                                             f"{lup}",
                                        reply_markup=win_markup, parse_mode=enums.ParseMode.MARKDOWN)
            player["xp"] += enemy["xp"]
            player["money"] += enemy["money"]
            player["location_id"] = cur_fights[player["name"]][2]
            cur_fights.pop(player["name"])
        else:
            for i in range(0, 4):
                await cq.edit_message_text(f"{crit}\n**The Enemy Has** `{enemy["hp"]}` **Health.**\n\n"
                                                 f"`The Enemy Is attacking`" + "." * (i % 4), parse_mode=enums.ParseMode.Markdown)
                await asyncio.sleep(0.6)
            if enemy["attack_type"] == "phys":
                enemy_damage = random.choices([enemy["attack"], enemy["attack"] * 1.5], weights=[0.8, 0.2])[0]
                player["cur_hp"] -= max((enemy_damage - player["armour"]), 0)
                if player["cur_hp"] <= 0:
                    await cq.edit_message_text(f"**Opponent** `{random.choice(["Hit", "Wounded", "Scratched"])}` **You On** `{max((enemy_damage - player["armour"]), 0)}` **Damage.**\n\n"
                                                     f"**You Perished! :(**",
                                                reply_markup=death_markup, parse_mode=enums.ParseMode.Markdown)
                else:
                    await cq.edit_message_text(f"**Opponent** `{random.choice(["Hit", "Wounded", "Scratched"])}` **You On** `{max((enemy_damage - player["armour"]), 0)}` **Damage.**\n\n"
                                                     f"**You Have Left** `{player["cur_hp"]}` **Health.**",
                                                reply_markup=battle_markup, parse_mode=enums.ParseMode.MARKDOWN)
                    state = State()
                    cur_fights[cq.from_user.id][3] = state
                    await wait(cq, state)
            elif enemy["attack_type"] == "mag":
                enemy_damage = random.choices([enemy["attack"], enemy["attack"] * 1.5], weights=[0.8, 0.2])[0]
                player["cur_hp"] -= max((enemy_damage - player["magic_armour"]), 0)
                if player["cur_hp"] <= 0:
                    await cq.edit_message_text(f"**Opponent** `{random.choice(["Hit", "Hurt", "Scratched"])}` **You On** `{max((enemy_damage - player["magic_armour"]), 0)}` **Damage.**\n\n"
                                                     f"**You Perished ! :(**",
                                                reply_markup=death_markup, parse_mode=enums.ParseMode.MARKDOWN)
                else:
                    await cq.edit_message_text(f"**Opponent** `{random.choice(["Cast A Spell", "Fireball Launched", "Cast A Spell"])}` **And Wounded You On** `{max((enemy_damage - player["magic_armour"]), 0)}` **Damage.**\n\n"
                                                    f"**You Have Left** `{player["cur_hp"]}` **Health.**",
                                                reply_markup=battle_markup, parse_mode=enums.ParseMode.MARKDOWN)
                    state = State()
                    cur_fights[cq.from_user.id][3] = state
                    await wait(cq, state)
        await db.persons.replace_one({"user_id": cq.from_user.id}, player)
    elif cq.data == "check":
        print(cur_fights)
        enemy = cur_fights[cq.from_user.id][0]
        await cq.edit_message_text(f"**{enemy["name"]}**:\n\n"
                                         f"**Health:** `{enemy["hp"]}`/`{(await db.mobs.find_one({"mob_name": name}))["name"]}`\n"
                                         f"**attack:** `{enemy["attack"]}` {"⚔️" if enemy["attack_type"] == "phys" else "🪄"}\n"
                                         f"**Protection:** `{enemy["armour"]}` 🛡️ `{enemy["magic_armour"]}` 🔮",
                                    reply_markup=check_markup, parse_mode=enums.ParseMode.MARKDOWN")
    elif cq.data == "revive":
        player = cur_fights[cq.from_user.id][1]
        cur_fights.pop(cq.from_user.id)
        player["location_id"] = 1
        player["cur_hp"] = player["hp"]
        await get_town(cq)
        await db.persons.replace_one({"user_id": cq.from_user.id}, player)
    elif cq.data[0:3] == "buy":
        player = await db.persons.find_one({"user_id": cq.from_user.id})
        item = await db.items.find_one({"_id": int(cq.data[4:])})
        if player["money"] < item["cost"]:
            if player["location_id"] == 1:
                await cq.edit_message_text("`Not Enough Coins.`", reply_markup=no_money_markup,
                                            parse_mode=enums.ParseMode.Markdown)
            elif player["location_id"] == 2:
                await cq.edit_message_text("`Not Enough Coins.`", reply_markup=no_money_markup,
                                            parse_mode=enums.ParseMode.Markdown)
        else:
            player["money"] -= item["cost"]
            await db.persons.replace_one({"user_id": cq.from_user.id}, player)
            item_in_inv = await db.inventory.find_one({"user_id": cq.from_user.id, "item_id": item["item_id"]})
            if item_in_inv is None:
                print("aaa")    
                new_data = Inventory(user_id=cq.from_user.id, name=player["name"], item_id=int(cq.data[4:]), quantity=0))
                await db.inventory.insert_one(new_data)
            item_in_inv_changeable = await db.inventory.find_one({"user_id": cq.from_user.id, "item_id": item["item_id"]})
            if item_in_inv_changeable["quantity"] <= 0:
                item_in_inv_changeable["quantity"] -= 1
            else:
                item_in_inv_changeable["quantity"] += 1
            await db.inventory.replace_one({"user_id": cq.from_user.id, "item_id": item["item_id"]}, item_in_inv_changeable)
            if player["location_id"] == 1:
                await cq.edit_message_text(f"**You Bought An Item** `{item["name"]}`. **You Now Have Them In Your Inventory** `{abs(amt)+1}`.",
                                            reply_markup=shop_markup_1, parse_mode=enums.ParseMode.Markdown)
            elif player["location_id"] == 2:
                await cq.edit_message_text(f"**You Bought An Item** `{item["name"]}`. **You Now Have Them In Your Inventory** `{abs(amt) + 1}`.",
                                            reply_markup=shop_markup_2, parse_mode=enums.ParseMode.Markdown)
    elif cq.data == "inventory":
        inventory_markup = []
        cur_inv = await db.inventory.find_one({"user_id": cq.from_user.id})
        text = ""
        for item in cur_inv:
            item_doc = await db.items.find_one({"item_id": item["item_id"]})
            name = item_doc["name"]
            quantity = item["quantity"]
            item_type = item_doc["item_type"]
            if quantity != 0:
                if quantity < 0 and item_type != "potion":
                    inventory_markup.append(InlineKeyboardButton(
                        f"Put On {name}",
                        callback_data=f"wear_{item["item_id"]}"))
                text += f"{name} - {abs(quantity)} PC. {"✅" if quantity > 0 else ""}\n"
                inventory_markup.append(InlineKeyboardButton(
                    f"Sell {name} ({item_doc["sell_cost"]} 💎)",
                    callback_data=f"sell_{item["item_id"]}"))
        await cq.edit_message_text(f"**Your Inventory:**\n\n"
                                         f"{"`Empty`!" if text == "" else `text`}",
                                    reply_markup=InlineKeyboardMarkup(inventory_markup), parse_mode=enums.ParseMode.Markdown)
    elif cq.data[0:3] == "sel":
        item_to_sell = int(cq.data[5:])
        item_in_inv = await db.inventory.find_one({"user_id": cq.from_user.id, "item_id": item_to_sell})
        if item_in_inv["quantity"] < 0:
            item_in_inv["quantity"] += 1
        elif item_in_inv["quantity"] > 0:
            item_in_inv["quantity"] -= 1
        user = await db.persons.find_one({"user_id": cq.from_user.id})
        item_cost = await db.items.find_one({"item_id": item_to_sell})
        user["money"] += item_cost["sell_cost"]
        await db.persons.replace_one({"user_id": cq.from_user.id}, user)
        await db.inventory.replace_one({"user_id": cq.from_user.id, "item_id": item_to_sell}, item_in_inv)
        await cq.edit_message_text(f"**You Sold** {item_cost["name"]}",
                                    reply_markup=after_deal_markup, parse_mode=enums.ParseMode.Markdown)
    elif cq.data[0:3] == "wea":
        user = await db.persons.find_one({"user_id": cq.from_user.id})
        item_to_wear = int(cq.data[5:])
        item_to_wear_inst = await db.items.find_one({"item_id": item_to_wear})
        item_type = item_to_wear_inst["item_type"]
        print(item_type)
        if item_to_wear_inst["req_level"] > user["level"]:
            await cq.edit_message_text(f"`You Are Too Small, To Wear This Item.`",
                                        reply_markup=after_deal_markup, parse_mode=enums.ParseMode.Markdown)
        else:
            player_inv = await db.inventory.find_one({"user_id": cq.from_user.id})
            for item in player_inv:
                inv_item_type = await db.items.find_one({"item_id": item["Inventory"]["item_id"]})
                if inv_item_type == item_type:
                    found_item = await db.inventory.find_one({"user_id": cq.from_user.id, "item_id": item["Inventory"]["item_id"]})
                    found_item_inst = await db.items.find_one({"item_id": item["Inventory"]["item_id"]})
                    if found_item["quantity"] > 0:
                        found_item["quantity"] *= -1
                        user = await db.persons.find_one({"user_id": cq.from_user.id})
                        user["hp"] -= found_item_inst["hp"]
                        user["attack"] -= found_item_inst["attack"]
                        user["magic_attack"] -= found_item_inst["magic_attack"]
                        user["armour"] -= found_item_inst["armour"]
                        user["magic_armour"] -= found_item_inst["magic_armour"]
                        await db.persons.replace_one({"user_id": cq.from_user.id}, user)
                        await db.inventory.replace_one({"user_id": cq.from_user.id, "item_id": item["Inventory"]["item_id"]}, found_item)
            stmt = await db.inventory.find_one({"user_id": cq.from_user.id, "item_id": item_to_wear})
            stmt["quantity"] *= -1
            user = await db.persons.find_one({"user_id": cq.from_user.id})
            user["hp"] += item_to_wear_inst["hp"]
            user["attack"] += item_to_wear_inst["attack"]
            user["magic_attack"] += item_to_wear_inst["magic_attack"]
            user["armour"] += item_to_wear_inst["armour"]
            user["magic_armour"] += item_to_wear_inst["magic_armour"]
            await db.persons.replace_one({"user_id": cq.from_user.id}, user)
            await db.inventory.replace_one({"user_id": cq.from_user.id, "item_id": item_to_wear}, stmt)
            await cq.edit_message_text(f"**You Put On** `{(await db.items.find_one({"item_id": item_to_wear}))["name"]}`",
                                    reply_markup=after_deal_markup, parse_mode=enums.ParseMode.Markdown)
    elif cq.data == "heal":
        cur_fights[cq.from_user.id][3].answered = True
        enemy = cur_fights[cq.from_user.id][0]
        player = cur_fights[cq.from_user.id][1]
        stmt = await db.inventory.find_one({"user_id": cq.from_user.id, "item_id": heal_potion})
        if stmt["quantity"] != 0:
            stmt1 = await db.persons.find_one({"user_id": cq.from_user.id})
            if stmt["quantity"] > 0:
                stmt["quantity"] -= 1
            else:
                stmt["quantity"] += 1
            stmt1["cur_hp"] = min((stmt1["cur_hp"] + 5), stmt1["hp"])
            await db.persons.replace_one({"user_id": cq.from_user.id}, stmt1)
            await db.inventory.replace_one({"user_id": cq.from_user.id, "item_id": heal_potion}, stmt)
            for i in range(0, 4):
                await cq.edit_message_text(f"**You Drank A Health Potion! Restored 5 hp. Current Health:** {stmt1["cur_hp"]}\n\n"
                                                 f"`The Enemy Is attacking`" + "." * (i % 4), parse_mode=enums.ParseMode.Markdown)
                await asyncio.sleep(0.6)
        else:
            for i in range(0, 4):
                await cq.edit_message_text(f"**You Reached Into Your Backpack For A Potion, But He Wasn"t There!**\n\n"
                                                 f"`The Enemy Is attacking`" + "." * (i % 4), parse_mode=enums.ParseMode.Markdown)
                await asyncio.sleep(0.6)
        if enemy["attack_type"] == "phys":
            enemy_damage = random.choices([enemy["attack"], enemy["attack"] * 1.5], weights=[0.8, 0.2])[0]
            player["cur_hp"] -= max((enemy_damage - player["armour"]), 0)
            await db.persons.replace_one({"user_id": cq.from_user.id}, player)
            if player["cur_hp"] <= 0:
                await cq.edit_message_text(f"**Opponent** `{random.choice(["Hit", "Wounded", "Scratched"])}` **You On** `{max((enemy_damage - player["armour"]), 0)}` **Damage.**\n\n"
                                                 f"**You Perished! :(**",
                                            reply_markup=death_markup, parse_mode=enums.ParseMode.Markdown)
            else:
                await cq.edit_message_text(f"**Opponent** `{random.choice(["Hit", "Wounded", "Scratched"])}` **You On** `{max((enemy_damage - player["armour"]), 0)}` **Damage.**\n\n"
                                                 f"**You Have Left** `{player["cur_hp"]}` **Health.**",
                                            reply_markup=battle_markup, parse_mode=enums.ParseMode.Markdown)
                state = State()
                cur_fights[cq.from_user.id][3] = state
                await wait(cq, state)
        elif enemy["attack_type"] == "mag":
            enemy_damage = enemy["attack"] * 1.5 if random.random() < 0.2 else enemy["attack"]
            player["cur_hp"] -= max((enemy_damage - player["magic_armour"]), 0)
            await db.persons.replace_one({"user_id": cq.from_user.id}, player)
            if player["cur_hp"] <= 0:
                await cq.edit_message_text(f"**Opponent** `{random.choice(["Hit", "Hurt", "Scratched"])}` **You On** `{max((enemy_damage - player["magic_armour"]), 0)}` **Damage.**\n\n"
                                                 f"**You Perished ! :(**",
                                            reply_markup=death_markup, parse_mode=enums.ParseMode.Markdown)
            else:
                await cq.edit_message_text(f"**Opponent** `{random.choice(["Cast A Spell", "Fireball Launched", "Cast A Spell"])}` **And Wounded You On** `{max((enemy_damage - player["magic_armour"]), 0)}` **Damage.**\n\n"
                                                 f"**You Have Left** `{player["cur_hp"]}` **Health.**",
                                            reply_markup=battle_markup, parse_mode=enums.ParseMode.Markdown)
                state = State()
                cur_fights[cq.from_user.id][3] = state
                await wait(cq, state)
    await bot.answer_callback_query(cq.id)
