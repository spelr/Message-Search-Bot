# (c) @AbirHasan2005
# I just made this for searching a channel message from inline.
# Maybe you can use this for something else.
# I first made this for @AHListBot ...
# Edit according to your use.

from configs import Config
from pyrogram import Client, filters, idle
from pyrogram.errors import QueryIdInvalid
from pyrogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton, InlineQuery, InlineQueryResultArticle, \
    InputTextMessageContent

# Bot Client for Inline Search
Bot = Client(
    session_name=Config.BOT_SESSION_NAME,
    api_id=Config.API_ID,
    api_hash=Config.API_HASH,
    bot_token=Config.BOT_TOKEN
)
# User Client for Searching in Channel.
User = Client(
    session_name=Config.USER_SESSION_STRING,
    api_id=Config.API_ID,
    api_hash=Config.API_HASH
)


@Bot.on_message(filters.private & filters.command("start"))
async def start_handler(_, event: Message):
    await event.reply_text(
        "مرحبا أنا بوت أبحث عن الرسائل!\n\n"
        "**Developer:** @AbirHasan2005\n"
        "**Demo Bot:** @AHListBot",
        reply_markup=InlineKeyboardMarkup([
            [InlineKeyboardButton("مجموعة الدعم", url="https://t.me/BotsArabic"),
             InlineKeyboardButton("قناة البوت", url="https://t.me/BotsListAR")],
            [InlineKeyboardButton("البحث المضمن", switch_inline_query_current_chat=""), InlineKeyboardButton("البحث في محادثة", switch_inline_query="")]
        ])
    )


@Bot.on_inline_query()
async def inline_handlers(_, event: InlineQuery):
    answers = list()
    # If Search Query is Empty
    if event.query == "":
        answers.append(
            InlineQueryResultArticle(
                title="يمكنك البحث بالمضمنة باستخدام هذا البوت",
                description="البحث في القناة عن جميع القوائم",
                input_message_content=InputTextMessageContent(
                    message_text="Using this Bot you can Search a Channel All Messages using this bot.\n\n"
                                 "Made by @BotsListAR",
                    disable_web_page_preview=True
                ),
                reply_markup=InlineKeyboardMarkup([
                    [InlineKeyboardButton("إبحث هنا", switch_inline_query_current_chat="")],
                    [InlineKeyboardButton("مجموعة الدعم", url="https://t.me/BotsArabic"),
                     InlineKeyboardButton("قناة البوت", url="https://t.me/BotsListAR")]
                ])
            )
        )
    # Search Channel Message using Search Query Words
    else:
        async for message in User.search_messages(chat_id=Config.CHANNEL_ID, limit=50, query=event.query):
            if message.text:
                answers.append(InlineQueryResultArticle(
                    title="{}".format(message.text.split("\n", 1)[0]),
                    description="{}".format(message.text.rsplit("\n", 1)[-1]),
                    reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("Search Again", switch_inline_query_current_chat="")]]),
                    input_message_content=InputTextMessageContent(
                        message_text=message.text.markdown,
                        parse_mode="markdown",
                        disable_web_page_preview=True
                    )
                ))
    try:
        await event.answer(
            results=answers,
            cache_time=0
        )
        print(f"[{Config.BOT_SESSION_NAME}] - Answered Successfully - {event.from_user.first_name}")
    except QueryIdInvalid:
        print(f"[{Config.BOT_SESSION_NAME}] - Failed to Answer - {event.from_user.first_name}")

# Start Clients
Bot.start()
User.start()
# Loop Clients till Disconnects
idle()
# After Disconnects,
# Stop Clients
Bot.stop()
User.stop()




