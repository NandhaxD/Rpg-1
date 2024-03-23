import pyromod

from pyrogram import *
from motor.motor_asyncio import AsyncIOMotorClient as async_mongo
from config import *

app = Client(
    "Sylvie",
    api_id="14676558",
    api_hash="b3c4bc0ba6a4fc123f4d748a8cc39981",
    bot_token="6690815586:AAGsAZ4n8fJX6t_jgdJmvNaKErpvEp5VXxs"
)
app.start()
async_mongo_client = async_mongo("mongodb+srv://Aasf:<password>@aasf.ere7cca.mongodb.net/?retryWrites=true&w=majority&appName=Aasf")
db = async_mongo_client.Sylvie
