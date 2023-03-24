from pyrogram import *
from motor.motor_asyncio import AsyncIOMotorClient as async_mongo
from config import *

app = Client(
    'Sylvie',
    api_id=API_ID,
    api_hash=API_HASH,
    bot_token=BOT_TOKEN
)
app.start()
bot = app
async_mongo_client = async_mongo(MONGO_URI)
db = async_mongo_client.Sylvie
