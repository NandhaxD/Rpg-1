from .functions import *

# Items
common_sword  = {"name" : "Regular Sword", "cost" : 10, "sell_cost" : 8, "item_type" : "weapon", "hp" : 0, "mana" : 0, "attack" : 2,
                             "magic_attack" : 0, "armour" : 0, "magic_armour" : 0, "req_level" : 1, "availability" : 1}
sharp_sword  = {"name" : "Sharp Sword", "cost" : 25, "sell_cost" : 15, "item_type" : "weapon", "hp" : 0, "mana" : 0, "attack" : 4,
                            "magic_attack" : 0, "armour" : 0, "magic_armour" : 0, "req_level" : 2, "availability" : 2}
common_wand  = {"name" : "Common Staff", "cost" : 10, "sell_cost" : 8, "item_type" : "weapon", "hp" : 0, "mana" : 0, "attack" : 0,
                            "magic_attack" : 2, "armour" : 0, "magic_armour" : 0, "req_level" : 1, "availability" : 1}
uncommon_wand  = {"name" : "Uncommon Staff", "cost" : 25, "sell_cost" : 15, "item_type" : "weapon", "hp" : 0, "mana" : 0, "attack" : 0,
                              "magic_attack" : 4, "armour" : 0, "magic_armour" : 0, "req_level" : 2, "availability" : 2}
old_jacket  = {"name" : "Old Jacket", "cost" : 10, "sell_cost" : 8, "item_type" : "armour", "hp" : 5, "mana" : 0, "attack" : 0,
                           "magic_attck" : 0, "armour" : 2, "magic_armour" : 0, "req_level" : 1, "availability" : 1}
sturdy_jacket  = {"name" : "Strong Jacket", "cost" : 20, "sell_cost" : 18, "item_type" : "armour", "hp" : 10, "mana" : 0, "attack" : 0,
                              "magic_attack" : 0, "armour" : 4, "magic_armour" : 0, "req_level" : 2, "availability" : 2}
common_helmet  = {"name" : "Regular Helmet", "cost" : 5, "sell_cost" : 3, "item_type" : "helmet", "hp" : 2, "mana" : 0, "attack" : 0,
                              "magic_attack" : 0, "armour" : 1, "magic_armour" : 0, "req_level" : 1, "availability" : 1}
common_boots  =  {"name" : "Regular Boots", "cost" : 4, "sell_cost" : 2, "item_type" : "boots", "hp" : 2, "mana" : 0, "attack" : 0,
                             "magic_attack" : 0, "armour" : 1, "magic_armour" : 0, "req_level" : 1, "availability" : 1}
common_hp  =  {"name" : "Health Potion", "cost" : 5, "sell_cost" : 3, "item_type" : "potion", "hp" : 5, "mana" : 0, "attack" : 0,
                          "magic_attack" : 0, "armour" : 0, "magic_armour" : 0, "req_level" : 1, "availability" : 1}

create_item(common_sword)
create_item(sharp_sword)
create_item(common_wand)
create_item(uncommon_wand)
create_item(old_jacket)
create_item(sturdy_jacket)
create_item(common_helmet)
create_item(common_boots)
create_item(common_hp)

# Locations
stormwind  =  {"location_name" : "Stormgrad", "x_coord" : 0, "y_coord" : 0, "location_type" : "town"}
solitude  =  {"location_name" : "Solitude", "x_coord" : -7, "y_coord" : -7, "location_type" : "town"}
cobalt_mine  =  {"location_name" : "Cobalt Cave", "x_coord" : 5, "y_coord" : 4, "location_type" : "dungeon"}
dwemer_ruins  =  {"location_name" : "Dwemer Ruins", "x_coord" : -13, "y_coord" : -13, "location_type" : "dungeon"}

create_location(cobalt_mine)
create_location(dwemer_ruins)
create_location(stormwind)
create_location(solitude)


# Mobs
cobalt  =  {"mob_name" : "Kobold", "hp" : 10, "xp" : 15, "money" : 5, "req_level" : 1, "attack_type" : "phys", "attack" : 2, "armour" : 0,
                      "magic_armour" : 0}
candle_cobalt  =  {"mob_name" : "Candle Kobold", "hp" : 20, "xp" : 30, "money" : 10, "req_level" : 1, "attack_type" : "phys",
                             "attack" : 4, "armour" : 2, "magic_armour" : 0}
dwemer_spider  =  {"mob_name" : "Dwarven Spider", "hp" : 40, "xp" : 40, "money" : 20, "req_level" : 4, "attack_type" : "phys", "attack" : 3,
                             "armour" : 2, "magic_armour" : 2}
dwemer_attacker  =  {"mob_name" : "Dwemer Robot", "hp" : 70, "xp" : 60, "money" : 40, "req_level" : 4, "attack_type" : "mag",
                               "attack" : 5, "armour" : 3, "magic_armour" : 2}
dwemer_centurion  =  {"mob_name" : "Dwarven Centurion", "hp" : 130, "xp" : 100, "money" : 60, "req_level" : 4, "attack_type" : "phys",
                                "attack" : 7, "armour" : 5, "magic_armour" : 5}

create_mob(dwemer_spider)
create_mob(dwemer_attacker)
create_mob(dwemer_centurion)
create_mob(cobalt)
create_mob(candle_cobalt)
