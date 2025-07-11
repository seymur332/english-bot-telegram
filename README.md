📘 English Bot Telegram
Описание проекта
Telegram‑бот для изучения английского языка, написанный на Python 3. Он помогает расширить словарный запас, улучшить понимание и тренировать навыки через различные команды:

/send_quote — случайная мотивационная цитата

/send_podcast — ссылка на подкаст

/word — новое слово для изучения

/repeat_word — повторение ранее выученного слова

/get_learned_words — список изученных слов

/get_words_to_repeat — слова, которые нужно повторить

/get_mem — смешное мем‑изображение из Reddit

/read_easy_news, /read_hard_news, /read_business_news — новости разного уровня сложности

🚀 Быстрый старт
Клонируй репозиторий:

bash
Copy
Edit
git clone https://github.com/seymur332/english-bot-telegram.git
cd english-bot-telegram
Создай виртуальное окружение и активируй его:

bash
Copy
Edit
python3 -m venv venv
source venv/bin/activate  # Linux/macOS
venv\Scripts\activate     # Windows
Установи зависимости:

bash
Copy
Edit
pip install -r requirements.txt
Создай файл .env рядом с main.py с такими переменными:

ini
Copy
Edit
BOT_TOKEN=ваш_токен_бота
REDDIT_CLIENT_ID=...
REDDIT_SECRET=...
REDDIT_USER_AGENT=...

Запусти проект в VS Code:

Открой папку проекта в VS Code.

Убедись, что виртуальное окружение выбрано (Ctrl+Shift+P → Python: Select Interpreter).

Запусти main.py, нажав ▶️ в строке запуска.

Альтернативный способ — из командной строки:

bash
Copy
Edit
python main.py
🛠 Структура репозитория
bash
Copy
Edit
english-bot-telegram/
├── main.py                # точка входа
├── requirements.txt       # список зависимостей
├── bot/                   # модули с командами бота
│   ├── quotes.py
│   ├── words.py
│   └── news.py
├── utils/                 # вспомогательные функции (реддит, API и пр.)
├── .env.example           # пример файла с переменными среды
└── README.md
