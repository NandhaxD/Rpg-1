import pyromod

from pyrogram import *
from motor.motor_asyncio import AsyncIOMotorClient as async_mongo


app = Client(
    "Aasf",
    "14676558",
    "b3c4bc0ba6a4fc123f4d748a8cc39981",
    "6690815586:AAFdkuqgTo2EHlkXlid9HBC2hnsW0flVsDU"
)
app.start()
async_mongo_client = async_mongo("mongodb+srv://Aasf:Aasf@aasf.ere7cca.mongodb.net/?retryWrites=true&w=majority&appName=Aasf")
db = async_mongo_client.Aasf
