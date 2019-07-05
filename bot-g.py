import telebot
import math
import requests
import json
# from telebot import apihelper
from telebot import types
# apihelper.proxy = {'https': 'https://62.141.35.197:3128'}
# proxies = {"https": "https://62.141.35.197:3128"}
# apihelper.proxy = {'https': 'https://188.216.77.95:8118'}
# apihelper.proxy = {'https': 'https://185.69.152.18:3128'}
TOKEN = '781098537:AAEGQ7-kRv6Pt8KGs5CfW9RiPRLU8lKHp58'
# TOKEN = '644721358:AAFoPs-lWeq6zEzxeJal5joAr2kPfCTtPag'
bot = telebot.TeleBot(TOKEN)

with open('pr.json', encoding='utf-8') as f:
    d = json.load(f)

pr = d['price']
model_i = d['ip_m']
model_m = d['mac']
pb_i = d['problem_iphone']
pb_m = d['problem_two']

contact_massage = '...............................\nтел 89313403833\nтелеграм чат @gerz_og\n'

mine_bt = list(pr)
mine_bt.append('определить модель')
mine_bt.append('контакты')
ct = ''
couse = ''

# ------------------------------


def find_mac(s):
    se = s[0:5].upper() + 'XX' + s[-2:].upper()
    print(se)
    for i in model_m:
        for e in model_m[i][1][0]:
            print(e)
            if e == se:
                m = f'{model_m[i][0][0]}\nартикулы: {", ".join(model_m[i][1][0])}\n{model_m[i][2][0]}'
                return m
            else:
                m = 'ой..'
                return m 


# -----------------------------
def getMassagePrice(m):
    global ct, pb_i, pb_m
    couse = pb_i
    if ct != 'iPhone':
        couse = pb_m
    arr = [f'🍏 {ct} {m}:\n...............................']
    num = 0
    if m in list(pr[ct]):
        for key in pr[ct][m]:
            if key != '---':
                arr.append(f'{couse[num]} {key}р.')
            num += 1
    else:
        text = 'ой..'
        return text
    arr.append(contact_massage)
    text = '\n'.join(arr)
    return text

# -------------------------------


def creatBtn(arr, collum):
    markup = types.ReplyKeyboardMarkup(True)
    array = []
    collum = 3
    if ct == 'iPhone':
        collum = 4
    for i in arr:
        w = 0
        for iter in range(math.ceil(len(i) / collum)):
            array.append(i[w:w+collum])
            w = w + collum
    for i in array:
        markup.row(*[types.KeyboardButton(name) for name in i])
    return markup
# ==================================


@bot.message_handler(commands=['start'])
def start_massage(m):
    mt = creatBtn([mine_bt], 3)
    bot.send_message(m.from_user.id, 'главное меню', reply_markup=mt)


@bot.message_handler(content_types=['text'])
def answe(m):
    print(m.text)
    global ct

    if m.text == 'в начало':
        ct = ''
        mt = creatBtn([mine_bt], 3)
        bot.send_message(m.from_user.id, 'главное меню', reply_markup=mt)

    elif ct == m.text:
        ct = m.text

    elif ct == 'определить модель':
        if m.text in list(model_i):
            bot.send_message(m.from_user.id, model_i[m.text])
        elif len(m.text) > 3:
            bot.send_message(m.from_user.id, find_mac(m.text))
        else:
            bot.send_message(
                m.from_user.id, 'Или все сломалось или укажите правильно модель')

        requests.get(
            f"https://api.telegram.org/bot716800010:AAGDzPcbgMuqqIMJGUE85gRnFfayQkcYoTw/sendMessage?chat_id=79802958&text=запрос - {m.text}")

    elif ct in list(pr):
        massage = getMassagePrice(m.text)
        bot.send_message(m.from_user.id, massage)

        requests.get(
            f"https://api.telegram.org/bot716800010:AAGDzPcbgMuqqIMJGUE85gRnFfayQkcYoTw/sendMessage?chat_id=79802958&text=запрос - {m.text}")

    elif m.text in list(pr):
        ct = m.text
        mt = creatBtn([list(pr[ct])], 4)
        mt.row('в начало')
        bot.send_message(
            m.from_user.id, 'Прайс на ремонт айфонов', reply_markup=mt)

    elif m.text == 'определить модель':
        ct = m.text
        mt = types.ReplyKeyboardMarkup(True)
        mt.row('в начало')
        bot.send_message(
            m.from_user.id, 'у iPhone модель типа - AXXXX (только цифры!)\nу MacBook модель типа - MC503RU/A (регистр не важен)', reply_markup=mt)

    elif m.text == 'контакты':
        mt = types.InlineKeyboardMarkup()
        bt_site = types.InlineKeyboardButton(
            'Наш сайт', 'https://profiphone.ru/')
        bt_vk = types.InlineKeyboardButton(
            'Вконтакте', 'https://vk.com/yablonya_spb')
        bt_ya_map = types.InlineKeyboardButton(
            'Яндекс карта', 'https://yandex.ru/maps/?um=constructor%3Ac25054319007c6053f87b0125d81dd198df8a2759cb2b885d40629cf0ad770e1&source=constructorLink')
        mt.row(bt_site, bt_vk, bt_ya_map)
        mt.row(bt_ya_map)
        bot.send_message(m.from_user.id, d['contact'], reply_markup=mt)

    else:
        mt = types.ReplyKeyboardMarkup(True)
        mt.row('в начало')
        bot.send_message(
            m.from_user.id, 'что-то не понятно, начни с начала', reply_markup=mt)


bot.polling()
