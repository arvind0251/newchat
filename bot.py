import telebot
import openai
import random
import requests

# 🔑 Replace with your API Keys
TELEGRAM_TOKEN = "8092574352:AAHlKwKMGuaEhQhwY47_x6M_sbko8okTgy8"
OPENAI_API_KEY = "YOUR_OPENAI_API_KEY"

# Bot Initialization
bot = telebot.TeleBot(TELEGRAM_TOKEN)
openai.api_key = OPENAI_API_KEY

# 🎭 Random Funny Replies (Agar AI Reply na de to backup ke liye)
funny_replies = [
    "Haan bhai, batao kya scene hai? 😂",
    "Aree o Babu Bhaiya! Kaise ho? 😎",
    "Aaj kuch toofani karte hain! 🚀",
    "Mat pucho, dukh bhari kahani hai... 😢",
    "Code likhne de yaar, kyun pareshaan kar raha hai? 🤖"
]

# 🔥 AI-Based Response Function
def get_ai_reply(text):
    try:
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",  # Ya "gpt-4" agar better response chahiye
            messages=[{"role": "user", "content": text}]
        )
        return response['choices'][0]['message']['content']
    except:
        return random.choice(funny_replies)  # Agar error aaye to backup reply de

# 🎯 Message Handler
@bot.message_handler(func=lambda message: True)
def handle_messages(message):
    text = message.text.lower()

    # 📌 Special Commands
    if "/joke" in text:
        bot.reply_to(message, "😂 " + get_ai_reply("Tell me a joke in Hindi"))
    elif "/quote" in text:
        bot.reply_to(message, "🌟 " + get_ai_reply("Give me a motivational quote in Hindi"))
    elif "/shayari" in text:
        bot.reply_to(message, "🎭 " + get_ai_reply("Mujhe ek mazedar Urdu shayari suna do"))
    elif "/roast" in text:
        bot.reply_to(message, "🔥 " + get_ai_reply("Roast me in a funny way"))

    # 📌 AI Response for Normal Messages
    else:
        bot.reply_to(message, get_ai_reply(text))

# 🚀 Start the Bot
print("🤖 AI Bot is Running...")
bot.polling(none_stop=True)
