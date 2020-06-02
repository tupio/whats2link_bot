import logging
import os
import urllib.parse
import urllib.request

import telegram
from telegram.ext import Updater, InlineQueryHandler, CommandHandler, CommandHandler, MessageHandler, Filters, Updater
from telegram.utils.helpers import escape_markdown
from telegram import InlineKeyboardButton, InlineKeyboardMarkup, ParseMode, InputTextMessageContent
from telegram.error import (TelegramError, Unauthorized, BadRequest,
                            TimedOut, ChatMigrated, NetworkError)

TOKEN = "969636671:AAFMA4L8LSLXZm4aEln2lYWwVOdzQlKzNY8"
PRIVATE_ID = "355535470"

start_msg = "You can use this bot to generate *WhatsApp share links*.\nYou can find more information at [WhatsApp " \
            "FAQ](https://faq.whatsapp.com/en/android/26000030/).\n\n*Commands Available*\n" \
            "\n*Instructions*\nReply the required message with @whats2link-bot "

HOST = ''
PORT = int(os.environ.get('PORT', 5000))

# Enable logging
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)
logger = logging.getLogger(__name__)


def error_callback(bot, update, error):
    try:
        raise error
    except Unauthorized as e:
        bot.send_message(chat_id=PRIVATE_ID,
                         text="Unauthorised access," + e.message)
        # remove update.message.chat_id from conversation list
    except BadRequest as e:
        bot.send_message(chat_id=update.message.chat_id,
                         text="Sorry," + e.message)
        # handle malformed requests - read more below!
    except TimedOut:
        pass
        # handle slow connection problems
    except NetworkError:
        pass
        # handle other connection problems
    except ChatMigrated as e:
        pass
        # the chat_id of a group has changed, use e.new_chat_id instead
    except TelegramError:
        pass
        # handle all other telegram related errors


def message(update, context):
    context.bot.send_message(chat_id=update.effective_chat.id,
                             text="Here is your [Link.](https://api.whatsapp.com/send?phone=" + "&text=" + urllib.parse.quote(update.message.text)+")", parse_mode=ParseMode.MARKDOWN, reply_to_message_id=update.message.message_id)


def unknown(update, context):
    context.bot.send_message(chat_id=update.message.chat_id,
                             text="Sorry, I didn't understand that command.")


def start(update, context):
    context.bot.send_message(chat_id=update.message.chat_id, text=start_msg, parse_mode=telegram.ParseMode.MARKDOWN,
                             disable_web_page_preview=True)
    context.bot.send_message(chat_id=PRIVATE_ID, text="New user:`" + str(update.message.chat_id) + "`",
                             disable_notification=False,
                             parse_mode=telegram.ParseMode.MARKDOWN, disable_web_page_preview=True)


def main():
    updater = Updater(token=TOKEN, use_context=True)
    dispatcher = updater.dispatcher

    # Adding start command
    start_handler = CommandHandler('start', start)
    dispatcher.add_handler(start_handler)

    # Adding inline command
    messager = MessageHandler(Filters.all, message)
    dispatcher.add_handler(messager)

    # Handling unknown msgs
    unknown_handler = MessageHandler(Filters.command, unknown)
    dispatcher.add_handler(unknown_handler)

    # Start polling
    updater.start_webhook(listen="0.0.0.0",
                          port=PORT,
                          url_path=TOKEN)
    updater.bot.set_webhook("https://whats2link-bot.herokuapp.com/"+TOKEN)
    updater.idle()


if __name__ == '__main__':
    main()
