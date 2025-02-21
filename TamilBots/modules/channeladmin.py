from asyncio.queues import QueueEmpty
from Cyber.config import que
from pyrogram import Client, filters
from pyrogram.types import Message

from Cyber.function.admins import set
from Cyber.helpers.channelmusic import get_chat_id
from Cyber.helpers.decorators import authorized_users_only, errors
from Cyber.helpers.filters import command, other_filters
from Cyber.services.callsmusic import callsmusic
from Cyber.services.queues import queues


@Client.on_message(filters.command(["channelpause","cpause"]) & filters.group & ~filters.edited)
@errors
@authorized_users_only
async def pause(_, message: Message):
    try:
      conchat = await _.get_chat(message.chat.id)
      conid = conchat.linked_chat.id
      chid = conid
    except:
      await message.reply("𝐈𝐬 𝐂𝐡𝐚𝐭 𝐄𝐯𝐞𝐧 𝐋𝐢𝐧𝐤𝐞𝐝...")
      return    
    chat_id = chid
    if (chat_id not in callsmusic.active_chats) or (
        callsmusic.active_chats[chat_id] == "paused"
    ):
        await message.reply_text("❗ 𝐍𝐨𝐭𝐡𝐢𝐧𝐠 𝐢𝐬 𝐩𝐥𝐚𝐲𝐢𝐧𝐠! ☹")
    else:
        callsmusic.pause(chat_id)
        await message.reply_text("▶️ 𝐏𝐚𝐮𝐬𝐞𝐝! 😑")


@Client.on_message(filters.command(["channelresume","cresume"]) & filters.group & ~filters.edited)
@errors
@authorized_users_only
async def resume(_, message: Message):
    try:
      conchat = await _.get_chat(message.chat.id)
      conid = conchat.linked_chat.id
      chid = conid
    except:
      await message.reply("𝐈𝐬 𝐂𝐡𝐚𝐭 𝐄𝐯𝐞𝐧 𝐋𝐢𝐧𝐤𝐞𝐝...")
      return    
    chat_id = chid
    if (chat_id not in callsmusic.active_chats) or (
        callsmusic.active_chats[chat_id] == "playing"
    ):
        await message.reply_text("❗ 𝐍𝐨𝐭𝐡𝐢𝐧𝐠 𝐢𝐬 𝐩𝐚𝐮𝐬𝐞𝐝! 😕")
    else:
        callsmusic.resume(chat_id)
        await message.reply_text("⏸ 𝐑𝐞𝐬𝐮𝐦𝐞𝐝! 😍")


@Client.on_message(filters.command(["channelend","cend"]) & filters.group & ~filters.edited)
@errors
@authorized_users_only
async def stop(_, message: Message):
    try:
      conchat = await _.get_chat(message.chat.id)
      conid = conchat.linked_chat.id
      chid = conid
    except:
      await message.reply("Is chat even linked")
      return    
    chat_id = chid
    if chat_id not in callsmusic.active_chats:
        await message.reply_text("❗ 𝐍𝐨𝐭𝐡𝐢𝐧𝐠 𝐢𝐬 𝐬𝐭𝐫𝐞𝐚𝐦𝐢𝐧𝐠! 😒")
    else:
        try:
            queues.clear(chat_id)
        except QueueEmpty:
            pass

        await callsmusic.stop(chat_id)
        await message.reply_text("❌ 𝐒𝐭𝐨𝐩𝐩𝐞𝐝 𝐒𝐭𝐫𝐞𝐚𝐦𝐢𝐧𝐠! 😶")


@Client.on_message(filters.command(["channelskip","cskip"]) & filters.group & ~filters.edited)
@errors
@authorized_users_only
async def skip(_, message: Message):
    global que
    try:
      conchat = await _.get_chat(message.chat.id)
      conid = conchat.linked_chat.id
      chid = conid
    except:
      await message.reply("Is chat even linked")
      return    
    chat_id = chid
    if chat_id not in callsmusic.active_chats:
        await message.reply_text("❗ 𝐍𝐨𝐭𝐡𝐢𝐧𝐠 𝐢𝐬 𝐩𝐥𝐚𝐲𝐢𝐧𝐠 𝐭𝐨 𝐬𝐤𝐢𝐩! 😒")
    else:
        queues.task_done(chat_id)

        if queues.is_empty(chat_id):
            await callsmusic.stop(chat_id)
        else:
            await callsmusic.set_stream(
                chat_id, 
                queues.get(chat_id)["file_path"]
            )

    qeue = que.get(chat_id)
    if qeue:
        skip = qeue.pop(0)
    if not qeue:
        return
    await message.reply_text(f"- Skipped **{skip[0]}**\n- Now Playing **{qeue[0][0]}**")


@Client.on_message(filters.command("channeladmincache"))
@errors
async def admincache(client, message: Message):
    try:
      conchat = await client.get_chat(message.chat.id)
      conid = conchat.linked_chat.id
      chid = conid
    except:
      await message.reply("Is chat even linked")
      return
    set(
        chid,
        [
            member.user
            for member in await conchat.linked_chat.get_members(filter="administrators")
        ],
    )
    await message.reply_text("✨ 𝐀𝐝𝐦𝐢𝐧 𝐂𝐚𝐜𝐡𝐞 𝐑𝐞𝐟𝐫𝐞𝐬𝐡𝐞𝐝! 🥰")
