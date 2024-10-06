# Don't Remove Credit @VJ_Botz
# Subscribe YouTube Channel For Amazing Bot @Tech_VJ
# Ask Doubt on telegram @KingVJ01

import re
from pyrogram import filters, Client, enums
from pyrogram.errors.exceptions.bad_request_400 import ChannelInvalid, UsernameInvalid, UsernameNotModified
from config import ADMINS, LOG_CHANNEL, PUBLIC_FILE_STORE, WEBSITE_URL, WEBSITE_URL_MODE
from plugins.database import unpack_new_file_id
from plugins.users_api import get_user, get_short_link
import re
import os
import json
import base64
import logging

# Don't Remove Credit Tg - @VJ_Botz
# Subscribe YouTube Channel For Amazing Bot https://youtube.com/@Tech_VJ
# Ask Doubt on telegram @KingVJ01

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

async def allowed(_, __, message):
    if PUBLIC_FILE_STORE:
        return True
    if message.from_user and message.from_user.id in ADMINS:
        return True
    return False

# Don't Remove Credit Tg - @VJ_Botz
# Subscribe YouTube Channel For Amazing Bot https://youtube.com/@Tech_VJ
# Ask Doubt on telegram @KingVJ01

@Client.on_message(filters.command(['link', 'plink']) & filters.create(allowed))
async def gen_link_s(bot, message):
    username = (await bot.get_me()).username
    replied = message.reply_to_message
    
    # Check if the user replied to a message
    if not replied:
        return await message.reply('Reply to a message to get a shareable link.')

    # Handle media replies
    if replied.media:
        file_type = replied.media
        if file_type not in [enums.MessageMediaType.VIDEO, enums.MessageMediaType.AUDIO, enums.MessageMediaType.DOCUMENT]:
            return await message.reply("**ʀᴇᴘʟʏ ᴛᴏ ᴀ sᴜᴘᴘᴏʀᴛᴇᴅ ᴍᴇᴅɪᴀ**")
        
        # Unpack the file ID and generate the share link
        file_id, ref = unpack_new_file_id((getattr(replied, file_type.value)).file_id)
        string = 'filep_' if message.text.lower().strip() == "/plink" else 'file_'
        string += file_id
        outstr = base64.urlsafe_b64encode(string.encode("ascii")).decode().strip("=")
    
    # Handle text replies
    elif replied.text:
        string = 'text_'
        string += base64.urlsafe_b64encode(replied.text.encode("ascii")).decode().strip("=")
        outstr = string

    else:
        return await message.reply("**ʀᴇᴘʟʏ ᴛᴏ ᴀ sᴜᴘᴘᴏʀᴛᴇᴅ ᴛᴇxᴛ ᴏʀ ᴍᴇᴅɪᴀ**")

    # Check if the message has protected content and the user is not an admin
    if message.has_protected_content and message.chat.id not in ADMINS:
        return await message.reply("okDa")

    user_id = message.from_user.id
    user = await get_user(user_id)
    
    # Generate the share link based on website URL mode
    if WEBSITE_URL_MODE == True:
        share_link = f"{WEBSITE_URL}?Tech_VJ={outstr}"
    else:
        share_link = f"https://t.me/{username}?start={outstr}"

    # Shorten the link if applicable
    if user["base_site"] and user["shortener_api"] is not None:
        short_link = await get_short_link(user, share_link)
        await message.reply(f"<b>⭕ ʜᴇʀᴇ ɪs ʏᴏᴜʀ ʟɪɴᴋ:\n\n🖇️ sʜᴏʀᴛ ʟɪɴᴋ :- {short_link}</b>")
    else:
        await message.reply(f"<b>⭕ ʜᴇʀᴇ ɪs ʏᴏᴜʀ ʟɪɴᴋ:\n\n🔗 ᴏʀɪɢɪɴᴀʟ ʟɪɴᴋ :- {share_link}</b>")
