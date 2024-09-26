
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
from database.database import * 
import subprocess
import sys
from plugins.advance_features import convert_time, auto_del_notification, delete_message
from plugins.FORMATS import START_MSG, FORCE_MSG, BAN_TXT

@Bot.on_message(filters.command('start') & filters.private & subscribed & ~banUser)
async def start_command(client: Client, message: Message): 
    await message.reply_chat_action(ChatAction.CHOOSE_STICKER)
    id = message.from_user.id  
    
    #banned_users = await get_ban_users()
    #if await ban_user_exist(id):
        #return await message.reply(text=BAN_TXT, message_effect_id=5046589136895476101)
    
    if not await present_user(id):
        try:
            await add_user(id)
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
            
        AUTO_DEL = await get_auto_delete(); DEL_TIMER = await get_del_timer()
        HIDE_CAPTION = await get_hide_caption(); CHNL_BTN = await get_channel_button(); PROTECT_MODE = await get_protect_content()   
            
        if CHNL_BTN:
            button_name, button_link = await get_channel_button_link()
            
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
    #if await ban_user_exist(user_id):
        #return await message.reply(text=BAN_TXT, message_effect_id=5046589136895476101)
	    
    
    excl = '! '
        
    #banned_users = await get_ban_users()
    #if user_id in banned_users:
        #return await temp.edit(BAN_TXT)
               
    channels = await get_all_channels()
    buttons = []
    count = 0

    try:
        for id in channels:
            if not await is_userJoin(client, user_id, id):
                try:
                    data = await client.get_chat(id)
                    link = data.invite_link 
                    cname = data.title
                                                
                    if not link:
                        await client.export_chat_invite_link(id)
                        link = (await client.get_chat(id)).invite_link 
                                                        
                    buttons.append([InlineKeyboardButton(text=cname, url=link)])
                    count += 1
                    await temp.edit(f'<b>{excl*count}</b>')
                                                
                except Exception as e:
                    print(f"Can't Export Channel Name and Link..., Please Check If the Bot is admin in the FORCE SUB CHANNELS:\nProvided Force sub Channel:- {id}")
                    return await temp.edit(f"<blockquote><b><i>! Eʀʀᴏʀ, Cᴏɴᴛᴀᴄᴛ ᴅᴇᴠᴇʟᴏᴘᴇʀ ᴛᴏ sᴏʟᴠᴇ ᴛʜᴇ ɪssᴜᴇs @Shidoteshika1</i></b></blockquote>\n\n<blockquote><b>Rᴇᴀsᴏɴ:</b> {e}</blockquote>")

        try:
            buttons.append([InlineKeyboardButton(text='♻️ Tʀʏ Aɢᴀɪɴ', url=f"https://t.me/{client.username}?start={message.command[1]}")])
        except IndexError:
            pass
                        
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



#import asyncio
#from pyrogram import Client, filters
#from pyrogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton
#from bot import Bot

#=====================================================================================##
#=====================================================================================##
#=====================================================================================##
#=====================================================================================##

BTTH = -1001602389428; CHIDORI = -1002012128164; BTTHAXIN = -1002231690719

# #@Bot.on_message(filters.text & filters.chat(BTTHAXIN))
# #async def AxinText(client, message):
# 	name = message.text
# 	store = name.split();
# 	if store[0] == '🔴' and store[1] == 'Season' and store[2].isdigit() and store[3] == '|' and store[4] == 'Episode' and store[5].isdigit() :
# 		lepisode = int(store[5])+1
# 		newName = f'<b>🔴 Season 05 | Episode {lepisode}</b>'
# 		link = f"https://t.me/BTTH_EngSub_AnimeXin/{message.id}"
# 		#sendFormat = f"""<b>Battle Through The Heavens 

# #Season 05 ➪ EPISODE {lepisode}

# #<blockquote>‣ Eng-Sub By AnimeXin | Multiple Quality</blockquote></b>"""
# 		#sendButton = [[InlineKeyboardButton(f'Watch Episode {lepisode}', url = link)]]

# 		await client.edit_message_text(chat_id = BTTHAXIN, message_id = message.id, text = newName)
# 		#await client.send_photo(BTTH, photo = 'https://telegra.ph/file/91e0323437f14c76f9223.jpg', caption = sendFormat, reply_markup = InlineKeyboardMarkup(sendButton))

@Bot.on_message(filters.document & filters.chat(-1002184292114))
async def HeavensWork(client, message):
	file_name = message.document.file_name
	store = file_name.split()
	if store[6].startswith('[') and store[6].endswith(']'):
		link = "https://t.me/BTTH480P"
		if store[6].upper() == "[FSP]":
			esub = f"<a href = {link}>Falling Star Pavilion</a>"
		else:
			esub = f"<a href = {link}>{store[6].removeprefix('[').removesuffix(']')}</a>"

		new_caption = f"<blockquote><b>ESUB BY: {esub}</b></blockquote>"
		#new_caption = f'<b>Episode {episode} | Season {season}\n<a href={link}>Battle Through The Heavens</a>\n\n<blockquote>BY: {subs}</blockquote></b>'
		await client.edit_message_caption(chat_id=-1002184292114, message_id = message.id, caption=new_caption)


