import os
import json
from aiogram import Bot, Dispatcher, types
from aiogram.types import FSInputFile
from aiogram.filters import Command
import logging
from wit import Wit
from database.transactions import (
    save_message,
    clear_message_table,
    get_dialog,
    get_from_dishes,
    get_names_through_time)
from dotenv import load_dotenv
from parser.DateParser import DateParser

load_dotenv()

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

bot = Bot(token=os.getenv('TELEGRAM_TOKEN'))
dp = Dispatcher()
wit_client = Wit(os.getenv('WIT_AI_TOKEN'))

@dp.message(Command("start"))
async def start(message: types.Message):
    await message.reply("Бот запущен. Поговорим о кулинарии? ")

@dp.message(Command("help"))
async def command_help(message: types.Message):
    help_text = """
Добро пожаловать в кулинарный бот!
Эта диалоговая система предназначена для помощи вам с готовкой популярных блюд. Я могу подсказать:
- Рецепт блюда
- Его калорийность
- Время приготовления
- Рекомендуемые ингредиенты
- Инструменты.
Я знаю некоторые вегетарианские, веганские, низкокалорийные и детские блюда, а также блюда некоторых национальных кухонь!
Если Вы бы хотели экспортировать весь диалог, пожалуйста, выберите команду "/extract - Экспорт диалога (JSON)".
"""
    await message.reply(help_text)


@dp.message(Command('extract'))
async def command_extract(message: types.Message):
    user_id = message.from_user.id
    records = await get_dialog()
    logging.info(records)

    if not records:
        await message.reply("Диалог пуст.")
        return

    dialog_data = [
        {
            "user_id": record['user_id'],
            "timestamp": record['created_at'].isoformat(),
            "user_message": record['message'],
            "bot_response": record['response']
        }
        for record in records
    ]

    filename = f"dialog_{user_id}.json"
    with open(filename, 'w', encoding='utf-8') as f:
        json.dump(dialog_data, f, ensure_ascii=False, indent=2)
    await message.reply_document(FSInputFile(filename), caption="Ваш диалог в JSON")
    os.remove(filename)


@dp.message()
async def handle_message(message: types.Message):
    response = ''
    # анализ через Wit.ai
    wit_response = wit_client.message(message.text)
    logging.info(wit_response)
    intent = wit_response.get('intents', [{}])[0].get('name', 'unknown')
    entities = wit_response.get('entities', {})
    traits = wit_response.get('traits', {})
    if entities != {} and intent != 'name':
        column, value = list(entities.keys())[0].split(':')
        if column and value:
            records = await get_from_dishes(intent, column, value)
            if intent == 'recipe':
                ru_name = await get_ru_name(column, value)
                response = await get_recipe(records, ru_name)
            elif intent == 'ingredients':
                ru_name = await get_ru_name(column, value)
                response = await get_ingredients(records, ru_name)
            elif intent == 'instruments':
                ru_name = await get_ru_name(column, value)
                response = await get_instruments(records, ru_name)
            elif intent == 'calories':
                ru_name = await get_ru_name(column, value)
                response = await get_calories(records, ru_name)
            elif intent == 'cooking_time':
                ru_name = await get_ru_name(column, value)
                response = await get_cooking_time(records, ru_name)
    elif intent == 'name':
        response = await get_names(traits, intent, entities)


    elif intent == 'start_dialog':
        response = f"Здравствуйте! Что приготовим сегодня?"
        await clear_message_table()
    elif intent == 'thanks':
        response = "Всегда пожалуйста! Если нужно больше информации о блюдах и идеях их приготовления, спрашивайте!"
    else:
        response = "Не понял запрос. Пожалуйста, попробуйте уточнить."
    await save_message(
        user_id=message.from_user.id,
        message=message.text,
        response=response
    )
    await message.reply(response)

async def get_recipe(records, ru_name):
    recipe = records[0]['recipe']
    response = f"Вот рецепт для блюда {ru_name}: {recipe}"
    return response

async def get_ingredients(records, ru_name):
    ingredients = records[0]['ingredients']
    response = f"Вот рекомендуемые ингредиенты для блюда {ru_name}: {ingredients}"
    return response

async def get_instruments(records, ru_name):
    instruments = records[0]['instruments']
    response = f"Вот необходимые инструменты для блюда {ru_name}: {instruments}"
    return response

async def get_calories(records, ru_name):
    calories = records[0]['calories']
    response = f"В блюде {ru_name} {calories} ккал на порцию."
    return response

async def get_cooking_time(records, ru_name):
    cooking_time = records[0]['cooking_time']
    response = f"Для приготовления блюда {ru_name} требуется {cooking_time}."
    return response

async def get_ru_name(column, value):
    value_ru_name = await get_from_dishes('name', column, value)
    ru_name = value_ru_name[0]['name']
    return ru_name

async def get_names(traits, intent, entities):
    names = ''
    column, value = list(entities.keys())[0].split(':')
    if value == 'duration':
        unit = entities.get(list(entities.keys())[0])[0].get('unit')
        time_value = entities.get(list(entities.keys())[0])[0].get('value')
        search_value = DateParser.parse(unit, time_value)
        if traits:
            if list(traits.keys())[0] == 'less':
                try:
                    names = await get_names_through_time(search_value, '<')
                except Exception as e:
                    logging.error(f"Ошибка запроса: {e}")
                    raise
    else:
        try:
            names = await get_from_dishes(intent, column, value)
        except Exception as e:
            logging.error(f"Ошибка запроса: {e}")
            raise
    if names:
        names_str = ''.join(str(name['name']) + ', ' for name in names)
        names_str = names_str.strip(', ')
        response = f"Вот известные мне блюда: {names_str}."
    else:
        response = "Хм, такие блюда мне не известны"
    return response


if __name__ == '__main__':
    dp.run_polling(bot)