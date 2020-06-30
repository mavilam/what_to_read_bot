# -*- coding: utf-8 -*-

import psycopg2
import os
import logging

conn = psycopg2.connect(os.getenv("DATABASE_URL"))


def get_highlights_text():
    logging.info('Requesting recommendations')
    cur = conn.cursor()
    cur.execute("select * from whattoread.highlights where isoffer = false;")
    rows = cur.fetchall()
    text = 'En este espacio quiero dejarte unas recomendaciones de libros que he leído recientemente y me han marcado: \n'
    for row in rows:
        text = f'{text}<a href="{row[2]}">{row[1]}</a>: {row[3]}'
    return text


def get_offers_text():
    logging.info('Requesting offers')
    cur = conn.cursor()
    cur.execute("select * from whattoread.highlights where isoffer = true;")
    rows = cur.fetchall()
    text = ''
    for row in rows:
        text = f'{text}<a href="{row[2]}">{row[1]}</a>: {row[3]}'

    if text != '':
        return f'Además te dejo unos enlaces que creo que te pueden interesar: \n{text}'
    else:
        return ''


def close_connection():
    conn.close()