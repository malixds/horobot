import telebot
import psycopg2
import db
from telebot import types
from telebot.util import quick_markup
import pars as p
import requests
from bs4 import BeautifulSoup as bs
import pandas as pd
import re
import configparser


config = configparser.ConfigParser()

config.read('config.ini')

API_TOKEN = config.get("bot", "API_TOKEN")

print(API_TOKEN)

conn = psycopg2.connect(
    dbname="horodatabase",
    user="hastrologybot",
    password="123",
    host="localhost"
)

cursor = conn.cursor()




bot = telebot.TeleBot(API_TOKEN)

selected_zodiac_1 = None
selected_zodiac_2 = None
a = None
b = None


@bot.message_handler(commands=['start', 'help'])
def welcome(message):
    print(message)
    if message.text == '/start':
        print('asdasdas')
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
        item1 = types.KeyboardButton("💖 Совместимость")
        item2 = types.KeyboardButton("⚛ Гороскоп на сегодня")
        item3 = types.KeyboardButton("☯ Общий гороскоп")
        item4 = types.KeyboardButton("🐉 Китайский гороскоп")

        markup.add(item1, item2, item3, item4)

        bot.send_message(
            message.chat.id, "Открыл меню для Вас", reply_markup=markup)
    else:
        bot.reply_to(message, """
         HELP
           """)


@bot.message_handler(func=lambda message: True)
def china_horo(message):
    global selected_zodiac_1
    print(message.text)
    if message.text == "🐉 Китайский гороскоп":
        print(message.text)
        keyboard = quick_markup({
            'Крыса': {'callback_data': 'Крыса'},
            'Бык': {'callback_data': 'Бык'},
            'Тигр': {'callback_data': 'Тигр'},
            'Дракон': {'callback_data': 'Дракон'},
            'Змея': {'callback_data': 'Змея'},
            'Овца': {'callback_data': 'Овца'},
            'Обезьяна': {'callback_data': 'Обезьяна'},
            'Петух': {'callback_data': 'Петух'},
            'Собака': {'callback_data': 'Собака'},
            'Кабан': {'callback_data': 'Кабан'},
        }, row_width=2)
        bot.send_message(
            message.chat.id, "🐈 Подберите животное, соответствующее году вашего рождения, и получите прогноз на 2023 год", reply_markup=keyboard)
    elif message.text == '☯ Общий гороскоп':
        print('asdasd')
        keyboard = quick_markup({
            'Овен': {'callback_data': 'Овен'},
            'Телец': {'callback_data': 'Телец'},
            'Близнецы': {'callback_data': 'Близнецы'},
            'Рак': {'callback_data': 'Рак'},
            'Лев': {'callback_data': 'Лев'},
            'Дева': {'callback_data': 'Дева'},
            'Весы': {'callback_data': 'Весы'},
            'Скорпион': {'callback_data': 'Скорпион'},
            'Стрелец': {'callback_data': 'Стрелец'},
            'Козерог': {'callback_data': 'Козерог'},
            'Водолей': {'callback_data': 'Водолей'},
            'Рыбы': {'callback_data': 'Рыбы'},
        }, row_width=2)
        bot.send_message(
            message.chat.id, "☯️ Выберите знака зодиака", reply_markup=keyboard)

    elif message.text == '⚛ Гороскоп на сегодня':
        print('asdasd')
        keyboard = quick_markup({
            'Овен': {'callback_data': 'Овен ♈️'},
            'Телец': {'callback_data': 'Телец ♉️'},
            'Близнецы': {'callback_data': 'Близнецы ♊️'},
            'Рак': {'callback_data': 'Рак ♋️'},
            'Лев': {'callback_data': 'Лев ♌️'},
            'Дева': {'callback_data': 'Дева ♍️'},
            'Весы': {'callback_data': 'Весы ♎️'},
            'Скорпион': {'callback_data': 'Скорпион ♏️'},
            'Стрелец': {'callback_data': 'Стрелец ♐️'},
            'Козерог': {'callback_data': 'Козерог ♑️'},
            'Водолей': {'callback_data': 'Водолей ♒️'},
            'Рыбы': {'callback_data': 'Рыбы ♓️'},
        }, row_width=2)

        bot.send_message(
            message.chat.id, "☯️ Выберите знака зодиака", reply_markup=keyboard)

    elif message.text == "💖 Совместимость":
        keyboard = quick_markup({
            'Овен': {'callback_data': 'Овен♈️'},
            'Телец': {'callback_data': 'Телец♉️'},
            'Близнецы': {'callback_data': 'Близнецы♊️'},
            'Рак': {'callback_data': 'Рак♋️'},
            'Лев': {'callback_data': 'Лев♌️'},
            'Дева': {'callback_data': 'Дева♍️'},
            'Весы': {'callback_data': 'Весы♎️'},
            'Скорпион': {'callback_data': 'Скорпион♏️'},
            'Стрелец': {'callback_data': 'Стрелец♐️'},
            'Козерог': {'callback_data': 'Козерог♑️'},
            'Водолей': {'callback_data': 'Водолей♒️'},
            'Рыбы': {'callback_data': 'Рыбы♓️'},
        }, row_width=2)
        bot.send_message(
            message.chat.id, "❤️ Совместимость \n \n 👉 Между женщиной ____ и мужчиной ____  \n \n ⚖️ Выберите первый знак зодиака", reply_markup=keyboard)


