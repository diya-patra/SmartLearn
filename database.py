
import os
from pymongo import MongoClient
from dotenv import load_dotenv

load_dotenv()

MONGODB_URI = os.getenv("MONGODB_URI")

client = None


def get_database():
    global client

    if not MONGODB_URI:
        raise ValueError("MONGODB_URI is missing from the .env file.")

    if client is None:
        client = MongoClient(
            MONGODB_URI,
            serverSelectionTimeoutMS=5000
        )

    try:
        client.admin.command("ping")
        print("MongoDB connected successfully!")
        return client["smartlearn_db"]

    except Exception as error:
        print("MongoDB connection failed:", error)
        raise