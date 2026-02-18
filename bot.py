import telebot
from telebot import types
import os

TOKEN = os.getenv("TOKEN")
bot = telebot.TeleBot(TOKEN)

user_scores = {}

questions = [
    "HTF Structure Aligned?",
    "Valid POI Reaction?",
    "Liquidity Sweep Taken?",
    "Strong BOS + Displacement?",
    "15m Entry Precision?",
    "Minimum 1:3 R:R Available?",
    "Correct Session?",
    "Not Emotional?",
    "Clean Structure?",
    "Not Extended Entry?"
]

@bot.message_handler(commands=['start'])
def start(message):
    user_scores[message.chat.id] = 0
    ask_question(message.chat.id, 0)

def ask_question(chat_id, q_index):
    if q_index < len(questions):
        markup = types.InlineKeyboardMarkup()
        yes_btn = types.InlineKeyboardButton("✅ Yes", callback_data=f"yes_{q_index}")
        no_btn = types.InlineKeyboardButton("❌ No", callback_data=f"no_{q_index}")
        markup.add(yes_btn, no_btn)
        bot.send_message(chat_id, questions[q_index], reply_markup=markup)
    else:
        final_score(chat_id)

@bot.callback_query_handler(func=lambda call: True)
def callback(call):
    answer, q_index = call.data.split("_")
    q_index = int(q_index)

    if answer == "yes":
        user_scores[call.message.chat.id] += 10

    ask_question(call.message.chat.id, q_index + 1)

def final_score(chat_id):
    score = user_scores[chat_id]

    if score >= 90:
        decision = "✅ A+ EXECUTE"
    elif score >= 80:
        decision = "⚠️ B SETUP (Optional)"
    else:
        decision = "❌ REJECT"

    bot.send_message(chat_id, f"""
🤖 A+ STRUCTURE BOT RESULT

Score: {score}%

Decision: {decision}

Risk: $100
Minimum RR: 1:3
""")

bot.infinity_polling()
