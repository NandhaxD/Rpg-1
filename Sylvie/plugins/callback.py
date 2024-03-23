    elif cq.data == 'attack':
        await update_time(cq.from_user.id)
        battle = get_battle(cq.from_user.id)
        enemy = battle["enemy"]
        player = await get_player(cq.from_user.id)
        damage = player['attack'] * 1.5 if random.random() < 0.2 else player['attack']
        enemy['hp'] -= max(damage - enemy['armour'], 0)
        crit = f"**Attack On** `{damage}` **Damage!**"
        win_markup = InlineKeyboardMarkup(
            inline_keyboard=[
                [InlineKeyboardButton("Back", callback_data="leave_city")],
                [InlineKeyboardButton("Keep Going", callback_data="enter_dungeon")]
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
            await cq.edit_message_text(f"{crit}\n\n**You Won! Received** `{enemy['exp']}` **Experience And** `{enemy['money']}` **Coins.**"
                                             f"{lup}",
                                        reply_markup=win_markup, parse_mode=enums.ParseMode.MARKDOWN)
            player['exp'] += enemy['exp']
            player['money'] += enemy['money']
            player['location_id'] = cur_fights[player['name']][2]
            cur_fights.pop(player['name'])
        else:
            for i in range(0, 4):
                await cq.edit_message_text(f"{crit}\n**The Enemy Has** `{enemy['hp']}` **Health.**\n\n"
                                                 f"`The Enemy Is Attacking`" + "." * (i % 4), parse_mode=enums.ParseMode.Markdown)
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
