import asyncio
from bson.objectid import ObjectId
from Sylvie import *

class Enemy:
    def __init__(self, id):
        self.enemy = await db.mobs.find_one({"_id": ObjectId(id)})
        self.name = self.enemy["MobName"]
        self.hp = self.enemy["HP"]
        self.attack = self.enemy["Attack"]
        self.armour = self.enemy["Armour"]
        self.m_armour = self.enemy["MagicArmour"]
        self.xp = self.enemy["XP"]
        self.attack_type = self.enemy["AttackType"]
        self.money = self.enemy["Money"]

class Timer:
    async def start(self):
        await asyncio.sleep(60)
        if not self.answer:
            return False
        else:
            return True
    def __init__(self):
        self.answer = False

class Persons:
    def __init__(self, data):
        self.user = data
        self.user_id = data["user_id"]
        self.name = data["name"]
        self.level = data["Level"]
        self.hp = data["HP"]
        self.cur_hp = data["CurHP"]
        self.money = data["Money"]
        self.attack = data["Attack"]
        self.magic_attack = data["MagicAttack"]
        self.xp = data["XP"]
        self.armour = data["Armour"]
        self.magic_armour = data["MagicArmour"]
        self.location_id = data["LocationID"]

class Mobs:
    def __init__(self, data):
        self.mob = data
        self.mob_id = data["_id"]
        self.mob_name = data["MobName"]
        self.hp = data["HP"]
        self.xp = data["XP"]
        self.money = data["Money"]
        self.req_level = data["ReqLevel"]
        self.attack_type = data["AttackType"]
        self.attack = data["Attack"]
        self.armour = data["Armour"]
        self.magic_armour = data["MagicArmour"]

class Locations:
    def __init__(self, data):
        self.location = data
        self.location_id = data["_id"]
        self.location_name = data["LocationName"]
        self.x_coord = data["XCoord"]
        self.y_coord = data["YCoord"]
        self.location_type = data["LocationType"]

class Items:
    def __init__(self, data):
        self.item = data
        self.item_id = data["_id"]
        self.name = data["Name"]
        self.cost = data["Cost"]
        self.cost_to_sale = data["CostToSale"]
        self.item_type = data["ItemType"]
        self.hp = data["HP"]
        self.mana = data["Mana"]
        self.attack = data["Attack"]
        self.magic_attack = data["MagicAttack"]
        self.armour = data["Armour"]
        self.magic_armour = data["MagicArmour"]
        self.req_level = data["ReqLevel"]
        self.availability = data["Availability"]

class Inventory:
    def __init__(self, data):
        self.inventory = data
        self.user_id = data["_id"]
        self.nickname = data["Nickname"]
        self.item_id = data["ItemID"]
        self.quantity = data["Quantity"]
