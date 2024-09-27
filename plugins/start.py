
import os
import asyncio
import random
from pyrogram import Client, filters
from pyrogram.enums import ParseMode, ChatAction
from pyrogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton, CallbackQuery
from pyrogram.errors import FloodWait

from bot import Bot
from config import CUSTOM_CAPTION, OWNER_ID, PICS
from helper_func import banUser, is_userJoin, is_admin, subscribed, encode, decode, get_messages
from database.database import kingdb #.* 
import subprocess
import sys
from plugins.advance_features import convert_time, auto_del_notification, delete_message
from plugins.FORMATS import START_MSG, FORCE_MSG, BAN_TXT
from plugins.request_forcesub import *

@Bot.on_message(filters.command('start') & filters.private & subscribed & ~banUser)
async def start_command(client: Client, message: Message): 
    await message.reply_chat_action(ChatAction.CHOOSE_STICKER)
    id = message.from_user.id  
    
    #banned_users = await get_ban_users()
    #if await ban_user_exist(id):
        #return await message.reply(text=BAN_TXT, message_effect_id=5046589136895476101)
    
    if not await kingdb.present_user(id):
        try:
            await kingdb.add_user(id)
        except:
            pass
                
    text = message.text        
    if len(text)>7:
        transfer = message.command[1]
        await message.delete()
        try:
            base64_string = text.split(" ", 1)[1]
        except:
            return
                
        string = await decode(base64_string)
        argument = string.split("-")
        
        if len(argument) == 3:
            try:
                start = int(int(argument[1]) / abs(client.db_channel.id))
                end = int(int(argument[2]) / abs(client.db_channel.id))
            except:
                return
                    
            if start <= end:
                ids = range(start,end+1)
            else:
                ids = []
                i = start
                while True:
                    ids.append(i)
                    i -= 1
                    if i < end:
                        break
                            
        elif len(argument) == 2:
            try:
                ids = [int(int(argument[1]) / abs(client.db_channel.id))]
            except:
                return
                    
        last_message = None
        await message.reply_chat_action(ChatAction.UPLOAD_DOCUMENT)  
        
        try:
            messages = await get_messages(client, ids)
        except:
            return await message.reply("<b><i>Sᴏᴍᴇᴛʜɪɴɢ ᴡᴇɴᴛ ᴡʀᴏɴɢ..!</i></b>")
            
        AUTO_DEL = await kingdb.get_auto_delete(); DEL_TIMER = await kingdb.get_del_timer()
        HIDE_CAPTION = await kingdb.get_hide_caption(); CHNL_BTN = await kingdb.get_channel_button(); PROTECT_MODE = await kingdb.get_protect_content()   
            
        if CHNL_BTN:
            button_name, button_link = await kingdb.get_channel_button_link()
            
        # temp_msg = await message.reply("<b>. . . </b>")
        # await temp_msg.delete()
        
        for idx, msg in enumerate(messages):
            if bool(CUSTOM_CAPTION) & bool(msg.document):
                caption = CUSTOM_CAPTION.format(previouscaption = "" if not msg.caption else msg.caption.html, filename = msg.document.file_name)
            elif HIDE_CAPTION:
                if msg.document or msg.audio:
                    caption = ""
                else:
                    caption = "" if not msg.caption else msg.caption.html
            else:
                caption = "" if not msg.caption else msg.caption.html

            if CHNL_BTN:
                reply_markup = InlineKeyboardMarkup([[InlineKeyboardButton(text=button_name, url=button_link)]]) if msg.document or msg.photo or msg.video or msg.audio else None
            else:
                reply_markup = msg.reply_markup   
                    
            try:
                copied_msg = await msg.copy(chat_id=id, caption = caption, parse_mode = ParseMode.HTML, reply_markup = reply_markup, protect_content=PROTECT_MODE)
                await asyncio.sleep(0.1)
                asyncio.create_task(delete_message(copied_msg, DEL_TIMER))
                if idx == len(messages) - 1 and AUTO_DEL: 
                        last_message = copied_msg
            except FloodWait as e:
                await asyncio.sleep(e.x)
                copied_msg = await msg.copy(chat_id=id, caption = caption, parse_mode = ParseMode.HTML, reply_markup = reply_markup, protect_content=PROTECT_MODE)
                await asyncio.sleep(0.1)
                asyncio.create_task(delete_message(copied_msg, DEL_TIMER))
                if idx == len(messages) - 1 and AUTO_DEL:
                    last_message = copied_msg
                        
        if AUTO_DEL and last_message:
                asyncio.create_task(auto_del_notification(client, last_message, DEL_TIMER, transfer))
                
        return
            
    else:
        # temp_msg = await message.reply("<b>. . .</b>")
        # await temp_msg.delete()
            
        reply_markup = InlineKeyboardMarkup([[InlineKeyboardButton('🤖 Aʙᴏᴜᴛ ᴍᴇ', callback_data= 'about'), InlineKeyboardButton('Sᴇᴛᴛɪɴɢs ⚙️', callback_data='setting')]])
        await message.reply_photo(
            photo = random.choice(PICS),
            caption = START_MSG.format(
                first = message.from_user.first_name,
                last = message.from_user.last_name,
                username = None if not message.from_user.username else '@' + message.from_user.username,
                mention = message.from_user.mention,
                id = message.from_user.id
            ),
            reply_markup = reply_markup,
	    message_effect_id=5104841245755180586 #🔥
            #quote = True
        )
        try:
            await message.delete()
        except:
            pass
        return

   
