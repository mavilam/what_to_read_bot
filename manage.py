# -*- coding: utf-8 -*-

from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, CallbackQueryHandler
from telegram import ReplyKeyboardMarkup, KeyboardButton

import scrappingbooks

import logging
import os


# Enable logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)

logger = logging.getLogger(__name__)

LCDL_FICTION = 0
LCDL_NOFICTION = 1


keyboard = [[KeyboardButton("Fnac ficcion", callback_data='AF'),
             KeyboardButton("Fnac no ficcion", callback_data='ANF')],
            [KeyboardButton("Casa del libro ficcion", callback_data='LCDLF'),
             KeyboardButton("Casa del libro no ficcion", callback_data='LCDLNF')],
            [KeyboardButton("La central ficcion", callback_data='LCF'),
             KeyboardButton("La central no ficcion", callback_data='LCF')]]


def get_books_fiction(bot, update):
    logger.info("Books fiction request")

    tag = "ficcion"
    scrappingbooks.result_scrapping_fnac(bot, update, tag)
    scrappingbooks.result_scrapping_lcdl(bot, update, tag)


def get_books_nonfiction(bot, update):
    logger.info("Books non fiction request")

    global url_nonfiction

    tag = "no ficcion"
    global url_lcdl
    scrappingbooks.result_scrapping_fnac(bot, update, tag)
    scrappingbooks.result_scrapping_lcdl(bot, update, tag)


def get_user_info(update):
    username = update.message.from_user.username
    if username is None:
        name = update.message.from_user.first_name
        id = update.message.from_user.id
        username = str(id) + ' ' + name

    return username


def reply_method(bot, update):
    button(bot, update)


def button(bot, update):
    query = update.message.text
    user = get_user_info(update)
    logger.info(user)
    result = ''
    if query == 'Fnac ficcion':
        logger.info("Fnac fiction")
        result = scrappingbooks.result_scrapping_fnac("ficcion")
    elif query == 'Fnac no ficcion':
        logger.info("Fnac non fiction")
        result = scrappingbooks.result_scrapping_fnac("no ficcion")
    elif query == 'LCDL ficcion' or query == 'Casa del libro ficcion':
        logger.info("La casa del libro fiction")
        result = scrappingbooks.result_scrapping_lcdl("ficcion")
    elif query == 'LCDL no ficcion' or query == 'Casa del libro no ficcion':
        logger.info("La casa del libro fiction")
        result = scrappingbooks.result_scrapping_lcdl("no ficcion")
    elif query == 'La central ficcion':
        logger.info("La central ficcion")
        result = scrappingbooks.result_scrapping_laCentral("ficcion")
    elif query == 'La central no ficcion':
        logger.info("La central no ficcion")
        result = scrappingbooks.result_scrapping_laCentral("no ficcion")
    else:
        result = "No te he entendido :("

    reply_markup = ReplyKeyboardMarkup(keyboard)
    bot.send_message(chat_id=update.message.chat_id, text=result, reply_markup=reply_markup)


def start(bot, update):
    reply_markup = ReplyKeyboardMarkup(keyboard)

    update.message.reply_text("Hola! soy WhatToReadBot, vengo a recomendarte que libros leer cada semana!",
                              reply_markup=reply_markup)


def error(bot, update, errormsg):
    logger.warning('Update "%s" caused error "%s"' % (update, errormsg))


def set_up_dispatcher_and_updater(token):
    updater = Updater(token=token)

    dispatcher = updater.dispatcher

    start_handler = CommandHandler("start", start)
    fiction_handler = CommandHandler("getbooksfiction", get_books_fiction)
    nonfiction_handler = CommandHandler("getbooksnonfiction", get_books_nonfiction)
    reply_handler = MessageHandler(Filters.text, reply_method)

    dispatcher.add_handler(CallbackQueryHandler(button))
    dispatcher.add_handler(start_handler)
    dispatcher.add_handler(fiction_handler)
    dispatcher.add_handler(nonfiction_handler)
    dispatcher.add_handler(reply_handler)

    # log all errors
    dispatcher.add_error_handler(error)

    # Start the Bot
    updater.start_polling()

    # Block until you press Ctrl-C or the process receives SIGINT, SIGTERM or
    # SIGABRT. This should be used most of the time, since start_polling() is
    # non-blocking and will stop the bot gracefully.
    updater.idle()


def main():
    logger.info('I\'m running now!')
    set_up_dispatcher_and_updater(os.getenv("TELEGRAM_TOKEN"))


if __name__ == '__main__':
    main()
