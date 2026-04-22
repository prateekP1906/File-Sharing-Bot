import pymongo, os
from config import DB_URL, DB_NAME

dbclient = pymongo.MongoClient(DB_URL)
database = dbclient[DB_NAME]
user_data = database['users']

async def present_user(user_id : int):
    found = user_data.find_one({'_id': user_id})
    return bool(found)

async def add_user(user_id: int):
    user_data.insert_one({'_id': user_id})
    return

async def full_userbase():
    user_docs = user_data.find()
    user_ids = []
    for doc in user_docs:
        user_ids.append(doc['_id'])
    return user_ids

async def del_user(user_id: int):
    user_data.delete_one({'_id': user_id})
    return

# --- NEW FUNCTIONS ADDED BELOW ---

async def update_request_status(user_id: int, channel_num: int, status: bool):
    # This creates fields: has_requested_1 and has_requested_2
    field = f"has_requested_{channel_num}"
    user_data.update_one({'_id': user_id}, {'$set': {field: status}}, upsert=True)

async def check_request_status(user_id: int):
    user = user_data.find_one({'_id': user_id})
    if user:
        # Returns (True/False for Ch1, True/False for Ch2)
        return user.get('has_requested_1', False), user.get('has_requested_2', False)
    return False, False
    
