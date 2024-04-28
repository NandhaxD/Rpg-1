import config

from nandha import *
from nandha.helpers.decorator import *
from datetime import *

from pyrogram import *
from pyrogram.types import *

app = bot
types = [{"text": "General", "info": "just genral quiz"}, {"text": "rare", "info": "uff rarest quiz"}]

@app.on_message(filters.command('request', prefixes=config.PREFIXES))
async def upload_data(_, message):
    if not message.chat.type == enums.ChatType.PRIVATE:
        return await message.reply_text("`Request Your Own Quiz On Dm`")
    else:
        buttons = []
        text = "**Choose Your Quiz Type: **\n\n"
        for x in types:
            buttons.append([InlineKeyboardButton(x["text"], callback_data=f"request:{x["text"]}")])
            text += f"• `{x["text"]` - `{x["info"]}`}\n"
        await message.reply_text(text, reply_markup=Inlinekeyboardmarkup(buttons))

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
