from telegram import Update
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, CallbackContext
from textblob import TextBlob
import random

TOKEN = "YOUR_BOT_TOKEN"

# Stylish text conversion
def stylish_text(text):
    styles = ["𝓢𝓽𝔂𝓵𝓲𝓼𝓱", "Ⓢⓣⓨⓛⓘⓢⓗ", "🅂🅃🅈🄻🄸🅂🄷", "🆂🆃🆈🅻🅸🆂🅷"]
    return f"{random.choice(styles)} ➤ {text}"

# Welcome new members in groups
def welcome(update: Update, context: CallbackContext):
    for member in update.message.new_chat_members:
        update.message.reply_text(f"👋 Welcome, {member.first_name}! Enjoy the chat 😊")

# Command: /start
def start(update: Update, context: CallbackContext):
    chat_type = update.message.chat.type
    if chat_type == "private":
        update.message.reply_text("Hello! 🤖 I am your personal chatbot. Type anything, and I'll reply!")
    else:
        update.message.reply_text("Hey everyone! I'm active in this group. Mention me or talk normally!")

# Command: /help
def help_command(update: Update, context: CallbackContext):
    update.message.reply_text("🤖 I can:\n- Talk in **groups & private chats**\n- **Stylish text replies**\n- **AI-powered chat**\n- **Spam filtering**\n- **Auto-welcome new users**")

# AI-powered response for private & group chat
def chat_ai(update: Update, context: CallbackContext):
    user_text = update.message.text
    chat_type = update.message.chat.type

    # Spam protection (block repeated words)
    words = user_text.split()
    if len(words) != len(set(words)):
        update.message.reply_text("🚫 Stop spamming!")
        return

    # AI response based on message sentiment
    blob = TextBlob(user_text)
    if blob.sentiment.polarity > 0:
        response = stylish_text("That sounds great! 😊")
    else:
        response = stylish_text("Hmm, tell me more... 🤔")

    # Send reply based on chat type
    if chat_type == "private":
        update.message.reply_text(f"💬 {response}")  # Private chat
    else:
        update.message.reply_text(f"👥 {update.message.from_user.first_name}: {response}")  # Group chat

# Main function
def main():
    updater = Updater(TOKEN, use_context=True)
    dp = updater.dispatcher

    # Commands
    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(CommandHandler("help", help_command))

    # Welcome new members
    dp.add_handler(MessageHandler(Filters.status_update.new_chat_members, welcome))

    # Message handler for chat AI
    dp.add_handler(MessageHandler(Filters.text & ~Filters.command, chat_ai))

    updater.start_polling()
    updater.idle()

if __name__ == '__main__':
    main()
