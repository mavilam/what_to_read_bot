# -*- coding: utf-8 -*-

from bs4 import BeautifulSoup
import logging
import re

from src.utils import http_utils
from src.utils import response_utils

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)
logger = logging.getLogger(__name__)
LIMIT = 5


def result_scrapping(type_of_book, books_urls):
    logger.info("Result scrapping laCentral")
    text = response_utils.compose_main_response_text(type_of_book, "fnac")

    url_laCentral = books_urls[f'La Central|{type_of_book}']

    return scrapping_chart(url_laCentral, text)


def scrapping_chart(url, init_text):
    result = http_utils.perform_get(url)
    if result is None:
        return "Ha ocurrido un error, inténtalo más tarde"

    html = BeautifulSoup(result, "html.parser")

    ul = html.find_all('ul', {'class': 'resultList'})
    entry = ul[0]
    text = init_text

    books = entry.find_all('div', {'class': 'content'}, limit=LIMIT)

    for i, book in enumerate(books):
        text = compose_text(book, text, str(i + 1))

    return text


def compose_text(book, prev_text, number_of_book):
    author = book.a.getText()
    title_html = str(book.span)
    title_str = re.sub(r'<(|/)span>', '', title_html)
    return f'{prev_text} \t {number_of_book} - {title_str} por {author} \n'

