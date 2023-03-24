from telebot.async_telebot import AsyncTeleBot, types
import sqlite3
from sqlalchemy import select
from math import floor
import numpy
import asyncio

from init_session import session
from functions import count_distance, get_town, get_map, get_dungeon, go_loc
from classes import Enemy, Inventory, Persons, Items, Mobs, Locations

TOKEN = '6202624871:AAES0GPYkc3mPND0qYbj21TqhcnhVxp0ldA'
bot = AsyncTeleBot(TOKEN)

db = sqlite3.connect('gametools.db')


# cities interface
town_markup = types.InlineKeyboardMarkup()
dungeons_list = types.InlineKeyboardButton("Leave The City", callback_data="leave_city")
shop = types.InlineKeyboardButton("Local Store", callback_data="shop")
stats = types.InlineKeyboardButton("Character Stats", callback_data="stats")
inventory = types.InlineKeyboardButton("Inventory", callback_data='inventory')
town_markup.add(dungeons_list)
town_markup.add(inventory)
town_markup.add(shop)
town_markup.add(stats)

# shop interface
shop_markup_1 = types.InlineKeyboardMarkup()
shop_markup_2 = types.InlineKeyboardMarkup()
back_shop_town = types.InlineKeyboardButton("Back", callback_data='back_town')
items_1 = session.execute(select(Items).where(Items.Availability == 1))
items_2 = session.execute(select(Items).where(Items.Availability == 2))
for item_1 in items_1:
    t_item = types.InlineKeyboardButton(f"Buy {item_1.Items.Name}: {item_1.Items.Cost} 💎",
                                        callback_data=f'buy_{item_1.Items.ItemID}')
    shop_markup_1.add(t_item)
for item_2 in items_2:
    t_item = types.InlineKeyboardButton(f"Buy {item_2.Items.Name}: {item_2.Items.Cost} 💎",
                                        callback_data=f'buy_{item_2.Items.ItemID}')
    shop_markup_2.add(t_item)
shop_markup_1.add(back_shop_town)
shop_markup_2.add(back_shop_town)

# statistics interface
stats_markup = types.InlineKeyboardMarkup()
back_stats_town = types.InlineKeyboardButton("Back", callback_data='back_town')
stats_markup.add(back_stats_town)

# location selection interface
choose_location_1_markup = types.InlineKeyboardMarkup()
choose_location_2_markup = types.InlineKeyboardMarkup()
choose_location_3_markup = types.InlineKeyboardMarkup()
choose_location_4_markup = types.InlineKeyboardMarkup()
x_1 = session.execute(select(Locations.XCoord).where(Locations.LocationID == 1)).scalar()
y_1 = session.execute(select(Locations.YCoord).where(Locations.LocationID == 1)).scalar()
x_2 = session.execute(select(Locations.XCoord).where(Locations.LocationID == 2)).scalar()
y_2 = session.execute(select(Locations.YCoord).where(Locations.LocationID == 2)).scalar()
x_3 = session.execute(select(Locations.XCoord).where(Locations.LocationID == 3)).scalar()
y_3 = session.execute(select(Locations.YCoord).where(Locations.LocationID == 3)).scalar()
x_4 = session.execute(select(Locations.XCoord).where(Locations.LocationID == 4)).scalar()
y_4 = session.execute(select(Locations.YCoord).where(Locations.LocationID == 4)).scalar()

# interface paint
battle_markup = types.InlineKeyboardMarkup()
check = types.InlineKeyboardButton("Estimate", callback_data='check')
attack = types.InlineKeyboardButton("Attack", callback_data='attack')
heal = types.InlineKeyboardButton("Drink The Potion", callback_data='heal')
battle_markup.add(check)
battle_markup.add(attack)
battle_markup.add(heal)

# evaluation interface
check_markup = types.InlineKeyboardMarkup()
check_markup.add(attack)

