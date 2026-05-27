import logging
from aiogram import Bot, Dispatcher, executor, types
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

# Bot tokenini kiriting (BotFather'dan olinadi)
API_TOKEN = '8445588672:AAGrCR6r-gG213vOOe8ftqUQqNTbW686BJk'

logging.basicConfig(level=logging.INFO)
bot = Bot(token=API_TOKEN)
dp = Dispatcher(bot)

# Ma'lumotlarni saqlash uchun vaqtinchalik baza (Xotira)
user_scores = {}
user_names = {}

@dp.message_handler(commands=['start'])
async def send_welcome(message: types.Message):
    user_id = message.from_user.id
    user_names[user_id] = message.from_user.full_name
    if user_id not in user_scores:
        user_scores[user_id] = 0
        
    keyboard = InlineKeyboardMarkup()
    btn_click = InlineKeyboardButton(text=f"Tugma ➕ (Sizda: {user_scores[user_id]})", callback_data="click")
    btn_leaderboard = InlineKeyboardButton(text="🏆 Reytingni ko'rish", callback_data="leaderboard")
    keyboard.add(btn_click).add(btn_leaderboard)
    
    await message.reply("Xush kelibsiz! Tugmani bosing va ball yiging:", reply_markup=keyboard)

@dp.callback_query_handler(lambda c: c.data == 'click')
async def process_callback_click(callback_query: types.CallbackQuery):
    user_id = callback_query.from_user.id
    user_names[user_id] = callback_query.from_user.full_name
    
    user_scores[user_id] = user_scores.get(user_id, 0) + 1
    current_score = user_scores[user_id]
    
    keyboard = InlineKeyboardMarkup()
    btn_click = InlineKeyboardButton(text=f"Tugma ➕ (Sizda: {current_score})", callback_data="click")
    btn_leaderboard = InlineKeyboardButton(text="🏆 Reytingni ko'rish", callback_data="leaderboard")
    keyboard.add(btn_click).add(btn_leaderboard)
    
    await bot.answer_callback_query(callback_query.id, text=f"Ballingiz: {current_score}")
    
    await bot.edit_message_reply_markup(
        chat_id=callback_query.message.chat_id,
        message_id=callback_query.message.message_id,
        reply_markup=keyboard
    )

@dp.callback_query_handler(lambda c: c.data == 'leaderboard')
async def process_callback_leaderboard(callback_query: types.CallbackQuery):
    sorted_scores = sorted(user_scores.items(), key=lambda item: item[1], reverse=True)
    
    text = "🏆 **Natijalar jadvali (Top 20):**\n\n"
    for index, (u_id, score) in enumerate(sorted_scores[:20], start=1):
        name = user_names.get(u_id, "Noma'lum foydalanuvchi")
        text += f"{index}. {name} — {score} ta\n"
        
    await bot.send_message(callback_query.message.chat.id, text, parse_mode="Markdown")
    await bot.answer_callback_query(callback_query.id)

if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)
      
