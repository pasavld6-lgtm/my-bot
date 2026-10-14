import telebot
from groq import Groq
import os

TOKEN = os.getenv("TOKEN")
GROQ_KEY = os.getenv("GROQ_KEY")

bot = telebot.TeleBot(TOKEN)
client = Groq(api_key=GROQ_KEY)

MODEL = "qwen/qwen3.8-27b"

@bot.message_handler(commands=["start"])
def start(message):
    bot.reply_to(message, "Привет! Я Qwen через Groq 🤖")

# сначала — .квен (чтоб перехватывать до общего хендлера)
@bot.message_handler(func=lambda m: m.text and m.text.startswith(".квен"))
def qwen_handler(message):
    query = message.text[len(".квен"):].strip()
    if not query:
        bot.reply_to(message, "Напиши вопрос после .квен 👊")
        return
    try:
        resp = client.chat.completions.create(
            model=MODEL,
            messages=[{"role": "user", "content": query}]
        )
        bot.send_message(message.chat.id, resp.choices[0].message.content)
    except Exception as e:
        bot.send_message(message.chat.id, f"Ошибка: {e}")

# потом — всё остальное
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
