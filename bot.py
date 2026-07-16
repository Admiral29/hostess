import os
import logging
from pyrogram import Client, filters

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

API_ID = int(os.getenv("API_ID"))
API_HASH = os.getenv("API_HASH")
BOT_TOKEN = os.getenv("BOT_TOKEN")

app = Client("welcome_bot", api_id=API_ID, api_hash=API_HASH, bot_token=BOT_TOKEN)

# Для отладки: сохраняем ID группы, куда будем слать отчёты (замените на ваш chat_id, если надо)
# Но мы будем слать в ту же группу, где происходит событие.

# ---------- Обработчик всех сообщений (с отправкой отчёта) ----------
message_counter = 0

@app.on_message(filters.all & filters.group)
async def debug_all(client, message):
    global message_counter
    message_counter += 1
    # Чтобы не спамить, отправляем отчёт только для первых 5 сообщений
    if message_counter <= 5:
        try:
            await message.reply(f"🔍 Бот видит сообщение #{message_counter}: тип={message.chat.type}")
        except:
            pass

    if message.new_chat_members:
        # Это событие о новом участнике
        await message.reply(f"🔔 Обнаружен новый участник! Количество: {len(message.new_chat_members)}")
        for user in message.new_chat_members:
            if user.is_bot:
                continue
            mention = f"@{user.username}" if user.username else f"[{user.first_name}](tg://user?id={user.id})"
            await message.reply(
                f"👋 Добро пожаловать, {mention}!\nРады видеть тебя в нашей группе! 🎉"
            )

# ---------- Обработчик команды /start (скажет, что бот жив) ----------
@app.on_message(filters.command("start") & filters.group)
async def start_cmd(client, message):
    await message.reply("✅ Бот работает! Я вижу команды в группе.")

# ---------- Обработчик команды /test ----------
@app.on_message(filters.command("test") & filters.group)
async def test_cmd(client, message):
    await message.reply("✅ Бот отвечает на /test! Всё хорошо.")

# ---------- При запуске отправить сообщение в группу (опционально) ----------
@app.on_message(filters.command("init") & filters.group)
async def init_cmd(client, message):
    await message.reply("✅ Бот запущен и готов работать в этой группе!")

logger.info("🚀 Бот запущен...")
app.run()
