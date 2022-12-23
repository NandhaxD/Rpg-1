import asyncio
from math import floor

import numpy

from sqlalchemy.orm import Session
from telebot.async_telebot import AsyncTeleBot, types
import sqlite3
from sqlalchemy import create_engine, Column, Integer, String, Float, select, update, ARRAY
from sqlalchemy.ext.declarative import declarative_base

TOKEN = '5953711879:AAFVh4Chk58HE8ovsBXdT6zwq_yU5IozZ9s'
bot = AsyncTeleBot(TOKEN)

db = sqlite3.connect('gametools.db')
engine = create_engine('sqlite+pysqlite:///gametools.db', echo=True)
Base = declarative_base()


class Enemy:
    def __init__(self, id):
        enemy = session.execute(select(Mobs).where(Mobs.MobID == int(id))).one()
        self.name = enemy.Mobs.MobName
        self.hp = enemy.Mobs.HP
        self.attack = enemy.Mobs.Attack
        self.armour = enemy.Mobs.Armour
        self.m_armour = enemy.Mobs.MagicArmour
        self.xp = enemy.Mobs.XP
        self.attack_type = enemy.Mobs.AttackType
        self.money = enemy.Mobs.Money

class Timer:

    async def start(self):
        await asyncio.sleep(60)
        if not self.answer:
            return False
        else:
            return True

    def __init__(self):
        self.answer = False


# class Player:
#     def __init__(self, id):
#         player = session.execute(select(Persons).where(Persons.UserID == id)).scalar()
#         self.name = player.MobName
#         self.hp = player.MobHP
#         self.attack = player.Attack
#         self.armour = player.Armour
#         self.m_armour = player.MagicArmour
#         self.xp = player.XP

class Persons(Base):
    __tablename__ = 'Persons'  # имя таблицы
    UserID = Column(Integer, name='UserID', primary_key=True)
    Nickname = Column(String)
    Level = Column(Integer)
    HP = Column(Integer)
    CurHP = Column(Integer)
    Money = Column(Integer)
    Attack = Column(Integer)
    MagicAttack = Column(Integer)
    XP = Column(Integer)
    Armour = Column(Integer)
    MagicArmour = Column(Integer)
    LocationID = Column(Integer)


class Mobs(Base):
    __tablename__ = 'Mobs'  # имя таблицы
    MobID = Column(Integer, primary_key=True)
    MobName = Column(String)
    HP = Column(Integer)
    XP = Column(Integer)
    Money = Column(Integer)
    ReqLevel = Column(Integer)
    AttackType = Column(String)
    Attack = Column(Integer)
    Armour = Column(Integer)
    MagicArmour = Column(Integer)


class Locations(Base):
    __tablename__ = 'Locations'
    LocationID = Column(Integer, primary_key=True)
    LocationName = Column(String)
    XCoord = Column(Integer)
    YCoord = Column(Integer)
    LocationType = Column(String)


class Items(Base):
    __tablename__ = 'Items'
    ItemID = Column(Integer, primary_key=True)
    Name = Column(String)
    Cost = Column(Integer)
    CostToSale = Column(Integer)
    ItemType = Column(String)
    HP = Column(Integer)
    Mana = Column(Integer)
    Attack = Column(Integer)
    MagicAttack = Column(Integer)
    Armour = Column(Integer)
    MagicArmour = Column(Integer)
    ReqLevel = Column(Integer)
    Availability = Column(Integer)


class Inventory(Base):
    __tablename__ = 'Inventory'
    UserID = Column(Integer, primary_key=True)
    Nickname = Column(String)
    ItemID = Column(Integer)
    Quantity = Column(Integer)  # положительная - в инвентаре несколько таких вещей, одна из них надета
    # отрицательная - в инвентаре несколько, не надета


Base.metadata.create_all(engine)
session = Session(engine)


