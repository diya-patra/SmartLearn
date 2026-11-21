
import os
import streamlit as st
from pymongo import MongoClient
from dotenv import load_dotenv

# Load environment variables from the local .env file
load_dotenv()


def get_mongodb_uri():
    """
    Get MongoDB connection string.

    Local development: Reads from .env
    Streamlit Cloud: Reads from Streamlit Secrets
    """

    # First, check local environment variables
    mongodb_uri = os.getenv("MONGODB_URI")

    # If not found, check Streamlit Cloud secrets
    if not mongodb_uri:
        try:
            mongodb_uri = st.secrets["MONGODB_URI"]
        except (KeyError, FileNotFoundError):
            mongodb_uri = None

    if not mongodb_uri:
        raise ValueError(
            "MONGODB_URI is missing. Configure it in your local .env "
            "file or Streamlit Cloud Secrets."
        )

    return mongodb_uri


# MongoDB client is reused across application calls
client = None


def get_database():
    global client

    if client is None:
        mongodb_uri = get_mongodb_uri()

        client = MongoClient(
            mongodb_uri,
            serverSelectionTimeoutMS=5000
        )

    try:
        client.admin.command("ping")
        print("MongoDB connected successfully!")

        return client["smartlearn_db"]

    except Exception as error:
        print("MongoDB connection failed:", error)
        raise
