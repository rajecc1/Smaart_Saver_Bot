import logging
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ApplicationBuilder, ContextTypes, CommandHandler, MessageHandler, filters, CallbackQueryHandler

TOKEN = '8623046652:AAF_201pX_nnlDHyrJVtZ6Fvii3paPSY5WM'

logging.basicConfig(level=logging.INFO)

LANGS = {
    'ru': {'greet': "🇷🇺 Выбран русский язык. Напиши товар для поиска:", 'search': "Ищу"},
    'ua': {'greet': "🇺🇦 Обрано українську мову. Напишіть товар для пошуку:", 'search': "Шукаю"},
    'cz': {'greet': "🇨🇿 Byla zvolena čeština. Napište název zboží:", 'search': "Hledám"}
}

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    keyboard = [[
        InlineKeyboardButton("🇷🇺 RU", callback_data='set_ru'),
        InlineKeyboardButton("🇺🇦 UA", callback_data='set_ua'),
        InlineKeyboardButton("🇨🇿 CZ", callback_data='set_cz')
    ]]
    await update.message.reply_text("Выберите язык / Оберіть мову / Vyberte jazyk:", reply_markup=InlineKeyboardMarkup(keyboard))

async def set_language(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    lang = query.data.split('_')[1]
    context.user_data['lang'] = lang
    await query.edit_message_text(LANGS[lang]['greet'])

async def search(update: Update, context: ContextTypes.DEFAULT_TYPE):
    lang = context.user_data.get('lang', 'ru')
    query_text = update.message.text
    s = query_text.replace(" ", "+")
    keyboard = [
        [InlineKeyboardButton("🇨🇿 Heureka.cz", url=f"https://www.heureka.cz/?h%5Bfraze%5D={s}")],
        [InlineKeyboardButton("🇺🇦 Hotline.ua", url=f"https://hotline.ua/sr/?q={s}")],
        [InlineKeyboardButton("🇪🇺 Amazon.de", url=f"https://www.amazon.de/s?k={s}")]
    ]
    await update.message.reply_text(f"🔍 {LANGS[lang]['search']} '{query_text}':", reply_markup=InlineKeyboardMarkup(keyboard))

if __name__ == '__main__':
    app = ApplicationBuilder().token(TOKEN).build()
    app.add_handler(CommandHandler('start', start))
    app.add_handler(CallbackQueryHandler(set_language, pattern='^set_'))
    app.add_handler(MessageHandler(filters.TEXT & (~filters.COMMAND), search))
    app.run_polling()
