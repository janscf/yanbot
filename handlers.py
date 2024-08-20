import aiohttp
from aiogram import Router
from aiogram.filters import Command
from aiogram.types import Message

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
    NEWS_DEFAULT_QUERY
)

router = Router()


@router.channel_post(Command('цитата', prefix=COMMAND_PREFIX))
async def get_random_quote(msg: Message):
    async with aiohttp.ClientSession() as session:
        response = await session.get(
            FORISMATIC_URL,
            raise_for_status=True,
            params={'method': 'getQuote', 'key': 457653, 'format': 'json', 'lang': 'ru'}
        )
        async with response:
            data = await response.json()

    await msg.answer(f'«{data["quoteText"]}»\n\n{data["quoteAuthor"]}')


@router.channel_post(Command('погода', prefix=COMMAND_PREFIX))
async def get_weather_forecast(msg: Message):
    args = msg.text.split(' ')
    destination = WEATHER_DEFAULT_DESTINATION
    if len(args) > 1:
        destination = args[1]

    async with aiohttp.ClientSession() as session:
        response = await session.get(
            WEATHER_URL.format(destination),
            raise_for_status=True
        )
        async with response:
            weather = await response.text()

    await msg.answer(weather)


@router.channel_post(Command('котэ', prefix=COMMAND_PREFIX))
async def get_random_cat(msg: Message):
    async with aiohttp.ClientSession() as session:
        response = await session.get(
            CATS_API_URL,
            raise_for_status=True,
            headers={'x-api-key': CATS_API_KEY}
        )
        async with response:
            data = await response.json()

    await msg.answer_photo(data[0]['url'])


@router.channel_post(Command('собакен', prefix=COMMAND_PREFIX))
async def get_random_cat(msg: Message):
    async with aiohttp.ClientSession() as session:
        response = await session.get(
            DOGS_API_URL,
            raise_for_status=True,
            headers={'x-api-key': DOGS_API_KEY}
        )
        async with response:
            data = await response.json()

    await msg.answer_photo(data[0]['url'])


@router.channel_post(Command('новость', prefix=COMMAND_PREFIX))
async def get_random_news(msg: Message):
    args = msg.text.split(' ')
    query = NEWS_DEFAULT_QUERY
    if len(args) > 1:
        query = args[1]

    async with aiohttp.ClientSession() as session:
        response = await session.get(
            NEWS_API_URL.format(query),
            raise_for_status=True,
        )
        async with response:
            data = await response.json()

    if data.get('status') != 'ok':
        return await msg.answer('Какая-то ошибка, уже чиню 8(')

    if data.get('totalResults', 0) == 0:
        return await msg.answer('Ничего не нашлось. Увы!')

    news = data['articles'][0]
    await msg.answer(f'<b>{news["title"]}</b>\n\n{news["description"]}\n\n{news["url"]}')
