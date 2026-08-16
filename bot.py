import os
from openai import OpenAI
from telegram import Update, ReplyKeyboardMarkup
from telegram.ext import (
    Application,
    CommandHandler,
    MessageHandler,
    ContextTypes,
    filters,
)

TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

client = OpenAI(api_key=OPENAI_API_KEY)

SYSTEM_PROMPT = """
Ты — ИИ-Завуч РК, профессиональный помощник заместителя директора
школы Республики Казахстан по учебной работе.

Ты помогаешь завучу:
- составлять приказы;
- готовить справки ВШК;
- составлять планы внутришкольного контроля;
- готовить педагогические советы;
- составлять протоколы;
- анализировать уроки;
- готовить объявления педагогам;
- составлять аналитические справки;
- готовить планы методической работы;
- работать с нормативными документами системы образования РК.

Пиши профессионально, грамотно и естественно.
Для официальных документов используй официально-деловой стиль.
Учитывай специфику системы образования Республики Казахстан.

Если запрос понятен и данных достаточно, сразу выполняй задачу и выдавай готовый результат. Не задавай лишних уточняющих вопросов.
Если каких-то данных не хватает, но без них можно подготовить качественный вариант, самостоятельно используй нейтральную формулировку или оставь место для заполнения.
Уточняющий вопрос задавай только тогда, когда без ответа действительно невозможно выполнить задачу. Не выдумывай номера и даты нормативных документов.
"""

keyboard = [
    ["📄 Приказ", "📊 Справка ВШК"],
    ["📋 План ВШК", "🎓 Педсовет"],
    ["📝 Протокол", "🔎 Анализ урока"],
    ["📢 Объявление", "🤖 Спросить ИИ"],
]

markup = ReplyKeyboardMarkup(
    keyboard,
    resize_keyboard=True
)


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = (
        "Здравствуйте! 👋\n\n"
        "Я — ИИ-Завуч РК 🇰🇿\n"
        "Помощник заместителя директора школы.\n\n"
        "Выберите нужный раздел ниже или просто напишите свой вопрос."
    )

    await update.message.reply_text(
        text,
        reply_markup=markup
    )


async def answer(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_text = update.message.text
    if user_text == "🤖 Спросить ИИ":
        await update.message.reply_text(
            "Напишите свой вопрос по работе заместителя директора школы — я постараюсь помочь."
        )
        return

    

    
    
    
    
    prompts = {
        "📄 Приказ":
            "Помоги составить приказ по школе. "
            "Спроси тему приказа и необходимые данные.",

        "📊 Справка ВШК":
            "Помоги подготовить аналитическую справку "
            "по внутришкольному контролю. Сначала уточни тему контроля.",

        "📋 План ВШК":
            "Помоги составить профессиональный план "
            "внутришкольного контроля.",

        "🎓 Педсовет":
            "Помоги подготовить педагогический совет. "
            "Сначала уточни тему и цель.",

        "📝 Протокол":
            "Помоги составить протокол в формате "
            "СЛУШАЛИ — ВЫСТУПИЛИ — РЕШИЛИ.",

        "🔎 Анализ урока":
            "Помоги провести профессиональный анализ урока. "
            "Уточни предмет, класс, тему и цель посещения.",

        "📢 Объявление":
            "Помоги написать краткое и грамотное "
            "объявление для педагогического коллектива.",

        "🤖 Спросить ИИ":
            "Предложи пользователю написать любой вопрос "
            "по работе заместителя директора школы."
    }

    question = prompts.get(user_text, user_text)

    try:
        response = client.responses.create(
            model="gpt-4.1-mini",
            instructions=SYSTEM_PROMPT,
            input=question
        )

        await update.message.reply_text(
            response.output_text
        )

    except Exception as e:
        print(e)
        await update.message.reply_text(
            "Не удалось получить ответ ИИ. Попробуйте ещё раз."
        )


def main():
    if not TELEGRAM_TOKEN:
        raise RuntimeError("TELEGRAM_TOKEN не задан")

    if not OPENAI_API_KEY:
        raise RuntimeError("OPENAI_API_KEY не задан")

    app = Application.builder().token(TELEGRAM_TOKEN).build()

    app.add_handler(CommandHandler("start", start))

    app.add_handler(
        MessageHandler(
            filters.TEXT & ~filters.COMMAND,
            answer
        )
    )

    print("ИИ-Завуч РК запущен")

    app.run_polling()


if __name__ == "__main__":
    main()
