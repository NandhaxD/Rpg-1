from main import Items, session, Locations, engine, Mobs

Items.__table__.drop(engine, checkfirst=True)
Items.__table__.create(engine, checkfirst=True)
Locations.__table__.drop(engine, checkfirst=True)
Locations.__table__.create(engine, checkfirst=True)

common_sword = Items(Name="Обычный меч", Cost=10, CostToSale=8, ItemType='weapon', HP=0, Mana=0, Attack=2,
                     MagicAttack=0, Armour=0, MagicArmour=0, ReqLevel=1, Availability=1)
sharp_sword = Items(Name="Острый меч", Cost=25, CostToSale=15, ItemType='weapon', HP=0, Mana=0, Attack=4,
                    MagicAttack=0, Armour=0, MagicArmour=0, ReqLevel=2, Availability=2)
common_wand = Items(Name="Обычный посох", Cost=10, CostToSale=8, ItemType='weapon', HP=0, Mana=0, Attack=0,
                    MagicAttack=2, Armour=0, MagicArmour=0, ReqLevel=1, Availability=1)
uncommon_wand = Items(Name="Необычный посох", Cost=25, CostToSale=15, ItemType='weapon', HP=0, Mana=0, Attack=0,
                    MagicAttack=4, Armour=0, MagicArmour=0, ReqLevel=2, Availability=2)
old_jacket = Items(Name="Старая куртка", Cost=10, CostToSale=8, ItemType='armour', HP=5, Mana=0, Attack=0,
                    MagicAttack=0, Armour=2, MagicArmour=0, ReqLevel=1, Availability=1)
sturdy_jacket = Items(Name="Крепкая куртка", Cost=20, CostToSale=18, ItemType='armour', HP=10, Mana=0, Attack=0,
                    MagicAttack=0, Armour=4, MagicArmour=0, ReqLevel=2, Availability=2)
common_helmet = Items(Name="Обычный шлем", Cost=5, CostToSale=3, ItemType='helmet', HP=2, Mana=0, Attack=0,
                    MagicAttack=0, Armour=1, MagicArmour=0, ReqLevel=1, Availability=1)
common_boots = Items(Name="Обычные ботинки", Cost=4, CostToSale=2, ItemType='boots', HP=2, Mana=0, Attack=0,
                    MagicAttack=0, Armour=1, MagicArmour=0, ReqLevel=1, Availability=1)
common_hp = Items(Name="Зелье здоровья", Cost=5, CostToSale=3, ItemType='potion', HP=5, Mana=0, Attack=0,
                    MagicAttack=0, Armour=0, MagicArmour=0, ReqLevel=1, Availability=1)
session.add_all([common_sword, sharp_sword, common_wand, uncommon_wand, old_jacket, sturdy_jacket, common_helmet, common_boots, common_hp])
session.commit()


stormwind = Locations(LocationName='Штормград', XCoord=0, YCoord=0, LocationType='town')
solitude = Locations(LocationName='Солитьюд', XCoord=-7, YCoord=-7, LocationType='town')
session.add(stormwind)
session.add(solitude)

cobalt_mine = Locations(LocationName='Кобальтовая пещера', XCoord=5, YCoord=4, LocationType='dungeon')
dwemer_ruins = Locations(LocationName='Двемерские руины', XCoord=-13, YCoord=-13, LocationType='dungeon')
session.add(cobalt_mine)
session.add(dwemer_ruins)
session.commit()


cobalt = Mobs(MobName='Кобольд', HP=10, XP=15, Money=5, ReqLevel=1, AttackType='phys', Attack=2, Armour=0, MagicArmour=0)
candle_cobalt = Mobs(MobName='Кобольд со свечой', HP=20, XP=30, Money=10, ReqLevel=1, AttackType='phys', Attack=4, Armour=2, MagicArmour=0)
session.add(cobalt)
session.add(candle_cobalt)

dwemer_spider = Mobs(MobName='Двемерский паук', HP=40, XP=40, Money=20, ReqLevel=4, AttackType='phys', Attack=3, Armour=2, MagicArmour=2)
dwemer_attacker = Mobs(MobName='Двемерский робот', HP=70, XP=60, Money=40, ReqLevel=4, AttackType='mag', Attack=5, Armour=3, MagicArmour=2)
dwemer_centurion = Mobs(MobName='Двемерский центурион', HP=130, XP=100, Money=60, ReqLevel=4, AttackType='phys', Attack=7, Armour=5, MagicArmour=5)
session.add(dwemer_spider)
session.add(dwemer_attacker)
session.add(dwemer_centurion)
session.commit()