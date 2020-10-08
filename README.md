# what_to_read_bot [![Build Status](https://travis-ci.org/mavilam/what_to_read_bot.svg?branch=master)](https://travis-ci.org/mavilam/what_to_read_bot)
Bot para recomendar los libros más leídos de cada semana en distintas plataformas de venta de libros.

Pruébalo en [Telegram](https://telegram.me/what_to_read_bot)

## Funcionamiento
El bot consiste en un servicio web que se nutre de las webs de Fnac, Amazon, La casa del libro y La central para recoger los libros más leídos. Cada llamada scrappea la web de la tienda seleccionada y muestra los resultados.

Si quieres saber como registrar tu bot en telegram, echa un vistazo a este [enlace](https://core.telegram.org/bots#3-how-do-i-create-a-bot)

## Ejecución

Antes de nada es necesario instalar las dependencias
```bash
cd what_to_read_bot
pip install requirements
````

Una vez instaladas las dependencias, es necesario añadir una variable de entorno con el nombre *TELEGRAM_TOKEN* con el token de tu bot de telegram. Opcionalmente se puede añadir la variable *PORT* para indicar el puerto donde va a ejecutar el servicio, por defecto se ejecuta en el 8443.

Para indicar la url pública que va a usar telegram como webhook hay que reemplazar la siguiente variable en manage.py:
```python
webhook_base_url = 'tu url'
```
Yo uso [ngrok](https://ngrok.com/) para desarrollar en local.

Para ejecutar el bot:
```bash
python src/manage.py
```
