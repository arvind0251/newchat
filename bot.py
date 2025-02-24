import logging
import torch
from transformers import AutoModelForCausalLM, AutoTokenizer
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup, InputFile
from telegram.ext import (ApplicationBuilder, CommandHandler, MessageHandler, filters, CallbackContext)

# 🔑 Bot Token (Replace this with your actual bot token)
TOKEN = "8092574352:AAHlKwKMGuaEhQhwY47_x6M_sbko8okTgy8"
OWNER_USERNAME = "@RU_DRA_65"
GROUP_LINK = "https://t.me/@RU_DRA_098"

# 🤖 Load GPT-2 Model & Tokenizer
device = "cuda" if torch.cuda.is_available() else "cpu"
model_name = "microsoft/DialoGPT-medium"
tokenizer = AutoTokenizer.from_pretrained(model_name)
model = AutoModelForCausalLM.from_pretrained(model_name).to(device)

# 📌 Logging setup
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)
logger = logging.getLogger(__name__)

# 🤖 Generate AI Response
def generate_response(user_input):
    inputs = tokenizer.encode(user_input + tokenizer.eos_token, return_tensors="pt").to(device)
    response_ids = model.generate(inputs, max_length=1000, pad_token_id=tokenizer.eos_token_id)
    response = tokenizer.decode(response_ids[:, inputs.shape[-1]:][0], skip_special_tokens=True)
    return response

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
