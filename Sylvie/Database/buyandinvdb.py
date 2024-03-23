from Sylvie import *

async def add_item(user_id, item_id):
    doc = {'player': user_id, 'item_id': item_id, 'quantity': 1}
    result = await db.inventory.find_one(doc)
    if not result:
        result = await db.inventory.insert_one(doc)
    else:
        return None

async def increase_item(user_id, item_id):
    filter = {'player': user_id, 'item_id': item_id}
    update = {'$inc': {'quantity': 1}}
    result = await db.inventory.update_one(filter, update)
    return None

async def get_item(user_id, item_id):
    filter = {'player': user_id, 'item_id': item_id}
    item = await db.inventory.find_one(filter)
    if item:
        return item
    else:
        return False

async def get_inventory(user_id):
    user_filter = {'player': user_id}
    user_inv = []
    async for doc in db.inventory.find(user_filter):
        user_inv.append(doc)
    if not user_inv:
        return None
    return user_inv

async def update_inventory(user_id, item_id, inv):
    inventory = await db.find_one({'player': user_id, 'item_id': item_to_sell})
    if inventory:
        await db.inventory.replace_one({'player': user_id, 'item_id': item_id}, inv)
        return True
    else:
        return False
def get_key(val, my_dict):
    for key, value in my_dict.items():
        if val == value:
            return key
    return "key doesn't exist"
