from Aasf.Database.battledb import *
from Aasf.Database.buyandinvdb import *
from Aasf.Database.functions import *
from Aasf.Database.playerdb import *
from Aasf.Database.chatdb import *
from Aasf.Database.userdb import *
from Aasf import *

# locations 
locations = {
    1: {"location_name": "Adventurer's Guild", "x_coord": 0, "y_coord": 0, "location_type": "town", "location_id": 1, "req_level": 1},
    2: {"location_name": "Ancient Ruins", "x_coord": 5, "y_coord": 4, "location_type": "dungeon", "location_id": 2, "req_level": 3},
    3: {"location_name": "Enchanted Forest", "x_coord": -13, "y_coord": -13, "location_type": "dungeon", "location_id": 3, "req_level": 5},
    4: {"location_name": "Dragon's Den", "x_coord": 10, "y_coord": -5, "location_type": "dungeon", "location_id": 4, "req_level": 7},
    5: {"location_name": "Magic Academy", "x_coord": 7, "y_coord": 7, "location_type": "town", "location_id": 5, "req_level": 10}
}

async def get_location(loc_id: int):
    location = locations.get(loc_id)
    if location:
        return location
    else:
        return False

# items 
items = {
1 : {"name" : "Regular Sword", "cost" : 10, "sell_cost" : 8, "item_type" : "weapon", "item_symbol" : "🗡️", "hp" : 0, "mana" : 0, "attack" : 2,
                             "magic_attack" : 0, "armour" : 0, "magic_armour" : 0, "req_level" : 1, "availability" : 1},
2 : {"name" : "Dual Edge Sword", "cost" : 25, "sell_cost" : 15, "item_type" : "weapon", "item_symbol" : "🗡️", "hp" : 0, "mana" : 0, "attack" : 4,
                            "magic_attack" : 0, "armour" : 0, "magic_armour" : 0, "req_level" : 2, "availability" : 2},
3 : {"name" : "Holy Sword", "cost" : 70, "sell_cost" : 55, "item_type" : "weapon", "item_symbol" : "🗡️", "hp" : 0, "mana" : 0, "attack" : 7,
                            "magic_attack" : 0, "armour" : 0, "magic_armour" : 0, "req_level" : 3, "availability" : 3},
4 : {"name" : "Common Staff", "cost" : 10, "sell_cost" : 8, "item_type" : "weapon", "item_symbol" : "🗡️", "hp" : 0, "mana" : 0, "attack" : 0,
                            "magic_attack" : 2, "armour" : 0, "magic_armour" : 0, "req_level" : 1, "availability" : 1},
5 : {"name" : "Rare Staff", "cost" : 25, "sell_cost" : 15, "item_type" : "weapon", "item_symbol" : "🗡️", "hp" : 0, "mana" : 0, "attack" : 0,
                              "magic_attack" : 4, "armour" : 0, "magic_armour" : 0, "req_level" : 2, "availability" : 2},
6 : {"name" : "Old Jacket", "cost" : 10, "sell_cost" : 8, "item_type" : "armour", "item_symbol" : "🛡️", "hp" : 5, "mana" : 0, "attack" : 0,
                           "magic_attack" : 0, "armour" : 2, "magic_armour" : 0, "req_level" : 1, "availability" : 1},
7 : {"name" : "Strong Jacket", "cost" : 20, "sell_cost" : 18, "item_type" : "armour", "item_symbol" : "🛡️", "hp" : 10, "mana" : 0, "attack" : 0,
                              "magic_attack" : 0, "armour" : 4, "magic_armour" : 0, "req_level" : 2, "availability" : 2},
8 : {"name" : "Regular Helmet", "cost" : 5, "sell_cost" : 3, "item_type" : "helmet", "item_symbol" : "⛑️", "hp" : 2, "mana" : 0, "attack" : 0,
                              "magic_attack" : 0, "armour" : 1, "magic_armour" : 0, "req_level" : 1, "availability" : 1},
9 : {"name" : "Regular Boots", "cost" : 4, "sell_cost" : 2, "item_type" : "boots", "item_symbol" : "👢", "hp" : 2, "mana" : 0, "attack" : 0,
                             "magic_attack" : 0, "armour" : 1, "magic_armour" : 0, "req_level" : 1, "availability" : 1},
10 : {"name" : "Health Potion", "cost" : 5, "sell_cost" : 3, "item_type" : "potion", "item_symbol" : "🔮", "hp" : 5, "mana" : 0, "attack" : 0,
                          "magic_attack" : 0, "armour" : 0, "magic_armour" : 0, "req_level" : 1, "availability" : 1}
}