async def go_loc(username, loc_id, call):
    stmt = select(Persons).where(Persons.Nickname == username)
    user = session.scalars(stmt).one()
    user.LocationID = loc_id
    session.commit()
    if loc_id > 0:
        cur_place = session.execute(select(Locations.LocationType).where(Locations.LocationID == loc_id)).scalar()
        if cur_place == 'town':
            await get_town(call)
        elif cur_place == 'dungeon':
            await get_dungeon(call)


async def get_town(call):
    cur_town_id = session.execute(
        select(Persons.LocationID).where(Persons.Nickname == call.from_user.username)).scalar()
    cur_town = session.execute(select(Locations.LocationName).where(Locations.LocationID == cur_town_id)).scalar()
    stmt = select(Persons).where(Persons.Nickname == call.from_user.username)
    player = session.scalars(stmt).one()
    player.CurHP = player.HP
    await bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.id,
                                text=f"Ты в городе: 🏰 *{cur_town}*", reply_markup=town_markup, parse_mode="Markdown")


async def get_dungeon(call):
    cur_dungeon_id = session.execute(
        select(Persons.LocationID).where(Persons.Nickname == call.from_user.username)).scalar()
    cur_dungeon = session.execute(select(Locations.LocationName).where(Locations.LocationID == cur_dungeon_id)).scalar()
    await bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.id,
                                text=f"Ты в данже: ⛰️ *{cur_dungeon}*", reply_markup=dungeon_gate_markup,
                                parse_mode="Markdown")


async def get_map(call):
    cur_town_id = session.execute(
        select(Persons.LocationID).where(Persons.Nickname == call.from_user.username)).scalar()
    cur_town_x = session.execute(select(Locations.XCoord).where(Locations.LocationID == cur_town_id)).scalar()
    cur_town_y = session.execute(select(Locations.YCoord).where(Locations.LocationID == cur_town_id)).scalar()
    destinations = session.execute(select(Locations))
    text = '*Доступные локации:*\n\n'
    for el in destinations:
        dist = round(count_distance(cur_town_x, cur_town_y, el.Locations.XCoord, el.Locations.YCoord))
        if 0 < dist <= 10:
            text += f"{el.Locations.LocationName} - {dist} км 🛣️\n\n"
    if cur_town_id == 1:
        await bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.id,
                                    text=text, reply_markup=choose_location_1_markup,
                                    parse_mode="Markdown")
    elif cur_town_id == 2:
        await bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.id,
                                    text=text, reply_markup=choose_location_2_markup,
                                    parse_mode="Markdown")
    elif cur_town_id == 3:
        await bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.id,
                                    text=text, reply_markup=choose_location_3_markup,
                                    parse_mode="Markdown")
    elif cur_town_id == 4:
        await bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.id,
                                    text=text, reply_markup=choose_location_4_markup,
                                    parse_mode="Markdown")


def count_distance(x1, y1, x2, y2):
    return ((x1 - x2) ** 2 + (y1 - y2) ** 2) ** (1 / 2)


# интерфейс городов
town_markup = types.InlineKeyboardMarkup()
dungeons_list = types.InlineKeyboardButton("Покинуть город", callback_data="leave_city")
shop = types.InlineKeyboardButton("Местный магазин", callback_data="shop")
stats = types.InlineKeyboardButton("Статистика персонажа", callback_data="stats")
inventory = types.InlineKeyboardButton("Инвентарь", callback_data='inventory')
town_markup.add(dungeons_list)
town_markup.add(inventory)
town_markup.add(shop)
town_markup.add(stats)

# интерфейс магазинов
shop_markup_1 = types.InlineKeyboardMarkup()
shop_markup_2 = types.InlineKeyboardMarkup()
back_shop_town = types.InlineKeyboardButton("Назад", callback_data='back_town')
items_1 = session.execute(select(Items).where(Items.Availability == 1))
items_2 = session.execute(select(Items).where(Items.Availability == 2))
for el in items_1:
    t_item = types.InlineKeyboardButton(f"Купить {el.Items.Name}: {el.Items.Cost} 💎",
                                        callback_data=f'buy_{el.Items.ItemID}')
    shop_markup_1.add(t_item)
