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
        "🤖 Welcome to Calculator Bot!\n\n"
        "🧮 Use like:\n"
        "1+1\n2*2\n5-3\n10/2\n\n"
        "📌 Operators: + - * /\n\n"
        "Type /help for help.\n\n"
        "👨‍💻 Developer - @tumlu"
    )

# /help
async def help_cmd(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "📖 Help Menu\n\n"
        "Send simple calculations:\n\n"
        "1+1\n2*2\n5-2\n10/5\n\n"
        "Bot auto reply karega.\n\n"
        "👨‍💻 Developer - @tumlu"
    )

# Calculator
async def calculate(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = update.message.text.replace(" ", "")

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
        await update.message.reply_text("❌ Error")

def main():
    app = ApplicationBuilder().token(TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("help", help_cmd))
    app.add_handler(MessageHandler(filters.ALL, calculate))

    app.run_polling()

if __name__ == "__main__":
    main()
