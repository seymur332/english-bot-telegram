"""User interaction handlers (commands, quiz, callbacks)."""
from telegram import Update
from telegram.constants import ParseMode
from telegram.ext import ContextTypes, CommandHandler, MessageHandler, CallbackQueryHandler, filters


from create_bot import application
from keyboards.client_kb import MAIN_MENU, TEST_CONFIRM, answer_kb, trainer_kb
from data.questions import QUESTIONS, VARIANTS, CORRECT


import random
import re
#import feedparser
from deep_translator import GoogleTranslator
import urllib.request
import xml.etree.ElementTree as ET
import ssl
import certifi  # обязательно установить: pip install certifi




PROPOSAL_INCORRECT = [
   ['lost','my','somewhere','I','keys','house','the','in'],
   ['the','Please','door','close','quietly'],
   ['slept','The','cat','on','windowsill','the'],
   ['in','soccer','played','the','They','schoolyard'],
   ['cafe','my','forgot','at','I','umbrella','the'],
   ['jumped','The','cat','the','onto','windowsill'],
   ['when','saw','He','old','friend','smiled','he','his']
]
PROPOSAL_CORRECT = [
   ['I','lost','my','keys','somewhere','in','the','house'],
   ['Please','close','the','door','quietly'],
   ['The','cat','slept','on','the','windowsill'],
   ['They','played','soccer','in','the','schoolyard'],
   ['I','forgot','my','umbrella','at','the','cafe'],
   ['The','cat','jumped','onto','the','windowsill'],
   ['He','smiled','when','he','saw','his','old','friend']
]
NEW_WORDS = [
   "apple - яблоко","book-книга","walk-гулять",
   "cucumber-огурец","eggplant-баклажан"
]


#translate the words from en->ru and from ru->en
def translate_text(text:str)->str:
   is_eng = bool(re.search(r"[A-Za-z]",text))
   src,tgt =("en","ru") if is_eng else ("ru","en")
   try:
       return GoogleTranslator(source=src,target=tgt).translate(text)
   except Exception:
       return "Ошибка перевода! Попробуйте еще раз!"
  




def get_news_text(limit: int = 3) -> str:
   url = "https://feeds.bbci.co.uk/news/rss.xml"
   headers = {"User-Agent": "Mozilla/5.0"}
   req = urllib.request.Request(url, headers=headers)


   # Создаём SSL-контекст с валидными сертификатами
   context = ssl.create_default_context(cafile=certifi.where())


   try:
       with urllib.request.urlopen(req, context=context, timeout=10) as response:
           xml_data = response.read()
   except Exception as e:
       return f"⚠️ Ошибка загрузки: {e}"


   try:
       root = ET.fromstring(xml_data)
       items = root.findall("./channel/item")
       if not items:
           return "⚠️ Лента пуста."


       news_items = []
       for item in items[:limit]:
           title = item.findtext("title", default="(Без заголовка)")
           link = item.findtext("link", default="")
           news_items.append(f"🔹 <b>{title}</b>\n{link}")


       return "\n\n".join(news_items)


   except Exception as e:
       return f"⚠️ Ошибка обработки XML: {e}"




# Helper to register handlers automatically on import
def register_handlers():
   application.add_handler(CommandHandler(['start', 'help'], start))
   application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, menu_router))
   application.add_handler(CallbackQueryHandler(answer_callback, pattern='^(right|wrong)$'))


# ---- Handlers ----


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
   await update.message.reply_text(
       "👋 Привет! Я бот для практики английского языка. Выбери действие:",
       reply_markup=MAIN_MENU
   )