for el in items_2:
    t_item = types.InlineKeyboardButton(f"Купить {el.Items.Name}: {el.Items.Cost} 💎",
                                        callback_data=f'buy_{el.Items.ItemID}')
    shop_markup_2.add(t_item)
shop_markup_1.add(back_shop_town)
shop_markup_2.add(back_shop_town)

# интерфейс статистики
stats_markup = types.InlineKeyboardMarkup()
back_stats_town = types.InlineKeyboardButton("Назад", callback_data='back_town')
stats_markup.add(back_stats_town)

# интерфейс выбора локации
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

# интерфейс боя
battle_markup = types.InlineKeyboardMarkup()
check = types.InlineKeyboardButton("Оценить", callback_data='check')
attack = types.InlineKeyboardButton("Атаковать", callback_data='attack')
heal = types.InlineKeyboardButton("Выпить зелье", callback_data='heal')
battle_markup.add(check)
battle_markup.add(attack)
battle_markup.add(heal)

# интерфейс оценки
check_markup = types.InlineKeyboardMarkup()
check_markup.add(attack)

back_location_town = types.InlineKeyboardButton("Назад", callback_data='back_town')
back_location_dungeon = types.InlineKeyboardButton("Назад", callback_data='back_dungeon')
destinations = session.execute(select(Locations))
for el in destinations:
    el_x = session.execute(select(Locations.XCoord).where(Locations.LocationID == el.Locations.LocationID)).scalar()
    el_y = session.execute(select(Locations.YCoord).where(Locations.LocationID == el.Locations.LocationID)).scalar()
    dist_1 = count_distance(x_1, y_1, el_x, el_y)
    dist_2 = count_distance(x_2, y_2, el_x, el_y)
    dist_3 = count_distance(x_3, y_3, el_x, el_y)
    dist_4 = count_distance(x_4, y_4, el_x, el_y)
    if 0 < dist_1 <= 10:
        choose_location_1_markup.add(types.InlineKeyboardButton(f"Отправиться: {el.Locations.LocationName}",
                                                                callback_data=f'go_{el.Locations.LocationID}'))
    if 0 < dist_2 <= 10:
        choose_location_2_markup.add(types.InlineKeyboardButton(f"Отправиться: {el.Locations.LocationName}",
                                                                callback_data=f'go_{el.Locations.LocationID}'))
    if 0 < dist_3 <= 10:
        choose_location_3_markup.add(types.InlineKeyboardButton(f"Отправиться: {el.Locations.LocationName}",
                                                                callback_data=f'go_{el.Locations.LocationID}'))
    if 0 < dist_4 <= 10:
        choose_location_4_markup.add(types.InlineKeyboardButton(f"Отправиться: {el.Locations.LocationName}",
                                                                callback_data=f'go_{el.Locations.LocationID}'))
choose_location_1_markup.add(back_location_town)
choose_location_2_markup.add(back_location_town)
choose_location_3_markup.add(back_location_dungeon)
choose_location_4_markup.add(back_location_dungeon)

# интерфейс входа в данж
dungeon_gate_markup = types.InlineKeyboardMarkup()
back_to_map = types.InlineKeyboardButton(f"Назад", callback_data='leave_city')
enter_dungeon = types.InlineKeyboardButton(f"Зайти в данж!", callback_data='enter_dungeon')
dungeon_gate_markup.add(enter_dungeon)
dungeon_gate_markup.add(stats)
dungeon_gate_markup.add(back_to_map)

# интерфейс победы
win_markup = types.InlineKeyboardMarkup()
go_further = types.InlineKeyboardButton(f"Продолжать путь", callback_data='enter_dungeon')
win_markup.add(back_to_map)
win_markup.add(go_further)

# интерфейс смерти
death_markup = types.InlineKeyboardMarkup()
revive = types.InlineKeyboardButton(f"Возродиться", callback_data='revive')
death_markup.add(revive)

# интерфейс в ситуации, когда нет денег
no_money_markup = types.InlineKeyboardMarkup()
no_money_markup.add(back_location_town)

