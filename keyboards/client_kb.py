from telegram import ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardMarkup, InlineKeyboardButton


# --- Reply Keyboards (main menu & sub‑menus) ---

translate_btn = KeyboardButton("Перевод слова")
MAIN_MENU = ReplyKeyboardMarkup(
   keyboard=[
       [KeyboardButton("Тестирование 📝"), KeyboardButton("Материал 📚")],
       [KeyboardButton("Новости 📰"), KeyboardButton("Тренажёр 🏋🏼")],
       [translate_btn]
   ],
   resize_keyboard=True
)


TEST_CONFIRM = ReplyKeyboardMarkup(
   keyboard=[[KeyboardButton("Да"), KeyboardButton("Нет")]],
   resize_keyboard=True
)


# --- Inline Keyboard for quiz answers ---


def answer_kb(answers: list[str], correct: str) -> InlineKeyboardMarkup:
   """Create inline kb with 'right' / 'wrong' callback_data"""
   buttons = [
       [InlineKeyboardButton(text=a, callback_data='right' if a == correct else 'wrong')]
       for a in answers
   ]
   return InlineKeyboardMarkup(buttons)
trainer_kb = ReplyKeyboardMarkup(
   keyboard=[
      [KeyboardButton("Новое слово")],
      [KeyboardButton("Собери предложение")],
      [KeyboardButton("Назад")],
   ],
   resize_keyboard=True
)
