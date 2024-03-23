@bot.callback_query()
async def handle(_, cq):
    cur_loc = (await db.persons.find_one({'user_id': message.from_user.id}))['location_id']
    cur_loc_x = (await db.locations.find_one({'location_id': cur_loc}))['x_coord']
    cur_loc_y = (await db.locations.find_one({'location_id': cur_loc}))['y_coord']

    elif cq.data == 'back_town':
        user_id = int(cq.data.split("_")[1])
        cur_loc = await get_player(user_id)["location_id"]
        if (await get_location(cur_loc)["location_type"]) == "dungeon":
            await get_dungeon(cq)
        else:
            await get_town(cq)
    elif cq.data == 'back_dungeon':
        await get_dungeon(cq)
    elif cq.data == 'leave_city':
        await get_map(cq)
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
        enemy_name = enemy['name']
        player = await db.persons.find_one({'user_id': cq.from_user.id})
        await cq.edit_message_text(f"`{enemy_name}` `{random.choice(['Got In The Way!', 'Jumped Out Of The Corner!', 'Crept Unnoticed!'])}`",
                                    reply_markup=battle_markup)
        player['location_id'] = -2
        await db.persons.replace_one({'user_id': cq.from_user.id}, player)
        state = State()
        cur_fights[player['name']] = [enemy, player, cur_loc, state]
        await wait(cq, state)
    elif cq.data == 'attack':
        cur_fights[cq.from_user.id][3].answered = True
        enemy = cur_fights[cq.from_user.id][0]
        player = cur_fights[cq.from_user.id][1]
        damage = player['attack'] * 1.5 if random.random() < 0.2 else player['attack']
        enemy['hp'] -= max(damage - enemy['armour'], 0)
        crit = f"**attack On** `{damage}` **Damage!**"
        if damage > player['attack']:
            crit = f"**Critical attack On** `{damage}` **Damage!**"
        if enemy['hp'] <= 0:
            lup = ""
            new_xp = player['xp'] + enemy['xp']
            if new_xp >= 100:
                player['level'] += 1
                player['hp'] += 10
                player['xp'] = new_xp - 100
                lup = f"\n\n**level Up! Now Your level:** `{player['level']}`"
            else:
                player['xp'] = new_xp
            player['money'] += enemy['money']
            await cq.edit_message_text(f"{crit}\n\n**You Won! Received** `{enemy['xp']}` **Experience And** `{enemy['money']}` **Coins.**"
                                             f"{lup}",
                                        reply_markup=win_markup, parse_mode=enums.ParseMode.MARKDOWN)
            player['xp'] += enemy['xp']
            player['money'] += enemy['money']
            player['location_id'] = cur_fights[player['name']][2]
            cur_fights.pop(player['name'])
        else:
            for i in range(0, 4):
                await cq.edit_message_text(f"{crit}\n**The Enemy Has** `{enemy['hp']}` **Health.**\n\n"
                                                 f"`The Enemy Is attacking`" + "." * (i % 4), parse_mode=enums.ParseMode.Markdown)
                await asyncio.sleep(0.6)
            if enemy['attack_type'] == 'phys':
                enemy_damage = random.choices([enemy['attack'], enemy['attack'] * 1.5], weights=[0.8, 0.2])[0]
                player['cur_hp'] -= max((enemy_damage - player['armour']), 0)
                if player['cur_hp'] <= 0:
                    await cq.edit_message_text(f"**Opponent** `{random.choice(['Hit', 'Wounded', 'Scratched'])}` **You On** `{max((enemy_damage - player['armour']), 0)}` **Damage.**\n\n"
                                                     f"**You Perished! :(**",
                                                reply_markup=death_markup, parse_mode=enums.ParseMode.Markdown)
                else:
                    await cq.edit_message_text(f"**Opponent** `{random.choice(['Hit', 'Wounded', 'Scratched'])}` **You On** `{max((enemy_damage - player['armour']), 0)}` **Damage.**\n\n"
                                                     f"**You Have Left** `{player['cur_hp']}` **Health.**",
                                                reply_markup=battle_markup, parse_mode=enums.ParseMode.MARKDOWN)
                    state = State()
                    cur_fights[cq.from_user.id][3] = state
                    await wait(cq, state)
            elif enemy['attack_type'] == 'mag':
                enemy_damage = random.choices([enemy['attack'], enemy['attack'] * 1.5], weights=[0.8, 0.2])[0]
                player['cur_hp'] -= max((enemy_damage - player['magic_armour']), 0)
                if player['cur_hp'] <= 0:
                    await cq.edit_message_text(f"**Opponent** `{random.choice(['Hit', 'Hurt', 'Scratched'])}` **You On** `{max((enemy_damage - player['magic_armour']), 0)}` **Damage.**\n\n"
                                                     f"**You Perished ! :(**",
                                                reply_markup=death_markup, parse_mode=enums.ParseMode.MARKDOWN)
                else:
                    await cq.edit_message_text(f"**Opponent** `{random.choice(['Cast A Spell', 'Fireball Launched', 'Cast A Spell'])}` **And Wounded You On** `{max((enemy_damage - player['magic_armour']), 0)}` **Damage.**\n\n"
                                                    f"**You Have Left** `{player['cur_hp']}` **Health.**",
                                                reply_markup=battle_markup, parse_mode=enums.ParseMode.MARKDOWN)
                    state = State()
                    cur_fights[cq.from_user.id][3] = state
                    await wait(cq, state)
        await db.persons.replace_one({'user_id': cq.from_user.id}, player)
    elif cq.data == 'check':
        print(cur_fights)
        enemy = cur_fights[cq.from_user.id][0]
        await cq.edit_message_text(f"**{enemy['name']}**:\n\n" + f"**Health:** `{enemy['hp']}`/`{(await db.mobs.find_one({'mob_name': name}))['name']}`\n" + "**attack:** `{}` {}\n".format(enemy['attack'], '⚔️' if enemy['attack_type'] == 'phys' else '🪄') + f"**Protection:** `{enemy['armour']}` 🛡️ `{enemy['magic_armour']}` 🔮",
                                    reply_markup=check_markup, parse_mode=enums.ParseMode.MARKDOWN)
    elif cq.data == 'revive':
        player = cur_fights[cq.from_user.id][1]
        cur_fights.pop(cq.from_user.id)
        player['location_id'] = 1
        player['cur_hp'] = player['hp']
        await get_town(cq)
        await db.persons.replace_one({'user_id': cq.from_user.id}, player)

