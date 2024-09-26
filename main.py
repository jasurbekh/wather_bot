from telebot import TeleBot
from telebot.types import Message, ReplyKeyboardRemove
from keyboards import generate_button
import requests

TOKEN = '7416593806:AAEQkt2xcTuNTW6zGEuCNKIlqSR9FilpikM'

bot = TeleBot(TOKEN)


@bot.message_handler(commands=['start'])
def command_start(message: Message):
    chat_id = message.chat.id
    bot.send_message(chat_id, 'Salom! Men ob-xavo bo`timan 🌤',
                     reply_markup=generate_button())


@bot.message_handler(regexp='⛅ Ob-xavo')
def ask_city(message: Message):
    chat_id = message.chat.id
    msg = bot.send_message(chat_id, 'Shaxar nomini kiriting: ',
                           reply_markup=ReplyKeyboardRemove())
    bot.register_next_step_handler(msg, answer_to_user)


def answer_to_user(message: Message):
    chat_id = message.chat.id
    text = message.text
    bot.send_message(chat_id, f'Siz kiritgan shaxar: {text}')

    KEY = '6418b539e0697f54de8a3df65ebe9444'
    params = {
        'appid': KEY,
        'units': 'metric',
        'lang': 'ru',
        'q': text
    }
    data = requests.get('https://api.openweathermap.org/data/2.5/weather', params=params).json()

    try:
        temp = data['main']['temp']
        wind_speed = data['wind']['speed']
        description = data['weather'][0]['description']
        clouds = data['clouds']['all']
        answer = f'Shaxar {text} da xozir {description}\nXarorati: {temp} °C\nShamol tezligi: {wind_speed},\n' \
                 f'Bulut: {clouds}'
        bot.send_message(chat_id, answer)
        ask_again(message)
    except:
        bot.send_message(chat_id, 'Xatolik yuzaga keldi!!! Yana bir bor tugmani bosing 👇',
                         reply_markup=generate_button())


def ask_again(message: Message):
    chat_id = message.chat.id
    bot.send_message(chat_id, 'Tugmani bosing va shaxar kiriting 👇🏻',
                     reply_markup=generate_button())



bot.polling(none_stop=True)
