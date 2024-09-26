
from aiohttp import web
from plugins import web_server

import asyncio
import pyromod.listen
from pyrogram import Client
from pyrogram.enums import ParseMode
import sys
from datetime import datetime

from config import API_HASH, APP_ID, LOGGER, TG_BOT_TOKEN, TG_BOT_WORKERS, CHANNEL_ID, PORT, OWNER_ID

class Bot(Client):
    def __init__(self):
        super().__init__(
            name="Bot",
            api_hash=API_HASH,
            api_id=APP_ID,
            plugins={
                "root": "plugins"
            },
            workers=TG_BOT_WORKERS,
            bot_token=TG_BOT_TOKEN
        )
        self.LOGGER = LOGGER

    async def start(self):
        await super().start()
        bot_info = await self.get_me()
        self.name = bot_info.first_name
        self.username = bot_info.username
        self.uptime = datetime.now()
                
        try:
            db_channel = await self.get_chat(CHANNEL_ID)
            self.db_channel = db_channel
            test = await self.send_message(chat_id = db_channel.id, text = "Testing")
            await test.delete()
        except Exception as e:
            self.LOGGER(__name__).warning(e)
            self.LOGGER(__name__).warning(f"Make Sure bot is Admin in DB Channel, and Double check the CHANNEL_ID Value, Current Value {CHANNEL_ID}")
            self.LOGGER(__name__).info("Bot Stopped..")
            sys.exit()

        self.set_parse_mode(ParseMode.HTML)
        self.LOGGER(__name__).info(f"Aᴅ-RᴇǫFsᴜʙ-FS-BᴏᴛV𝟹 Mᴀᴅᴇ Bʏ ➪ @Shidoteshika1 [Tᴇʟᴇɢʀᴀᴍ Usᴇʀɴᴀᴍᴇ]")
        self.LOGGER(__name__).info(f"{self.name} Bot Running..!")
        self.LOGGER(__name__).info(f"OPERATION SUCCESSFULL ✅")
        #web-response
        app = web.AppRunner(await web_server())
        await app.setup()
        bind_address = "0.0.0.0"
        await web.TCPSite(app, bind_address, PORT).start()

        #s_msg = await self.send_message(chat_id = LOG_CHNL, text = f"<b>🤖 <a href='t.me/{self.username}'>{self.name}</a> bot Restarted...</b>", disable_web_page_preview=True)
        await self.send_message(OWNER_ID, text = f"<b><blockquote>🤖 Bᴏᴛ Rᴇsᴛᴀʀᴛᴇᴅ ♻️</blockquote></b>")
        #await asyncio.sleep(30)
        #await s_msg.delete()

    async def stop(self, *args):
        await super().stop()
        self.LOGGER(__name__).info(f"{self.name} Bot stopped.")