back_location_town = types.InlineKeyboardButton("Back", callback_data='back_town')
back_location_dungeon = types.InlineKeyboardButton("Back", callback_data='back_dungeon')
destinations = session.execute(select(Locations))
for destination in destinations:
    el_x = session.execute(select(Locations.XCoord).where(Locations.LocationID == destination.Locations.LocationID)).scalar()
    el_y = session.execute(select(Locations.YCoord).where(Locations.LocationID == destination.Locations.LocationID)).scalar()
    dist_1 = count_distance(x_1, y_1, el_x, el_y)
    dist_2 = count_distance(x_2, y_2, el_x, el_y)
    dist_3 = count_distance(x_3, y_3, el_x, el_y)
    dist_4 = count_distance(x_4, y_4, el_x, el_y)
    if 0 < dist_1 <= 10:
        choose_location_1_markup.add(types.InlineKeyboardButton(f"Go: {destination.Locations.LocationName}",
                                                                callback_data=f'go_{destination.Locations.LocationID}'))
    if 0 < dist_2 <= 10:
        choose_location_2_markup.add(types.InlineKeyboardButton(f"Go: {destination.Locations.LocationName}",
                                                                callback_data=f'go_{destination.Locations.LocationID}'))
    if 0 < dist_3 <= 10:
        choose_location_3_markup.add(types.InlineKeyboardButton(f"Go: {destination.Locations.LocationName}",
                                                                callback_data=f'go_{destination.Locations.LocationID}'))
    if 0 < dist_4 <= 10:
        choose_location_4_markup.add(types.InlineKeyboardButton(f"Go: {destination.Locations.LocationName}",
                                                                callback_data=f'go_{destination.Locations.LocationID}'))
choose_location_1_markup.add(back_location_town)
choose_location_2_markup.add(back_location_town)
choose_location_3_markup.add(back_location_dungeon)
choose_location_4_markup.add(back_location_dungeon)

# dungeon login interface
dungeon_gate_markup = types.InlineKeyboardMarkup()
back_to_map = types.InlineKeyboardButton(f"Back", callback_data='leave_city')
enter_dungeon = types.InlineKeyboardButton(f"Go To The Dungeon!", callback_data='enter_dungeon')
dungeon_gate_markup.add(enter_dungeon)
dungeon_gate_markup.add(stats)
dungeon_gate_markup.add(back_to_map)

# victory interface
win_markup = types.InlineKeyboardMarkup()
go_further = types.InlineKeyboardButton(f"Keep Going", callback_data='enter_dungeon')
win_markup.add(back_to_map)
win_markup.add(go_further)

# death interface
death_markup = types.InlineKeyboardMarkup()
revive = types.InlineKeyboardButton(f"Be Reborn", callback_data='revive')
death_markup.add(revive)

# interface in a situation where there is no money
no_money_markup = types.InlineKeyboardMarkup()
no_money_markup.add(back_location_town)

# interface after purchase
after_deal_markup = types.InlineKeyboardMarkup()
back_to_inv = types.InlineKeyboardButton(f"Back", callback_data='inventory')
after_deal_markup.add(back_to_inv)

cur_fights = dict()


@bot.message_handler(commands=['start'])
async def register(message):
    nickname = session.execute(select(Persons.Nickname).where(Persons.Nickname == message.from_user.username)).scalar()
    if nickname is None:
        session.add(
            Persons(Nickname=message.from_user.username, Level=1, HP=10, CurHP=10, Money=50, Attack=1, MagicAttack=0,
                    XP=0, Armour=0, MagicArmour=0, LocationID=1))
        session.commit()
        await bot.send_message(message.chat.id,
                               f"You Have Successfully Registered. Welcome To The Game, {message.from_user.username}!")
        cur_town_id = session.execute(
            select(Persons.LocationID).where(Persons.Nickname == message.from_user.username)).scalar()
        cur_town = session.execute(select(Locations.LocationName).where(Locations.LocationID == cur_town_id)).scalar()
        await bot.send_message(message.chat.id, f"You Are In The City: 🏰 *{cur_town}*", reply_markup=town_markup,
                               parse_mode="Markdown")
    else:
        cur_loc_id = session.execute(
            select(Persons.LocationID).where(Persons.Nickname == message.from_user.username)).scalar()
        if cur_loc_id == -1:
            pass
        else:
            cur_loc_type = session.execute(
                select(Locations.LocationType).where(Locations.LocationID == cur_loc_id)).scalar()
            if cur_loc_type == 'town':
                cur_town = session.execute(
                    select(Locations.LocationName).where(Locations.LocationID == cur_loc_id)).scalar()
                await bot.send_message(message.chat.id, f"You Are In The City: 🏰 *{cur_town}*", reply_markup=town_markup,
                                       parse_mode="Markdown")
            elif cur_loc_type == 'dungeon':
                cur_dungeon = session.execute(
                    select(Locations.LocationName).where(Locations.LocationID == cur_loc_id)).scalar()
                await bot.send_message(message.chat.id, f"You Are In The Dungeon: ⛰️ *{cur_dungeon}*", reply_markup=town_markup,
                                       parse_mode="Markdown")

