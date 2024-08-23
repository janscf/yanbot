from random import choice
import aiohttp
from aiogram import Router
from aiogram.filters import Command
from aiogram.types import Message

from filters import ChatTypeFilter
from config import (
    COMMAND_PREFIX,
    FORISMATIC_URL,
    WEATHER_URL,
    WEATHER_DEFAULT_DESTINATION,
    CATS_API_URL,
    CATS_API_KEY,
    DOGS_API_URL,
    DOGS_API_KEY,
    NEWS_API_URL,
    NEWS_DEFAULT_QUERY,
    PROXY_URL,
    RATES_URL,
    RATES_DEFAULT_CURRENCIES,
    QR_URL,
    SHORT_JOKES_URL,
)
from utils.xml import find_currency_rates

router = Router()
filter = ChatTypeFilter(chat_type=["group", "supergroup"])


@router.channel_post(Command('цитата', prefix=COMMAND_PREFIX))
@router.message(filter, Command('цитата', prefix=COMMAND_PREFIX))
async def get_random_quote(msg: Message):
    async with aiohttp.ClientSession() as session:
        response = await session.get(
            FORISMATIC_URL,
            raise_for_status=True,
            params={'method': 'getQuote', 'key': 457653, 'format': 'json', 'lang': 'ru'},
            proxy=PROXY_URL,
        )
        async with response:
            data = await response.json()

    await msg.answer(f'«{data["quoteText"]}»\n\n{data["quoteAuthor"]}')


@router.channel_post(Command('погода', prefix=COMMAND_PREFIX))
@router.message(filter, Command('погода', prefix=COMMAND_PREFIX))
async def get_weather_forecast(msg: Message):
    args = msg.text.split(' ')
    destination = WEATHER_DEFAULT_DESTINATION
    if len(args) > 1:
        destination = args[1]

    async with aiohttp.ClientSession() as session:
        response = await session.get(
            WEATHER_URL.format(destination),
            raise_for_status=True,
            proxy=PROXY_URL,
        )
        async with response:
            weather = await response.text()

    await msg.answer(weather)


@router.channel_post(Command('котик', prefix=COMMAND_PREFIX))
@router.message(filter, Command('котик', prefix=COMMAND_PREFIX))
async def get_random_cat(msg: Message):
    async with aiohttp.ClientSession() as session:
        response = await session.get(
            CATS_API_URL,
            raise_for_status=True,
            headers={'x-api-key': CATS_API_KEY},
            proxy=PROXY_URL,
        )
        async with response:
            data = await response.json()

    await msg.answer_photo(data[0]['url'])


@router.channel_post(Command('песик', prefix=COMMAND_PREFIX))
@router.message(filter, Command('песик', prefix=COMMAND_PREFIX))
async def get_random_cat(msg: Message):
    async with aiohttp.ClientSession() as session:
        response = await session.get(
            DOGS_API_URL,
            raise_for_status=True,
            headers={'x-api-key': DOGS_API_KEY},
            proxy=PROXY_URL,
        )
        async with response:
            data = await response.json()

    await msg.answer_photo(data[0]['url'])


@router.channel_post(Command('новость', prefix=COMMAND_PREFIX))
@router.message(filter, Command('новость', prefix=COMMAND_PREFIX))
async def get_random_news(msg: Message):
    args = msg.text.split(' ')
    query = NEWS_DEFAULT_QUERY
    if len(args) > 1:
        query = args[1]

    async with aiohttp.ClientSession() as session:
        response = await session.get(
            NEWS_API_URL.format(query),
            raise_for_status=True,
            proxy=PROXY_URL,
        )
        async with response:
            data = await response.json()

    if data.get('status') != 'ok':
        return await msg.answer('Какая-то ошибка, уже чиню 8(')

    if data.get('totalResults', 0) == 0:
        return await msg.answer('Ничего не нашлось. Увы!')

    news = choice(data['articles'])
    await msg.answer(f'<b>{news["title"]}</b>\n\n{news["description"]}\n\n{news["url"]}')


@router.channel_post(Command('курс', prefix=COMMAND_PREFIX))
@router.message(filter, Command('курс', prefix=COMMAND_PREFIX))
async def get_cbr_rate(msg: Message):
    currencies = msg.text.split(' ')[1:] or RATES_DEFAULT_CURRENCIES

    async with aiohttp.ClientSession() as session:
        response = await session.get(
            RATES_URL,
            raise_for_status=True,
            proxy=PROXY_URL,
        )
        async with response:
            data = await response.text()

    currency_rates = find_currency_rates(data, currencies)
    message = '\n'.join(
        f'{name} ({code}): {value} р.'
        for code, name, value in currency_rates
    )
    await msg.answer(message)


@router.channel_post(Command('qr', prefix=COMMAND_PREFIX))
@router.message(filter, Command('qr', prefix=COMMAND_PREFIX))
async def get_qr(msg: Message):
    data = ' '.join(msg.text.split(' ')[1:]).strip()
    await msg.answer_photo(QR_URL.format(data))


@router.channel_post(Command('шутка', prefix=COMMAND_PREFIX))
@router.message(filter, Command('шутка', prefix=COMMAND_PREFIX))
async def get_short_joke(msg: Message):
    async with aiohttp.ClientSession() as session:
        response = await session.get(
            SHORT_JOKES_URL,
            raise_for_status=True,
            proxy=PROXY_URL,
        )
        async with response:
            data = await response.json()

    if not data:
        return await msg.answer('Какие уж тут шутки!')

    joke = choice(data)
    await msg.answer(joke['content'])


@router.channel_post(Command('кто', prefix=COMMAND_PREFIX))
@router.message(filter, Command('кто', prefix=COMMAND_PREFIX))
async def get_who(msg: Message):
    await msg.answer('🖕 Это ты! 🖕')
