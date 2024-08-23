import os
from dotenv import load_dotenv

load_dotenv()

TOKEN = os.environ['BOT_TOKEN']
COMMAND_PREFIX = '!'
PROXY_URL = None

FORISMATIC_URL = 'http://api.forismatic.com/api/1.0/'

WEATHER_URL = 'http://wttr.in/{}?m1&lang=ru&format=4&T'
WEATHER_DEFAULT_DESTINATION = 'tomsk'

CATS_API_URL = 'https://api.thecatapi.com/v1/images/search?format=json'
CATS_API_KEY = os.environ['CATS_API_KEY']

DOGS_API_URL = 'https://api.thedogapi.com/v1/images/search'
DOGS_API_KEY = os.environ['DOGS_API_KEY']

NEWS_API_KEY = os.environ['NEWS_API_KEY']
NEWS_API_URL = 'https://newsapi.org/v2/everything?q={}' + f'&apiKey={NEWS_API_KEY}'
NEWS_DEFAULT_QUERY = 'томск'

RATES_URL = 'https://www.cbr.ru/scripts/XML_daily.asp'
RATES_DEFAULT_CURRENCIES = ('USD', 'EUR', 'CNY')

QR_URL = 'https://api.qrserver.com/v1/create-qr-code/?size=150x150&data={}'

SHORT_JOKES_URL = 'https://shortiki.com/export/api.php?format=json&amount=100&type=random'