import logging
from telegram import Update
from telegram.ext import ApplicationBuilder, ContextTypes, CommandHandler, MessageHandler, filters
from config import TG_BOT_TOKEN
from modules.yandex_assistant_module import YandexAssistant
from modules.database_module import Database
from modules.parser_module import BitrixParser

assistant = YandexAssistant()
db = Database()

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Привет! Я эксперт по API Bitrix24. Задавай свой вопрос.")

async def update_docs(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("🔄 Запущен процесс актуализации знаний через Selenium...")
    parser = BitrixParser()
    url = "https://apidocs.bitrix24.ru/api_help/crm/deals/crm_deal_add.php"
    data = parser.get_method_details(url)
    if "error" not in data:
        await update.message.reply_text(f"✅ Данные метода {data['title']} успешно спарсены.")
    else:
        await update.message.reply_text("❌ Ошибка при парсинге документации.")

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_text = update.message.text
    user_id = update.message.from_user.id
    
    answer = assistant.get_answer(user_text)
    
    db.save_message(user_id, user_text, answer)
    
    await update.message.reply_text(answer, parse_mode='Markdown')

if __name__ == '__main__':
    app = ApplicationBuilder().token(TG_BOT_TOKEN).build()
    
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("update", update_docs))
    app.add_handler(MessageHandler(filters.TEXT & (~filters.COMMAND), handle_message))
    
    print("Бот запущен...")
    app.run_polling()