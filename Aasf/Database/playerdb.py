from Aasf import db

async def get_player(user_id: int):
    player = await db.player.find_one({"player": user_id})
    if player:
        return player
    else:
        return False


async def create_player(user_id: int, name: str):
    player = await get_player(user_id)
    if not player:
        result = await db.player.insert_one({
            "player": user_id,
            "name": name,
            "level": 1,
            "hp": 10,
            "cur_hp": 10,
            "money": 50,
            "attack": 1,
            "magic_attack": 0,
            "exp": 0,
            "armour": 0,
            "magic_armour": 0,
            "location_id": 1
        })
        if result.inserted_id:
            return True
        else:
            return False
    else:
        return False


async def delete_player(user_id: int):
    player = await get_player(user_id)
    if player:
        result = await db.player.delete_one({"player": user_id})
        if result.deleted_count == 1:
            return True
        else:
            return False
    else:
        return False


async def update_player(user_id: int, ply):
    player = await get_player(user_id)
    if player:
        result = await db.player.replace_one({
            "player": user_id
        }, ply)
        if result.matched_count == 1 and result.modified_count == 1:
            return True
        else:
            return False
    else:
        return False
