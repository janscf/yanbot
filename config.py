import os
from dotenv import load_dotenv

load_dotenv()

TOKEN = os.environ['BOT_TOKEN']
COMMAND_PREFIX = '!'
FORISMATIC_URL = 'http://api.forismatic.com/api/1.0/'
WEATHER_URL = 'http://wttr.in/{}?m1&lang=ru&format=4&T'
WEATHER_DEFAULT_DESTINATION = 'tomsk'
CATS_API_URL = 'https://api.thecatapi.com/v1/images/search?format=json'
CATS_API_KEY = 'live_7Uu2nyZ0u55Dy1W8jsrlCjCzGe3MjiWxauSDdWpSDiMUpKkjp5XzWl9TrvIUrCiv'
DOGS_API_URL = 'https://api.thedogapi.com/v1/images/search'
DOGS_API_KEY = 'live_72E3WJJZycFIQyR8evxd3YhhDchL72GB0jZkj273NvMRjL43nviTowwbmlIkX8Gc'
NEWS_API_KEY = '0d034c922ea9480e9b34a8b686eb2415'
NEWS_API_URL = 'https://newsapi.org/v2/everything?q={}' + f'&sortBy=popularity&apiKey={NEWS_API_KEY}'
NEWS_DEFAULT_QUERY = 'новость дня'