#=====================================================================================##

WAIT_MSG = """"<b>Processing ...</b>"""

#=====================================================================================##   


@Bot.on_message(filters.command('start') & filters.private & ~banUser)
async def not_joined(client: Client, message: Message):
    temp = await message.reply(f"<b>??</b>")
    
    user_id = message.from_user.id
    excl = '! '
               
    channels = await kingdb.get_all_channels()
    REQFSUB = await kingdb.get_request_forcesub()
    buttons = []
    count = 0

    try:
        for id in channels:
            await message.reply_chat_action(ChatAction.FIND_LOCATION)
            if not await is_userJoin(client, user_id, id):
                try:
                    data = await client.get_chat(id)
                    cname = data.title
                    link = ""
                    
                    if REQFSUB and await privateChannel(client, id):
                        link = await kingdb.get_stored_reqLink(id); await kingdb.add_reqChannel(id)
                        if not link:
                            invite_link = (await client.create_chat_invite_link(chat_id=id, creates_join_request=True)).invite_link
                            await kingdb.store_reqLink(id, invite_link)
                            link = invite_link
                                                
                    if not link:
                        link = data.invite_link
                        
                    if not link:
                        await client.export_chat_invite_link(id)
                        link = (await client.get_chat(id)).invite_link 
                                                        
                    buttons.append([InlineKeyboardButton(text=cname, url=link)])
                    count += 1
                    await temp.edit(f'<b>{excl * count}</b>')
                                                
                except Exception as e:
                    print(f"Can't Export Channel Name and Link..., Please Check If the Bot is admin in the FORCE SUB CHANNELS:\nProvided Force sub Channel:- {id}")
                    return await temp.edit(f"<blockquote><b><i>! Eʀʀᴏʀ, Cᴏɴᴛᴀᴄᴛ ᴅᴇᴠᴇʟᴏᴘᴇʀ ᴛᴏ sᴏʟᴠᴇ ᴛʜᴇ ɪssᴜᴇs @Shidoteshika1</i></b></blockquote>\n\n<blockquote><b>Rᴇᴀsᴏɴ:</b> {e}</blockquote>")

        try:
            buttons.append([InlineKeyboardButton(text='♻️ Tʀʏ Aɢᴀɪɴ', url=f"https://t.me/{client.username}?start={message.command[1]}")])
        except IndexError:
            pass

        await message.reply_chat_action(ChatAction.CANCEL)
        await temp.edit(
            #photo = random.choice(PICS),   
            text=FORCE_MSG.format(
                first=message.from_user.first_name,
                last=message.from_user.last_name,
                username=None if not message.from_user.username else '@' + message.from_user.username,
                mention=message.from_user.mention,
                id=message.from_user.id,
                count=count
            ),
            reply_markup=InlineKeyboardMarkup(buttons),
            #message_effect_id=5107584321108051014, # 👍
            #quote=True,
            #disable_web_page_preview=True
        )
                
        try:
            await message.delete()
        except:
            pass
                        
    except Exception as e:
        print(f"Unable to perform forcesub buttons reason : {e}")
        return await temp.edit(f"<blockquote><b><i>! Eʀʀᴏʀ, Cᴏɴᴛᴀᴄᴛ ᴅᴇᴠᴇʟᴏᴘᴇʀ ᴛᴏ sᴏʟᴠᴇ ᴛʜᴇ ɪssᴜᴇs @Shidoteshika1</i></b></blockquote>\n\n<blockquote><b>Rᴇᴀsᴏɴ:</b> {e}</blockquote>")

#=====================================================================================##
#.........Extra Fetures .......#
#=====================================================================================##

@Bot.on_message(filters.command('restart') & filters.private & filters.user(OWNER_ID))
async def restart_bot(client: Client, message: Message):
    print("Restarting bot...")
    #name = (await client.get_me()).first_name
    msg = await message.reply(text=f"<b><i><blockquote>⚠️ {client.name} ɢᴏɪɴɢ ᴛᴏ Rᴇsᴛᴀʀᴛ...</blockquote></i></b>")
    try:
        await asyncio.sleep(6)  # Wait for 4 seconds before restarting
        await msg.delete()
        args = [sys.executable, "main.py"]  # Adjust this if your start file is named differently
        os.execl(sys.executable, *args)
    except Exception as e:
        print(f"Error occured while Restarting the bot: {e}")
        return await msg.edit_text(f"<blockquote><b><i>! Eʀʀᴏʀ, Cᴏɴᴛᴀᴄᴛ ᴅᴇᴠᴇʟᴏᴘᴇʀ ᴛᴏ sᴏʟᴠᴇ ᴛʜᴇ ɪssᴜᴇs @Shidoteshika1</i></b></blockquote>\n\n<blockquote><b>Rᴇᴀsᴏɴ:</b> {e}</blockquote>")
    # Optionally, you can add cleanup tasks here
    #subprocess.Popen([sys.executable, "main.py"])  # Adjust this if your start file is named differently
    #sys.exit()
