import os
import ast
import operator as op
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, filters, ContextTypes

TOKEN = os.getenv("TOKEN")

# operators
ops = {
    ast.Add: op.add,
    ast.Sub: op.sub,
    ast.Mult: op.mul,
    ast.Div: op.truediv,
    ast.Pow: op.pow,
    ast.Mod: op.mod,
    ast.USub: op.neg
}

# safe eval
def safe_eval(expr):
    def eval_node(node):
        if isinstance(node, ast.Num):
            return node.n
        elif isinstance(node, ast.BinOp):
            return ops[type(node.op)](eval_node(node.left), eval_node(node.right))
        elif isinstance(node, ast.UnaryOp):
            return ops[type(node.op)](eval_node(node.operand))
        else:
            raise Exception("Invalid")

    return eval_node(ast.parse(expr, mode='eval').body)


# /start
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.effective_chat.type != "private":
        return
    await update.message.reply_text(
        "⚡ Advanced Calculator\n\n"
        "Try: 10*10\n"
        "Supports: + - * / % ** ( )\n\n"
        "ℹ️ /help\n"
        "dev - @tumlu"
    )

# /help
async def help_cmd(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "📖 Examples:\n\n"
        "10*10\n"
        "1.5*10\n"
        "(2+3)*5\n\n"
        "Just send calculation.\n"
        "Works everywhere ✅\n\n"
        "dev - @tumlu"
    )

# calculator
async def calculate(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not update.message or not update.message.text:
        return

    text = update.message.text.replace(" ", "").split("@")[0]

    try:
        result = safe_eval(text)

        if isinstance(result, float) and result.is_integer():
            result = int(result)

        await update.message.reply_text(f"{text} = ({result})")

    except Exception:
        return


# run bot
app = ApplicationBuilder().token(TOKEN).build()

app.add_handler(CommandHandler("start", start))
app.add_handler(CommandHandler("help", help_cmd))
app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, calculate))

app.run_polling()