# интерфейс после покупки
after_deal_markup = types.InlineKeyboardMarkup()
back_to_inv = types.InlineKeyboardButton(f"Назад", callback_data='inventory')
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
                               f"Ты успешно зарегистрировался. Добро пожаловать в игру, {message.from_user.username}!")
        cur_town_id = session.execute(
            select(Persons.LocationID).where(Persons.Nickname == message.from_user.username)).scalar()
        cur_town = session.execute(select(Locations.LocationName).where(Locations.LocationID == cur_town_id)).scalar()
        await bot.send_message(message.chat.id, f"Ты в городе: 🏰 *{cur_town}*", reply_markup=town_markup,
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
                await bot.send_message(message.chat.id, f"Ты в городе: 🏰 *{cur_town}*", reply_markup=town_markup,
                                       parse_mode="Markdown")
            elif cur_loc_type == 'dungeon':
                cur_dungeon = session.execute(
                    select(Locations.LocationName).where(Locations.LocationID == cur_loc_id)).scalar()
                await bot.send_message(message.chat.id, f"Ты в данже: ⛰️ *{cur_dungeon}*", reply_markup=town_markup,
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
                                        text=f"Вы заснули на поле боя и стали лёгкой мишенью для врага.\n\n"
                                             f"*Вы погибли! :(*", reply_markup=death_markup,
                                        parse_mode="Markdown")

    cur_loc = session.execute(select(Persons.LocationID).where(Persons.Nickname == call.from_user.username)).scalar()
    cur_loc_x = session.execute(select(Locations.XCoord).where(Locations.LocationID == cur_loc)).scalar()
    cur_loc_y = session.execute(select(Locations.YCoord).where(Locations.LocationID == cur_loc)).scalar()
    if call.data == "shop":
        # text = ''
        # available_items = session.execute(select(Items).where(Items.Availability == loc_id))
        # for el in available_items:
        #     text += f"{el.Items.Name}: {el.Items.Cost} 💎\n\n"
        if cur_loc == 1:
            await bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.id,
                                        text=f"🛒 *Добро пожаловать в магазин!*", reply_markup=shop_markup_1,
                                        parse_mode="Markdown")
        elif cur_loc == 2:
            await bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.id,
                                        text=f"🛒 *Добро пожаловать в магазин!*", reply_markup=shop_markup_2,
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
                                    text=f"🧝 *Статистика Вашего персонажа:*\n\n"
                                         f"*Имя:* {name}\n\n"
                                         f"*Уровень:* {level} ({100 - xp} до сл.)\n\n"
                                         f"*Здоровье:* {cur_hp}/{hp}\n\n"
                                         f"*Урон:* {attack} ⚔️  {m_attack} 🪄\n\n"
                                         f"*Броня:* {armour} 🛡️  {m_armour} 🔮\n\n"
                                         f"*Баланс:* {balance} 💎", reply_markup=stats_markup,
                                    parse_mode="Markdown")
    elif call.data == "back_town":
        if cur_loc >= 3:  # будет ломаться при наивном добавлении новых лок, надо внимательно
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
                                        text=f"В пути" + "." * (i % 4),
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
                                    text=f"{enemy_name} {numpy.random.choice(['встал на пути!', 'выскочил из-за угла!', 'подкрался незаметно!'])}",
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
        crit = f"Атака на {damage} урона!"
        if damage > player.Attack:
            crit = f"*Критическая атака на {damage} урона!*"
        if enemy.hp <= 0:
            lup = ""
            new_xp = player.XP + enemy.xp
            if new_xp >= 100:
                player.Level += 1
                player.HP += 10
                player.XP = new_xp - 100
                lup = f"\n\n*Level up!* Теперь ваш уровень: {player.Level}"
            else:
                player.XP = new_xp
            player.Money += enemy.money
            await bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.id,
                                        text=f"{crit}\n\nВы победили! Получено {enemy.xp} опыта и {enemy.money} монет."
                                             f"{lup}",
                                        reply_markup=win_markup, parse_mode="Markdown")
            player.XP += enemy.xp
            player.Money += enemy.money
            player.LocationID = cur_fights[player.Nickname][2]
            cur_fights.pop(player.Nickname)
        else:
            for i in range(0, 4):
                await bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.id,
                                            text=f"{crit}\nУ противника осталось {enemy.hp} здоровья.\n\n"
                                                 f"Противник атакует" + "." * (i % 4), parse_mode="Markdown")
                await asyncio.sleep(0.6)
            if enemy.attack_type == 'phys':
                enemy_damage = numpy.random.choice([enemy.attack, enemy.attack * 1.5], p=[0.8, 0.2])
                player.CurHP -= max((enemy_damage - player.Armour), 0)
                if player.CurHP <= 0:
                    await bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.id,
                                                text=f"Противник {numpy.random.choice(['ударил', 'поранил', 'поцарапал'])} вас на {max((enemy_damage - player.Armour), 0)} урона.\n\n"
                                                     f"*Вы погибли! :(*",
                                                reply_markup=death_markup, parse_mode="Markdown")
                else:
                    await bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.id,
                                                text=f"Противник {numpy.random.choice(['ударил', 'поранил', 'поцарапал'])} вас на {max((enemy_damage - player.Armour), 0)} урона.\n\n"
                                                     f"У вас осталось {player.CurHP} здоровья.",
                                                reply_markup=battle_markup, parse_mode="Markdown")
                    state = State()
                    cur_fights[call.from_user.username][3] = state
                    await wait(call, state)
            elif enemy.attack_type == 'mag':
                enemy_damage = numpy.random.choice([enemy.attack, enemy.attack * 1.5], p=[0.8, 0.2])
                player.CurHP -= max((enemy_damage - player.MagicArmour), 0)
                if player.CurHP <= 0:
                    await bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.id,
                                                text=f"Противник {numpy.random.choice(['ударил', 'поранил', 'поцарапал'])} вас на {max((enemy_damage - player.MagicArmour), 0)} урона.\n\n"
                                                     f"*Вы погибли ! :(*",
                                                reply_markup=death_markup, parse_mode="Markdown")
                else:
                    await bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.id,
                                                text=f"Противник {numpy.random.choice(['скастовал заклинание', 'запустил фаербол', 'наложил заклинание'])} и поранил вас на {max((enemy_damage - player.MagicArmour), 0)} урона.\n\n"
                                                    f"У вас осталось {player.CurHP} здоровья.",
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
                                         f"Здоровье: {enemy.hp}/{session.execute(select(Mobs.HP).where(Mobs.MobName == enemy.name)).scalar()}\n"
                                         f"Атака: {enemy.attack} {'⚔️' if enemy.attack_type == 'phys' else '🪄'}\n"
                                         f"Защита: {enemy.armour} 🛡️ {enemy.m_armour} 🔮",
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
                                            text="Не хватает монет.", reply_markup=no_money_markup,
                                            parse_mode="Markdown")
            elif player.LocationID == 2:
                await bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.id,
                                            text="Не хватает монет.", reply_markup=no_money_markup,
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
                                            text=f"Вы купили предмет {item.Name}. Теперь в инвентаре у вас их {abs(amt)+1}.",
                                            reply_markup=shop_markup_1, parse_mode="Markdown")
            elif player.LocationID == 2:
                await bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.id,
                                            text=f"Вы купили предмет {item.Name}. Теперь в инвентаре у вас их {abs(amt) + 1}.",
                                            reply_markup=shop_markup_2, parse_mode="Markdown")
        session.commit()
    elif call.data == 'inventory':
        # интерфейс инвентаря
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
                        f"Надеть {name}",
                        callback_data=f'wear_{item.ItemID}'))
                text += f'{name} - {abs(quantity)} шт. {"✅" if quantity > 0 else ""}\n'
                inventory_markup.add(types.InlineKeyboardButton(
                    f"Продать {name} ({session.execute(select(Items.CostToSale).where(Items.ItemID == item.ItemID)).scalar()} 💎)",
                    callback_data=f'sell_{item.ItemID}'))
        inventory_markup.add(back_stats_town)
        await bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.id,
                                    text=f"*Ваш инвентарь:*\n\n"
                                         f"{'Пусто!' if text == '' else text}",
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
                                    text=f"Вы продали {session.execute(select(Items.Name).where(Items.ItemID == item_to_sell)).scalar()}",
                                    reply_markup=after_deal_markup, parse_mode="Markdown")
    elif call.data[0:3] == 'wea':
        item_to_wear = int(call.data[5:])
        item_to_wear_inst = session.execute(select(Items).where(Items.ItemID == item_to_wear)).scalar()
        item_type = item_to_wear_inst.ItemType
        print(item_type)
        if item_to_wear_inst.ReqLevel > session.execute(select(Persons.Level).where(Persons.Nickname == call.from_user.username)).scalar():
            await bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.id,
                                        text=f"Вы слишком маленького уровня, чтобы носить этот предмет.",
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
                                    text=f"Вы надели {session.execute(select(Items.Name).where(Items.ItemID == item_to_wear)).scalar()}",
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
                                            text=f"Вы выпили зелье здоровья! Восстановлено 5 хп. Текущее здоровье: {session.scalars(stmt1).one().CurHP}\n\n"
                                                 f"Противник атакует" + "." * (i % 4), parse_mode="Markdown")
                await asyncio.sleep(0.6)
        else:
            for i in range(0, 4):
                await bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.id,
                                            text=f"Вы полезли в рюкзак за зельем, но его там не оказалось!\n\n"
                                                 f"Противник атакует" + "." * (i % 4), parse_mode="Markdown")
                await asyncio.sleep(0.6)
        if enemy.attack_type == 'phys':
            enemy_damage = numpy.random.choice([enemy.attack, enemy.attack * 1.5], p=[0.8, 0.2])
            player.CurHP -= max((enemy_damage - player.Armour), 0)
            if player.CurHP <= 0:
                await bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.id,
                                            text=f"Противник {numpy.random.choice(['ударил', 'поранил', 'поцарапал'])} вас на {max((enemy_damage - player.Armour), 0)} урона.\n\n"
                                                 f"*Вы погибли! :(*",
                                            reply_markup=death_markup, parse_mode="Markdown")
            else:
                await bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.id,
                                            text=f"Противник {numpy.random.choice(['ударил', 'поранил', 'поцарапал'])} вас на {max((enemy_damage - player.Armour), 0)} урона.\n\n"
                                                 f"У вас осталось {player.CurHP} здоровья.",
                                            reply_markup=battle_markup, parse_mode="Markdown")
                state = State()
                cur_fights[call.from_user.username][3] = state
                await wait(call, state)
        elif enemy.attack_type == 'mag':
            enemy_damage = numpy.random.choice([enemy.attack, enemy.attack * 1.5], p=[0.8, 0.2])
            player.CurHP -= max((enemy_damage - player.MagicArmour), 0)
            if player.CurHP <= 0:
                await bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.id,
                                            text=f"Противник {numpy.random.choice(['ударил', 'поранил', 'поцарапал'])} вас на {max((enemy_damage - player.MagicArmour), 0)} урона.\n\n"
                                                 f"*Вы погибли ! :(*",
                                            reply_markup=death_markup, parse_mode="Markdown")
            else:
                await bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.id,
                                            text=f"Противник {numpy.random.choice(['скастовал заклинание', 'запустил фаербол', 'наложил заклинание'])} и поранил вас на {max((enemy_damage - player.MagicArmour), 0)} урона.\n\n"
                                                 f"У вас осталось {player.CurHP} здоровья.",
                                            reply_markup=battle_markup, parse_mode="Markdown")
                state = State()
                cur_fights[call.from_user.username][3] = state
                await wait(call, state)
    await bot.answer_callback_query(call.id)


async def main():
    await asyncio.gather(bot.infinity_polling())


if __name__ == '__main__':
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        stmt = select(Persons)
        users = session.scalars(stmt)
        for user in users:
            user.CurHP = user.HP
            user.LocationID = 1
            session.commit()
