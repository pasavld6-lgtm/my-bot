import telebot
from groq import Groq
import os

TOKEN = os.getenv("TOKEN")
GROQ_KEY = os.getenv("GROQ_KEY")

bot = telebot.Bot(TOKEN)
client = Groq(api_key=GROQ_KEY)

MODEL = "qwen/qwen3.8-27b"

@bot.message_handler(commands=["start"])
def start(message):
    bot.reply_to(message, "Привет! Я Qwen через Groq 🤖")

@bot.message_handler(func=lambda m: True)
def ask(message):
    try:
        r = client.chat.completions.create(
            model=MODEL,
            messages=[{"role": "user", "content": message.text}]
        )
        bot.reply_to(message, r.choices[0].message.content)
    except Exception as e:
        bot.reply_to(message, f"Ошибка: {e}")

bot.infinity_polling()
