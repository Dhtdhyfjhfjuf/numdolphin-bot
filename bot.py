import os
from telegram import Update
from telegram.ext import Application, MessageHandler, filters, ContextTypes
import requests

TELEGRAM_TOKEN = os.getenv("BOT_TOKEN")
API_KEY = os.getenv("OPENROUTER_KEY")  # هنسيبه بنفس الاسم عشان الكوماند اللي انت كتبته يشتغل

def ask_dolphin(text):
    r = requests.post("https://api.groq.com/openai/v1/chat/completions",
        headers={"Authorization": f"Bearer {API_KEY}"},
        json={"model": "llama-3.3-70b-versatile",
              "messages": [{"role": "user", "content": text}]})
    print(r.text) # عشان لو حصل خطأ يبان
    return r.json()["choices"][0]["message"]["content"]

async def reply(update: Update, context: ContextTypes.DEFAULT_TYPE):
    ans = ask_dolphin(update.message.text)
    await update.message.reply_text(ans)

app = Application.builder().token(TELEGRAM_TOKEN).proxy_url("http://proxy.server:3128").build()
app.add_handler(MessageHandler(filters.TEXT, reply))
app.run_polling()
