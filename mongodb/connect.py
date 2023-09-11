import os
import sys

sys.path.append(os.path.abspath("."))

from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi
from mongoengine import connect

from conf import USERNAME_MONGO, PASSWORD_MONGO, CLUSTER_MONGO, MONGO_DB_NAME


uri = f"mongodb+srv://{USERNAME_MONGO}:{PASSWORD_MONGO}@{CLUSTER_MONGO}.hmksneo.mongodb.net/{MONGO_DB_NAME}?retryWrites=true&w=majority"

# Create a new client and connect to the server
client = MongoClient(uri, server_api=ServerApi("1"))

db = client.book

# Send a ping to confirm a successful connection
try:
    client.admin.command("ping")
    print("Pinged your deployment. You successfully connected to MongoDB!")
except Exception as e:
    print(e)


connect(host=uri)
