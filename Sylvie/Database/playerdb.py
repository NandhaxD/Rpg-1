from Sylvie import *

async def get_player(user_id: int):
    player = await db.player.find_one({"player": user_id})
    if player:
        return player
    else:    
        return False

async def create_player(user_id: int, name: str):
    player = await get_player(user_id)
    if not player:
        await db.player.insert_one({"player": user_id, "name": name, "level": 1, "hp": 10, "cur_hp": 10, "money": 50, "attack": 1, "magic_attack=": 0, "exp": 0, "armour": 0, "magic_armour": 0, "location_id": 1})
        return True
    else:    
        return False

async def delete_player(user_id: int):
    player = await get_player(user_id)
    if player:
        await db.player.delete_one({"player": user_id})
        return True
    else:    
        return False

async def update_player(user_id, ply):
    player = await db.player.find_one({'player': user_id})
    if player:
        await db.player.replace_one({'player': user_id}, ply)
        return True
    else:
        return False
