# -*- coding: utf-8 -*-

import logging
import requests

logger = logging.getLogger(__name__)

headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.13; rv:61.0) Gecko/20100101 Firefox/'}


def perform_get(url):
    req = requests.get(url, headers=headers)

    status_code = req.status_code
    if status_code == 200:
        return req.text
    else:
        logger.error("Status Code %d" % status_code)
        return None
