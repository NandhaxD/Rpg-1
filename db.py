import motor.motor_asyncio
from bson.objectid import ObjectId
from config import MONGO_DB

client = motor.motor_asyncio.AsyncIOMotorClient(MONGO_DB)
db = client.Rpg

async def get_item_by_name(name):
    item = await db.items.find_one({'Name': name})
    return item

async def get_location_by_name(name):
    location = await db.locations.find_one({'LocationName': name})
    return location

async def get_mob_by_name(name):
    mob = await db.mobs.find_one({'MobName': name})
    return mob

async def create_item(item_data):
    result = await db.items.insert_one(item_data)
    return result.inserted_id

async def create_location(location_data):
    result = await db.locations.insert_one(location_data)
    return result.inserted_id

async def create_mob(mob_data):
    result = await db.mobs.insert_one(mob_data)
    return result.inserted_id
