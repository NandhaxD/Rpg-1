import os
import io
import sys
import traceback
import asyncio

from pyrogram import *
from pyrogram.types import *
from contextlib import *
from subprocess import getoutput as run

from Aasf import *
from Aasf.Database import *

async def aexec(code, client, message):
    exec(
        "async def __aexec(client, message): "
        + "".join(f"\n {l_}" for l_ in code.split("\n"))
    )
    return await locals()["__aexec"](client, message)

@app.on_message(filters.command("sh"))
def sh(_, m):
    if m.from_user.id in DEVS:
        code = m.text.replace(m.text.split(" ")[0], "")
        x = run(code)
        msg = m.reply_text(
            f"**SHELL**: `{code}`\n\n**OUTPUT**:\n`{x}`")
        if len(m.command) <2:
           msg.edit_caption("`Give A Command To Run...`")    
    else:
        return
   
@app.on_message(filters.user(DEVS) & filters.command("eval"))
async def eval(client, message):
    status_message = await message.reply_text("Processing ...")
    if len(message.command) <2:
        return await status_message.edit("`Give A Command To Run..`")
    cmd = message.text.split(" ", maxsplit=1)[1]

    reply_to_ = message
    if message.reply_to_message:
        reply_to_ = message.reply_to_message

    old_stderr = sys.stderr
    old_stdout = sys.stdout
    redirected_output = sys.stdout = io.StringIO()
    redirected_error = sys.stderr = io.StringIO()
    stdout, stderr, exc = None, None, None

    try:
        await aexec(cmd, client, message)
    except Exception:
        exc = traceback.format_exc()

    stdout = redirected_output.getvalue()
    stderr = redirected_error.getvalue()
    sys.stdout = old_stdout
    sys.stderr = old_stderr

    evaluation = ""
    if exc:
        evaluation = exc
    elif stderr:
        evaluation = stderr
    elif stdout:
        evaluation = stdout
    else:
        evaluation = "Success"

    final_output = "<b>EVAL</b>: "
    final_output += f"<code>{cmd}</code>\n\n"
    final_output += "<b>OUTPUT</b>:\n"
    final_output += f"<code>{evaluation.strip()}</code> \n"

    if len(final_output) > 4096:
        with io.BytesIO(str.encode(final_output)) as out_file:
            out_file.name = "eval.text"
            await reply_to_.reply_document(
                document=out_file, caption=cmd, disable_notification=True
            )
    else:
        await reply_to_.reply_text(final_output)
    await status_message.delete()

async def send_msg(user_id, message):
    try:
        await message.copy(chat_id=user_id)
    except FloodWait as e:
        await asyncio.sleep(e.x)
        return send_msg(user_id, message)
    except InputUserDeactivated:
        return 400, f"{user_id} : deactivated\n"
    except UserIsBlocked:
        return 400, f"{user_id} : blocked the bot\n"
    except PeerIdInvalid:
        return 400, f"{user_id} : user id invalid\n"
    except Exception:
        return 500, f"{user_id} : {traceback.format_exc()}\n"

@app.on_message(filters.command("broadcast") & filters.user(DEVS))
async def broadcast(_, message):
    if not message.reply_to_message:
        await message.reply_text("Reply To A Message To Broadcast It")
        return    
    exmsg = await message.reply_text("Started Broadcasting!")
    all_chats = (await get_chats()) or {}
    all_users = (await get_users()) or {}
    done_chats = 0
    done_users = 0
    failed_chats = 0
    failed_users = 0
    for chat in all_chats:
        try:
            await send_msg(chat, message.reply_to_message)
            done_chats += 1
            await asyncio.sleep(0.1)
        except Exception:
            pass
            failed_chats += 1

    for user in all_users:
        try:
            await send_msg(user, message.reply_to_message)
            done_users += 1
            await asyncio.sleep(0.1)
        except Exception:
            pass
            failed_users += 1
    if failed_users == 0 and failed_chats == 0:
        await exmsg.edit_text(
            f"**Done Broadcasted ✅**\n\n**Sent Message To** `{done_chats}` **Chats &** `{done_users}` **Users**",
        )
    else:
        await exmsg.edit_text(
            f"**Done Broadcasted ✅**\n\n**Sent Message To** `{done_chats}` **Chats &** `{done_users}` **Users**\n\n**Note:-** `Due To Some Issues Can't Able To Broadcast` `{failed_users}` **Users And** `{failed_chats}` **Chats**",
        )
