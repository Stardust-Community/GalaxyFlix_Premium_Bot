import asyncio
from pyrogram import Client, filters
from pyrogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton
from bot import Bot

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
	if store[0].startswith('EP') and store[1].startswith('S') and store[2]=='BTTH' and store[4]=='ESUB' and store[5]=='🜲':
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

	if store[0].startswith('EP') and store[1].startswith('S') and store[2]=='BTTH' and store[4]=='ESUB' and store[5]=='🜲':
		episode = store[0].removeprefix('EP')
		quality = store[3].removeprefix('(').removesuffix(')')
		season = store[1][1:]
		subs, c_4k, new_caption, hdint='', '', '', 1081
		link = f"https://t.me/btth480p/{message.id}"

		if store[6].lower() != '@btth480p.mkv':
			if store[6].upper() == "[FSP]":
				subs = "Falling Star Pavilion"
				if quality.lower()=='4k':
					c_4k="<b>4K(2160p) Compressed File</b>\n\n🔺ᴜsᴇ ᴍx/ᴠʟᴄ ᴘʟᴀʏᴇʀ ғᴏʀ\n🔻ᴇɴɢʟɪsʜ sᴜʙᴛɪᴛʟᴇs."
					await client.send_sticker(chat_id=BTTH, sticker = 'CAACAgUAAxkBAAJV5GYSuV-NfATO-wvJtgXjoAzWoZSuAALgCwAC3T7ZV0GHY7Qivb0JHgQ')

			else:
				subs = store[6].removeprefix('[').removesuffix(']')
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
