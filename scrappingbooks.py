# -*- coding: utf-8 -*-

from bs4 import BeautifulSoup
import requests
import logging
import re

# Enable logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)
books_urls = {
    "Fnac|Más vendidos": "https://www.fnac.es/c19449/No-ficcion",
    "Fnac|Ficcion y fantasía": "https://www.fnac.es/n2433/Novela-de-Ciencia-Ficcion-y-Fantasy/Libros-mas-vendidos-Ciencia-Ficcion-y-Fantasy",
    "Fnac|Policiaca/Terror": "https://www.fnac.es/n2386/Novela-policiaca-y-terror/Libros-mas-vendidos-Policiaca-Terror#bl=LINovela-polic%C3%ADaca-y-terrorARBO",
    "Fnac|Histórica": "https://www.fnac.es/n2427/Novela-historica-y-de-aventuras/Libros-mas-vendidos-novela-historica#bl=LINovela-hist%C3%B3rica-y-de-aventurasARBO",
    "Fnac|Romántica": "https://www.fnac.es/n110830/Novela-romantica/Destacados#bl=LINovela-rom%C3%A1nticaARBO",
    "Fnac|Juvenil": "https://www.fnac.es/n105348/Literatura-juvenil/Destacados#bl=LILiteratura-juvenilARBO",
    "Casa del libro|Más vendidos": "https://www.casadellibro.com/libros-mas-vendidos/20?gclid=Cj0KCQjwz_TMBRD0ARIsADfk7hSKfsQ-Ec1IyAu1AdZBNz994EIF6EAyB6FVaTRgWzdsoNMT9rDw0nMaAvQdEALw_wcB",
    "Casa del libro|Ficcion y fantasía": "https://www.casadellibro.com/libros/literatura/generos-literarios/narrativa-de-ciencia-ficcion/121004001",
    "Casa del libro|Policiaca/Terror": "https://www.casadellibro.com/libros/literatura/generos-literarios/narrativa-de-terror/121004003",
    "Casa del libro|Histórica": "https://www.casadellibro.com/libros/narrativa-historica/125000000",
    "Casa del libro|Romántica": "https://www.casadellibro.com/libros/romantica-y-erotica/narrativa-romantica/127000000",
    "Casa del libro|Juvenil": "https://www.casadellibro.com/libros/juvenil/117001014",
    "La Central|Más vendidos": "https://www.lacentral.com/materias/?novedades=LGB",
    "La Central|Ficcion y fantasía": "https://www.lacentral.com/materias/?novedades=LGF",
    "La Central|Policiaca/Terror": "https://www.lacentral.com/materias/?novedades=LGN",
    "La Central|Histórica": "https://www.lacentral.com/materias/?novedades=LGH",
    "La Central|Romántica": "https://www.lacentral.com/materias/?novedades=LGE",
    "La Central|Juvenil": "https://www.lacentral.com/web/materias/?novedades=UJ"
}


url_laCentral = "https://www.lacentral.com/web/masvendidos/"

LACENTRAL_FICTION = 1
LACENTRAL_NOFICTION = 3

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
    return checkAndReturnResult(result)


def result_scrapping_lcdl(type_of_book):
    logger.info("Result scrapping lcdl")
    text = get_text(type_of_book, "La casa del libro")
    url_lcdl = books_urls[f'Casa del libro|{type_of_book}']

    result = scrapping_lcdl_chart(url_lcdl, text)
    return checkAndReturnResult(result)


def result_scrapping_laCentral(type_of_book):
    logger.info("Result scrapping laCentral")
    text = get_text(type_of_book, "La Central")

    url_laCentral = books_urls[f'La Central|{type_of_book}']

    result = scrapping_laCentral_chart(url_laCentral, text)
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
            if author != None:
                author_str = author.getText().strip(' \t\n\r')
                text += " por " + author_str + " \n"
            else:
                text += " \n"

        return text
    else:
        logger.error("Status Code %d" % status_code)
        return None


def scrapping_laCentral_chart(url, init_text):
    req = requests.get(url, headers=headers)
    status_code = req.status_code
    if status_code == 200:
        html = BeautifulSoup(req.text, "html.parser")

        ul = html.find_all('ul', {'class': 'resultList'})
        entry = ul[0]
        text = init_text

        books = entry.find_all('div', {'class': 'content'}, limit=LIMIT)
        #print(authors)

        for i, book in enumerate(books):
            author = book.find_all('a', limit=1)[0].getText()
            title_html = str(book.find_all('span', limit=1)[0])
            title_str = re.sub(r'<(|/)span>', '', title_html)
            text += "\t" + str(i + 1) + " -" + title_str + " por " + author + " \n"

        return text
    else:
        logger.error("Status Code %d" % status_code)
        return None


def scrapping_lcdl_chart(url, init_text):
    req = requests.get(url, headers=headers)

    status_code = req.status_code
    if status_code == 200:
        html = BeautifulSoup(req.text, "html.parser")

        entries = html.find_all('div', {'class': 'carousel-inner'})

        text = init_text
        entry = entries[len(entries) - 1]
        titles = entry.find_all('a', {'class': 'title-link'}, limit=LIMIT)
        authors = entry.find_all('a', {'class': 'book-header-2-subtitle-author'}, limit=LIMIT)

        for i in range(len(authors)):
            text += "\t" + str(i + 1) + " -" + titles[i].getText().lower().title() + " por " + authors[i].getText().lower().title() + " \n"

        return text
    else:
        logger.error("Status Code %d" % status_code)
        return None


def checkAndReturnResult(result):
    if result is None:
        logger.error("There was an error scrapping")
        return "Lo siento, hubo un error"
    else:
        logger.info("Finished scrapping")
        return result
