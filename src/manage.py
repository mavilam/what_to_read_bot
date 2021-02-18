# -*- coding: utf-8 -*-

from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, CallbackQueryHandler
from telegram import ReplyKeyboardMarkup, KeyboardButton

from src.scrap import scrappingbooks

import logging
import os

webhook_base_url = 'https://whattoreadbot.herokuapp.com/'

# Enable logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)

logger = logging.getLogger(__name__)


types_of_books = ["Más vendidos", "Ficcion y fantasía", "Policiaca/Terror",
                  "Histórica", "Romántica", "Juvenil"]

defaultKeyboard = [[KeyboardButton(types_of_books[i]), KeyboardButton(types_of_books[i + 1])] for i in range(0, len(types_of_books), 2)]


def get_books_fiction(bot, update):
    logger.info("Books fiction request")

    tag = "ficcion"
    scrappingbooks.result_scrapping_fnac(tag)
    scrappingbooks.result_scrapping_lcdl(tag)


def get_books_nonfiction(bot, update):
    logger.info("Books non fiction request")

    global url_nonfiction

    tag = "no ficcion"
    global url_lcdl
    scrappingbooks.result_scrapping_fnac(tag)
    scrappingbooks.result_scrapping_lcdl(tag)


def get_user_info(update):
    username = update.message.from_user.username
    if username is None:
        name = update.message.from_user.first_name
        id = update.message.from_user.id
        username = str(id) + ' ' + name

    return username


def reply_method(bot, update):
    query = update.message.text
    user = get_user_info(update)
    logger.info(user)
    result = ''
    reply_markup = None
    if "|" in query:
        vendor_and_type = query.split("|")
        result = scrappingbooks.scrap_books(vendor_and_type[0], vendor_and_type[1])
    elif query == "🔙":
        result = 'Volvemos a atrás ¿Qué tipo de libros quieres?'
        reply_markup = ReplyKeyboardMarkup(defaultKeyboard)
    elif query in types_of_books:
        result = '¿Qué fuente de libros quieres?'
        reply_markup = ReplyKeyboardMarkup(compose_keyboard(query))
    elif query not in types_of_books:
        result = 'Puede que esté en mi última versión o que no hayas pulsado en tipo de libro del teclado 🤔. Prueba otra vez por favor'
        reply_markup = ReplyKeyboardMarkup(defaultKeyboard)

    send_bot_response(bot, update, result, reply_markup)


def compose_keyboard(type_of_book):
    return [[KeyboardButton(f'Fnac|{type_of_book}', callback_data='bestsellers')],
            [KeyboardButton(f'Casa del libro|{type_of_book}', callback_data='black')],
            [KeyboardButton(f'La Central|{type_of_book}', callback_data='black')],
            [KeyboardButton(f'Amazon|{type_of_book}', callback_data='black')],
            [KeyboardButton("🔙", callback_data='back')]]


def send_bot_response(bot, update, text, keyboard):
    if keyboard is None:
        bot.send_message(chat_id=update.message.chat_id, text=text, parse_mode="HTML")
    else:
        bot.send_message(chat_id=update.message.chat_id, text=text, reply_markup=keyboard, parse_mode="HTML")


def start(bot, update):
    reply_markup = ReplyKeyboardMarkup(defaultKeyboard)

    update.message.reply_text("Hola! soy WhatToReadBot, vengo a recomendarte que libros leer cada semana!",
                              reply_markup=reply_markup)


def error(bot, update, errormsg):
    logger.warning('Update "%s" caused error "%s"' % (update, errormsg))
    text = 'Ups parece que he tenido un error interno 😖'
    bot.send_message(chat_id=update.message.chat_id, text=text, parse_mode="HTML")


def set_up_dispatcher_and_updater(token):
    updater = Updater(token=token)
    port = int(os.environ.get('PORT', '8443'))

    dispatcher = updater.dispatcher

    start_handler = CommandHandler("start", start)
    fiction_handler = CommandHandler("getbooksfiction", get_books_fiction)
    nonfiction_handler = CommandHandler("getbooksnonfiction", get_books_nonfiction)
    reply_handler = MessageHandler(Filters.text, reply_method)

    dispatcher.add_handler(CallbackQueryHandler(reply_method))
    dispatcher.add_handler(start_handler)
    dispatcher.add_handler(fiction_handler)
    dispatcher.add_handler(nonfiction_handler)
    dispatcher.add_handler(reply_handler)

    dispatcher.add_error_handler(error)

    updater.start_webhook(listen="0.0.0.0", port=port, url_path=token)
    updater.bot.set_webhook(f'{webhook_base_url}{token}')

    updater.idle()


def main():
    logger.info('I\'m running now!')
    set_up_dispatcher_and_updater(os.getenv("TELEGRAM_TOKEN"))


if __name__ == '__main__':
    main()
