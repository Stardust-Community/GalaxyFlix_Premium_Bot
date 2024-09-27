# +++ Made By King [telegram user id: @Shidoteshika1] +++

import os
import asyncio
from asyncio import Lock
from bot import Bot
from config import OWNER_ID
import time
from datetime import datetime 
from pyrogram import Client, filters
from helper_func import is_admin, get_readable_time, banUser
from plugins.FORMATS import HELP_TEXT, BAN_TXT, CMD_TXT, USER_CMD_TXT, FSUB_CMD_TXT
from pyrogram.errors import FloodWait, UserIsBlocked, InputUserDeactivated
from database.database import kingdb 
from pyrogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton, CallbackQuery

REPLY_ERROR = """Usᴇ ᴛʜɪs ᴄᴏᴍᴍᴀɴᴅ ᴀs ᴀ ʀᴇᴘʟʏ ᴛᴏ ᴀɴʏ Tᴇʟᴇɢʀᴀᴍ ᴍᴇssᴀɢᴇ ᴡɪᴛʜᴏᴜᴛ ᴀɴʏ sᴘᴀᴄᴇs."""
# Define a global variable to store the cancel state
is_canceled = False
cancel_lock = Lock()

#Settings for banned users..
@Bot.on_message(filters.private & banUser & filters.command(['start', 'help']))
async def handle_banuser(client, message):
    return await message.reply(text=BAN_TXT, message_effect_id=5046589136895476101,)#💩)

#--------------------------------------------------------------[[ADMIN COMMANDS]]---------------------------------------------------------------------------#
# Handler for the /cancel command
@Bot.on_message(filters.private & filters.command('cancel') & is_admin)
async def cancel_broadcast(client: Bot, message: Message):
    global is_canceled
    async with cancel_lock:
        is_canceled = True

@Bot.on_message(filters.private & filters.command('broadcast') & is_admin)
async def send_text(client: Bot, message: Message):
    global is_canceled
    async with cancel_lock:
        is_canceled = False
    mode = False
    broad_mode = ''
    store = message.text.split()[1:]
    
    if store and len(store) == 1 and store[0] == 'silent':
        mode = True
        broad_mode = 'SILENT '

    if message.reply_to_message:
        query = await kingdb.full_userbase()
        broadcast_msg = message.reply_to_message
        total = len(query)
        successful = 0
        blocked = 0
        deleted = 0
        unsuccessful = 0

        pls_wait = await message.reply("<i>Bʀᴏᴀᴅᴄᴀsᴛɪɴɢ Mᴇssᴀɢᴇ... Tʜɪs ᴡɪʟʟ ᴛᴀᴋᴇ sᴏᴍᴇ ᴛɪᴍᴇ.</i>")
        bar_length = 20
        final_progress_bar = "●" * bar_length
        complete_msg = f"🤖 {broad_mode}BROADCAST COMPLETED ✅"
        progress_bar = ''
        last_update_percentage = 0
        percent_complete = 0
        update_interval = 0.05  # Update progress bar every 5%

        for i, chat_id in enumerate(query, start=1):
            async with cancel_lock:
                if is_canceled:
                    final_progress_bar = progress_bar
                    complete_msg = f"🤖 {broad_mode}BROADCAST CANCELED ❌"
                    break
            try:
                await broadcast_msg.copy(chat_id, disable_notification=mode)
                successful += 1
            except FloodWait as e:
                await asyncio.sleep(e.x)
                await broadcast_msg.copy(chat_id, disable_notification=mode)
                successful += 1
            except UserIsBlocked:
                await kingdb.del_user(chat_id)
                blocked += 1
            except InputUserDeactivated:
                await kingdb.del_user(chat_id)
                deleted += 1
            except:
                unsuccessful += 1
                await kingdb.del_user(chat_id)
                pass

            # Calculate percentage complete
            percent_complete = i / total

            # Update progress bar
            if percent_complete - last_update_percentage >= update_interval or last_update_percentage == 0:
                num_blocks = int(percent_complete * bar_length)
                progress_bar = "●" * num_blocks + "○" * (bar_length - num_blocks)
    
                # Send periodic status updates
                status_update = f"""<b>🤖 {broad_mode}BROADCAST IN PROGRESS...

<blockquote>⏳:</b> [{progress_bar}] <code>{percent_complete:.0%}</code></blockquote>

<b>🚻 Tᴏᴛᴀʟ Usᴇʀs: <code>{total}</code>
✅ Sᴜᴄᴄᴇssғᴜʟ: <code>{successful}</code>
🚫 Bʟᴏᴄᴋᴇᴅ Usᴇʀs: <code>{blocked}</code>
⚠️ Dᴇʟᴇᴛᴇᴅ Aᴄᴄᴏᴜɴᴛs: <code>{deleted}</code>
❌ Uɴsᴜᴄᴄᴇssғᴜʟ: <code>{unsuccessful}</code></b>

<i>➪ Tᴏ sᴛᴏᴘ ᴛʜᴇ ʙʀᴏᴀᴅᴄᴀsᴛɪɴɢ ᴄʟɪᴄᴋ: <b>/cancel</b></i>"""
                await pls_wait.edit(status_update)
                last_update_percentage = percent_complete

        # Final status update
        final_status = f"""<b>{complete_msg}

<blockquote>Dᴏɴᴇ:</b> [{final_progress_bar}] {percent_complete:.0%}</blockquote>

<b>🚻 Tᴏᴛᴀʟ Usᴇʀs: <code>{total}</code>
✅ Sᴜᴄᴄᴇssғᴜʟ: <code>{successful}</code>
🚫 Bʟᴏᴄᴋᴇᴅ Usᴇʀs: <code>{blocked}</code>
⚠️ Dᴇʟᴇᴛᴇᴅ Aᴄᴄᴏᴜɴᴛs: <code>{deleted}</code>
❌ Uɴsᴜᴄᴄᴇssғᴜʟ: <code>{unsuccessful}</code></b>"""
        return await pls_wait.edit(final_status)

    else:
        msg = await message.reply(REPLY_ERROR)
        await asyncio.sleep(8)
        await msg.delete()


