
import pymongo, os
from config import DB_URI, DB_NAME

class sidDataBase:

    def __init__(self, DB_URI, DB_NAME):
        self.dbclient = pymongo.MongoClient(DB_URI)
        self.database = self.dbclient[DB_NAME]
        
        self.user_data = self.database['users']
        self.channel_data = self.database['channels']
        self.admins_data = self.database['admins']
        self.banned_user_data = self.database['banned_user']
        self.autho_user_data = self.database['autho_user']
        
        self.auto_delete_data = self.database['auto_delete']
        self.hide_caption_data = self.database['hide_caption']
        self.protect_content_data = self.database['protect_content']
        self.channel_button_data = self.database['channel_button']
        
        self.del_timer_data = self.database['del_timer']
        self.channel_button_link_data = self.database['channelButton_link']
    
    
    async def set_channel_button_link(self, button_name: str, button_link: str):
        channel_button_link_data = self.channel_button_link_data
        
        channel_button_link_data.delete_many({})  # Remove all existing documents
        channel_button_link_data.insert_one({'button_name': button_name, 'button_link': button_link}) # Insert the new document
    
    async def get_channel_button_link(self):
        data = self.channel_button_link_data.find_one({})
        if data:
            return data.get('button_name'), data.get('button_link')
        return 'Join Channel', 'https://t.me/btth480p'
    
    
    async def set_del_timer(self, value: int):
        del_timer_data = self.del_timer_data
        
        existing = del_timer_data.find_one({})
        if existing:
            del_timer_data.update_one({}, {'$set': {'value': value}})
        else:
            del_timer_data.insert_one({'value': value})
    
    async def get_del_timer(self):
        data = self.del_timer_data.find_one({})
        if data:
            return data.get('value', 600)
        return 600
    
    
    async def set_auto_delete(self, value: bool):
        auto_delete_data = self.auto_delete_data
        
        existing = auto_delete_data.find_one({})
        if existing:
            auto_delete_data.update_one({}, {'$set': {'value': value}})
        else:
            auto_delete_data.insert_one({'value': value})
    
    async def set_hide_caption(self, value: bool):
        hide_caption_data = self.hide_caption_data
        
        existing = hide_caption_data.find_one({})
        if existing:
            hide_caption_data.update_one({}, {'$set': {'value': value}})
        else:
            hide_caption_data.insert_one({'value': value})
    
    async def set_protect_content(self, value: bool):
        protect_content_data = self.protect_content_data

        existing = protect_content_data.find_one({})
        if existing:
            protect_content_data.update_one({}, {'$set': {'value': value}})
        else:
            protect_content_data.insert_one({'value': value})
    
    async def set_channel_button(self, value: bool):
        channel_button_data = self.channel_button_data
        
        existing = channel_button_data.find_one({})
        if existing:
            channel_button_data.update_one({}, {'$set': {'value': value}})
        else:
            channel_button_data.insert_one({'value': value})
    
    async def set_request_forcesub(self, value: bool):
        request_forcesub_data = self.request_forcesub_data
        
        existing = request_forcesub_data.find_one({})
        if existing:
            request_forcesub_data.update_one({}, {'$set': {'value': value}})
        else:
            request_forcesub_data.insert_one({'value': value})
    
    async def get_auto_delete(self):
        data = self.auto_delete_data.find_one({})
        if data:
            return data.get('value', False)
        return False
    
    async def get_hide_caption(self):
        data = self.hide_caption_data.find_one({})
        if data:
            return data.get('value', False)
        return False
    
    async def get_protect_content(self):
        data = self.protect_content_data.find_one({})
        if data:
            return data.get('value', False)
        return False
    
    async def get_channel_button(self):
        data = self.channel_button_data.find_one({})
        if data:
            return data.get('value', False)
        return False
    
    async def get_request_forcesub(self):
        data = self.request_forcesub_data.find_one({})
        if data:
            return data.get('value', False)
        return False
    
    async def present_user(self, user_id : int):
        found = self.user_data.find_one({'_id': user_id})
        return bool(found)
    
    async def add_user(self, user_id: int):
        self.user_data.insert_one({'_id': user_id})
        return
    
    async def full_userbase(self):
        user_docs = self.user_data.find()
        user_ids = []
        for doc in user_docs:
            user_ids.append(doc['_id'])
            
        return user_ids
    
    async def del_user(self, user_id: int):
        self.user_data.delete_one({'_id': user_id})
        return
    
    # New channel functions
    async def channel_exist(self, channel_id: int):
        found = self.channel_data.find_one({'_id': channel_id})
        return bool(found)
        
    async def add_channel(self, channel_id: int):
        if not await channel_exist(channel_id):
            self.channel_data.insert_one({'_id': channel_id})
            return
    
    async def del_channel(self, channel_id: int):
        if await channel_exist(channel_id):
            self.channel_data.delete_one({'_id': channel_id})
            return
    
    async def get_all_channels(self):
        channel_docs = self.channel_data.find()
        channel_ids = [doc['_id'] for doc in channel_docs]
        return channel_ids
    
    # New Admin adding functions
    async def admin_exist(self, admin_id: int):
        found = self.admins_data.find_one({'_id': admin_id})
        return bool(found)
        
    async def add_admin(self, admin_id: int):
        if not await admin_exist(admin_id):
            self.admins_data.insert_one({'_id': admin_id})
            return
    
    async def del_admin(self, admin_id: int):
        if await admin_exist(admin_id):
            self.admins_data.delete_one({'_id': admin_id})
            return
    
    async def get_all_admins(self):
        users_docs = self.admins_data.find()
        user_ids = [doc['_id'] for doc in users_docs]
        return user_ids
    
    
    # Banned User functions
    async def ban_user_exist(self, user_id: int):
        found = self.banned_user_data.find_one({'_id': user_id})
        return bool(found)
        
    async def add_ban_user(self, user_id: int):
        if not await ban_user_exist(user_id):
            self.banned_user_data.insert_one({'_id': user_id})
            return
    
    async def del_ban_user(self, user_id: int):
        if await ban_user_exist(user_id):
            self.banned_user_data.delete_one({'_id': user_id})
            return
    
    async def get_ban_users(self):
        users_docs = self.banned_user_data.find()
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


kingdb = sidDataBase(DB_URI, DB_NAME)
