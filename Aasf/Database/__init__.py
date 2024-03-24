from Aasf.Database.battledb import *
from Aasf.Database.buyandinvdb import *
from Aasf.Database.functions import get_map, get_town, get_dungeon
from Aasf.Database.playerdb import *
from Aasf.Database.chatdb import *
from Aasf.Database.userdb import *
from Aasf import *

# locations 
locations = {
    1: {"location_name": "Adventurer's Guild", "x_coord": 0, "y_coord": 0, "location_type": "town", "location_id": 1, "req_level": 1}
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
    {"mob_name": "Slime", "mob_img": "https://graph.org/file/9dc1ae4629bee38d70ede.jpg", "hp": 10, "exp": 15, "money": 5, "req_level": 1, "attack_type": "magic", "attack": 2, "armour": 0, "magic_armour": 2},
    {"mob_name": "Goblin", "mob_img": "https://graph.org/file/f786d797e884441edf5be.jpg", "hp": 15, "exp": 20, "money": 10, "req_level": 1, "attack_type": "phys", "attack": 3, "armour": 1, "magic_armour": 0},
    {"mob_name": "Harpy", "mob_img": "https://graph.org/file/65623978721a8642ad45a.jpg", "hp": 20, "exp": 30, "money": 15, "req_level": 2, "attack_type": "phys", "attack": 4, "armour": 2, "magic_armour": 1},
    {"mob_name": "Troll", "mob_img": "https://graph.org/file/9760cb22bc2a830791806.jpg", "hp": 30, "exp": 40, "money": 20, "req_level": 3, "attack_type": "phys", "attack": 5, "armour": 3, "magic_armour": 0},
    {"mob_name": "Dragon", "mob_img": "https://graph.org/file/7386dadc8a32de7baa03c.jpg", "hp": 50, "exp": 60, "money": 30, "req_level": 5, "attack_type": "magic", "attack": 8, "armour": 5, "magic_armour": 5}
]
}
