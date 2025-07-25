# Don't Remove Credit Tg - @VJ_Botz
# Subscribe YouTube Channel For Amazing Bot https://youtube.com/@Tech_VJ
# Ask Doubt on telegram @KingVJ01

import os
import re
import sys
import json
import time
import asyncio
import requests
import subprocess

import core as helper
from utils import progress_bar
from vars import API_ID, API_HASH, BOT_TOKEN
from aiohttp import ClientSession
from pyrogram import Client, filters
from pyrogram.types import Message
from pyrogram.errors import FloodWait
from subprocess import getstatusoutput

# ENV variables
TXT_FILE_URL = os.environ.get("TXT_FILE_URL")  # Public link to your txt file
START_INDEX = int(os.environ.get("START_INDEX", 1))
BATCH_NAME = os.environ.get("BATCH_NAME", "DefaultBatch")
RESOLUTION = os.environ.get("RESOLUTION", "360")
CAPTION = os.environ.get("CAPTION", "")
THUMB_URL = os.environ.get("THUMB_URL", "no")

bot = Client("bot", api_id=API_ID, api_hash=API_HASH, bot_token=BOT_TOKEN)


@bot.on_message(filters.command("start"))
async def start_cmd(_, m: Message):
    await m.reply_text("Bot is alive and ready!")


@bot.on_message(filters.command("upload"))
async def upload_cmd(_, m: Message):
    msg = await m.reply("⏬ Starting Upload Process...")

    # Download .txt from remote URL
    r = requests.get(TXT_FILE_URL)
    if r.status_code != 200:
        return await msg.edit("❌ Failed to fetch the TXT file.")

    content = r.text.strip().split("\n")
    links = [i.split("://", 1) for i in content if "://" in i]
    await msg.edit(f"✅ Found {len(links)} links. Starting from index {START_INDEX}.")

    # Resolution mapping
    res_map = {
        "144": "256x144", "240": "426x240", "360": "640x360",
        "480": "854x480", "720": "1280x720", "1080": "1920x1080"
    }
    resolution_str = res_map.get(RESOLUTION, "UN")
    count = START_INDEX

    # Handle thumbnail
    if THUMB_URL.startswith("http"):
        getstatusoutput(f"wget '{THUMB_URL}' -O 'thumb.jpg'")
        thumb = "thumb.jpg"
    else:
        thumb = None

    for i in range(count - 1, len(links)):
        try:
            name_part, raw_url = links[i]
            url = "https://" + raw_url.replace("file/d/", "uc?export=download&id=")
            name = f"{str(count).zfill(3)}) {name_part.strip()[:60]}"
            ytf = f"b[height<={RESOLUTION}][ext=mp4]/bv[height<={RESOLUTION}]+ba[ext=m4a]"

            caption = f"**[📽️] Vid_ID:** {count:03}. {name_part.strip()} {CAPTION}\n**Batch** » **{BATCH_NAME}**"
            filename = f"{name}.mp4"
            cmd = f'yt-dlp -f "{ytf}" "{url}" -o "{filename}"'

            await msg.edit(f"⬇️ Downloading `{name}`...")
            os.system(cmd)

            await bot.send_video(m.chat.id, filename, caption=caption, thumb=thumb)
            os.remove(filename)
            count += 1
            time.sleep(1)

        except FloodWait as e:
            await asyncio.sleep(e.x)
        except Exception as e:
            await m.reply_text(f"❌ Failed to download `{name}`\n{str(e)}")
            continue

    await msg.edit("✅ All done!")


bot.run()
