from strands import tool
from pymongo import MongoClient
from config import MONGO_URI

client = MongoClient(MONGO_URI)

db = client.voicebot

@tool
def query_database(question: str):

    data = db.data.find_one({"question": question})

    if data:
        return data["answer"]

    return "No record found"