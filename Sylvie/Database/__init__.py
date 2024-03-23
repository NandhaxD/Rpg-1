from .battledb import *
from .buyandinvdb import *
from .functions import *
from .locationdb import *
from .playerdb import *
from Sylvie import *

# locations 
locations = {
    1: {"location_name": "Adventurer's Guild", "x_coord": 0, "y_coord": 0, "location_type": "town", "location_id": 1, "req_level": 1}
}

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
