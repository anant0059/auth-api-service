from pymongo import MongoClient
import os
import time
import motor.motor_asyncio
from app.utils.utilities import AuthEngine
from app.config.settings import MONGO_URI, DB_NAME


async def mongo_connection_obj():
    try:
        print(f"Connecting to MongoDB at {MONGO_URI}")
        client =  motor.motor_asyncio.AsyncIOMotorClient(MONGO_URI, serverSelectionTimeoutMS=5000)

        await client.server_info()
        print("MongoDB connection established.")
        
        db = client[DB_NAME]
        return db
    except Exception as e:
        print(f"Error connecting to MongoDB: {e}")
        raise


async def insert_one_into_db(tableName,value):
    try:
        in_time = time.time()
        cursor = AuthEngine().mongoDb[f"{tableName}"].insert_one(value)
        print(f"Time Taken by insert_one_into_db  {str(time.time() - in_time)}")
        return cursor
    except Exception as e:
        print(f"Failed to insert data into the database: {e}")


async def get_data_from_db(tableName, query):
    try:
        in_time = time.time()
        
        cursor = await AuthEngine().mongoDb[f"{tableName}"].find_one(query)
        print(f"Query result type: {type(cursor)}, value: {cursor}")
        
        print(f"here get data {in_time}")
        print(f"Time Taken by get_response_from_db data count {cursor} {str(time.time() - in_time)}")
        
        return cursor
    except Exception as e:
        print(f"Failed to fetch data from the database: {e}")
        return None
