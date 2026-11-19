import os
from telegram import Update
from telegram.ext import Application, MessageHandler, filters, ContextTypes
import requests

TELEGRAM_TOKEN = os.getenv("BOT_TOKEN")
API_KEY = os.getenv("OPENROUTER_KEY")

def ask_dolphin(text):
    r = requests.post("https://openrouter.ai/api/v1/chat/completions",
        headers={"Authorization": f"Bearer {API_KEY}"},
        json={"model": "cognitivecomputations/dolphin-mistral-24b-venice-edition",
              "messages": [{"role": "user", "content": text}]})
    return r.json()["choices"][0]["message"]["content"]

async def reply(update: Update, context: ContextTypes.DEFAULT_TYPE):
    ans = ask_dolphin(update.message.text)
    await update.message.reply_text(ans)

app = Application.builder().token(TELEGRAM_TOKEN).build()
app.add_handler(MessageHandler(filters.TEXT, reply))
app.run_polling()
