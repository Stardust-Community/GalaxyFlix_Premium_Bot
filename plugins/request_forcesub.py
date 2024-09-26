#adding soon
import logging
import os
import asyncio
from pyrogram import Client, filters
from pyrogram.enums import ParseMode
from pyrogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton, CallbackQuery
from pyrogram.errors import FloodWait

from bot import Bot
#from helper_func import is_userJoin, is_admin, subscribed
from database.database import kingdb#get_all_channels, store_req_link, get_req_link, del_req_link, store_reqsent_id, get_reqsent_ids, del_reqsent_id, get_request_forcesub, set_request_forcesub, get_ban_users

from pyrogram.types import ChatMemberUpdated, ChatMemberLeft

# This handler captures membership updates (like when a user leaves)
@Bot.on_chat_member_updated()
async def handle_member_leave(client, chat_member_updated: ChatMemberUpdated):
    print("Bot.on_chat_member_updated() Triggred....")
    # Check if the new status of the user is 'left'
    if isinstance(chat_member_updated.new_chat_member, ChatMemberLeft):
        user_id = chat_member_updated.from_user.id  # User ID of the person who left
        chat_id = chat_member_updated.chat.id  # Channel ID from which the user left
        
        print(f"User ID: {user_id} has left Channel ID: {chat_id}")
      
        if await kingdb.reqChannel_exist(chat_id) and kingdb.reqSent_user_exist(chat_id, user_id):
            print(f'{user_id} successfully removed from {chat_id} Database')  
            await kingdb.del_reqSent_user(chat_id, user_id)

# This handler will capture any join request to the channel/group where the bot is an admin
@Bot.on_chat_join_request()
async def handle_join_request(client, chat_join_request):
    print("Bot.on_chat_join_request() Triggred....")
    user_id = chat_join_request.from_user.id  # The user who sent the join request
    chat_id = chat_join_request.chat.id  # The channel/group where the request was sent
    
    print(f"User ID: {user_id} has sent a join request to Channel ID: {chat_id}")

    if await kingdb.reqChannel_exist(chat_id):
        await kingdb.reqSent_user(chat_id, user_id)
        print(f'{user_id} successfully added to SET[{chat_id}] Database')


async def privateChannel(client, channel_id):
    # Replace 'CHANNEL_ID' with the channel ID you want to check
    try:
        chat = await client.get_chat(channel_id)
        return not bool(chat.username)
    except Exception as e:
        print(f"Unexcpected error in privateChannel(): {e}")
        return False
  
    #if chat.username:
        #print("This is a public channel.")
    #else:
        #print("This is a private channel.")

