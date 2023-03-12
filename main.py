import telebot
import wikipedia
from telebot import types

wikipedia.set_lang("ru")
bot = telebot.TeleBot('6166512579:AAGHpTkEO13NvghuDXhc9_-6GL1JRtZCoEM')

@bot.callback_query_handler(func=lambda call: True)
def callback_worker(call):
    delete_text_message(call.message.chat.id, call.message.id)
    msg = bot.send_message(call.message.chat.id, "Пожалуйста подождите...")
    wiki_search = wikipedia.page(call.data)
    try:
        content = f"<b>{call.data}</b>\n{wiki_search.summary}\nПодробнее читайте по ссылке: {wiki_search.url}"
        if wiki_search.images != None:
            if len(wiki_search.images) > 0:
                for image in wiki_search.images:
                    if image[-3:] == "jpg":
                        bot.send_photo(call.message.chat.id, image)
                        break
        delete_text_message(call.message.chat.id, msg.message_id)
        bot.send_message(call.message.chat.id, content, parse_mode="HTML")
    except Exception as e:
        bot.send_message(call.message.chat.id, "Что-то пошло не так. Повторите запрос позже.", parse_mode="HTML")
        print(e)

@bot.message_handler(commands=["start"])
def send_command(message):
        bot.send_message(message.chat.id, f"Добро пожаловать! Это бот-Wikipedia. Введите сообщение с любым запросом, "
                                          f"информацию о котором хотите найти")

@bot.message_handler(content_types=['text'])
def get_text_messages(message):
    suggestion = wikipedia.search(message.text, results=3)
    keyboard = types.InlineKeyboardMarkup()
    for suggest in suggestion:
        key = types.InlineKeyboardButton(text=suggest, callback_data=suggest)
        keyboard.add(key)
    bot.send_message(message.chat.id, "Выберите более точный запрос", reply_markup=keyboard)


def delete_text_message(chat_id, message_id):
    bot.delete_message(chat_id=chat_id, message_id=message_id)


bot.polling(none_stop=True, interval=0)