@Bot.on_message(filters.document & filters.chat(BTTHAXIN))
async def Axin(client, message):
	file_name = message.document.file_name
	store = file_name.split()
	if store[0].startswith('EP') and store[1].startswith('S') and store[2]=='BTTH' and store[4]=='ESUB' and store[7].lower()=='@btth480p.mkv':
		episode = store[0].removeprefix('EP'); season = store[1][1:]; quality = store[3].removeprefix('(').removesuffix(')')
		link = f"https://t.me/BTTH_EngSub_AnimeXin/{message.id}"; subs = store[6][1:-1]
		if quality == '1080p' :
			await client.send_sticker(chat_id=BTTHAXIN, sticker = 'CAACAgUAAxkBAAJV5GYSuV-NfATO-wvJtgXjoAzWoZSuAALgCwAC3T7ZV0GHY7Qivb0JHgQ')
		new_caption = f'<b>Episode {episode} | Season {season}\n<a href={link}>Battle Through The Heavens</a>\n\n<blockquote>ESUB BY: <a href = {link}>{subs}</a></blockquote></b>'
		await client.edit_message_caption(chat_id=BTTHAXIN, message_id = message.id, caption=new_caption)

@Bot.on_message(filters.document & filters.chat(BTTH))
async def handle_document(client: Client, message: Message):
	file_name = message.document.file_name
	store = file_name.split()

	if store[0].startswith('EP') and store[1].startswith('S') and store[2]=='BTTH' and store[4]=='ESUB' and store[6]=='王':
		episode = store[0].removeprefix('EP')
		quality = store[3].removeprefix('(').removesuffix(')')
		season = store[1][1:]
		subs, c_4k, new_caption, hdint='', '', '', 1081
		link = f"https://t.me/btth480p/{message.id}"

		if store[5].lower() != '@btth480p.mkv':
			if store[5].upper() == "[FSP]":
				subs = "Falling Star Pavilion"
				if quality.lower()=='4k':
					c_4k="<b>4K(2160p) Compressed File</b>\n\n🔺ᴜsᴇ ᴍx/ᴠʟᴄ ᴘʟᴀʏᴇʀ ғᴏʀ\n🔻ᴇɴɢʟɪsʜ sᴜʙᴛɪᴛʟᴇs."
					await client.send_sticker(chat_id=BTTH, sticker = 'CAACAgUAAxkBAAJV5GYSuV-NfATO-wvJtgXjoAzWoZSuAALgCwAC3T7ZV0GHY7Qivb0JHgQ')

			else:
				subs = 'MyanimeLive'#store[5].removeprefix('[').removesuffix(']')
		else:
			subs='UNKNOWN'

		if c_4k:
			new_caption = f'<b>Episode {episode} | Season {season}\n<a href={link}>Battle Through The Heavens</a></b>\n\n{c_4k}\n\n<b><blockquote>ESUB BY: <a href={link}>{subs}</a></blockquote></b>'
		else:
			new_caption = f'<b>Episode {episode} | Season {season}\n<a href={link}>Battle Through The Heavens</a>\n\n<blockquote>ESUB BY: <a href={link}>{subs}</a></blockquote></b>'

		await client.edit_message_caption(chat_id=BTTH, message_id = message.id, caption=new_caption)


@Bot.on_message(filters.video & filters.chat(BTTH))
async def handle_video(client: Client, message: Message):
    video = message.video
    file_name = video.file_name if video.file_name else 'Unnamed video'
    store = file_name.split()
    if len(store)==10 and (store[9]== '@BTTH480P.mp4' or store[9]== '@BTTH480P.mkv'):
        #if store[7]=='1080P':
            #await client.send_sticker(chat_id=BTTH, sticker = 'CAACAgUAAxkBAAJt_2ZZ4dg3zAPATULBZepvg0Iv-N9DAAKmDAACMl7ZV4Yg8mRtJQglHgQ')   
        new_caption = f"<b>{video.file_name[:-4]}</b>"
        await client.edit_message_caption(chat_id=BTTH, message_id=message.id, caption=new_caption)
    #new_caption = f'Video received: {file_name}'

@Bot.on_message(filters.photo & filters.chat(BTTH))
async def photo_handler(client: Client, message: Message):
    photo_caption = message.caption
    store = photo_caption.split()
    if store[0] == '🔴' and store[1] == 'Season' and store[3] == '➪' and store[4] == 'EPISODE':
        link = f"https://t.me/btth480p/{message.id}"
        episode = int(store[5])
        new_caption = f"<b>🔴 Season 05 ➪ EPISODE {episode+1}\n\n‣ ENG-SUB | MULTIPLE QUALITY\n<blockquote>Dᴏᴡɴʟᴏᴀᴅ Sᴏᴜʀᴄᴇ :</b> Mʏᴀɴɪᴍᴇʟɪᴠᴇ, Fᴀʟʟɪɴɢ sᴛᴀʀ ᴘᴀᴠɪʟɪᴏɴ</blockquote>\n\n<i>🌟 Battle Through The Heavens</i>"
        await client.edit_message_caption(chat_id=BTTH, message_id=message.id, caption=new_caption, reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton(f"Download Episode {episode+1}",url=link)]]))
        await client.send_sticker(chat_id=BTTH, sticker = 'CAACAgUAAxkBAAJV5GYSuV-NfATO-wvJtgXjoAzWoZSuAALgCwAC3T7ZV0GHY7Qivb0JHgQ')
        await client.pin_chat_message(chat_id=BTTH, message_id=message.id, disable_notification=False)

        chidori_format = f"""<b>Battle Through The Heavens
──────────────────────
<blockquote>‣ Season: 05
‣ Episode: {episode+1}
‣ Quality:  Multi [English Sub]</blockquote>
──────────────────────
@UCHIHA_X_CLAN</b>"""
        await client.send_photo(chat_id=CHIDORI, photo="https://telegra.ph/file/1a2d93181bdb692229b9d.jpg", caption=chidori_format, reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("Download",url=link)]]))
                    