# mobs
mobs = {
1: [
    {"name": "Goblin", "mob_img": "https://graph.org/file/f786d797e884441edf5be.jpg", "hp": 15, "exp": 20, "money": 10, "req_level": 1, "attack_type": "phys", "attack": 3, "armour": 1, "magic_armour": 0},
    {"name": "Slime", "mob_img": "https://graph.org/file/9dc1ae4629bee38d70ede.jpg", "hp": 10, "exp": 15, "money": 5, "req_level": 1, "attack_type": "magic", "attack": 2, "armour": 0, "magic_armour": 2},
    {"name": "Harpy", "mob_img": "https://graph.org/file/65623978721a8642ad45a.jpg", "hp": 20, "exp": 30, "money": 15, "req_level": 2, "attack_type": "phys", "attack": 4, "armour": 2, "magic_armour": 1},
    {"name": "Troll", "mob_img": "https://graph.org/file/9760cb22bc2a830791806.jpg", "hp": 30, "exp": 40, "money": 20, "req_level": 3, "attack_type": "phys", "attack": 5, "armour": 3, "magic_armour": 0},
    {"name": "Dragon", "mob_img": "https://graph.org/file/7386dadc8a32de7baa03c.jpg", "hp": 50, "exp": 60, "money": 30, "req_level": 5, "attack_type": "magic", "attack": 8, "armour": 5, "magic_armour": 5}
],
2: [
    {"name": "Mummy", "mob_img": "https://graph.org/file/47c5143da006c8a35e426.jpg", "hp": 20, "exp": 30, "money": 15, "req_level": 3, "attack_type": "phys", "attack": 4, "armour": 2, "magic_armour": 2},
    {"name": "Scarab", "mob_img": "https://graph.org/file/3ea972dcd3580abebd77b.jpg", "hp": 15, "exp": 20, "money": 10, "req_level": 2, "attack_type": "phys", "attack": 3, "armour": 1, "magic_armour": 1},
    {"name": "Gargoyle", "mob_img": "https://graph.org/file/4937c9ce70b8285e32662.jpg", "hp": 30, "exp": 40, "money": 20, "req_level": 4, "attack_type": "phys", "attack": 5, "armour": 3, "magic_armour": 0},
    {"name": "Skeleton Mage", "mob_img": "https://graph.org/file/d232ed318bef13c4b197d.jpg", "hp": 25, "exp": 35, "money": 18, "req_level": 3, "attack_type": "magic", "attack": 5, "armour": 0, "magic_armour": 3},
    {"name": "Ancient Golem", "mob_img": "https://graph.org/file/097edf0a9ee5c0c9b09d2.jpg", "hp": 50, "exp": 60, "money": 30, "req_level": 5, "attack_type": "phys", "attack": 7, "armour": 5, "magic_armour": 5}
],
3: [
    {"name": "Forest Spirit", "mob_img": "https://telegra.ph/file/69d0090b00336cc5b342f.jpg", "hp": 35, "exp": 50, "money": 25, "req_level": 5, "attack_type": "magic", "attack": 6, "armour": 2, "magic_armour": 4},
    {"name": "Thorned Vine", "mob_img": "https://telegra.ph/file/1a00a413c2866cc42e763.jpg", "hp": 40, "exp": 45, "money": 20, "req_level": 4, "attack_type": "phys", "attack": 4, "armour": 4, "magic_armour": 2},
    {"name": "Giant Toad", "mob_img": "https://telegra.ph/file/9c5918b899c5b7c703283.jpg", "hp": 45, "exp": 55, "money": 22, "req_level": 5, "attack_type": "phys", "attack": 5, "armour": 3, "magic_armour": 1},
    {"name": "Cursed Tree", "mob_img": "https://telegra.ph/file/51e4d3cfce551c4d32bc2.jpg", "hp": 60, "exp": 70, "money": 35, "req_level": 6, "attack_type": "magic", "attack": 7, "armour": 2, "magic_armour": 6},
    {"name": "Enchanted Wolf", "mob_img": "https://telegra.ph/file/3ffaa90def746273e5a9e.jpg", "hp": 50, "exp": 60, "money": 30, "req_level": 6, "attack_type": "phys", "attack": 7, "armour": 4, "magic_armour": 2}
],
4: [
    {"name": "Dragonling", "mob_img": "https://telegra.ph/file/9c6d3663ca65f8c44a0a2.jpg", "hp": 70, "exp": 100, "money": 50, "req_level": 7, "attack_type": "magic", "attack": 10, "armour": 6, "magic_armour": 8},
    {"name": "Fire Elemental", "mob_img": "https://telegra.ph/file/9e9fcedd9c2f2f8c80203.jpg", "hp": 60, "exp": 80, "money": 40, "req_level": 8, "attack_type": "magic", "attack": 12, "armour": 4, "magic_armour": 10},
    {"name": "Armored Drake", "mob_img": "https://telegra.ph/file/8c9b0e3eefcde68e232a8.jpg", "hp": 80, "exp": 120, "money": 60, "req_level": 9, "attack_type": "phys", "attack": 12, "armour": 10, "magic_armour": 4},
    {"name": "Dragon's Spawn", "mob_img": "https://telegra.ph/file/4e02024f9eb1944d4c5a5.jpg", "hp": 90, "exp": 140, "money": 70, "req_level": 10, "attack_type": "phys", "attack": 14, "armour": 8, "magic_armour": 6},
    {"name": "Dragon Priest", "mob_img": "https://telegra.ph/file/bc82cf65e0fa9c27fc17d.jpg", "hp": 100, "exp": 160, "money": 80, "req_level": 11, "attack_type": "magic", "attack": 14, "armour": 6, "magic_armour": 12}
],
5: [
    {"name": "Elemental Apprentice", "mob_img": "https://telegra.ph/file/3f245cbef1e3d48cb9768.jpg", "hp": 60, "exp": 80, "money": 40, "req_level": 10, "attack_type": "magic", "attack": 10, "armour": 4, "magic_armour": 8},
    {"name": "Golem Guardian", "mob_img": "https://telegra.ph/file/6f9d6f5e6c5db2d4bb71b.jpg", "hp": 70, "exp": 100, "money": 50, "req_level": 11, "attack_type": "phys", "attack": 12, "armour": 10, "magic_armour": 4},
    {"name": "Necromancer Acolyte", "mob_img": "https://telegra.ph/file/007306f89155ec3b69a0d.jpg", "hp": 80, "exp": 120, "money": 60, "req_level": 12, "attack_type": "magic", "attack": 12, "armour": 6, "magic_armour": 10},
    {"name": "Enchanted Book", "mob_img": "https://telegra.ph/file/0d18d9f21c3f0cd3c63dd.jpg", "hp": 50, "exp": 60, "money": 30, "req_level": 13, "attack_type": "magic", "attack": 8, "armour": 2, "magic_armour": 6},
    {"name": "Arcane Apprentice", "mob_img": "https://telegra.ph/file/131f0c1d6a3a0197e3c2e.jpg", "hp": 90, "exp": 140, "money": 70, "req_level": 14, "attack_type": "magic", "attack": 14, "armour": 4, "magic_armour": 12}
]
}

def get_mob(name, mobs_dict):
    for key, mobs_list in mobs_dict.items():
        for mob in mobs_list:
            if mob['name'] == name:
                return key
    return None
