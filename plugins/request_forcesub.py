# +++ Made By King [telegram user id: @Shidoteshika1] +++

import asyncio
from pyrogram import Client, filters
from pyrogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton, CallbackQuery,  ChatMemberUpdated

from bot import Bot
from database.database import kingdb
from pyrogram.enums import ChatMemberStatus

#import logging
#import os
#from pyrogram.enums import ParseMode

# This handler captures membership updates (like when a user leaves)
@Bot.on_chat_member_updated()
async def handle_Chatmembers(client, chat_member_updated: ChatMemberUpdated):
    #print("Bot.on_chat_member_updated() Triggred....")
    
    new_member = chat_member_updated.new_chat_member
    old_member = chat_member_updated.old_chat_member
    if any([new_member, old_member]):
        member = new_member if new_member else old_member
    else:
        #print(f'Both new member and old meber are None')
        return
    
    member_status = ChatMemberStatus.MEMBER, ChatMemberStatus.LEFT, ChatMemberStatus.BANNED
    
    if member.status in member_status:
        user_id = member.user.id
        chat_id = chat_member_updated.chat.id
        #print(f"A Specified Event Occured between User ID: {user_id} and Channel ID: {chat_id}")
        
        if await kingdb.reqChannel_exist(chat_id) and await kingdb.reqSent_user_exist(chat_id, user_id):
            await kingdb.del_reqSent_user(chat_id, user_id)
            #print(f'{user_id} successfully removed from {chat_id} Database')  
            
      
# This handler will capture any join request to the channel/group where the bot is an admin
@Bot.on_chat_join_request()
async def handle_join_request(client, chat_join_request):
    #print("Bot.on_chat_join_request() Triggred....")
    user_id = chat_join_request.from_user.id  # The user who sent the join request
    chat_id = chat_join_request.chat.id  # The channel/group where the request was sent
    
    #print(f"User ID: {user_id} has sent a join request to Channel ID: {chat_id}")

    if await kingdb.reqChannel_exist(chat_id) and not await kingdb.reqSent_user_exist(chat_id, user_id):
        await kingdb.reqSent_user(chat_id, user_id)
        #print(f'{user_id} successfully added to SET[{chat_id}] Database')
        

#Check If a channel is private or public
"""async def privateChannel(client, channel_id):
    try:
        chat = await client.get_chat(channel_id)
        return not bool(chat.username)
    except Exception as e:
        print(f"Unexcpected error in privateChannel(): {e}")
        return False"""
  

