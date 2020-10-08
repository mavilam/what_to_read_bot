# -*- coding: utf-8 -*-

from bs4 import BeautifulSoup
import logging

from utils import http_utils
from utils import response_utils

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)
logger = logging.getLogger(__name__)
LIMIT = 8


def result_scrapping(type_of_book, books_urls):
    logger.info("Result scrapping fnac")
    text = response_utils.compose_main_response_text(type_of_book, "fnac")

    fnac_url = books_urls[f'Fnac|{type_of_book}']

    return scrapping_chart(fnac_url, text) + " \n"


def scrapping_chart(url, init_text):
    result = http_utils.perform_get(url)
    if result is None:
        return "Ha ocurrido un error, inténtalo más tarde"

    html = BeautifulSoup(result, "html.parser")
    entries = html.find_all('div', {'class': 'Article-infoContent'}, limit=(LIMIT + 3))
    filtered_entries = list(filter(lambda entry: (entry.find('p', {'class': 'Article-desc'}).find('a').getText() != ''), entries))
    text = init_text

    for i, entry in enumerate(filtered_entries):
        text = compose_text(entry, text, str(i + 1))

    return text


def compose_text(entry, prev_text, number_of_book):
    title = entry.find('p', {'class': 'Article-desc'}).find('a').getText()
    author = entry.find('p', {'class': 'Article-descSub'}).find('a')

    title_str = title.strip(' \t\n\r')

    text = f'{prev_text} \t {number_of_book} - {title_str}'
    if author is not None:
        author_str = author.getText().strip(' \t\n\r')
        text = f'{text} por {author_str} \n'
    else:
        text = f'{text} \n'
    return text
