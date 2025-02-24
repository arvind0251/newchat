import logging
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, CallbackContext, CallbackQueryHandler

# 🔑 Bot ke Token aur IDs (Replace karein)
TOKEN = "8092574352:AAHlKwKMGuaEhQhwY47_x6M_sbko8okTgy8"
OWNER_ID_1 = "7408008545"
OWNER_ID_2 = "7256617868"
SUPPORT_CHANNEL = "https://t.me/@RU_DRA_098"

# 📌 Logging setup
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)
logger = logging.getLogger(__name__)

# ⚙️ Features ko control karne ka system
enabled_features = {
    "stats": True,
    "spam_filter": True,
    "bad_words": True,
    "custom_replies": True,
    "games": True,
    "admin_commands": True,
    "welcome": True,
    "yt_downloader": True,
    "sticker_converter": True,
    "ai_chatbot": True,
    "auto_responder": True,
    "insta_downloader": True
}

# 🚫 Bad words filter
bad_words = ["badword1", "badword2"]

# 📝 Custom Replies
custom_replies = {"hello": "Hi there!", "bye": "Goodbye!"}

# 🏠 Start Command
def start(update: Update, context: CallbackContext) -> None:
    keyboard = [
        [InlineKeyboardButton("Enable/Disable Features", callback_data='toggle_features')],
        [InlineKeyboardButton("Owner 1", url=f"tg://user?id={OWNER_ID_1}"),
         InlineKeyboardButton("Owner 2", url=f"tg://user?id={OWNER_ID_2}")],
        [InlineKeyboardButton("Support Channel", url=SUPPORT_CHANNEL)]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    update.message.reply_text("Welcome! Choose an option:", reply_markup=reply_markup)

# 🔄 Features Enable/Disable karne ka command
def toggle_features(update: Update, context: CallbackContext) -> None:
    query = update.callback_query
    keyboard = [[InlineKeyboardButton(f"{key} - {'ON' if val else 'OFF'}", callback_data=key)] for key, val in enabled_features.items()]
    query.message.reply_text("Click to toggle features:", reply_markup=InlineKeyboardMarkup(keyboard))

def feature_toggle(update: Update, context: CallbackContext) -> None:
    query = update.callback_query
    feature = query.data
    enabled_features[feature] = not enabled_features[feature]
    query.answer(f"{feature} is now {'enabled' if enabled_features[feature] else 'disabled'}!")
    toggle_features(update, context)

# 🎉 Auto-Welcome Message
def welcome(update: Update, context: CallbackContext) -> None:
    if enabled_features["welcome"]:
        for member in update.message.new_chat_members:
            update.message.reply_text(f"Welcome {member.full_name}!")

# 🎥 YouTube Downloader (Dummy Response)
def youtube_download(update: Update, context: CallbackContext) -> None:
    if enabled_features["yt_downloader"] and context.args:
        url = context.args[0]
        update.message.reply_text(f"Downloading YouTube video from: {url}")

# 🖼️ Sticker to Image Converter (Dummy Response)
def sticker_to_image(update: Update, context: CallbackContext) -> None:
    if enabled_features["sticker_converter"] and update.message.sticker:
        update.message.reply_text("Sticker converted to image!")

# 🤖 AI Chatbot Response
def ai_chatbot(update: Update, context: CallbackContext) -> None:
    if enabled_features["ai_chatbot"]:
        update.message.reply_text(f"AI Response: {update.message.text}")

# 🔁 Auto-Responder
def auto_responder(update: Update, context: CallbackContext) -> None:
    if enabled_features["auto_responder"] and update.message.text.lower() in custom_replies:
        update.message.reply_text(custom_replies[update.message.text.lower()])

# 📲 Instagram Reel Downloader (Dummy Response)
def insta_download(update: Update, context: CallbackContext) -> None:
    if enabled_features["insta_downloader"] and context.args:
        url = context.args[0]
        update.message.reply_text(f"Downloading Instagram reel from: {url}")

# 🚀 **Main Function (Bot Initialization)**
def main() -> None:
    updater = Updater(TOKEN)
    dp = updater.dispatcher

    # 🔥 Commands Handlers
    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(CommandHandler("yt", youtube_download))
    dp.add_handler(CommandHandler("insta", insta_download))
    
    # 📌 Callback Handlers
    dp.add_handler(CallbackQueryHandler(toggle_features, pattern='toggle_features'))
    dp.add_handler(CallbackQueryHandler(feature_toggle))
    
    # 📨 Message Handlers
    dp.add_handler(MessageHandler(Filters.status_update.new_chat_members, welcome))
    dp.add_handler(MessageHandler(Filters.sticker, sticker_to_image))
    dp.add_handler(MessageHandler(Filters.text & ~Filters.command, ai_chatbot))
    dp.add_handler(MessageHandler(Filters.text & ~Filters.command, auto_responder))

    # 🔄 Polling System
    updater.start_polling()
    updater.idle()

# 🔥 **Bot Execution**
if __name__ == '__main__':
    main()
