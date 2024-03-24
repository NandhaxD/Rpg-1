import pyromod

from pyrogram import *
from motor.motor_asyncio import AsyncIOMotorClient as async_mongo

app = Client(
    name="Aasf",
    api_id="14676558",
    api_hash="b3c4bc0ba6a4fc123f4d748a8cc39981",
    bot_token="6690815586:AAFh5kcrmt7Heggp-Syg66FDlGP9idUzQEI"
)
DEVS = [5456798232]
app.start()
async_mongo_client = async_mongo("mongodb+srv://jinn1:jinn1@cluster0.iug55ex.mongodb.net/?retryWrites=true&w=majority")
db = async_mongo_client.Aasf
