import classes
from init_session import engine, session

classes.Items.__table__.drop(engine, checkfirst=True)
classes.Items.__table__.create(engine, checkfirst=True)
classes.Locations.__table__.drop(engine, checkfirst=True)
classes.Locations.__table__.create(engine, checkfirst=True)
classes.Mobs.__table__.drop(engine, checkfirst=True)
classes.Mobs.__table__.create(engine, checkfirst=True)
classes.Persons.__table__.drop(engine, checkfirst=True)
classes.Persons.__table__.create(engine, checkfirst=True)
classes.Inventory.__table__.drop(engine, checkfirst=True)
classes.Inventory.__table__.create(engine, checkfirst=True)

common_sword = classes.Items(Name="Regular Sword", Cost=10, CostToSale=8, ItemType='weapon', HP=0, Mana=0, Attack=2,
                             MagicAttack=0, Armour=0, MagicArmour=0, ReqLevel=1, Availability=1)
sharp_sword = classes.Items(Name="Sharp Sword", Cost=25, CostToSale=15, ItemType='weapon', HP=0, Mana=0, Attack=4,
                            MagicAttack=0, Armour=0, MagicArmour=0, ReqLevel=2, Availability=2)
common_wand = classes.Items(Name="Common Staff", Cost=10, CostToSale=8, ItemType='weapon', HP=0, Mana=0, Attack=0,
                            MagicAttack=2, Armour=0, MagicArmour=0, ReqLevel=1, Availability=1)
uncommon_wand = classes.Items(Name="Uncommon Staff", Cost=25, CostToSale=15, ItemType='weapon', HP=0, Mana=0, Attack=0,
                              MagicAttack=4, Armour=0, MagicArmour=0, ReqLevel=2, Availability=2)
old_jacket = classes.Items(Name="Old Jacket", Cost=10, CostToSale=8, ItemType='armour', HP=5, Mana=0, Attack=0,
                           MagicAttack=0, Armour=2, MagicArmour=0, ReqLevel=1, Availability=1)
sturdy_jacket = classes.Items(Name="Strong Jacket", Cost=20, CostToSale=18, ItemType='armour', HP=10, Mana=0, Attack=0,
                              MagicAttack=0, Armour=4, MagicArmour=0, ReqLevel=2, Availability=2)
common_helmet = classes.Items(Name="Regular Helmet", Cost=5, CostToSale=3, ItemType='helmet', HP=2, Mana=0, Attack=0,
                              MagicAttack=0, Armour=1, MagicArmour=0, ReqLevel=1, Availability=1)
common_boots = classes.Items(Name="Regular Boots", Cost=4, CostToSale=2, ItemType='boots', HP=2, Mana=0, Attack=0,
                             MagicAttack=0, Armour=1, MagicArmour=0, ReqLevel=1, Availability=1)
common_hp = classes.Items(Name="Health Potion", Cost=5, CostToSale=3, ItemType='potion', HP=5, Mana=0, Attack=0,
                          MagicAttack=0, Armour=0, MagicArmour=0, ReqLevel=1, Availability=1)
session.add_all(
    [common_sword, sharp_sword, common_wand, uncommon_wand, old_jacket, sturdy_jacket, common_helmet, common_boots,
     common_hp])
session.commit()

stormwind = classes.Locations(LocationName='Stormgrad', XCoord=0, YCoord=0, LocationType='town')
solitude = classes.Locations(LocationName='Solitude', XCoord=-7, YCoord=-7, LocationType='town')
session.add(stormwind)
session.add(solitude)

cobalt_mine = classes.Locations(LocationName='Cobalt Cave', XCoord=5, YCoord=4, LocationType='dungeon')
dwemer_ruins = classes.Locations(LocationName='Dwemer Ruins', XCoord=-13, YCoord=-13, LocationType='dungeon')
session.add(cobalt_mine)
session.add(dwemer_ruins)
session.commit()

cobalt = classes.Mobs(MobName='Kobold', HP=10, XP=15, Money=5, ReqLevel=1, AttackType='phys', Attack=2, Armour=0,
                      MagicArmour=0)
candle_cobalt = classes.Mobs(MobName='Candle Kobold', HP=20, XP=30, Money=10, ReqLevel=1, AttackType='phys',
                             Attack=4, Armour=2, MagicArmour=0)
session.add(cobalt)
session.add(candle_cobalt)

dwemer_spider = classes.Mobs(MobName='Dwarven Spider', HP=40, XP=40, Money=20, ReqLevel=4, AttackType='phys', Attack=3,
                             Armour=2, MagicArmour=2)
dwemer_attacker = classes.Mobs(MobName='Dwemer Robot', HP=70, XP=60, Money=40, ReqLevel=4, AttackType='mag',
                               Attack=5, Armour=3, MagicArmour=2)
dwemer_centurion = classes.Mobs(MobName='Dwarven Centurion', HP=130, XP=100, Money=60, ReqLevel=4, AttackType='phys',
                                Attack=7, Armour=5, MagicArmour=5)
session.add(dwemer_spider)
session.add(dwemer_attacker)
session.add(dwemer_centurion)
session.commit()
