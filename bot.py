from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update
from telegram.ext import Application, CommandHandler, CallbackQueryHandler, ContextTypes

TOKEN = "8259663640:AAFSYEKdjNUSZVTFLZehjLwZDax9blzqBZw"
INVITE_LINK = "https://www.canva.com/brand/join?token=TCz8bsmAp69E5Skd3A6pZw&brandingVariant=edu&referrer=team-invite"

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    keyboard = [
        [InlineKeyboardButton("1 Year ₹149", callback_data="149")],
        [InlineKeyboardButton("2 Years ₹199", callback_data="199")],
        [InlineKeyboardButton("3 Years ₹299", callback_data="299")]
    ]

    await update.message.reply_text(
        "Choose Canva Pro Plan",
        reply_markup=InlineKeyboardMarkup(keyboard)
    )

async def button(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()

    file_name = f"qr{query.data}.jpg"

    keyboard = [[
        InlineKeyboardButton("🎨 Canva Invite Link", url=INVITE_LINK)
    ]]

    await query.message.reply_photo(
        photo=open(file_name, "rb"),
        caption="Payment karke screenshot bhejiye.",
        reply_markup=InlineKeyboardMarkup(keyboard)
    )

app = Application.builder().token(TOKEN).build()

app.add_handler(CommandHandler("start", start))
app.add_handler(CallbackQueryHandler(button))

app.run_polling()
