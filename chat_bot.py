import requests
import xml.etree.ElementTree as ET
from telegram import Bot, InputMediaPhoto
from telegram.ext import Updater, Filters, MessageHandler, CommandHandler
from pprint import pprint

RANDOM_JOKE_URL = 'http://rzhunemogu.ru/Rand.aspx?CType={}'
GET_WEATHER_URL = 'http://wttr.in/{}?m1&lang=ru&format=4&T'
RANDOM_KOTIK_URL = 'https://api.thecatapi.com/v1/images/search'

SHUFFLE_DECK_URL = 'https://deckofcardsapi.com/api/deck/new/shuffle/?deck_count=1'
GET_CARDS_URL = 'https://deckofcardsapi.com/api/deck/{}/draw/?count=2'

API_TOKEN = '5755531575:AAEd-w5X-1qEPrJmsYXUFtm2cy854ZQU_co'
MARGINALS_CHAT_ID = -272673944
MY_CHAT_ID = 1189120977


bot = Bot(token=API_TOKEN)
updater = Updater(token=API_TOKEN)


def get_response(url, format='text', decode_from='utf8') -> str:
    try:
        response = requests.get(url)
        if format == 'json':
            return response.json()

        response_text = response.content.decode(decode_from)
        if decode_from != 'utf8':
            response_text = response_text.encode('utf8')

        if format == 'xml':
            return ET.fromstring(response_text)

        return response_text
    except Exception as e:
        print(e)
        return None


def send_random_joke(update, context, joke_id=1):
    chat = update.effective_chat
    response_text = get_response(RANDOM_JOKE_URL.format(joke_id), decode_from='cp1251')
    root = ET.fromstring(response_text)
    joke = root.find('content').text
    if joke:
        context.bot.send_message(chat_id=chat.id, text=joke)


def send_random_stih(update, context):
    send_random_joke(update, context, 13)


def get_weather_forecast(update, context):
    chat = update.effective_chat
    if not context.args:
        context.bot.send_message(chat_id=chat.id, text='Где тебе погоду показать, пёс? Деревню-то свою укажи.')
        return
    destination = context.args[0]
    response_text = get_response(GET_WEATHER_URL.format(destination))
    if response_text:
        context.bot.send_message(chat_id=chat.id, text=response_text)


def send_random_kotik(update, context):
    chat = update.effective_chat
    response_json = get_response(RANDOM_KOTIK_URL, format='json')
    url = response_json[0].get('url')
    if url:
        context.bot.send_photo(chat.id, url)


deck_id = None
def send_two_cards(update, context):
    global deck_id
    chat = update.effective_chat
    if deck_id is None:
        response_json = get_response(SHUFFLE_DECK_URL, format='json')
        is_success = response_json.get('success', False)
        if not is_success:
            return
        deck_id = response_json['deck_id']

    response_json = get_response(GET_CARDS_URL.format(deck_id), format='json')
    is_success = response_json.get('success', False)
    if not is_success:
        return

    images = [card['images']['png'] for card in response_json['cards']]
    medias = [InputMediaPhoto(media=image) for image in images]
    context.bot.send_media_group(chat.id, medias)


# def do_start(update, context):
#     chat = update.effective_chat
#     first_name = update.message.chat.first_name
#     context.bot.send_message(chat_id=chat.id, text=f'Спасибо, что включили меня, {first_name}!')


updater.dispatcher.add_handler(CommandHandler('anek', send_random_joke))
updater.dispatcher.add_handler(CommandHandler('stih', send_random_stih))
updater.dispatcher.add_handler(CommandHandler('pogoda', get_weather_forecast, pass_args=True))
updater.dispatcher.add_handler(CommandHandler('kotik', send_random_kotik))
updater.dispatcher.add_handler(CommandHandler('ochko', send_two_cards))
# updater.dispatcher.add_handler(MessageHandler(Filters.text, say_hi))
updater.start_polling(poll_interval=20.0)
updater.idle()


"""
{
    'update_id': 994132689,
    'message':
    {
        'new_chat_photo': [],
        'new_chat_members': [],
        'message_id': 32,
        'caption_entities': [],
        'delete_chat_photo': False,
        'chat': {
            'id': 1189120977,
            'type': 'private',
            'first_name': 'Yan',
            'last_name': 'Scherbatov',
            'username': 'yan_scherbatov'
        },
        'entities': [
            {
                'offset': 0,
                'type': 'bot_command',
                'length': 6
            }
        ],
        'text': '/start',
        'photo': [],
        'channel_chat_created': False,
        'date': 1663158733,
        'supergroup_chat_created': False,
        'group_chat_created': False,
        'from': {
            'id': 1189120977,
            'username': 'yan_scherbatov',
            'last_name':
            'Scherbatov',
            'is_bot': False,
            'first_name': 'Yan',
            'language_code': 'en'
        }
    }
}
"""