from sqlalchemy import select
from bot import bot, session, choose_location_1_markup, choose_location_2_markup, choose_location_3_markup, choose_location_4_markup, dungeon_gate_markup, town_markup
from classes import Persons, Locations

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