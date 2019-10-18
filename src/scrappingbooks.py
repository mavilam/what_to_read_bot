# -*- coding: utf-8 -*-

from bs4 import BeautifulSoup
import requests
import logging
import re
import json
import os

# Enable logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)

books_urls = {}
if os.path.exists('/app/static/book_sources.json'):
    with open('/app/static/book_sources.json') as json_data:
        books_urls = json.load(json_data)
else:
    with open('./static/book_sources.json') as json_data:
        books_urls = json.load(json_data)


LIMIT = 5

logger = logging.getLogger(__name__)

headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.13; rv:61.0) Gecko/20100101 Firefox/'}


def get_text(arg, vendor):
    return "Aqui estan los libros de " + arg + " mas leidos de la lista de " + vendor + " de esta semana: \n"


def scrap_books(vendor, type):
    if vendor == "Fnac":
        return result_scrapping_fnac(type)
    elif vendor == "Casa del libro":
        return result_scrapping_lcdl(type)
    elif vendor == "La Central":
        return result_scrapping_laCentral(type)


def result_scrapping_fnac(type_of_book):
    logger.info("Result scrapping fnac")
    text = get_text(type_of_book, "fnac")

    fnac_url = books_urls[f'Fnac|{type_of_book}']

    result = scrapping_fnac_chart(fnac_url, text) + " \n"
    return check_and_return_result(result)


def result_scrapping_lcdl(type_of_book):
    logger.info("Result scrapping lcdl")
    text = get_text(type_of_book, "La casa del libro")
    url_lcdl = books_urls[f'Casa del libro|{type_of_book}']

    result = scrapping_lcdl_chart(url_lcdl, text)
    return check_and_return_result(result)


def result_scrapping_laCentral(type_of_book):
    logger.info("Result scrapping laCentral")
    text = get_text(type_of_book, "La Central")

    url_laCentral = books_urls[f'La Central|{type_of_book}']

    result = scrapping_laCentral_chart(url_laCentral, text)
    return check_and_return_result(result)


def scrapping_fnac_chart(url, init_text):
    req = requests.get(url, headers=headers)

    status_code = req.status_code
    if status_code == 200:
        html = BeautifulSoup(req.text, "html.parser")
        entries = html.find_all('div', {'class': 'Article-infoContent'}, limit=LIMIT)
        text = init_text

        for i, entry in enumerate(entries):
            text = compose_fnac_text(entry, text, str(i + 1))

        return text
    else:
        logger.error("Status Code %d" % status_code)
        return None


def compose_fnac_text(entry, prev_text, number_of_book):
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


def scrapping_laCentral_chart(url, init_text):
    req = requests.get(url, headers=headers)
    status_code = req.status_code
    if status_code == 200:
        html = BeautifulSoup(req.text, "html.parser")

        ul = html.find_all('ul', {'class': 'resultList'})
        entry = ul[0]
        text = init_text

        books = entry.find_all('div', {'class': 'content'}, limit=LIMIT)

        for i, book in enumerate(books):
            text = compose_laCentral_text(book, text, str(i + 1))

        return text
    else:
        logger.error("Status Code %d" % status_code)
        return None


def compose_laCentral_text(book, prev_text, number_of_book):
    author = book.a.getText()
    title_html = str(book.span)
    title_str = re.sub(r'<(|/)span>', '', title_html)
    return f'{prev_text} \t {number_of_book} - {title_str} por {author} \n'


def scrapping_lcdl_chart(url, init_text):
    req = requests.get(url, headers=headers)

    status_code = req.status_code
    if status_code == 200:
        html = BeautifulSoup(req.text, "html.parser")

        entries = html.find_all('div', {'class': 'product__info'}, limit=LIMIT)

        text = init_text

        for i in range(len(entries)):
            text = compose_lcld_text(entries[i], text, str(i + 1))

        return text
    else:
        logger.error("Status Code %d" % status_code)
        return None


def compose_lcld_text(entry, prev_text, number_of_book):
    title_raw = entry.a.getText().lower().title()
    author_element = entry.find('span', {'class': 'author'})

    if author_element.a is not None:
        author_raw = author_element.a
    else:
        author_raw = author_element.span

    author = author_raw.getText().strip(' \t\n\r')
    title = title_raw.strip(' \t\n\r')
    return f'{prev_text} \t {number_of_book} -{title} por {author.title()} \n'


def check_and_return_result(result):
    if result is None:
        logger.error("There was an error scrapping")
        return "Lo siento, hubo un error"
    else:
        logger.info("Finished scrapping")
        return result
