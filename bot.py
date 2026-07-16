import os
from pyrogram import Client, filters

# ---------- Переменные окружения (задаются на Bothost) ----------
API_ID = int(os.getenv("API_ID"))
API_HASH = os.getenv("API_HASH")
BOT_TOKEN = os.getenv("BOT_TOKEN")

app = Client("welcome_bot", api_id=API_ID, api_hash=API_HASH, bot_token=BOT_TOKEN)

# ---------- Обработчик новых участников ----------
@app.on_message(filters.new_chat_members)
async def welcome(client, message):
    for user in message.new_chat_members:
        # Пропускаем ботов (чтобы не приветствовать самого себя)
        if user.is_bot:
            continue

        # Формируем упоминание (через username, если есть, иначе через ссылку)
        if user.username:
            mention = f"@{user.username}"
        else:
            mention = f"[{user.first_name}](tg://user?id={user.id})"

        # Отправляем приветствие в тот же чат
        await message.reply(
            f"👋 Добро пожаловать, {mention}!\n"
            "Рады видеть тебя в нашей группе! 🎉"
        )

print("🚀 Бот запущен и ждёт новых участников...")
app.run()
