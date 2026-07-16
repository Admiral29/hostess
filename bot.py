import os
import logging
import re
from pyrogram import Client, filters

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

API_ID = int(os.getenv("API_ID"))
API_HASH = os.getenv("API_HASH")
BOT_TOKEN = os.getenv("BOT_TOKEN")

app = Client("welcome_bot", api_id=API_ID, api_hash=API_HASH, bot_token=BOT_TOKEN)

# ---------- Функция для парсинга имени из текста ----------
def extract_username_from_text(text):
    """
    Пытается извлечь имя пользователя из текста сообщения о вступлении.
    Примеры: "Иван Иванов присоединился" или "User joined"
    Возвращает имя или None.
    """
    # Паттерны для русского и английского языков
    patterns = [
        r'([А-Яа-яЁё\s]+)\s+присоединился',  # русский
        r'([А-Яа-яЁё\s]+)\s+вош[ёе]л',      # русский
        r'([A-Za-z\s]+)\s+joined',          # английский
        r'([A-Za-z\s]+)\s+вступил',          # русский (редко)
    ]
    for pattern in patterns:
        match = re.search(pattern, text, re.IGNORECASE)
        if match:
            return match.group(1).strip()
    return None

# ---------- Основной обработчик новых участников (через new_chat_members) ----------
@app.on_message(filters.new_chat_members & filters.group)
async def welcome_new_member(client, message):
    logger.info(f"🔥 Событие new_chat_members в чате {message.chat.id}")
    for user in message.new_chat_members:
        if user.is_bot:
            continue
        mention = f"@{user.username}" if user.username else f"[{user.first_name}](tg://user?id={user.id})"
        await message.reply(f"👋 Добро пожаловать, {mention}!\nРады видеть тебя в нашей группе! 🎉")
        logger.info(f"✅ Приветствие отправлено {user.first_name} (через new_chat_members)")

# ---------- Обработчик текстовых сообщений, если new_chat_members не сработал ----------
@app.on_message(filters.text & filters.group)
async def welcome_by_text(client, message):
    logger.info(f"📝 Текст сообщения: {message.text[:100]}")  # Логируем первые 100 символов
    # Проверяем, содержит ли текст признаки вступления
    text_lower = message.text.lower()
    keywords = ["присоединился", "joined", "вошёл", "вступил", "вступает"]
    if any(kw in text_lower for kw in keywords):
        logger.info(f"🔍 Обнаружено ключевое слово в сообщении: {message.text[:100]}")
        # Пытаемся извлечь имя
        name = extract_username_from_text(message.text)
        if name:
            # Отправляем приветствие от имени бота
            await message.reply(f"👋 Добро пожаловать, {name}!\nРады видеть тебя в нашей группе! 🎉")
            logger.info(f"✅ Приветствие отправлено (из текста) для {name}")
        else:
            # Если не удалось извлечь имя, можно отправить общее приветствие
            await message.reply("👋 Добро пожаловать в группу! 🎉")
            logger.info("✅ Отправлено общее приветствие (имя не извлечено)")

# ---------- Отладочный обработчик всех сообщений (для проверки) ----------
@app.on_message(filters.all & filters.group)
async def debug_all(client, message):
    # Логируем каждое сообщение с его типом
    logger.info(f"📨 Сообщение: id={message.id}, текст={message.text[:50] if message.text else 'нет текста'}, new_chat_members={bool(message.new_chat_members)}")
    # Если есть new_chat_members, выводим их имена
    if message.new_chat_members:
        for user in message.new_chat_members:
            logger.info(f"👤 Новый участник: {user.first_name} (бот: {user.is_bot})")

# ---------- Команда /test ----------
@app.on_message(filters.command("test") & filters.group)
async def test_cmd(client, message):
    await message.reply("✅ Бот работает и отвечает на команды!")

logger.info("🚀 Бот запущен. Логи будут выводиться в консоль.")
app.run()