class State:
    answered = False

@bot.callback_query_handler(func=lambda call: True)
async def handle(call):
    async def wait(call, state):
        for i in range(300):
            if state.answered:
                break
            await asyncio.sleep(0.2)
        if not state.answered:
            state.answered = True
            await bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.id,
                                        text=f"You Fell Asleep On The Battlefield And Became An Easy Target For The Enemy.\n\n"
                                             f"*You Perished! :(*", reply_markup=death_markup,
                                        parse_mode="Markdown")

    cur_loc = session.execute(select(Persons.LocationID).where(Persons.Nickname == call.from_user.username)).scalar()
    cur_loc_x = session.execute(select(Locations.XCoord).where(Locations.LocationID == cur_loc)).scalar()
    cur_loc_y = session.execute(select(Locations.YCoord).where(Locations.LocationID == cur_loc)).scalar()
    if call.data == "shop":
        if cur_loc == 1:
            await bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.id,
                                        text=f"🛒 *Welcome To Shop!*", reply_markup=shop_markup_1,
                                        parse_mode="Markdown")
        elif cur_loc == 2:
            await bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.id,
                                        text=f"🛒 *Welcome To Shop!*", reply_markup=shop_markup_2,
                                        parse_mode="Markdown")

    elif call.data == "stats":
        name = call.from_user.username
        level = session.execute(select(Persons.Level).where(Persons.Nickname == name)).scalar()
        hp = session.execute(select(Persons.HP).where(Persons.Nickname == name)).scalar()
        cur_hp = session.execute(select(Persons.CurHP).where(Persons.Nickname == name)).scalar()
        attack = session.execute(select(Persons.Attack).where(Persons.Nickname == name)).scalar()
        m_attack = session.execute(select(Persons.MagicAttack).where(Persons.Nickname == name)).scalar()
        armour = session.execute(select(Persons.Armour).where(Persons.Nickname == name)).scalar()
        m_armour = session.execute(select(Persons.MagicArmour).where(Persons.Nickname == name)).scalar()
        xp = session.execute(select(Persons.XP).where(Persons.Nickname == name)).scalar()
        balance = session.execute(select(Persons.Money).where(Persons.Nickname == name)).scalar()
        await bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.id,
                                    text=f"🧝 *Your Character's Statistics:*\n\n"
                                         f"*Name:* {name}\n\n"
                                         f"*Level:* {level} ({100 - xp} To Sl.)\n\n"
                                         f"*Health:* {cur_hp}/{hp}\n\n"
                                         f"*Damage:* {attack} ⚔️  {m_attack} 🪄\n\n"
                                         f"*Armor:* {armour} 🛡️  {m_armour} 🔮\n\n"
                                         f"*Balance:* {balance} 💎", reply_markup=stats_markup,
                                    parse_mode="Markdown")
    elif call.data == "back_town":
        if cur_loc >= 3:  # will break when naively adding new locks, you need to carefully
            await get_dungeon(call)
        else:
            await get_town(call)
    elif call.data == "back_dungeon":
        await get_dungeon(call)
    elif call.data == "leave_city":
        await get_map(call)
    elif call.data[0:2] == "go":
        aim_x = session.execute(select(Locations.XCoord).where(Locations.LocationID == int(call.data[3:]))).scalar()
        aim_y = session.execute(select(Locations.YCoord).where(Locations.LocationID == int(call.data[3:]))).scalar()
        delay = count_distance(cur_loc_x, cur_loc_y, aim_x, aim_y)
        await go_loc(call.from_user.username, -1, call)
        ticks = floor(delay / 0.6)
        for i in range(1, ticks):
            await bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.id,
                                        text=f"On My Way" + "." * (i % 4),
                                        parse_mode="Markdown")

            await asyncio.sleep(0.6)
        await go_loc(call.from_user.username, int(call.data[3:]), call)
    elif call.data == 'enter_dungeon':
        if cur_loc == 3:
            enemy_id = numpy.random.choice([1, 2], p=[0.8, 0.2])
        elif cur_loc == 4:
            enemy_id = numpy.random.choice([3, 4, 5], p=[0.6, 0.3, 0.1])
        enemy = Enemy(enemy_id)
        enemy_name = enemy.name
        stmt = select(Persons).where(Persons.Nickname == call.from_user.username)
        player = session.scalars(stmt).one()
        await bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.id,
                                    text=f"{enemy_name} {numpy.random.choice(['Got In The Way!', 'Jumped Out Of The Corner!', 'Crept Unnoticed!'])}",
                                    reply_markup=battle_markup)
        player.LocationID = -2
        session.commit()
        state = State()
        cur_fights[player.Nickname] = [enemy, player, cur_loc, state]
        await wait(call, state)
    elif call.data == 'attack':
        cur_fights[call.from_user.username][3].answered = True
        enemy = cur_fights[call.from_user.username][0]
        player = cur_fights[call.from_user.username][1]
        damage = numpy.random.choice([player.Attack, player.Attack * 1.5], p=[0.8, 0.2])
        enemy.hp -= max(damage - enemy.armour, 0)
        crit = f"Attack On {damage} Damage!"
        if damage > player.Attack:
            crit = f"*Critical Attack On {damage} Damage!*"
        if enemy.hp <= 0:
            lup = ""
            new_xp = player.XP + enemy.xp
            if new_xp >= 100:
                player.Level += 1
                player.HP += 10
                player.XP = new_xp - 100
                lup = f"\n\n*Level up!* Now Your Level: {player.Level}"
            else:
                player.XP = new_xp
            player.Money += enemy.money
            await bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.id,
                                        text=f"{crit}\n\nYou Won! Received {enemy.xp} Experience And {enemy.money} Coins."
                                             f"{lup}",
                                        reply_markup=win_markup, parse_mode="Markdown")
            player.XP += enemy.xp
            player.Money += enemy.money
            player.LocationID = cur_fights[player.Nickname][2]
            cur_fights.pop(player.Nickname)
        else:
            for i in range(0, 4):
                await bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.id,
                                            text=f"{crit}\nThe Enemy Has {enemy.hp} Health.\n\n"
                                                 f"The Enemy Is Attacking" + "." * (i % 4), parse_mode="Markdown")
                await asyncio.sleep(0.6)
            if enemy.attack_type == 'phys':
                enemy_damage = numpy.random.choice([enemy.attack, enemy.attack * 1.5], p=[0.8, 0.2])
                player.CurHP -= max((enemy_damage - player.Armour), 0)
                if player.CurHP <= 0:
                    await bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.id,
                                                text=f"Opponent {numpy.random.choice(['Hit', 'Wounded', 'Scratched'])} You On {max((enemy_damage - player.Armour), 0)} Damage.\n\n"
                                                     f"*You Perished! :(*",
                                                reply_markup=death_markup, parse_mode="Markdown")
                else:
                    await bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.id,
                                                text=f"Opponent {numpy.random.choice(['Hit', 'Wounded', 'Scratched'])} You On {max((enemy_damage - player.Armour), 0)} Damage.\n\n"
                                                     f"You Have Left {player.CurHP} Health.",
                                                reply_markup=battle_markup, parse_mode="Markdown")
                    state = State()
                    cur_fights[call.from_user.username][3] = state
                    await wait(call, state)
            elif enemy.attack_type == 'mag':
                enemy_damage = numpy.random.choice([enemy.attack, enemy.attack * 1.5], p=[0.8, 0.2])
                player.CurHP -= max((enemy_damage - player.MagicArmour), 0)
                if player.CurHP <= 0:
                    await bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.id,
                                                text=f"Opponent {numpy.random.choice(['Hit', 'Hurt', 'Scratched'])} You On {max((enemy_damage - player.MagicArmour), 0)} Damage.\n\n"
                                                     f"*You Perished ! :(*",
                                                reply_markup=death_markup, parse_mode="Markdown")
                else:
                    await bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.id,
                                                text=f"Opponent {numpy.random.choice(['Cast A Spell', 'Fireball Launched', 'Cast A Spell'])} And Wounded You On {max((enemy_damage - player.MagicArmour), 0)} Damage.\n\n"
                                                    f"You Have Left {player.CurHP} Health.",
                                                reply_markup=battle_markup, parse_mode="Markdown")
                    state = State()
                    cur_fights[call.from_user.username][3] = state
                    await wait(call, state)

        session.commit()
    elif call.data == 'check':
        print(cur_fights)
        enemy = cur_fights[call.from_user.username][0]
        await bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.id,
                                    text=f"*{enemy.name}*:\n\n"
                                         f"Health: {enemy.hp}/{session.execute(select(Mobs.HP).where(Mobs.MobName == enemy.name)).scalar()}\n"
                                         f"Attack: {enemy.attack} {'⚔️' if enemy.attack_type == 'phys' else '🪄'}\n"
                                         f"Protection: {enemy.armour} 🛡️ {enemy.m_armour} 🔮",
                                    reply_markup=check_markup, parse_mode="Markdown")
    elif call.data == 'revive':
        player = cur_fights[call.from_user.username][1]
        cur_fights.pop(call.from_user.username)
        player.LocationID = 1
        player.CurHP = player.HP
        session.commit()
        await get_town(call)
    elif call.data[0:3] == 'buy':
        stmt1 = select(Persons).where(Persons.Nickname == call.from_user.username)
        player = session.scalars(stmt1).one()
        stmt3 = select(Items).where(Items.ItemID == int(call.data[4:]))
        item = session.scalars(stmt3).one()
        if player.Money < item.Cost:
            if player.LocationID == 1:
                await bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.id,
                                            text="Not Enough Coins.", reply_markup=no_money_markup,
                                            parse_mode="Markdown")
            elif player.LocationID == 2:
                await bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.id,
                                            text="Not Enough Coins.", reply_markup=no_money_markup,
                                            parse_mode="Markdown")
        else:
            player.Money -= item.Cost
            session.commit()
            item_in_inv = session.execute(select(Inventory).where(Inventory.Nickname == call.from_user.username).where(
                Inventory.ItemID == item.ItemID))
            if item_in_inv.scalar() is None:
                print('aaa')
                session.add(
                    Inventory(Nickname=player.Nickname, ItemID=int(call.data[4:]), Quantity=0))
                session.commit()
            stmt2 = select(Inventory).where(Inventory.Nickname == call.from_user.username).where(
                Inventory.ItemID == item.ItemID)
            item_in_inv_changeable = session.scalars(stmt2)
            amt = session.execute(select(Inventory.Quantity).where(Inventory.ItemID == item.ItemID)).scalar()
            if amt <= 0:
                item_in_inv_changeable.one().Quantity -= 1
            else:
                item_in_inv_changeable.one().Quantity += 1
            session.commit()
            # new_amt = session.execute(select(Inventory.Quantity).where(Inventory.ItemID == item.Item))
            if player.LocationID == 1:
                await bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.id,
                                            text=f"You Bought An Item {item.Name}. You Now Have Them In Your Inventory {abs(amt)+1}.",
                                            reply_markup=shop_markup_1, parse_mode="Markdown")
            elif player.LocationID == 2:
                await bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.id,
                                            text=f"You Bought An Item {item.Name}. You Now Have Them In Your Inventory {abs(amt) + 1}.",
                                            reply_markup=shop_markup_2, parse_mode="Markdown")
        session.commit()
    elif call.data == 'inventory':
        # inventory interface
        inventory_markup = types.InlineKeyboardMarkup()
        stmt = select(Inventory).where(Inventory.Nickname == call.from_user.username)
        cur_inv = session.scalars(stmt)
        text = ''
        for item in cur_inv:
            name = session.execute(select(Items.Name).where(Items.ItemID == item.ItemID)).scalar()
            quantity = session.execute(select(Inventory.Quantity).where(Inventory.ItemID == item.ItemID)).scalar()
            item_type = session.execute(select(Items.ItemType).where(Items.ItemID == item.ItemID)).scalar()
            if quantity != 0:
                if quantity < 0 and item_type != 'potion':
                    inventory_markup.add(types.InlineKeyboardButton(
                        f"Put On {name}",
                        callback_data=f'wear_{item.ItemID}'))
                text += f'{name} - {abs(quantity)} PC. {"✅" if quantity > 0 else ""}\n'
                inventory_markup.add(types.InlineKeyboardButton(
                    f"Sell {name} ({session.execute(select(Items.CostToSale).where(Items.ItemID == item.ItemID)).scalar()} 💎)",
                    callback_data=f'sell_{item.ItemID}'))
        inventory_markup.add(back_stats_town)
        await bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.id,
                                    text=f"*Your Inventory:*\n\n"
                                         f"{'Empty!' if text == '' else text}",
                                    reply_markup=inventory_markup, parse_mode="Markdown")
    elif call.data[0:3] == 'sel':
        item_to_sell = int(call.data[5:])
        stmt = select(Inventory).where(Inventory.Nickname == call.from_user.username).where(
            Inventory.ItemID == item_to_sell)
        item_in_inv = session.scalars(stmt).one()
        if item_in_inv.Quantity < 0:
            item_in_inv.Quantity += 1
        elif item_in_inv.Quantity > 0:
            item_in_inv.Quantity -= 1
        stmt1 = select(Persons).where(Persons.Nickname == call.from_user.username)
        user = session.scalars(stmt1).one()
        user.Money += session.execute(select(Items.CostToSale).where(Items.ItemID == item_to_sell)).scalar()
        session.commit()
        await bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.id,
                                    text=f"You Sold {session.execute(select(Items.Name).where(Items.ItemID == item_to_sell)).scalar()}",
                                    reply_markup=after_deal_markup, parse_mode="Markdown")
    elif call.data[0:3] == 'wea':
        item_to_wear = int(call.data[5:])
        item_to_wear_inst = session.execute(select(Items).where(Items.ItemID == item_to_wear)).scalar()
        item_type = item_to_wear_inst.ItemType
        print(item_type)
        if item_to_wear_inst.ReqLevel > session.execute(select(Persons.Level).where(Persons.Nickname == call.from_user.username)).scalar():
            await bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.id,
                                        text=f"You Are Too Small, To Wear This Item.",
                                        reply_markup=after_deal_markup, parse_mode="Markdown")
        else:
            player_inv = session.execute(select(Inventory).where(Inventory.Nickname == call.from_user.username))
            for item in player_inv:
                inv_item_type = session.execute(select(Items.ItemType).where(Items.ItemID == item.Inventory.ItemID)).scalar()
                if inv_item_type == item_type:
                    stmt = select(Inventory).where(Inventory.Nickname == call.from_user.username).where(Inventory.ItemID == item.Inventory.ItemID)
                    found_item = session.scalars(stmt).one()
                    found_item_inst = session.execute(select(Items).where(Items.ItemID == item.Inventory.ItemID)).scalar()
                    if found_item.Quantity > 0:
                        found_item.Quantity *= -1
                        stmt1 = select(Persons).where(Persons.Nickname == call.from_user.username)
                        user = session.scalars(stmt1).one()
                        user.HP -= found_item_inst.HP
                        user.Attack -= found_item_inst.Attack
                        user.MagicAttack -= found_item_inst.MagicAttack
                        user.Armour -= found_item_inst.Armour
                        user.MagicArmour -= found_item_inst.MagicArmour
                        session.commit()
            stmt = select(Inventory).where(Inventory.Nickname == call.from_user.username).where(Inventory.ItemID == item_to_wear)
            session.scalars(stmt).one().Quantity *= -1
            stmt1 = select(Persons).where(Persons.Nickname == call.from_user.username)
            user = session.scalars(stmt1).one()
            user.HP += item_to_wear_inst.HP
            user.Attack += item_to_wear_inst.Attack
            user.MagicAttack += item_to_wear_inst.MagicAttack
            user.Armour += item_to_wear_inst.Armour
            user.MagicArmour += item_to_wear_inst.MagicArmour
            session.commit()
            await bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.id,
                                    text=f"You Put On {session.execute(select(Items.Name).where(Items.ItemID == item_to_wear)).scalar()}",
                                    reply_markup=after_deal_markup, parse_mode="Markdown")
    elif call.data == 'heal':
        cur_fights[call.from_user.username][3].answered = True
        enemy = cur_fights[call.from_user.username][0]
        player = cur_fights[call.from_user.username][1]
        stmt = select(Inventory).where(Inventory.Nickname == call.from_user.username).where(Inventory.ItemID == 9)
        if session.scalars(stmt).one().Quantity != 0:
            stmt1 = select(Persons).where(Persons.Nickname == call.from_user.username)
            if session.scalars(stmt).one().Quantity > 0:
                session.scalars(stmt).one().Quantity -= 1
            else:
                session.scalars(stmt).one().Quantity += 1
            session.scalars(stmt1).one().CurHP = min((session.scalars(stmt1).one().CurHP + 5), session.scalars(stmt1).one().HP)
            session.commit()
            for i in range(0, 4):
                await bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.id,
                                            text=f"You Drank A Health Potion! Restored 5 Hp. Current Health: {session.scalars(stmt1).one().CurHP}\n\n"
                                                 f"The Enemy Is Attacking" + "." * (i % 4), parse_mode="Markdown")
                await asyncio.sleep(0.6)
        else:
            for i in range(0, 4):
                await bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.id,
                                            text=f"You Reached Into Your Backpack For A Potion, But He Wasn't There!\n\n"
                                                 f"The Enemy Is Attacking" + "." * (i % 4), parse_mode="Markdown")
                await asyncio.sleep(0.6)
        if enemy.attack_type == 'phys':
            enemy_damage = numpy.random.choice([enemy.attack, enemy.attack * 1.5], p=[0.8, 0.2])
            player.CurHP -= max((enemy_damage - player.Armour), 0)
            if player.CurHP <= 0:
                await bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.id,
                                            text=f"Opponent {numpy.random.choice(['Hit', 'Wounded', 'Scratched'])} You On {max((enemy_damage - player.Armour), 0)} Damage.\n\n"
                                                 f"*You Perished! :(*",
                                            reply_markup=death_markup, parse_mode="Markdown")
            else:
                await bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.id,
                                            text=f"Opponent {numpy.random.choice(['Hit', 'Wounded', 'Scratched'])} You On {max((enemy_damage - player.Armour), 0)} Damage.\n\n"
                                                 f"You Have Left {player.CurHP} Health.",
                                            reply_markup=battle_markup, parse_mode="Markdown")
                state = State()
                cur_fights[call.from_user.username][3] = state
                await wait(call, state)
        elif enemy.attack_type == 'mag':
            enemy_damage = numpy.random.choice([enemy.attack, enemy.attack * 1.5], p=[0.8, 0.2])
            player.CurHP -= max((enemy_damage - player.MagicArmour), 0)
            if player.CurHP <= 0:
                await bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.id,
                                            text=f"Opponent {numpy.random.choice(['Hit', 'Hurt', 'Scratched'])} You On {max((enemy_damage - player.MagicArmour), 0)} Damage.\n\n"
                                                 f"*You Perished ! :(*",
                                            reply_markup=death_markup, parse_mode="Markdown")
            else:
                await bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.id,
                                            text=f"Opponent {numpy.random.choice(['Cast A Spell', 'Fireball Launched', 'Cast A Spell'])} And Wounded You On {max((enemy_damage - player.MagicArmour), 0)} Damage.\n\n"
                                                 f"You Have Left {player.CurHP} Health.",
                                            reply_markup=battle_markup, parse_mode="Markdown")
                state = State()
                cur_fights[call.from_user.username][3] = state
                await wait(call, state)
    await bot.answer_callback_query(call.id)
