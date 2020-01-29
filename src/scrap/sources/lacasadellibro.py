# -*- coding: utf-8 -*-

from bs4 import BeautifulSoup
import logging

from src.utils import http_utils
from src.utils import response_utils

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)
logger = logging.getLogger(__name__)
LIMIT = 5


def result_scrapping(type_of_book, books_urls):
    logger.info("Result scrapping lcdl")
    text = response_utils.compose_main_response_text(type_of_book, "fnac")
    url_lcdl = books_urls[f'Casa del libro|{type_of_book}']

    return scrapping_chart(url_lcdl, text)


def scrapping_chart(url, init_text):
    result = http_utils.perform_get(url)
    if result is None:
        return "Ha ocurrido un error, inténtalo más tarde"

    html = BeautifulSoup(result, "html.parser")

    entries = html.find_all('div', {'class': 'product__info'}, limit=LIMIT)

    text = init_text

    for i in range(len(entries)):
        text = compose_text(entries[i], text, str(i + 1))

    return text


def compose_text(entry, prev_text, number_of_book):
    title_raw = entry.a.getText().lower().title()
    author_element = entry.find('div', {'class': 'author'})

    if author_element.a is not None:
        author_raw = author_element.a
    elif author_element.a is not None:
        author_raw = author_element.span
    else:
        author_raw = ''

    author = author_raw.getText().strip(' \t\n\r')
    title = title_raw.strip(' \t\n\r')
    return f'{prev_text} \t {number_of_book} - {title} por {author.title()} \n'
