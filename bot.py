import os
import ast
import operator as op
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, filters, ContextTypes

TOKEN = os.getenv("TOKEN")

# safe operators
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
        "⚡ Calculator Bot\n\n"
        "Send any math:\n"
        "`10*1.5`  `0.002+0.01`\n\n"
        "Fast • Simple • Powerful\n"
        "ℹ️ /help",
        parse_mode="Markdown"
    )

# /help
async def help_cmd(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "📖 Usage:\n\n"
        "`1+1`  `5-2`\n"
        "`2*3`  `10/2`\n"
        "`(2+3)*5`\n\n"
        "Supports:\n"
        "+  -  *  /  %  **\n\n"
        "Works in groups ✅",
        parse_mode="Markdown"
    )

# calculator
async def calculate(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not update.message or not update.message.text:
        return

    text = update.message.text.replace(" ", "").split("@")[0]

    try:
        result = safe_eval(text)

        # clean float output (like 5.0 → 5)
        if isinstance(result, float) and result.is_integer():
            result = int(result)

        await update.message.reply_text(f"🧮 {text} = {result}")

    except Exception:
        return  # ignore invalid messages


# run bot
app = ApplicationBuilder().token(TOKEN).build()

app.add_handler(CommandHandler("start", start))
app.add_handler(CommandHandler("help", help_cmd))
app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, calculate))

app.run_polling()
