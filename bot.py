import os
import html
import logging
from telegram import Update
from telegram.ext import Application, MessageHandler, filters, ContextTypes

logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO
)
logger = logging.getLogger(__name__)

TOKEN = os.getenv("BOT_TOKEN")
if not TOKEN:
    raise ValueError("Переменная окружения BOT_TOKEN не установлена!")

async def welcome_new_member(update: Update, context: ContextTypes.DEFAULT_TYPE):
    for member in update.message.new_chat_members:
        safe_name = html.escape(member.full_name)
        welcome_text = (
            f"👋 Здравствуйте, {safe_name}! Добро пожаловать в чат орды!\n"
            f'Пожалуйста, укажите свой ник <a href="https://t.me/c/4329376403/13">в этой теме</a>.'
        )
        await update.message.reply_text(welcome_text, parse_mode='HTML')

def main():
    app = Application.builder().token(TOKEN).build()
    app.add_handler(
        MessageHandler(filters.StatusUpdate.NEW_CHAT_MEMBERS, welcome_new_member)
    )
    logger.info("Бот запущен...")
    app.run_polling(allowed_updates=Update.ALL_TYPES)

if __name__ == "__main__":
    main()
