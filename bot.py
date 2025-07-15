
import json
from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update
from telegram.ext import Updater, CommandHandler, CallbackQueryHandler, CallbackContext

# تحميل النقاط من ملف JSON
def load_data():
    try:
        with open("data.json", "r") as f:
            return json.load(f)
    except:
        return {}

# حفظ النقاط في ملف JSON
def save_data(data):
    with open("data.json", "w") as f:
        json.dump(data, f)

# أسئلة المسابقة
questions = [
    {
        "question": "ما هي عاصمة مصر؟",
        "options": ["القاهرة", "الرياض", "دمشق", "الخرطوم"],
        "answer": "القاهرة",
        "video": "https://youtube.com/@mahmuodtechnology"
    },
    {
        "question": "ما هو أسرع كائن حي؟",
        "options": ["الفهد", "السلحفاة", "النمر", "الحصان"],
        "answer": "الفهد",
        "video": "https://youtube.com/@mahmuodtechnology"
    },
    {
        "question": "ما هو عدد كواكب المجموعة الشمسية؟",
        "options": ["7", "8", "9", "10"],
        "answer": "8",
        "video": "https://youtube.com/@mahmuodtechnology"
    }
]

user_data = {}
question_index = {}

def start(update: Update, context: CallbackContext):
    user_id = str(update.effective_user.id)
    data = load_data()
    if user_id not in data:
        data[user_id] = 0
        save_data(data)
    question_index[user_id] = 0
    send_question(update, context)

def send_question(update: Update, context: CallbackContext):
    user_id = str(update.effective_user.id)
    idx = question_index.get(user_id, 0)
    if idx >= len(questions):
        update.message.reply_text("🎉 لقد أنهيت جميع الأسئلة!")
        return
    q = questions[idx]
    buttons = [
        [InlineKeyboardButton(opt, callback_data=opt)] for opt in q["options"]
    ]
    reply_markup = InlineKeyboardMarkup(buttons)
    context.bot.send_message(chat_id=update.effective_chat.id, text=f"❓ {q['question']}", reply_markup=reply_markup)

def button(update: Update, context: CallbackContext):
    query = update.callback_query
    query.answer()
    user_id = str(query.from_user.id)
    idx = question_index.get(user_id, 0)
    q = questions[idx]
    if query.data == q["answer"]:
        context.bot.send_message(chat_id=query.message.chat_id, text=f"✅ إجابة صحيحة!
🎥 شاهد الفيديو: {q['video']}", reply_markup=InlineKeyboardMarkup([
            [InlineKeyboardButton("🎥 شاهدت الفيديو", callback_data="watched")],
        ]))
    else:
        context.bot.send_message(chat_id=query.message.chat_id, text="❌ إجابة خاطئة. حاول مرة أخرى.")

def watched(update: Update, context: CallbackContext):
    query = update.callback_query
    user_id = str(query.from_user.id)
    data = load_data()
    data[user_id] = data.get(user_id, 0) + 10
    save_data(data)
    question_index[user_id] += 1
    context.bot.send_message(chat_id=query.message.chat_id, text="✅ تم تسجيل 10 نقاط
➡️ التالي", reply_markup=InlineKeyboardMarkup([
        [InlineKeyboardButton("➡️ التالي", callback_data="next")]
    ]))

def next_question(update: Update, context: CallbackContext):
    query = update.callback_query
    query.answer()
    send_question(query, context)

def mypoints(update: Update, context: CallbackContext):
    user_id = str(update.effective_user.id)
    data = load_data()
    points = data.get(user_id, 0)
    update.message.reply_text(f"🏆 نقاطك: {points}")

def main():
    updater = Updater("7328057055:AAH-P-3RqyalXJvI1zthPVGAO-ru-NaBE2c", use_context=True)
    dp = updater.dispatcher
    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(CommandHandler("mypoints", mypoints))
    dp.add_handler(CallbackQueryHandler(button, pattern="^(?!watched|next).+"))
    dp.add_handler(CallbackQueryHandler(watched, pattern="watched"))
    dp.add_handler(CallbackQueryHandler(next_question, pattern="next"))
    updater.start_polling()
    updater.idle()

if __name__ == "__main__":
    main()
