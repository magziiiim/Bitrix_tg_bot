import asyncio
import logging
from aiogram import Bot, Dispatcher, types
from aiogram.filters import Command
from config import TELEGRAM_TOKEN
from modules.database_module import save_message, init_db
from modules.yandex_assistant_module import YandexAssistant

logging.basicConfig(level=logging.INFO)

bot = Bot(token=TELEGRAM_TOKEN)
dp = Dispatcher()
ai_assistant = YandexAssistant()

@dp.message(Command("start"))
async def start_handler(message: types.Message):
    await message.answer("Бот-ассистент по Bitrix24 API запущен. Задайте ваш вопрос.")

@dp.message()
async def message_handler(message: types.Message):
    if not message.text:
        return

    response = ai_assistant.ask_question(message.text)
    save_message(message.from_user.id, message.text, response)
    await message.answer(response)

async def main():
    init_db()
    logging.info("Starting bot...")
    await dp.start_polling(bot)

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        pass