async def menu_router(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
   text = update.message.text
   if text == "Тестирование 📝":
       await update.message.reply_text(
           "Тест состоит из 5 вопросов. Готов?", reply_markup=TEST_CONFIRM
       )
   elif text == "Да":
       context.user_data['score'] = 0
       context.user_data['idx'] = 0
       await send_question(update, context, 0)
   elif text in {"Нет", "Назад ◀️"}:
       await update.message.reply_text("Возврат в меню", reply_markup=MAIN_MENU)
   elif text == "Тренажёр 🏋🏼":
       await update.message.reply_text("Выбери режим тренажера", reply_markup=trainer_kb)
   elif text == "Новое слово":
       word = random.choice(NEW_WORDS)
       await update.message.reply_text(f"Слово дня:\n<b>{word}</b>",parse_mode=ParseMode.HTML)
   elif text == "Собери предложение":
       idx = random.randint(0,len(PROPOSAL_INCORRECT)-1)
       words = PROPOSAL_INCORRECT[idx]
       context.user_data["translate_idx"] = idx
       context.user_data["translate_attempt"] = 0
       await update.message.reply_text(
           f"Собери правильное предложение из слов:\n<code>{' '.join(words)}</code>",
           parse_mode=ParseMode.HTML
       )
   elif context.user_data.get("translate_idx") is not None:
       idx = context.user_data["translate_idx"]
       attempt = update.message.text.strip().split()
       correct = PROPOSAL_CORRECT[idx]
       if attempt == correct:
           await update.message.reply_text("Правильно!",reply_markup=trainer_kb)
           context.user_data["translate_idx"] = None
       else:
           context.user_data["translate_attempt"]+=1
           await update.message.reply_text("Не правильно! Попробуй еще раз!")
   elif text == "Новости 📰":
       news = get_news_text()
       from telegram.helpers import escape
       if news.startswith("⚠️"):
           # ошибка: выводим без форматирования
           await update.message.reply_text(news)
       else:
           await update.message.reply_text(
               f"<b>Последние новости:</b>\n\n{escape(news)}",
               parse_mode=ParseMode.HTML,
               disable_web_page_preview=True
           )


   elif text == "Перевод слова":
       context.user_data["translation_mode"]=True
       await update.message.reply_text(
           "Отправь слово или фразу для перевода.\n"
           "Для выхода нажми \"Hазад\".",
           reply_markup = MAIN_MENU
       )
   elif context.user_data.get("translation_mode"):
       result = translate_text(text)
       await update.message.reply_text(f"->{result}")
   elif text == "Назад ◀️":
       await update.message.reply_text("Возврат в меню", reply_markup=MAIN_MENU)
   else:
       await update.message.reply_text("Я понимаю только кнопки меню 🙂", reply_markup=MAIN_MENU)


async def send_question(update: Update, context: ContextTypes.DEFAULT_TYPE, idx: int) -> None:
   if idx < len(QUESTIONS):
       await update.effective_chat.send_message(
           QUESTIONS[idx],
           reply_markup=answer_kb(VARIANTS[idx], CORRECT[idx])
       )
   else:
       score = context.user_data.get('score', 0)
       if score <= 1:
           level = 'Elementary'
       elif score <= 3:
           level = 'Intermediate'
       else:
           level = 'Advanced'


       await update.effective_chat.send_message(
           f"✅ Тест завершён!\n<b>{score}/{len(QUESTIONS)}</b> правильных ответов\n"
           f"Ваш уровень: <b>{level}</b>",
           parse_mode=ParseMode.HTML,
           reply_markup=MAIN_MENU
       )


async def answer_callback(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
   query = update.callback_query
   await query.answer()


   idx = context.user_data.get('idx', 0)
   if query.data == 'right':
       context.user_data['score'] = context.user_data.get('score', 0) + 1
   context.user_data['idx'] = idx + 1


   # edit original message to show tick/cross
   mark = "✅" if query.data == 'right' else "❌"
   await query.edit_message_reply_markup(reply_markup=None)
   await query.edit_message_text(f"{mark} {query.message.text}")


   await send_question(update, context, context.user_data['idx'])


# Register handlers at import time
register_handlers()
