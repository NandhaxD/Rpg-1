import config

from nandha import *
from nandha.helpers.decorator import *
from datetime import *

from pyrogram import *
from pyrogram.types import *

app = bot
types = [{"text": "General", "info": "just genral quiz"}, {"text": "rare", "info": "uff rarest quiz"}]
requests = {}

@app.on_message(filters.command('request', prefixes=config.PREFIXES))
async def request(_, message):
    if m.chat.type != enums.ChatType.PRIVATE:
        return await m.reply_text("`Request Your Own Quiz On Dm`")
    else:
        if requests[m.from_user.id]:
            return await message.reply_text("`Already Creating Quiz Process Going On`")
        buttons = []
        text = "**Choose Your Quiz Type: **\n\n"
        for x in types:
            buttons.append([InlineKeyboardButton(x["text"], callback_data=f"request:{x['text']}")])
            buttons.append([InlineKeyboardButton("Cancel 🚫", callback_data=f"delete:{m.from_user.id}")])            
            text += f"• `{x['text']}` - `{x['info']}`\n"
        await m.reply_text(text, reply_markup=Inlinekeyboardmarkup(buttons))

@app.on_callback_query(filters.regex("delete"))
async def delete(_, cq):
    user_id = int(cq.data.split("_")[1])
    if cq.from_user.id != user_id:
        return await cq.answer("This Wasn't Requested By You")
    else:
        if requests[cq.from_user.id]:
            requests.pop(cq.from_user.id)
        await cq.message.delete()

@app.on_callback_query(filters.regex("request"))
async def request(_, cq):
    type = str(cq.data.split(":")[1])
    await cq.edit_text(f"**Alright You Choosed Quiz Type As** `{type}`\n\n`Wants To Cancel This Progress At Any Moment Send /cancel`")
    num = 0
    question = []
    options = []
    answer = []
    explain = []
    q = await cq.message.chat.ask(f"**Now Send Me Your Question For The Quiz**", filters=filters.text)
    if (q.text).split()[0] == "/cancel":
        await q.sent_message.edit_text("`Process Cancelled ✅`")
        exit()
    question.append(q.text)
    await q.sent_message.delete()
    while num < 4:
        num += 1
        op = await cq.message.chat.ask(f"**Now Send Me Your Option {num} For The Quiz**\n\n`There Should 4 Options`", filters=filters.text)
        if (oq.text).split()[0] == "/cancel":
            await oq.sent_message.edit_text("`Process Cancelled ✅`")
            exit()
        options.append(op.text)
        await op.sent_message.delete()

    ans = await cq.message.chat.ask(f"**Now Tell Me Which Option Is The Corect One**\n\n`Note:- Send Your Option As Digit Like If Option 1 is correct send 1`", filters=filters.text)
    if (ans.text).split()[0] == "/cancel":
        await ans.sent_message.edit_text("`Process Cancelled ✅`")
        exit()
    while not ans.text.isdigit() or int(ans.text) > 4 or int(ans.text) == 0 and not (ans.text).split()[0] == "/cancel": # if ans text == /cancel the process should be cancelled 
        ans = await cq.message.chat.ask(f"**Now Tell Me Which Option Is The Corect One**\n\n`Note:- Send Your Option As Digit Like If Option 1 is correct send 1`", filters=filters.text)
    answer.append(int(ans.text))

    ex = await cq.message.chat.ask(f"**Now Give Me A Explanation For The Quiz**", filters=filters.text)
    if (ex.text).split()[0] == "/cancel":
        await ex.sent_message.edit_text("`Process Cancelled ✅`")
        exit()
    explain.append(ex.text)
    await ex.sent_message.delete()

    text = f"**Question**: `{question[0]}`**:-**\n\n"
    text += f"**• Type:** `{type}`\n"
    ops = 1
    for x in options:
        text += f"**• Option {ops}**: `{x}`"
        ops += 1
    text += f"\n**• Answer:** `{options[answer[0] - 1]}`"
    text += f"\n**• Explanation:** `{explain[0]}`"
    keyboard = [[
        InlineKeyboardButton("Confirm ✅", callback_data=f"review:{cq.from_user.id}"),
        InlineKeyboardButton("Cancel 🚫", callback_data=f"delete:{cq.from_user.id}")
    ]]

    await bot.send_poll(
        chat_id=cq.from_user.id,
        question=question[0],
        options=[options[0], options[1], options[2], options[3]],
        explanation=explain[0],
        correct_option_id=int(answer[0]),
        close_date=close_t,
        type=enums.PollType.QUIZ,
        is_anonymous=False
    )
    await bot.send_message(cq.from_user.id, text, reply_markup=Inlinekeyboardmarkup(keyboard))
    requests[cq.from_user.id] = {"question": question[0], "type": type, "options": options, "explanation": explain[0], "answer": int(answer[0])}
    
"""
    # /upload -q {question} -1 {option1} -2 {option2} -3 {option3} -4 {option4} -a {answer}
    try:
        text = format_data(message.text)
    except IndexError:
        return await message.reply(
            "Invalid message format. Please use the format #q question #1 option1 #2 option2 #3 option3 #4 option4 #e text #a num"
        )
    button = [[
       types.InlineKeyboardButton(
          text='Save ✅', callback_data=f'save:{user_id}')
    ]]
    msg = await bot.send_message(chat_id=config.GROUP_ID,
        text=f'''\n
Type: {text[0]}   

Question: {text[1]}
Option1: {text[2]}
Option2: {text[3]}
Option3: {text[4]}
Option4: {text[5]}
Explain: {text[6]}
Answer: {text[7]}

Question Uploaded by {mention}
        ''', reply_markup=types.InlineKeyboardMarkup(button))
    await message.reply(
       f'Thank you for participating, here you can see your post: {msg.link}'
    )
    close_t = datetime.now() + timedelta(seconds=60)
    explain = text[6]
    question = text[1]
    option1 = text[2]
    option2 = text[3]
    option3 = text[4]
    option4 = text[5]
    answer = int(text[7])
    if bool(await bot.send_poll(
        chat_id=config.GROUP_ID,
        question=question,
        options=[option1, option2, option3, option4],
        explanation=explain,
        correct_option_id=answer,
        close_date=close_t,
        type=enums.PollType.QUIZ,
        is_anonymous=False
    )):
       if user_id in data:
          data[user_id].append(text)
       else:
          data[user_id] = [text]
    return await message.reply(data)
"""