@bot.callback_query_handler(func=lambda call: True)
def handler_china_horo(call):

    lst_horos = ['Крыса', 'Бык', 'Тигр', 'Дракон', 'Змея',
                 'Лошадь', 'Овца', 'Обезьяна', 'Петух', 'Собака', 'Кабан']

    lst_zodiac = ['Овен', 'Телец', 'Близнецы', 'Дева', 'Рыбы',
                  'Весы', 'Стрелец', 'Козерог', 'Скорпион', 'Рак', 'Водолей', 'Лев']

    lst_today_zodiac = ['Овен ♈️', 'Телец ♉️', 'Близнецы ♊️', 'Дева ♍️', 'Рыбы ♓️',
                        'Весы ♎️', 'Стрелец ♐️', 'Козерог ♑️', 'Скорпион ♏️', 'Рак ♋️', 'Водолей ♒️', 'Лев ♌️']

    lst_compatibility = ['Овен♈️', 'Телец♉️', 'Близнецы♊️', 'Дева♍️', 'Рыбы♓️',
                         'Весы♎️', 'Стрелец♐️', 'Козерог♑️', 'Скорпион♏️', 'Рак♋️', 'Водолей♒️', 'Лев♌️']
    button_name = call.data

    if button_name in lst_horos:

        cursor.execute(
            "SELECT button_description FROM buttons WHERE button_name=%s", (button_name,))
        result = cursor.fetchone()
        for horo in lst_horos:
            if horo == button_name:
                bot.send_message(call.message.chat.id, result)

    elif button_name in lst_zodiac:
        zodiac_name = call.data
        cursor.execute(
            "SELECT zodiac_description FROM zodiac WHERE zodiac_name=%s", (zodiac_name,))
        result = cursor.fetchone()
        for zodiac in lst_zodiac:
            if zodiac == zodiac_name:
                bot.send_message(call.message.chat.id, result)

    elif button_name in lst_today_zodiac:
        name = button_name[:-3]
        result = button_name + '\n' + '\n' + p.dct[name]
        bot.send_message(call.message.chat.id, result)

