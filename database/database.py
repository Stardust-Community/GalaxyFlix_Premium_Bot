
import pymongo, os
from config import DB_URI, DB_NAME


dbclient = pymongo.MongoClient(DB_URI)
database = dbclient[DB_NAME]

user_data = database['users']
channel_data = database['channels']
admins_data = database['admins']
banned_user_data = database['banned_user']
autho_user_data = database['autho_user']

auto_delete_data = database['auto_delete']
hide_caption_data = database['hide_caption']
protect_content_data = database['protect_content']
channel_button_data = database['channel_button']

del_timer_data = database['del_timer']
channel_button_link_data = database['channelButton_link']


async def set_channel_button_link(button_name: str, button_link: str):
    channel_button_link_data.delete_many({})  # Remove all existing documents
    channel_button_link_data.insert_one({'button_name': button_name, 'button_link': button_link}) # Insert the new document

async def get_channel_button_link():
    data = channel_button_link_data.find_one({})
    if data:
        return data.get('button_name'), data.get('button_link')
    return 'Join Channel', 'https://t.me/btth480p'


async def set_del_timer(value: int):
    existing = del_timer_data.find_one({})
    if existing:
        del_timer_data.update_one({}, {'$set': {'value': value}})
    else:
        del_timer_data.insert_one({'value': value})

async def get_del_timer():
    data = del_timer_data.find_one({})
    if data:
        return data.get('value', 600)
    return 600


async def set_auto_delete(value: bool):
    existing = auto_delete_data.find_one({})
    if existing:
        auto_delete_data.update_one({}, {'$set': {'value': value}})
    else:
        auto_delete_data.insert_one({'value': value})

async def set_hide_caption(value: bool):
    existing = hide_caption_data.find_one({})
    if existing:
        hide_caption_data.update_one({}, {'$set': {'value': value}})
    else:
        hide_caption_data.insert_one({'value': value})

async def set_protect_content(value: bool):
    existing = protect_content_data.find_one({})
    if existing:
        protect_content_data.update_one({}, {'$set': {'value': value}})
    else:
        protect_content_data.insert_one({'value': value})

async def set_channel_button(value: bool):
    existing = channel_button_data.find_one({})
    if existing:
        channel_button_data.update_one({}, {'$set': {'value': value}})
    else:
        channel_button_data.insert_one({'value': value})

async def set_request_forcesub(value: bool):
    existing = request_forcesub_data.find_one({})
    if existing:
        request_forcesub_data.update_one({}, {'$set': {'value': value}})
    else:
        request_forcesub_data.insert_one({'value': value})

async def get_auto_delete():
    data = auto_delete_data.find_one({})
    if data:
        return data.get('value', False)
    return False

async def get_hide_caption():
    data = hide_caption_data.find_one({})
    if data:
        return data.get('value', False)
    return False

async def get_protect_content():
    data = protect_content_data.find_one({})
    if data:
        return data.get('value', False)
    return False

async def get_channel_button():
    data = channel_button_data.find_one({})
    if data:
        return data.get('value', False)
    return False

async def get_request_forcesub():
    data = request_forcesub_data.find_one({})
    if data:
        return data.get('value', False)
    return False

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

# New channel functions
async def channel_exist(channel_id: int):
    found = channel_data.find_one({'_id': channel_id})
    return bool(found)
    
async def add_channel(channel_id: int):
    if not await channel_exist(channel_id):
        channel_data.insert_one({'_id': channel_id})
        return

async def del_channel(channel_id: int):
    if await channel_exist(channel_id):
        channel_data.delete_one({'_id': channel_id})
        return

async def get_all_channels():
    channel_docs = channel_data.find()
    channel_ids = [doc['_id'] for doc in channel_docs]
    return channel_ids

# New Admin adding functions
async def admin_exist(admin_id: int):
    found = admins_data.find_one({'_id': admin_id})
    return bool(found)
    
async def add_admin(admin_id: int):
    if not await admin_exist(admin_id):
        admins_data.insert_one({'_id': admin_id})
        return

async def del_admin(admin_id: int):
    if await admin_exist(admin_id):
        admins_data.delete_one({'_id': admin_id})
        return

async def get_all_admins():
    users_docs = admins_data.find()
    user_ids = [doc['_id'] for doc in users_docs]
    return user_ids


# Banned User functions
async def ban_user_exist(user_id: int):
    found = banned_user_data.find_one({'_id': user_id})
    return bool(found)
    
async def add_ban_user(user_id: int):
    if not await ban_user_exist(user_id):
        banned_user_data.insert_one({'_id': user_id})
        return

async def del_ban_user(user_id: int):
    if await ban_user_exist(user_id):
        banned_user_data.delete_one({'_id': user_id})
        return

async def get_ban_users():
    users_docs = banned_user_data.find()
    user_ids = [doc['_id'] for doc in users_docs]
    return user_ids


"""# autho User functions
async def ban_user_exist(user_id: int):
    found = banned_user_data.find_one({'_id': user_id})
    return bool(found)
    
async def add_ban_user(user_id: int):
    if not await ban_user_exist(user_id):
        banned_user_data.insert_one({'_id': user_id})
        return

async def del_ban_user(user_id: int):
    if await ban_user_exist(user_id):
        banned_user_data.delete_one({'_id': user_id})
        return

async def get_ban_users():
    users_docs = banned_user_data.find()
    user_ids = [doc['_id'] for doc in users_docs]
    return user_ids"""
