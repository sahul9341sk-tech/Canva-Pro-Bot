from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update
from telegram.ext import (
Application,
CommandHandler,
CallbackQueryHandler,
MessageHandler,
ContextTypes,
filters,
)

TOKEN = "8259663640:AAFSYEKdjNUSZVTFLZehjLwZDax9blzqBZw"
INVITE_LINK = "https://www.canva.com/brand/join?token=TCz8bsmAp69E5Skd3A6pZw&brandingVariant=edu&referrer=team-invite"
ADMIN_ID = 7227441999

users = {}

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

async def plan_selected(update: Update, context: ContextTypes.DEFAULT_TYPE):
query = update.callback_query
await query.answer()

users[query.from_user.id] = query.data

file_name = f"qr{query.data}.jpg"

await query.message.reply_photo(
    photo=open(file_name, "rb"),
    caption="Payment karke screenshot bhejiye."
)

async def receive_screenshot(update: Update, context: ContextTypes.DEFAULT_TYPE):
user = update.message.from_user

if not update.message.photo:
    return

keyboard = [[
    InlineKeyboardButton(
        "✅ Approve",
        callback_data=f"approve_{user.id}"
    ),
    InlineKeyboardButton(
        "❌ Reject",
        callback_data=f"reject_{user.id}"
    )
]]

await context.bot.send_photo(
    chat_id=ADMIN_ID,
    photo=update.message.photo[-1].file_id,
    caption=f"""

New Payment Screenshot

User: @{user.username}
User ID: {user.id}
Plan: {users.get(user.id, 'Unknown')}
""",
reply_markup=InlineKeyboardMarkup(keyboard)
)

await update.message.reply_text(
    "Payment screenshot received. Please wait for admin approval."
)

async def admin_action(update: Update, context: ContextTypes.DEFAULT_TYPE):
query = update.callback_query
await query.answer()

action, user_id = query.data.split("_")
user_id = int(user_id)

if action == "approve":
    await context.bot.send_message(
        chat_id=user_id,
        text=f"✅ Payment Approved\n\nCanva Invite Link:\n{INVITE_LINK}"
    )

    await query.edit_message_caption(
        caption="✅ Payment Approved"
    )

else:
    await context.bot.send_message(
        chat_id=user_id,
        text="❌ Payment Rejected. Please contact admin."
    )

    await query.edit_message_caption(
        caption="❌ Payment Rejected"
    )

app = Application.builder().token(TOKEN).build()

app.add_handler(CommandHandler("start", start))
app.add_handler(CallbackQueryHandler(plan_selected, pattern="^(149|199|299)$"))
app.add_handler(CallbackQueryHandler(admin_action, pattern="^(approve|reject)_"))
app.add_handler(MessageHandler(filters.PHOTO, receive_screenshot))

app.run_polling()