########################################

    elif button_name in lst_compatibility:
        global selected_zodiac_1
        if selected_zodiac_1 is None:
            selected_zodiac_1 = call.data[:-2]
            bot.send_message(call.message.chat.id,
                             f"Вы выбрали первый знак зодиака: {selected_zodiac_1}")
            keyboard = quick_markup({
                        'Овен': {'callback_data': 'Овен♈️'},
                        'Телец': {'callback_data': 'Телец♉️'},
                        'Близнецы': {'callback_data': 'Близнецы♊️'},
                        'Рак': {'callback_data': 'Рак♋️'},
                        'Лев': {'callback_data': 'Лев♌️'},
                        'Дева': {'callback_data': 'Дева♍️'},
                        'Весы': {'callback_data': 'Весы♎️'},
                        'Скорпион': {'callback_data': 'Скорпион♏️'},
                        'Стрелец': {'callback_data': 'Стрелец♐️'},
                        'Козерог': {'callback_data': 'Козерог♑️'},
                        'Водолей': {'callback_data': 'Водолей♒️'},
                        'Рыбы': {'callback_data': 'Рыбы♓️'},
            }, row_width=2)
            bot.send_message(
                call.message.chat.id, f"❤️ Совместимость \n \n 👉 Между женщиной {selected_zodiac_1} и ____  \n \n ⚖️ Выберите первый знак зодиака", reply_markup=keyboard)
            bot.register_callback_query_handler(
                call.message, compatibility_step_2)

        else:
            global selected_zodiac_2
            selected_zodiac_2 = call.data[:-2]
            bot.send_message(call.message.chat.id,
                             f"{selected_zodiac_1} и {selected_zodiac_2}")
            print(type(selected_zodiac_1))
            compatibility_dct = {
                'Овен': 'oven',
                'Телец': 'teleс',
                'Близнецы': 'bliznecy',
                'Рак': 'rak',
                'Лев': 'lev',
                'Дева': 'deva',
                'Весы': 'vesy',
                'Скорпион': 'skorpion',
                'Стрелец': 'strelec',
                'Козерог': 'kozerog',
                'Водолей': 'vodolej',
                'Рыбы': 'ryby',
            }
            URL_TEMPLATE = f'https://horoscopes.rambler.ru/sovmestimost-znakov-zodiaka/zhenshhina-{compatibility_dct[selected_zodiac_1]}-muzhchina-{compatibility_dct[selected_zodiac_2]}/'
            # URL_TEMPLATE = f'https://www.kp.ru/woman/goroskop/sovmestimost-{compatibility_dct[selected_zodiac_2]}-i-{compatibility_dct[selected_zodiac_1]}/'
            print(URL_TEMPLATE)
            selected_zodiac_1 = None
            r = requests.get(URL_TEMPLATE)
            soup = bs(r.text, "html.parser")
            # titles = soup.find_all('h3', 'wp-block-heading')
            compability = soup.find('h1', '_3wtsS _1W8Ro _2kQY7').text
            titles = ['Любовь', 'Секс', 'Семья и брак', 'Дружба']
            # texts = soup.find_all('p', class_='mtZOt')
            content = soup.find('div', class_='_1E4Zo').get_text()
            print(content)
            

            pattern = r'(?<=[a-zа-я])(?=[A-ZА-Я])|(?<=\.)(?=[A-ZА-Я])'

            modified_text = re.sub(pattern, '\n\n', content)

            bot.send_message(call.message.chat.id, compability + '\n' + '\n' + modified_text)


def compatibility_step_2(message):
    print('OSKDJFKLSDJFLKSDJFKLSJ')
    # Эта функция будет вызвана после выбора второго знака зодиака
    global selected_zodiac_1
    selected_zodiac_1 = None
    selected_zodiac_2 = message.text

    bot.send_message(
        message.chat.id, f"{selected_zodiac_1} и {selected_zodiac_2}")
    # Вы можете выполнить нужные действия на основе выбранных знаков зодиака здесь
    # Например, выполнить расчет совместимости и отправить результат пользователю
    # Затем сбросьте переменную selected_zodiac_1 в None для будущих запросов

    # Другие действия...


print(a, b)


bot.infinity_polling()
