import logging
import http.client
import os
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import (ApplicationBuilder, CommandHandler, MessageHandler, filters, CallbackContext)

# 🔑 Bot Token & RapidAPI Key (Fetch from Environment Variables for Security)
TOKEN = os.getenv("BOT_TOKEN")
RAPIDAPI_KEY = os.getenv("RAPIDAPI_KEY")
OWNER_USERNAME = "RU_DRA_65"
GROUP_LINK = "https://t.me/RU_DRA_098"

# 📌 Logging setup
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)
logger = logging.getLogger(__name__)

# 🤖 Generate AI Response using RapidAPI GPT-4o
def generate_response(user_input):
    conn = http.client.HTTPSConnection("cheapest-gpt-4-turbo-gpt-4-vision-chatgpt-openai-ai-api.p.rapidapi.com")
    payload = f'{{"messages":[{{"role":"user","content":"{user_input}"}}],"model":"gpt-4o","max_tokens":100,"temperature":0.9}}'
    headers = {
        'x-rapidapi-key': RAPIDAPI_KEY,
        'x-rapidapi-host': "cheapest-gpt-4-turbo-gpt-4-vision-chatgpt-openai-ai-api.p.rapidapi.com",
        'Content-Type': "application/json"
    }
    conn.request("POST", "/v1/chat/completions", payload, headers)
    res = conn.getresponse()
    data = res.read()
    return data.decode("utf-8")

# 🏠 Start Command
async def start(update: Update, context: CallbackContext) -> None:
    keyboard = [
        [InlineKeyboardButton("👑 Owner", url=f"https://t.me/{OWNER_USERNAME}")],
        [InlineKeyboardButton("💬 Join Group", url=GROUP_LINK)]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    # 🖼️ Send Image from URL
    image_url = "https://your-image-url.com/start.jpg"  # 🛠️ Replace with your image URL
    await update.message.reply_photo(photo=image_url, caption="Hello! I'm YOUR BABY. Talk to me!", reply_markup=reply_markup)

# 🤖 Handle Messages
async def chat(update: Update, context: CallbackContext) -> None:
    user_message = update.message.text
    response = generate_response(user_message)
    await update.message.reply_text(response)

# 🚀 Main Function (Bot Initialization)
def main() -> None:
    app = ApplicationBuilder().token(TOKEN).build()
    
    # 🔥 Command Handlers
    app.add_handler(CommandHandler("start", start))
    
    # 📩 Message Handler
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, chat))
    
    # 🔄 Polling System
    app.run_polling()

# 🔥 Run Bot
if __name__ == "__main__":
    main()
