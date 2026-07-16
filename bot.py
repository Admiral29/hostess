import os
import logging
from telegram import Update
from telegram.ext import Application, MessageHandler, filters, ContextTypes

# Включаем логирование, чтобы видеть ошибки
logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO
)
logger = logging.getLogger(__name__)

# Токен бота берем из переменных окружения (безопасность!)
TOKEN = os.getenv("BOT_TOKEN")
if not TOKEN:
    raise ValueError("Переменная окружения BOT_TOKEN не установлена!")

async def welcome_new_member(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Приветствие каждого нового участника."""
    for member in update.message.new_chat_members:
        # Упоминаем пользователя (без ссылки, просто имя)
        user_name = member.full_name
        # Можно также использовать member.mention_html() для кликабельного упоминания
        welcome_text = f"👋 Привет, {user_name}! Добро пожаловать в чат!"
        await update.message.reply_text(welcome_text)

def main():
    # Создаем приложение
    app = Application.builder().token(TOKEN).build()

    # Обработчик: когда в сообщении есть новые участники (не боты)
    app.add_handler(
        MessageHandler(filters.StatusUpdate.NEW_CHAT_MEMBERS, welcome_new_member)
    )

    # Запускаем бота (long polling)
    logger.info("Бот запущен...")
    app.run_polling(allowed_updates=Update.ALL_TYPES)

if __name__ == "__main__":
    main()