elif cq.data == 'heal':
        cur_fights[cq.from_user.id][3].answered = True
        enemy = cur_fights[cq.from_user.id][0]
        player = cur_fights[cq.from_user.id][1]
        stmt = await db.inventory.find_one({'user_id': cq.from_user.id, 'item_id': heal_potion})
        if stmt['quantity'] != 0:
            stmt1 = await db.persons.find_one({'user_id': cq.from_user.id})
            if stmt['quantity'] > 0:
                stmt['quantity'] -= 1
            else:
                stmt['quantity'] += 1
            stmt1['cur_hp'] = min((stmt1['cur_hp'] + 5), stmt1['hp'])
            await db.persons.replace_one({'user_id': cq.from_user.id}, stmt1)
            await db.inventory.replace_one({'user_id': cq.from_user.id, 'item_id': heal_potion}, stmt)
            for i in range(0, 4):
                await cq.edit_message_text(f"**You Drank A Health Potion! Restored 5 hp. Current Health:** {stmt1['cur_hp']}\n\n"
                                                 f"`The Enemy Is attacking`" + "." * (i % 4), parse_mode=enums.ParseMode.Markdown)
                await asyncio.sleep(0.6)
        else:
            for i in range(0, 4):
                await cq.edit_message_text(f"**You Reached Into Your Backpack For A Potion, But He Wasn''t There!**\n\n"
                                                 f"`The Enemy Is attacking`" + "." * (i % 4), parse_mode=enums.ParseMode.Markdown)
                await asyncio.sleep(0.6)
        if enemy['attack_type'] == 'phys':
            enemy_damage = random.choices([enemy['attack'], enemy['attack'] * 1.5], weights=[0.8, 0.2])[0]
            player['cur_hp'] -= max((enemy_damage - player['armour']), 0)
            await db.persons.replace_one({'user_id': cq.from_user.id}, player)
            if player['cur_hp'] <= 0:
                await cq.edit_message_text(f"**Opponent** `{random.choice(['Hit', 'Wounded', 'Scratched'])}` **You On** `{max((enemy_damage - player['armour']), 0)}` **Damage.**\n\n"
                                                 f"**You Perished! :(**",
                                            reply_markup=death_markup, parse_mode=enums.ParseMode.Markdown)
            else:
                await cq.edit_message_text(f"**Opponent** `{random.choice(['Hit', 'Wounded', 'Scratched'])}` **You On** `{max((enemy_damage - player['armour']), 0)}` **Damage.**\n\n"
                                                 f"**You Have Left** `{player['cur_hp']}` **Health.**",
                                            reply_markup=battle_markup, parse_mode=enums.ParseMode.Markdown)
                state = State()
                cur_fights[cq.from_user.id][3] = state
                await wait(cq, state)
        elif enemy['attack_type'] == 'mag':
            enemy_damage = enemy['attack'] * 1.5 if random.random() < 0.2 else enemy['attack']
            player['cur_hp'] -= max((enemy_damage - player['magic_armour']), 0)
            await db.persons.replace_one({'user_id': cq.from_user.id}, player)
            if player['cur_hp'] <= 0:
                await cq.edit_message_text(f"**Opponent** `{random.choice(['Hit', 'Hurt', 'Scratched'])}` **You On** `{max((enemy_damage - player['magic_armour']), 0)}` **Damage.**\n\n"
                                                 f"**You Perished ! :(**",
                                            reply_markup=death_markup, parse_mode=enums.ParseMode.Markdown)
            else:
                await cq.edit_message_text(f"**Opponent** `{random.choice(['Cast A Spell', 'Fireball Launched', 'Cast A Spell'])}` **And Wounded You On** `{max((enemy_damage - player['magic_armour']), 0)}` **Damage.**\n\n"
                                                 f"**You Have Left** `{player['cur_hp']}` **Health.**",
                                            reply_markup=battle_markup, parse_mode=enums.ParseMode.Markdown)
                state = State()
                cur_fights[cq.from_user.id][3] = state
                await wait(cq, state)
    await bot.answer_callback_query(cq.id)
