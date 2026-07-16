import os
import logging
from pyrogram import Client, filters

# ---------- Настройка логирования (пишем и в консоль, и в файл) ----------
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

API_ID = int(os.getenv("API_ID"))
API_HASH = os.getenv("API_HASH")
BOT_TOKEN = os.getenv("BOT_TOKEN")

app = Client("welcome_bot", api_id=API_ID, api_hash=API_HASH, bot_token=BOT_TOKEN)

# ---------- Обработчик ВСЕХ сообщений (для отладки) ----------
@app.on_message(filters.all & filters.group)
async def debug_all_messages(client, message):
    logger.info(f"Получено сообщение в группе {message.chat.id} от {message.from_user.id}: {message.text if message.text else '[не текст]'}")
    # Если это служебное сообщение (например, о новом участнике), то у него есть атрибут new_chat_members
    if message.new_chat_members:
        logger.info(f"🔔 НОВЫЙ УЧАСТНИК! Количество: {len(message.new_chat_members)}")
        for user in message.new_chat_members:
            logger.info(f"Новичок: {user.first_name} (id={user.id}, is_bot={user.is_bot})")

# ---------- Основной обработчик новых участников ----------
@app.on_message(filters.new_chat_members & filters.group)
async def welcome(client, message):
    logger.info(f"🔥 Обработчик new_chat_members сработал в чате {message.chat.id}")
    for user in message.new_chat_members:
        if user.is_bot:
            logger.info(f"Пропускаем бота {user.first_name}")
            continue
        if user.username:
            mention = f"@{user.username}"
        else:
            mention = f"[{user.first_name}](tg://user?id={user.id})"
        try:
            await message.reply(
                f"👋 Добро пожаловать, {mention}!\nРады видеть тебя в нашей группе! 🎉"
            )
            logger.info(f"✅ Приветствие отправлено для {user.first_name}")
        except Exception as e:
            logger.error(f"❌ Ошибка при отправке приветствия: {e}")

# ---------- Команда /test (чтобы проверить, что бот жив) ----------
@app.on_message(filters.command("test") & filters.group)
async def test_cmd(client, message):
    await message.reply("✅ Бот работает и отвечает на команды!")

logger.info("🚀 Бот запущен и ждёт новых участников...")
app.run()
