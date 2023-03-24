from classes import *

# Items
common_sword = Items(Name="Regular Sword", Cost=10, CostToSale=8, ItemType='weapon', HP=0, Mana=0, Attack=2,
                             MagicAttack=0, Armour=0, MagicArmour=0, ReqLevel=1, Availability=1)
sharp_sword = Items(Name="Sharp Sword", Cost=25, CostToSale=15, ItemType='weapon', HP=0, Mana=0, Attack=4,
                            MagicAttack=0, Armour=0, MagicArmour=0, ReqLevel=2, Availability=2)
common_wand = Items(Name="Common Staff", Cost=10, CostToSale=8, ItemType='weapon', HP=0, Mana=0, Attack=0,
                            MagicAttack=2, Armour=0, MagicArmour=0, ReqLevel=1, Availability=1)
uncommon_wand = Items(Name="Uncommon Staff", Cost=25, CostToSale=15, ItemType='weapon', HP=0, Mana=0, Attack=0,
                              MagicAttack=4, Armour=0, MagicArmour=0, ReqLevel=2, Availability=2)
old_jacket = Items(Name="Old Jacket", Cost=10, CostToSale=8, ItemType='armour', HP=5, Mana=0, Attack=0,
                           MagicAttack=0, Armour=2, MagicArmour=0, ReqLevel=1, Availability=1)
sturdy_jacket = Items(Name="Strong Jacket", Cost=20, CostToSale=18, ItemType='armour', HP=10, Mana=0, Attack=0,
                              MagicAttack=0, Armour=4, MagicArmour=0, ReqLevel=2, Availability=2)
common_helmet = Items(Name="Regular Helmet", Cost=5, CostToSale=3, ItemType='helmet', HP=2, Mana=0, Attack=0,
                              MagicAttack=0, Armour=1, MagicArmour=0, ReqLevel=1, Availability=1)
common_boots = Items(Name="Regular Boots", Cost=4, CostToSale=2, ItemType='boots', HP=2, Mana=0, Attack=0,
                             MagicAttack=0, Armour=1, MagicArmour=0, ReqLevel=1, Availability=1)
common_hp = Items(Name="Health Potion", Cost=5, CostToSale=3, ItemType='potion', HP=5, Mana=0, Attack=0,
                          MagicAttack=0, Armour=0, MagicArmour=0, ReqLevel=1, Availability=1)

await create_item(common_sword)
await create_item(sharp_sword)
await create_item(common_wand)
await create_item(uncommon_wand)
await create_item(old_jacket)
await create_item(sturdy_jacket)
await create_item(common_helmet)
await create_item(common_boots)
await create_item(common_hp)

# Locations
stormwind = Locations(LocationName='Stormgrad', XCoord=0, YCoord=0, LocationType='town')
solitude = Locations(LocationName='Solitude', XCoord=-7, YCoord=-7, LocationType='town')
cobalt_mine = Locations(LocationName='Cobalt Cave', XCoord=5, YCoord=4, LocationType='dungeon')
dwemer_ruins = Locations(LocationName='Dwemer Ruins', XCoord=-13, YCoord=-13, LocationType='dungeon')

await create_location(cobalt_mine)
await create_location(dwemer_ruins)
await create_location(stormwind)
await create_location(solitude)


# Mobs
cobalt = Mobs(MobName='Kobold', HP=10, XP=15, Money=5, ReqLevel=1, AttackType='phys', Attack=2, Armour=0,
                      MagicArmour=0)
candle_cobalt = Mobs(MobName='Candle Kobold', HP=20, XP=30, Money=10, ReqLevel=1, AttackType='phys',
                             Attack=4, Armour=2, MagicArmour=0)
dwemer_spider = Mobs(MobName='Dwarven Spider', HP=40, XP=40, Money=20, ReqLevel=4, AttackType='phys', Attack=3,
                             Armour=2, MagicArmour=2)
dwemer_attacker = Mobs(MobName='Dwemer Robot', HP=70, XP=60, Money=40, ReqLevel=4, AttackType='mag',
                               Attack=5, Armour=3, MagicArmour=2)
dwemer_centurion = Mobs(MobName='Dwarven Centurion', HP=130, XP=100, Money=60, ReqLevel=4, AttackType='phys',
                                Attack=7, Armour=5, MagicArmour=5)

await create_mob(dwemer_spider)
await create_mob(dwemer_attacker)
await create_mob(dwemer_centurion)
await create_mob(cobalt)
await create_mob(candle_cobalt)
