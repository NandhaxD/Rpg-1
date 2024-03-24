from pyrogram import *
from Aasf import *
from Aasf.Database import *

@app.on_message(group=10)
async def chat_watcher_func(_, message):
    if message.from_user:
        us_in_db = await get_user(message.from_user.id)
        us_in_chat = await get_user_chat(message.chat.id, message.from_user.id)
        if not us_in_db or not us_in_chat:
            await add_user(message.from_user.id)
            await add_user_chat(message.chat.id, message.from_user.id)

    chat_id = (message.chat.id if message.chat.id != message.from_user.id else None)

    #blacklisted_chats_list = await blacklisted_chats()

    if not chat_id:
        return

    in_db = await get_chat(chat_id)
    if not in_db:
        await add_chat(chat_id)
        await db.count.insert_one({"chat_id": chat_id, "count": 0})
