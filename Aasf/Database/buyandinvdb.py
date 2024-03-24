from Aasf import db
from pymongo import ReturnDocument

async def add_item(user_id: int, item_id: int):
    filter = {'player': user_id, 'item_id': item_id}
    update = {'$inc': {'quantity': 1}}
    result = await db.inventory.find_one_and_update(filter, update, upsert=True, return_document=ReturnDocument.AFTER)
    return result

async def increase_item(user_id: int, item_id: int):
    filter = {'player': user_id, 'item_id': item_id}
    update = {'$inc': {'quantity': 1}}
    result = await db.inventory.update_one(filter, update)
    return None

async def get_item(user_id: int, item_id: int):
    filter = {'player': user_id, 'item_id': item_id}
    item = await db.inventory.find_one(filter)
    if item:
        return item
    else:
        return None

async def get_inventory(user_id: int):
    user_filter = {'player': user_id}
    user_inv = []
    async for doc in db.inventory.find(user_filter):
        user_inv.append(doc)
    if not user_inv:
        return None
    return user_inv

async def update_inventory(user_id: int, item_id: int, inv):
    filter = {'player': user_id, 'item_id': item_id}
    result = await db.inventory.replace_one(filter, inv)
    if result.modified_count == 1:
        return True
    else:
        return False

def get_key(val, my_dict):
    for key, value in my_dict.items():
        if val == value:
            return key
    return None
