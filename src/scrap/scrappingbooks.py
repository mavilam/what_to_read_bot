# -*- coding: utf-8 -*-

import logging
import json
import os

from scrap.sources import fnac
from scrap.sources import lacasadellibro
from scrap.sources import lacentral
from scrap.sources import amazon

# Enable logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)

books_urls = {}
if os.path.exists('/app/static/book_sources.json'):
    with open('/app/static/book_sources.json') as json_data:
        books_urls = json.load(json_data)
else:
    with open(f'{os.path.dirname(os.path.abspath(__file__))}/book_sources.json') as json_data:
        books_urls = json.load(json_data)

logger = logging.getLogger(__name__)

headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.13; rv:61.0) Gecko/20100101 Firefox/'}


def scrap_books(vendor, type):
    if vendor == "Fnac":
        return fnac.result_scrapping(type, books_urls)
    elif vendor == "Casa del libro":
        return lacasadellibro.result_scrapping(type, books_urls)
    elif vendor == "La Central":
        return lacentral.result_scrapping(type, books_urls)
    elif vendor == "Amazon":
        return amazon.result_scrapping(type, books_urls)

    return f'{prev_text} \t {number_of_book} -{title} por {author.title()} \n'
