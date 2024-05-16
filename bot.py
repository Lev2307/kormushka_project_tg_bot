from telebot import TeleBot
from telebot import types

from helpers import get_last_non_downloaded_user_image_url, if_equal_images_in_db_with_yadisk
from db_functions import DB_get_user_by_telegram_id, DB_table_val

TOKEN = ""
GET_IMAGE_OPTION = "Получить фотографию птицы"
BIRDS_FOLDER = "/birds/"

bot = TeleBot(TOKEN)

@bot.message_handler(commands=['start', 'help'])
def say_hello(message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    markup.add(
        types.KeyboardButton(GET_IMAGE_OPTION),
    )	
    bot.send_message(message.chat.id, 
                 "👋 Привет! Я Кормушка бот 🤖"
                 "\nЧем я могу быть полезен?", reply_markup=markup)    
    
@bot.message_handler(content_types='text')
def message_reply(message):
    pay_markup_image = types.InlineKeyboardMarkup()
    pay_markup_image.add(
        types.InlineKeyboardButton("Получить фото", callback_data="/get_image")
    )
    if DB_get_user_by_telegram_id(message.from_user.id) == []:
       DB_table_val(message.from_user.id, "")

    if message.text == GET_IMAGE_OPTION:
        if if_equal_images_in_db_with_yadisk(message.from_user.id):
            bot.send_message(message.chat.id, 'Похоже, новых фото с птицами не появилось к этому моменту. Попробуйте позже ;>')
        else:
            bot.send_message(message.chat.id, "Отличный выбор. Нажмите на кнопку для получения фотографии.", reply_markup=pay_markup_image)


@bot.callback_query_handler(func=lambda c: c.data == '/get_image')
def process_callback_payment(callback_query: types.CallbackQuery):
    bot.answer_callback_query(callback_query.id)
    if if_equal_images_in_db_with_yadisk(callback_query.from_user.id):
        bot.send_message(callback_query.from_user.id, 'Похоже, новых фото с птицами не появилось к этому моменту. Попробуйте позже ;>')
    else:
        image = get_last_non_downloaded_user_image_url(callback_query.from_user.id) 
        bot.send_photo(callback_query.from_user.id, photo=image["file"])

bot.infinity_polling(skip_pending=True)