import telebot
import requests
import random

# 🔑 Telegram Bot Token (BotFather se lein)
TOKEN = "8092574352:AAHlKwKMGuaEhQhwY47_x6M_sbko8okTgy8"
bot = telebot.TeleBot(TOKEN)

# 🎭 Random Funny Replies
funny_replies = [
    "Haan bhai, batao kya scene hai? 😂",
    "Aree o Babu Bhaiya! Kaise ho? 😎",
    "Aaj kuch toofani karte hain! 🚀",
    "Mat pucho, dukh bhari kahani hai... 😢",
    "Code likhne de yaar, kyun pareshaan kar raha hai? 🤖"
]

# 🎭 Random Roasts
roasts = [
    "Teri soch mere code jitni tez hoti to duniya jeet leta! 😆",
    "Bhai tu error message bhi nahi samajh sakta! 😂",
    "Akele akele hansi nahi aati? Mujhse baat kar le! 😜",
    "Tu chat GPT se tez hai kya? 😜"
]

# 🃏 Jokes API se Random Joke
def get_joke():
    try:
        response = requests.get("https://official-joke-api.appspot.com/random_joke")
        joke = response.json()
        return f"😂 {joke['setup']} ... {joke['punchline']}"
    except:
        return "Arre yaar, joke wali API so rahi hai! 😴"

# 🌟 Motivational Quotes API
def get_quote():
    try:
        response = requests.get("https://api.quotable.io/random")
        quote = response.json()
        return f"🌟 {quote['content']} - {quote['author']}"
    except:
        return "Quote ka stock khatam ho gaya, kal aana! 😜"

# 📝 Shayari Collection
shayari_list = [
    "Aankhon se door na ho dil se utar jaayega, waqt ka kya hai guzar jaayega! ✨",
    "Zindagi ek safar hai suhana, yahan kal kya ho kisne jaana! 🎶",
    "Tu jo muskura de to baatein bani rahe, zindagi teri ada pe fida hai! 💕"
]

# 🎯 Message Handler (Sabhi Messages Ko Handle Karega)
@bot.message_handler(func=lambda message: True)
def handle_messages(message):
    text = message.text.lower()

    if "hello" in text or "hi" in text:
        bot.reply_to(message, random.choice(funny_replies))
    
    elif "/joke" in text:
        bot.reply_to(message, get_joke())

    elif "/quote" in text:
        bot.reply_to(message, get_quote())

    elif "/shayari" in text:
        bot.reply_to(message, random.choice(shayari_list))

    elif "/roast" in text:
        bot.reply_to(message, random.choice(roasts))

    elif bot.get_me().username.lower() in text:
        bot.reply_to(message, "Bhai mujhe tag kyun kiya? Koi kaam batao! 😜")

    else:
        bot.reply_to(message, random.choice(funny_replies))

# 🚀 Start the Bot
print("🤖 Bot is running... Join the fun!")
bot.polling(none_stop=True)
