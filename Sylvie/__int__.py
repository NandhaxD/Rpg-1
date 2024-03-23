import pyromod

from pyrogram import *
from motor.motor_asyncio import AsyncIOMotorClient as async_mongo
from config import *

app = Client(
    "Sylvie",
    api_id="",
    api_hash="",
    bot_token=""
)
app.start()
async_mongo_client = async_mongo("mongodb+srv://Aasf:<password>@aasf.ere7cca.mongodb.net/?retryWrites=true&w=majority&appName=Aasf")
db = async_mongo_client.Sylvie
