import re
import os
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, filters, ContextTypes

TOKEN = os.getenv("TOKEN")

# /start (only DM)
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.effective_chat.type != "private":
        return
    await update.message.reply_text(
        "🤖 Calculator Bot\n\n"
        "Send any calculation:\n"
        "• 1+1\n• 2*2\n• 10/2\n\n"
        "⚡ Instant answer in groups & DM\n\n"
        "ℹ️ /help for guide\n"
        "👨‍💻 Developer - @tumlu"
    )

# /help
async def help_cmd(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "📖 Usage Guide\n\n"
        "Just send:\n"
        "• 1+1 → 2\n"
        "• 5-3 → 2\n"
        "• 4*2 → 8\n"
        "• 10/2 → 5\n\n"
        "Works in groups too ✅\n\n"
        "👨‍💻 Developer - @tumlu"
    )

# Calculator
async def calculate(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not update.message:
        return

    text = update.message.text
    if not text:
        return

    # clean text
    text = text.replace(" ", "").split("@")[0]

    match = re.match(r"^(-?\d+)([\+\-\*/])(-?\d+)$", text)
    if not match:
        return

    num1, operator, num2 = match.groups()
    num1, num2 = int(num1), int(num2)

    try:
        if operator == "+":
            result = num1 + num2
            op = "+"
        elif operator == "-":
            result = num1 - num2
            op = "-"
        elif operator == "*":
            result = num1 * num2
            op = "×"
        elif operator == "/":
            result = num1 / num2
            op = "÷"

        await update.message.reply_text(f"{num1} {op} {num2} = {result}")

    except:
        pass

def main():
    app = ApplicationBuilder().token(TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("help", help_cmd))

    # IMPORTANT (group + DM dono ke liye)
    app.add_handler(MessageHandler(filters.TEXT, calculate))

    app.run_polling()

if __name__ == "__main__":
    main()