@Bot.on_message(filters.command('status') & filters.private & is_admin)
async def info(client: Bot, message: Message):   
    reply_markup = InlineKeyboardMarkup([[InlineKeyboardButton("Cʟᴏsᴇ ✖️", callback_data = "close")]])
    #msg = await client.send_message(chat_id=message.chat.id, text=WAIT_MSG)
    
    start_time = time.time()
    temp_msg = await message.reply("<b><i>Pʀᴏᴄᴇssɪɴɢ....</i></b>", quote=True)  # Temporary message
    end_time = time.time()
    # Calculate ping time in milliseconds
    ping_time = (end_time - start_time) * 1000
    
    users = await kingdb.full_userbase()
    now = datetime.now()
    delta = now - client.uptime
    bottime = get_readable_time(delta.seconds)
    
    await temp_msg.edit(f"🚻 : <b>{len(users)} USERS\n\n🤖 UPTIME » {bottime}\n\n📡 PING » {ping_time:.2f} ms</b>", reply_markup = reply_markup,)


@Bot.on_message(filters.command('cmd') & is_admin)
async def bcmd(bot: Bot, message: Message):        
    reply_markup = InlineKeyboardMarkup([[InlineKeyboardButton("Cʟᴏsᴇ ✖️", callback_data = "close")]])
    await message.reply(text=CMD_TXT, reply_markup = reply_markup, quote= True)
    
#-----------------------------------------------------------------------------------------------------------------------------------------------------------------------#    

#--------------------------------------------------------------[[NORMAL USER ACCESSIBLE COMMANDS]]----------------------------------------------------------------------#

@Bot.on_message(filters.command('forcesub') & filters.private & ~banUser)
async def fsub_commands(client: Client, message: Message):
    #@id = message.from_user.id
    #@if await ban_user_exist(id):
        #return #await message.reply(BAN_TXT)
    
    button = [[InlineKeyboardButton("Cʟᴏsᴇ ✖️", callback_data="close")]]
    await message.reply(text=FSUB_CMD_TXT, reply_markup=InlineKeyboardMarkup(button), quote=True)


@Bot.on_message(filters.command('users') & filters.private & ~banUser)
async def user_setting_commands(client: Client, message: Message):
    #id = message.from_user.id
    #if await ban_user_exist(id):
        #return #await message.reply(text=BAN_TXT, message_effect_id=5046589136895476101)

    button = [[InlineKeyboardButton("Cʟᴏsᴇ ✖️", callback_data="close")]]
    await message.reply(text=USER_CMD_TXT, reply_markup=InlineKeyboardMarkup(button), quote=True)

    
HELP = "https://graph.org//file/10f310dd6a7cb56ad7c0b.jpg"
@Bot.on_message(filters.command('help') & filters.private & ~banUser)
async def help(client: Client, message: Message):
        #id = message.from_user.id
        #banned_users = await get_ban_users()
        #if await ban_user_exist(id):
            #return await message.reply(text=BAN_TXT, message_effect_id=5046589136895476101)
            
        reply_markup = InlineKeyboardMarkup([[InlineKeyboardButton('𝘚𝘵𝘪𝘭𝘭 𝘩𝘢𝘷𝘦 𝘥𝘰𝘶𝘣𝘵𝘴, 𝘊𝘰𝘯𝘵𝘢𝘤𝘵 𝘈𝘥𝘮𝘪𝘯', url='https://t.me/Shidoteshika1')]]) 
        await message.reply_photo(
            photo= HELP,
            caption = HELP_TEXT.format(
                first = message.from_user.first_name,
                last = message.from_user.last_name,
                username = None if not message.from_user.username else '@' + message.from_user.username,
                mention = message.from_user.mention,
                id = message.from_user.id
            ),
            reply_markup = reply_markup,
            #quote = True
        )
