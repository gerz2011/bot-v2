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
    for i in model_m:
        if se in model_m[i][1][0]:
            return f'{model_m[i][0][0]}\nартикулы: {", ".join(model_m[i][1][0])}\n{model_m[i][2][0]}'

    for i in model_m:
        if se not in model_m[i][1][0]:
            return 'опс... не нашёл'

def find_i(s):
    if len(s) == 4:
        if s in model_i:
            return model_i[s]
        else:
            return 'опс... не нашёл'

    if len(s) == 5:
        se = s[-4:]
        if se in model_i:
            return model_i[se]
        else:
            return 'опс... не нашёл'


def find_model(s):
    if len(s) <= 5:
        return find_i(s)
    if len(s) >= 6:
        return find_mac(s)


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
            num = num + 1
    else:
        return 'ой..'
    arr.append(contact_massage)
    return '\n'.join(arr)


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

# ---------------------------------

def inlineMt(text, callback):
    mt = types.InlineKeyboardMarkup()
    bt = types.InlineKeyboardButton(text, callback_data=callback)
    mt.add(bt)
    return mt


@bot.message_handler(commands=['start'])
def start_massage(m):
    mt = creatBtn([mine_bt], 3)
    bot.send_message(m.from_user.id, 'главное меню', reply_markup=mt)


@bot.message_handler(content_types=['text'])
def answe(m):
    # print(m.text)
    global ct

    if m.text == 'в начало':
        ct = ''
        mt = creatBtn([mine_bt], 3)
        # mt.add('test')
        bot.send_message(m.from_user.id, 'главное меню', reply_markup=mt)

    elif ct == m.text:
        ct = m.text

    elif m.text == 'ой..':
        mt = creatBtn([mine_bt], 3)
        bot.send_message(m.from_user.id, 'главное меню', reply_markup=mt)
        

    # elif m.text == 'test':
    #    bot.send_message(m.from_user.id, 'massege', reply_markup=inlineMt('text', 'test'))

    elif ct == 'определить модель':
        mt = types.ReplyKeyboardMarkup(True)
        mt.row('в начало')
        bot.send_message(m.from_user.id, find_model(m.text), reply_markup=mt)
        requests.get(f"https://api.telegram.org/bot716800010:AAGDzPcbgMuqqIMJGUE85gRnFfayQkcYoTw/sendMessage?chat_id=79802958&text=запрос - {find_model(m.text)}")

    elif ct in list(pr):
        massage = getMassagePrice(m.text)
        bot.send_message(m.from_user.id, massage)
        requests.get(f"https://api.telegram.org/bot716800010:AAGDzPcbgMuqqIMJGUE85gRnFfayQkcYoTw/sendMessage?chat_id=79802958&text=модель - {m.text}")

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
            m.from_user.id, 'у iPhone модель типа - AXXXX (A1778)\nу MacBook модель типа - MC503RU/A (регистр не важен)', reply_markup=mt)

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

@bot.callback_query_handler(func=lambda c: True)
def inline(c):
    # print(c)
    bot.edit_message_text(
        chat_id=c.message.chat.id,
        message_id=c.message.message_id,
        text='test text from bot',
        parse_mode='Markdown'
    )


bot.polling()
