# -*- coding: utf-8 -*-

from bs4 import BeautifulSoup
import requests
import logging

# Enable logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)

url_lcdl = "https://www.casadellibro.com/libros-mas-vendidos/20?gclid=Cj0KCQjwz_TMBRD0ARIsADfk7hSKfsQ-Ec1IyAu1AdZBNz994EIF6EAyB6FVaTRgWzdsoNMT9rDw0nMaAvQdEALw_wcB"
url_fiction = "https://www.fnac.es/n2433/Novela-de-Ciencia-Ficcion-y-Fantasy/Libros-mas-vendidos-Ciencia-Ficcion-y-Fantasy"
url_nonfiction = "https://www.fnac.es/c19449/No-ficcion"
url_laCentral = "https://www.lacentral.com/web/masvendidos/"

LCDL_FICTION = 0
LCDL_NOFICTION = 1

LACENTRAL_FICTION = 1
LACENTRAL_NOFICTION = 3

LIMIT = 5

logger = logging.getLogger(__name__)

headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.13; rv:61.0) Gecko/20100101 Firefox/'}


def get_text(arg, vendor):
    return "Aqui estan los libros de " + arg + " mas leidos de la lista de " + vendor + " de esta semana: \n"


def result_scrapping_fnac(type_of_book):
    logger.info("Result scrapping fnac")
    text = get_text(type_of_book, "fnac")

    fnac_url = get_fnac_url(type_of_book)

    result = scrapping_fnac_chart(fnac_url, text) + " \n"
    return checkAndReturnResult(result)


def result_scrapping_lcdl(type_of_book):
    logger.info("Result scrapping lcdl")
    text = get_text(type_of_book, "La casa del libro")
    lcdl_book_type = lcdl_type(type_of_book)

    result = scrapping_lcdl_chart(url_lcdl, text, lcdl_book_type)
    return checkAndReturnResult(result)


def result_scrapping_laCentral(type_of_book):
    logger.info("Result scrapping laCentral")
    text = get_text(type_of_book, "La Central")

    laCentral_book_type = laCentral_type(type_of_book)

    result = scrapping_laCentral_chart(url_laCentral, text, laCentral_book_type)
    return checkAndReturnResult(result)


def scrapping_fnac_chart(url, init_text):
    req = requests.get(url, headers=headers)

    status_code = req.status_code
    if status_code == 200:
        html = BeautifulSoup(req.text, "html.parser")

        entradas = html.find_all('li', {'class': 'clearfix Article-item js-ProductList'}, limit=LIMIT)

        text = init_text

        for i, entrada in enumerate(entradas):
            title = entrada.find('a', {'class': ' js-minifa-title'}).getText()
            author = entrada.find('p', {'class': 'Article-descSub'}).find('a')

            title_str = title.strip(' \t\n\r')

            text += "\t" + str(i + 1) + " -" + title_str
            if(author != None):
                author_str = author.getText().strip(' \t\n\r')
                text += " por " + author_str + " \n"
            else:
                text += " \n"

        return text
    else:
        logger.error("Status Code %d" % status_code)
        return None


def scrapping_laCentral_chart(url, init_text, laCentral_type):
    req = requests.get(url, headers=headers)
    status_code = req.status_code
    if status_code == 200:
        html = BeautifulSoup(req.text, "html.parser")

        entries = html.find_all('div', {'class': 'highlightBlack'})
        entry = entries[laCentral_type]
        text = init_text

        titles = entry.find_all('h4', limit=LIMIT)
        authors = entry.find_all('h5', limit=LIMIT)

        for i in range(len(authors)):
            text += "\t" + str(i + 1) + " -" + titles[i].find('a').getText() + " por " + authors[i].find('a').getText() + " \n"

        return text
    else:
        logger.error("Status Code %d" % status_code)
        return None


def scrapping_lcdl_chart(url, init_text, fiction_or_not):
    req = requests.get(url, headers=headers)

    status_code = req.status_code
    if status_code == 200:
        html = BeautifulSoup(req.text, "html.parser")

        entries = html.find_all('div', {'class': 'carousel-inner'})

        text = init_text
        entry = entries[fiction_or_not]
        titles = entry.find_all('a', {'class': 'title-link'}, limit=LIMIT)
        authors = entry.find_all('a', {'class': 'book-header-2-subtitle-author'}, limit=LIMIT)

        for i in range(len(authors)):
            text += "\t" + str(i + 1) + " -" + titles[i].getText().lower().title() + " por " + authors[i].getText().lower().title() + " \n"

        return text
    else:
        logger.error("Status Code %d" % status_code)
        return None


def lcdl_type(type_of_book):
    if type_of_book == "ficcion":
        return LCDL_FICTION
    else:
        return LCDL_NOFICTION

def laCentral_type(type_of_book):
    if type_of_book == "ficcion":
        return LACENTRAL_FICTION
    else:
        return LACENTRAL_NOFICTION


def get_fnac_url(type_of_book):
    if type_of_book == "ficcion":
        return url_fiction
    else:
        return url_nonfiction


def checkAndReturnResult(result):
    if result is None:
        logger.error("There was an error scrapping")
        return "Lo siento, hubo un error"
    else:
        logger.info("Finished scrapping")
        return result
