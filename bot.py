from telegram import Update, ChatPermissions
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, CallbackContext
from textblob import TextBlob
from tinydb import TinyDB, Query
import random
import time

TOKEN = "YOUR_BOT_TOKEN"

# Database setup for user stats & custom replies
db = TinyDB('data.json')
stats_table = db.table('stats')
replies_table = db.table('custom_replies')

# List of bad words to delete
BAD_WORDS = ["badword1", "badword2", "examplebadword"]

# Rock-Paper-Scissors choices
RPS_CHOICES = ["Rock", "Paper", "Scissors"]

# User Stats - Track messages
def track_user(update: Update):
    user_id = update.message.from_user.id
    stats_table.upsert({"user_id": user_id, "messages": stats_table.get(Query().user_id == user_id)['messages'] + 1 if stats_table.get(Query().user_id == user_id) else 1}, Query().user_id == user_id)

# Admin Command - Ban User
def ban(update: Update, context: CallbackContext):
    if update.message.reply_to_message:
        context.bot.ban_chat_member(update.message.chat_id, update.message.reply_to_message.from_user.id)
        update.message.reply_text("🚨 User banned!")

# Admin Command - Mute User
def mute(update: Update, context: CallbackContext):
    if update.message.reply_to_message:
        context.bot.restrict_chat_member(update.message.chat_id, update.message.reply_to_message.from_user.id, ChatPermissions(can_send_messages=False))
        update.message.reply_text("🔇 User muted!")

# Admin Command - Kick User
def kick(update: Update, context: CallbackContext):
    if update.message.reply_to_message:
        context.bot.kick_chat_member(update.message.chat_id, update.message.reply_to_message.from_user.id)
        update.message.reply_text("👢 User kicked!")

# Custom Replies
def custom_reply(update: Update):
    user_text = update.message.text.lower()
    custom_response = replies_table.get(Query().trigger == user_text)
    if custom_response:
        update.message.reply_text(custom_response['response'])

# Add Custom Reply Command
def add_reply(update: Update, context: CallbackContext):
    if len(context.args) >= 2:
        trigger = context.args[0].lower()
        response = " ".join(context.args[1:])
        replies_table.upsert({"trigger": trigger, "response": response}, Query().trigger == trigger)
        update.message.reply_text(f"✅ Custom reply added for '{trigger}'!")
    else:
        update.message.reply_text("Usage: /addreply <trigger> <response>")

# AI-Powered Response with Stylish Text
def stylish_text(text):
    styles = ["𝓢𝓽𝔂𝓵𝓲𝓼𝓱", "Ⓢⓣⓨⓛⓘⓢⓗ", "🅂🅃🅈🄻🄸🅂🄷", "🆂🆃🆈🅻🅸🆂🅷"]
    return f"{random.choice(styles)} ➤ {text}"

def chat_ai(update: Update):
    user_text = update.message.text
    words = user_text.split()
    
    # Anti-Spam Filter (Detect Repeated Words)
    if len(words) != len(set(words)):
        update.message.reply_text("🚫 Stop spamming!")
        return
    
    # Check for bad words & delete message
    if any(bad_word in user_text.lower() for bad_word in BAD_WORDS):
        update.message.delete()
        update.message.reply_text("⚠️ Watch your language!")
        return
    
    # AI-Powered Response
    blob = TextBlob(user_text)
    response = stylish_text("That sounds great! 😊") if blob.sentiment.polarity > 0 else stylish_text("Hmm, tell me more... 🤔")
    update.message.reply_text(response)

# Games - Rock Paper Scissors
def play_rps(update: Update, context: CallbackContext):
    bot_choice = random.choice(RPS_CHOICES)
    user_choice = context.args[0].capitalize() if context.args else ""
    
    if user_choice not in RPS_CHOICES:
        update.message.reply_text("🎮 Choose Rock, Paper, or Scissors! Example: `/rps Rock`")
        return
    
    result = "🤝 It's a tie!" if user_choice == bot_choice else "✅ You win!" if (user_choice, bot_choice) in [("Rock", "Scissors"), ("Paper", "Rock"), ("Scissors", "Paper")] else "❌ You lose!"
    
    update.message.reply_text(f"🎮 You: {user_choice}\n🤖 Bot: {bot_choice}\n{result}")

# Trivia Game
def trivia(update: Update):
    questions = {
        "What is the capital of France?": "Paris",
        "Who wrote 'Romeo and Juliet'?": "Shakespeare",
        "What is 5 + 7?": "12",
    }
    question, answer = random.choice(list(questions.items()))
    update.message.reply_text(f"🧠 Trivia Time: {question}")
    time.sleep(5)
    update.message.reply_text(f"✅ Answer: {answer}")

# Command Handlers
def main():
    updater = Updater(TOKEN, use_context=True)
    dp = updater.dispatcher

    # Admin Commands
    dp.add_handler(CommandHandler("ban", ban))
    dp.add_handler(CommandHandler("mute", mute))
    dp.add_handler(CommandHandler("kick", kick))

    # Custom Reply Commands
    dp.add_handler(CommandHandler("addreply", add_reply))

    # Games
    dp.add_handler(CommandHandler("rps", play_rps))
    dp.add_handler(CommandHandler("trivia", trivia))

    # Message Handlers
    dp.add_handler(MessageHandler(Filters.text & ~Filters.command, track_user))
    dp.add_handler(MessageHandler(Filters.text & ~Filters.command, custom_reply))
    dp.add_handler(MessageHandler(Filters.text & ~Filters.command, chat_ai))

    updater.start_polling()
    updater.idle()

if __name__ == '__main__':
    main()
