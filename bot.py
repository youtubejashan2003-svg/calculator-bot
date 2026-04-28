import os
import ast
import operator as op
import re
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, filters, ContextTypes

TOKEN = os.getenv("TOKEN")

ops = {
    ast.Add: op.add,
    ast.Sub: op.sub,
    ast.Mult: op.mul,
    ast.Div: op.truediv,
    ast.Pow: op.pow,
    ast.Mod: op.mod,
    ast.USub: op.neg
}

def safe_eval(expr):
    def eval_node(node):
        if isinstance(node, ast.Constant):
            return node.value
        elif isinstance(node, ast.BinOp):
            return ops[type(node.op)](eval_node(node.left), eval_node(node.right))
        elif isinstance(node, ast.UnaryOp):
            return ops[type(node.op)](eval_node(node.operand))
        else:
            raise Exception("Invalid")
    return eval_node(ast.parse(expr, mode='eval').body)


# ✅ STRICT CHECK (ONLY REAL EXPRESSIONS)
def is_valid_expression(text):
    # must contain operator
    if not re.search(r"[+\-*/%]", text):
        return False

    # only numbers + operators allowed
    if not re.fullmatch(r"[0-9+\-*/%.() ]+", text):
        return False

    return True


# /start
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    name = update.effective_user.first_name

    await update.message.reply_text(
        f"Hello {name} 👋\n\n"
        "⚡ Fast Calculator Bot\n"
        "Works in DM & Groups\n\n"
        "➡️ Send any math expression\n"
        "Example: 2*2, 10+5, 100/4\n\n"
        "Use /help for more info\n\n"
        "👨‍💻 Developer: @tumlu"
    )


# /help
async def help_cmd(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "📌 How to use:\n\n"
        "बस calculation भेजो 👇\n\n"
        "✔ 10+10\n"
        "✔ 5*6\n"
        "✔ 100/4\n"
        "✔ 9-3\n\n"
        "❌ Invalid:\n"
        "hello\n"
        "100\n"
        "abc123\n\n"
        "Bot sirf valid math pe reply karega ⚡\n\n"
        "👨‍💻 Developer: @tumlu"
    )


# calculator
async def calculate(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not update.message or not update.message.text:
        return

    text = update.message.text.replace(" ", "").split("@")[0]

    # ❌ ignore invalid messages
    if not is_valid_expression(text):
        return

    try:
        result = safe_eval(text)

        if isinstance(result, float) and result.is_integer():
            result = int(result)

        await update.message.reply_text(f"{text} = {result}")

    except Exception:
        return  # no spam reply


app = ApplicationBuilder().token(TOKEN).build()

app.add_handler(CommandHandler("start", start))
app.add_handler(CommandHandler("help", help_cmd))
app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, calculate))

print("Bot running...")
app.run_polling()
