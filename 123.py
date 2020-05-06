# Импорты
import json
import os
import random

import apiai
import pymorphy2
import requests
import vk_api
from vk_api.bot_longpoll import VkBotLongPoll, VkBotEventType
from vk_api.keyboard import VkKeyboard
from vk_api.upload import VkUpload

from x_0 import won, comp_course


# Построение клавиатуры для игры "Крестики - нолики"
def build_keyboard(li):
    a = VkKeyboard()
    a.add_button(li[0][0])
    a.add_button(li[0][1])
    a.add_button(li[0][2])
    a.add_line()
    a.add_button(li[1][0])
    a.add_button(li[1][1])
    a.add_button(li[1][2])
    a.add_line()
    a.add_button(li[2][0])
    a.add_button(li[2][1])
    a.add_button(li[2][2])
    a.add_line()
    a.add_button('Хочу поболтать опять')
    return a


# Глобальные переменные и строки, которые будут использованы
WORDS = ['давай сыграем в крестики-нолики', 'давай сыграем в угадай город', 'включи режим переводчика',
         'хочу поболтать опять']
translator = 'https://translate.yandex.net/api/v1.5/tr.json/translate?text={}&lang={}-{}&key={}'
geo = "http://geocode-maps.yandex.ru/1.x/?apikey=40d1649f-0493-4b70-98ba-98533de7710b&geocode={}&format=json"
map_resp = "http://static-maps.yandex.ru/1.x/?ll={}&spn=0.18,0.18&l=sat"
LANG = {'азербайджанский': 'az', 'албанский': 'sq', 'амхарский': 'am', 'английский': 'en',
        'арабский': 'ar', 'армянский': 'hy', 'африкаанс': 'af', 'баскский': 'eu',
        'башкирский': 'ba', 'белорусский': 'be', 'бенгальский': 'bn', 'бирманский': 'my',
        'болгарский': 'bg', 'боснийский': 'bs', 'валлийский': 'cy', 'венгерский': 'hu',
        'вьетнамский': 'vi', 'гаитянский': 'ht', 'галисийский': 'gl', 'голландский': 'nl',
        'горномарийский': 'mrj', 'греческий': 'el', 'грузинский': 'ka', 'гуджарати': 'gu',
        'датский': 'da', 'иврит': 'he', 'идиш': 'yi', 'индонезийский': 'id',
        'ирландский': 'ga', 'итальянский': 'it', 'исландский': 'is', 'испанский': 'es',
        'казахский': 'kk', 'каннада': 'kn', 'каталанский': 'ca', 'киргизский': 'ky',
        'китайский': 'zh', 'корейский': 'ko', 'коса': 'xh', 'кхмерский': 'km',
        'лаосский': 'lo', 'латынь': 'la', 'латышский': 'lv', 'литовский': 'lt',
        'люксембургский': 'lb', 'малагасийский': 'mg', 'малайский': 'ms', 'малаялам': 'ml',
        'мальтийский': 'mt', 'македонский': 'mk', 'маори': 'mi', 'маратхи': 'mr',
        'марийский': 'mhr', 'монгольский': 'mn', 'немецкий': 'de', 'непальский': 'ne',
        'норвежский': 'no', 'панджаби': 'pa', 'папьяменто': 'pap', 'персидский': 'fa',
        'польский': 'pa', 'португальский': 'pt', 'румынский': 'ro', 'русский': 'ru',
        'себуанский': 'ceb', 'сербский': 'sr', 'сингальский': 'si', 'словацкий': 'sk',
        'словенский': 'sl', 'суахили': 'sw', 'сунданский': 'su', 'таджикский': 'tg',
        'тайский': 'th', 'тагальский': 'tl', 'тамильский': 'ta', 'татарский': 'tt',
        'телугу': 'te', 'турецкий': 'tr', 'удмуртский': 'udm', 'узбекский': 'uz',
        'украинский': 'uk', 'урду': 'ur', 'финский': 'fi', 'французский': 'fr',
        'хинди': 'hi', 'хорватский': 'hr', 'чешский': 'cs', 'шведский': 'sv',
        'шотландский': 'gd', 'эстонский': 'et', 'эсперанто': 'eo', 'яванский': 'jv', 'японский': 'ja'}
CAPITALS = ['Амстердам', 'Андорра-ла-Велья', 'Афины', 'Белград', 'Берлин', 'Берн', 'Братислава', 'Брюссель',
            'Будапешт', 'Бухарест', 'Вадуц', 'Валлетта', 'Варшава', 'Ватикан', 'Вена', 'Вильнюс', 'Дублин',
            'Загреб', 'Киев', 'Кишинёв', 'Копенгаген', 'Лиссабон', 'Лондон', 'Любляна', 'Люксембург',
            'Мадрид', 'Минск', 'Монако', 'Москва', 'Осло', 'Париж', 'Подгорица', 'Прага', 'Рейкьявик',
            'Рига', 'Рим', 'Сан-Марино', 'Сараево', 'Скопье', "София", "Стокгольм", "Таллин", "Тирана", "Хельсинки"]
TRANAPI = 'trnsl.1.1.20200426T203403Z.e2882e1d8f28daaa.bb59eda4ee47959c0c49e8ee3f12667a92ef219b'


# Главная функция
def main():
    vk_session = vk_api.VkApi(
        token='b0509e54657471c56c239686f09a8322a37846b19769e902e69bf1136cc2f9c254a26499001c3e15f3dca')

    longpoll = VkBotLongPoll(vk_session, 194502422)
    # Списки и словари для хранения id пользователей, чтобы знать, кто из них сейчас в какой функции
    translator_mode = []
    city_game = []
    X_0_game = []
    city_u = {}
    lang_u = {}
    x_0_u = {}

    people = set()
    # Стандартные клавиатуры
    stop = VkKeyboard()
    stop.add_button('Хочу поболтать опять')

    a = VkKeyboard()
    a.add_button('Давай сыграем в Крестики-нолики')
    a.add_line()
    a.add_button('Давай сыграем в Угадай город')
    a.add_line()
    a.add_button('Включи режим переводчика')
    a.add_line()
    a.add_vkapps_button(7362610, 0, 'Коронавирус', '')

    vk = vk_session.get_api()

    for event in longpoll.listen():
        if event.type == VkBotEventType.MESSAGE_NEW:
            data = vk.messages.getHistory(offset=0,
                                          count=1,
                                          user_id=event.obj.message['from_id'])
            message = data['items'][0]['text']
            if event.obj.message['from_id'] not in people:
                vk.messages.send(user_id=event.obj.message['from_id'],
                                 message="Привет! Я бот! Я могу с тобой немного поболтать, "
                                         "поиграть в угадай город или в крестики-нолики и даже что-нибудь перевести",
                                 keyboard=a.get_keyboard(),
                                 random_id=random.randint(0, 2 ** 64))
                people.add(event.obj.message['from_id'])
            elif message == '':
                vk.messages.send(user_id=event.obj.message['from_id'],
                                 message='Что-то я ничегошеньки не понял, повторите пожалуйста',
                                 random_id=random.randint(0, 2 ** 64))
            # Обращение к Dialogflow и получение ответа
            elif (message.lower() not in WORDS and event.obj.message['from_id'] not in translator_mode
                  and event.obj.message['from_id'] not in city_game and event.obj.message['from_id'] not in X_0_game):
                request = apiai.ApiAI('36842227c2794094af0782eb01de4b99').text_request()
                request.lang = 'ru'
                request.session_id = 'Talk-With-Me-Bot'
                request.query = message
                responsejson = json.loads(request.getresponse().read().decode('utf-8'))
                response = responsejson['result']['fulfillment']['speech']
                if response:
                    vk.messages.send(user_id=event.obj.message['from_id'],
                                     message=response,
                                     random_id=random.randint(0, 2 ** 64))
                else:
                    vk.messages.send(user_id=event.obj.message['from_id'],
                                     message='Я не очень вас понял, вы можете выразиться по другому?',
                                     random_id=random.randint(0, 2 ** 64))
            # Проверка на вход в какую-нибудь
            elif message.lower() in WORDS:
                # Проверка на вход в игру "Крестики-нолики"
                if message.lower() == WORDS[0]:
                    X_0_game.append(event.obj.message['from_id'])
                    x_0_u[event.obj.message['from_id']] = [[['1', '2', '3'],
                                                            ['4', '5', '6'],
                                                            ['7', '8', '9']], VkKeyboard(), '''{} | {} | {}
                                                            ----------
                                                            {} | {} | {}
                                                            ----------
                                                            {} | {} | {}''', False]
                    x_0_u[event.obj.message['from_id']][1] = build_keyboard(x_0_u[event.obj.message['from_id']][0])
                    vk.messages.send(user_id=event.obj.message['from_id'],
                                     message='Сейчас мы сыграем в Крестики-нолики, '
                                             'вы будете играть за крестики, а я за нолики, '
                                             'чтобы поставь свою фигуру нажмите на соответсвующую кнопку. Ваш ход:',
                                     keyboard=x_0_u[event.obj.message['from_id']][1].get_keyboard(),
                                     random_id=random.randint(0, 2 ** 64))
                    vk.messages.send(user_id=event.obj.message['from_id'],
                                     message=x_0_u[event.obj.message['from_id']][2].format(1, 2, 3, 4, 5, 6, 7, 8, 9),
                                     keyboard=x_0_u[event.obj.message['from_id']][1].get_keyboard(),
                                     random_id=random.randint(0, 2 ** 64))
                # Проверка на вход в игру "Угадай город"
                if message.lower() == WORDS[1]:
                    city_game.append(event.obj.message['from_id'])
                    vk.messages.send(user_id=event.obj.message['from_id'],
                                     message='Сейчас я скину фото столицы какой-нибудь страны '
                                             'Европы со спутника, а ты угадай назание этого города',
                                     keyboard=stop.get_keyboard(),
                                     random_id=random.randint(0, 2 ** 64))
                    city_u[event.obj.message['from_id']] = [CAPITALS, [], False]
                # Проверка на вход в игру навык переводчика
                elif message.lower() == WORDS[2]:
                    translator_mode.append(event.obj.message['from_id'])
                    vk.messages.send(user_id=event.obj.message['from_id'],
                                     message='Введите язык, на котором вы будете писать',
                                     keyboard=stop.get_keyboard(),
                                     random_id=random.randint(0, 2 ** 64))
                    lang_u[event.obj.message['from_id']] = []
                # Проверка на выход
                elif (message.lower() == WORDS[3] and (event.obj.message['from_id'] in translator_mode or
                                                       event.obj.message['from_id'] in city_game or
                                                       event.obj.message['from_id'] in X_0_game)):
                    if event.obj.message['from_id'] in translator_mode:
                        del translator_mode[translator_mode.index(event.obj.message['from_id'])]
                    if event.obj.message['from_id'] in city_game:
                        del city_game[city_game.index(event.obj.message['from_id'])]
                    if event.obj.message['from_id'] in X_0_game:
                        del X_0_game[X_0_game.index(event.obj.message['from_id'])]
                    vk.messages.send(user_id=event.obj.message['from_id'],
                                     message='Ну что ж, я вновь готов общаться!',
                                     keyboard=a.get_keyboard(),
                                     random_id=random.randint(0, 2 ** 64))
            # Навык переводчика
            elif event.obj.message['from_id'] in translator_mode:
                if len(lang_u[event.obj.message['from_id']]) < 2:
                    morph = pymorphy2.MorphAnalyzer()
                    if ((morph.parse(message.lower())[0].tag.POS == 'ADJF' or
                         morph.parse(message.lower())[0].tag.POS == 'NOUN') and
                            morph.parse(message.lower())[0].normal_form in LANG.keys()):
                        lang_u[event.obj.message['from_id']].append(LANG[morph.parse(message.lower())[0].normal_form])
                        if len(lang_u[event.obj.message['from_id']]) < 2:
                            vk.messages.send(user_id=event.obj.message['from_id'],
                                             message='Теперь введите язык на который я буду переводить',
                                             random_id=random.randint(0, 2 ** 64))
                        if len(lang_u[event.obj.message['from_id']]) == 2:
                            vk.messages.send(user_id=event.obj.message['from_id'],
                                             message='Теперь вводите фразы, а я их переведу',
                                             random_id=random.randint(0, 2 ** 64))
                    else:
                        vk.messages.send(user_id=event.obj.message['from_id'],
                                         message='К сожалению, я на таком языке не разговариваю, попробуйте другой',
                                         random_id=random.randint(0, 2 ** 64))
                else:
                    resp = json.loads(requests.get(translator.format(message,
                                                                     lang_u[event.obj.message['from_id']][0],
                                                                     lang_u[event.obj.message['from_id']][1],
                                                                     TRANAPI)).content.decode('UTF-8'))
                    if resp:
                        vk.messages.send(user_id=event.obj.message['from_id'],
                                         message=resp['text'],
                                         random_id=random.randint(0, 2 ** 64))
                    else:
                        vk.messages.send(user_id=event.obj.message['from_id'],
                                         message='Что-то пошло не так. Возможно текст слишком большой. '
                                                 'Попробуйте ввести что-нибудь другое',
                                         random_id=random.randint(0, 2 ** 64))
            # Игра в "Крестики-нолики"
            elif event.obj.message['from_id'] in X_0_game:
                if message.isdigit():
                    if int(message) < 10:
                        if int(message) % 3 == 1 and not x_0_u[event.obj.message['from_id']][3]:
                            if message == '1':
                                x_0_u[event.obj.message['from_id']][0][0][0] = 'X'
                                x_0_u[event.obj.message['from_id']][1] = build_keyboard(
                                    x_0_u[event.obj.message['from_id']][0])
                                x_0_u[event.obj.message['from_id']][3] = True
                                vk.messages.send(user_id=event.obj.message['from_id'],
                                                 message=x_0_u[event.obj.message['from_id']][2].format(
                                                     x_0_u[event.obj.message['from_id']][0][0][0],
                                                     x_0_u[event.obj.message['from_id']][0][0][1],
                                                     x_0_u[event.obj.message['from_id']][0][0][2],
                                                     x_0_u[event.obj.message['from_id']][0][1][0],
                                                     x_0_u[event.obj.message['from_id']][0][1][1],
                                                     x_0_u[event.obj.message['from_id']][0][1][2],
                                                     x_0_u[event.obj.message['from_id']][0][2][0],
                                                     x_0_u[event.obj.message['from_id']][0][2][1],
                                                     x_0_u[event.obj.message['from_id']][0][2][2]),
                                                 keyboard=x_0_u[event.obj.message['from_id']][1].get_keyboard(),
                                                 random_id=random.randint(0, 2 ** 64))
                                vk.messages.send(user_id=event.obj.message['from_id'],
                                                 message='Мой ход:',
                                                 random_id=random.randint(0, 2 ** 64))
                            elif message == '4':
                                x_0_u[event.obj.message['from_id']][0][1][0] = 'X'
                                x_0_u[event.obj.message['from_id']][1] = build_keyboard(
                                    x_0_u[event.obj.message['from_id']][0])
                                x_0_u[event.obj.message['from_id']][3] = True
                                vk.messages.send(user_id=event.obj.message['from_id'],
                                                 message=x_0_u[event.obj.message['from_id']][2].format(
                                                     x_0_u[event.obj.message['from_id']][0][0][0],
                                                     x_0_u[event.obj.message['from_id']][0][0][1],
                                                     x_0_u[event.obj.message['from_id']][0][0][2],
                                                     x_0_u[event.obj.message['from_id']][0][1][0],
                                                     x_0_u[event.obj.message['from_id']][0][1][1],
                                                     x_0_u[event.obj.message['from_id']][0][1][2],
                                                     x_0_u[event.obj.message['from_id']][0][2][0],
                                                     x_0_u[event.obj.message['from_id']][0][2][1],
                                                     x_0_u[event.obj.message['from_id']][0][2][2]),
                                                 keyboard=x_0_u[event.obj.message['from_id']][1].get_keyboard(),
                                                 random_id=random.randint(0, 2 ** 64))
                                vk.messages.send(user_id=event.obj.message['from_id'],
                                                 message='Мой ход:',
                                                 random_id=random.randint(0, 2 ** 64))
                            elif message == '7':
                                x_0_u[event.obj.message['from_id']][0][2][0] = 'X'
                                x_0_u[event.obj.message['from_id']][1] = build_keyboard(
                                    x_0_u[event.obj.message['from_id']][0])
                                x_0_u[event.obj.message['from_id']][3] = True
                                vk.messages.send(user_id=event.obj.message['from_id'],
                                                 message=x_0_u[event.obj.message['from_id']][2].format(
                                                     x_0_u[event.obj.message['from_id']][0][0][0],
                                                     x_0_u[event.obj.message['from_id']][0][0][1],
                                                     x_0_u[event.obj.message['from_id']][0][0][2],
                                                     x_0_u[event.obj.message['from_id']][0][1][0],
                                                     x_0_u[event.obj.message['from_id']][0][1][1],
                                                     x_0_u[event.obj.message['from_id']][0][1][2],
                                                     x_0_u[event.obj.message['from_id']][0][2][0],
                                                     x_0_u[event.obj.message['from_id']][0][2][1],
                                                     x_0_u[event.obj.message['from_id']][0][2][2]),
                                                 keyboard=x_0_u[event.obj.message['from_id']][1].get_keyboard(),
                                                 random_id=random.randint(0, 2 ** 64))
                                vk.messages.send(user_id=event.obj.message['from_id'],
                                                 message='Мой ход:',
                                                 random_id=random.randint(0, 2 ** 64))
                            else:
                                vk.messages.send(user_id=event.obj.message['from_id'],
                                                 message='Место уже заполнено, выберите другое',
                                                 random_id=random.randint(0, 2 ** 64))
                        if int(message) % 3 == 2 and not x_0_u[event.obj.message['from_id']][3]:
                            if message == '2':
                                x_0_u[event.obj.message['from_id']][0][0][1] = 'X'
                                x_0_u[event.obj.message['from_id']][1] = build_keyboard(
                                    x_0_u[event.obj.message['from_id']][0])
                                x_0_u[event.obj.message['from_id']][3] = True
                                vk.messages.send(user_id=event.obj.message['from_id'],
                                                 message=x_0_u[event.obj.message['from_id']][2].format(
                                                     x_0_u[event.obj.message['from_id']][0][0][0],
                                                     x_0_u[event.obj.message['from_id']][0][0][1],
                                                     x_0_u[event.obj.message['from_id']][0][0][2],
                                                     x_0_u[event.obj.message['from_id']][0][1][0],
                                                     x_0_u[event.obj.message['from_id']][0][1][1],
                                                     x_0_u[event.obj.message['from_id']][0][1][2],
                                                     x_0_u[event.obj.message['from_id']][0][2][0],
                                                     x_0_u[event.obj.message['from_id']][0][2][1],
                                                     x_0_u[event.obj.message['from_id']][0][2][2]),
                                                 keyboard=x_0_u[event.obj.message['from_id']][1].get_keyboard(),
                                                 random_id=random.randint(0, 2 ** 64))
                                vk.messages.send(user_id=event.obj.message['from_id'],
                                                 message='Мой ход:',
                                                 random_id=random.randint(0, 2 ** 64))
                            elif message == '5':
                                x_0_u[event.obj.message['from_id']][0][1][1] = 'X'
                                x_0_u[event.obj.message['from_id']][1] = build_keyboard(
                                    x_0_u[event.obj.message['from_id']][0])
                                x_0_u[event.obj.message['from_id']][3] = True
                                vk.messages.send(user_id=event.obj.message['from_id'],
                                                 message=x_0_u[event.obj.message['from_id']][2].format(
                                                     x_0_u[event.obj.message['from_id']][0][0][0],
                                                     x_0_u[event.obj.message['from_id']][0][0][1],
                                                     x_0_u[event.obj.message['from_id']][0][0][2],
                                                     x_0_u[event.obj.message['from_id']][0][1][0],
                                                     x_0_u[event.obj.message['from_id']][0][1][1],
                                                     x_0_u[event.obj.message['from_id']][0][1][2],
                                                     x_0_u[event.obj.message['from_id']][0][2][0],
                                                     x_0_u[event.obj.message['from_id']][0][2][1],
                                                     x_0_u[event.obj.message['from_id']][0][2][2]),
                                                 keyboard=x_0_u[event.obj.message['from_id']][1].get_keyboard(),
                                                 random_id=random.randint(0, 2 ** 64))
                                vk.messages.send(user_id=event.obj.message['from_id'],
                                                 message='Мой ход:',
                                                 random_id=random.randint(0, 2 ** 64))
                            elif message == '8':
                                x_0_u[event.obj.message['from_id']][0][2][1] = 'X'
                                x_0_u[event.obj.message['from_id']][1] = build_keyboard(
                                    x_0_u[event.obj.message['from_id']][0])
                                x_0_u[event.obj.message['from_id']][3] = True
                                vk.messages.send(user_id=event.obj.message['from_id'],
                                                 message=x_0_u[event.obj.message['from_id']][2].format(
                                                     x_0_u[event.obj.message['from_id']][0][0][0],
                                                     x_0_u[event.obj.message['from_id']][0][0][1],
                                                     x_0_u[event.obj.message['from_id']][0][0][2],
                                                     x_0_u[event.obj.message['from_id']][0][1][0],
                                                     x_0_u[event.obj.message['from_id']][0][1][1],
                                                     x_0_u[event.obj.message['from_id']][0][1][2],
                                                     x_0_u[event.obj.message['from_id']][0][2][0],
                                                     x_0_u[event.obj.message['from_id']][0][2][1],
                                                     x_0_u[event.obj.message['from_id']][0][2][2]),
                                                 keyboard=x_0_u[event.obj.message['from_id']][1].get_keyboard(),
                                                 random_id=random.randint(0, 2 ** 64))
                                vk.messages.send(user_id=event.obj.message['from_id'],
                                                 message='Мой ход:',
                                                 random_id=random.randint(0, 2 ** 64))
                            else:
                                vk.messages.send(user_id=event.obj.message['from_id'],
                                                 message='Место уже заполнено, выберите другое',
                                                 random_id=random.randint(0, 2 ** 64))
                        if int(message) % 3 == 0 and not x_0_u[event.obj.message['from_id']][3]:
                            if message == '3':
                                x_0_u[event.obj.message['from_id']][0][0][2] = 'X'
                                x_0_u[event.obj.message['from_id']][1] = build_keyboard(
                                    x_0_u[event.obj.message['from_id']][0])
                                x_0_u[event.obj.message['from_id']][3] = True
                                vk.messages.send(user_id=event.obj.message['from_id'],
                                                 message=x_0_u[event.obj.message['from_id']][2].format(
                                                     x_0_u[event.obj.message['from_id']][0][0][0],
                                                     x_0_u[event.obj.message['from_id']][0][0][1],
                                                     x_0_u[event.obj.message['from_id']][0][0][2],
                                                     x_0_u[event.obj.message['from_id']][0][1][0],
                                                     x_0_u[event.obj.message['from_id']][0][1][1],
                                                     x_0_u[event.obj.message['from_id']][0][1][2],
                                                     x_0_u[event.obj.message['from_id']][0][2][0],
                                                     x_0_u[event.obj.message['from_id']][0][2][1],
                                                     x_0_u[event.obj.message['from_id']][0][2][2]),
                                                 keyboard=x_0_u[event.obj.message['from_id']][1].get_keyboard(),
                                                 random_id=random.randint(0, 2 ** 64))
                                vk.messages.send(user_id=event.obj.message['from_id'],
                                                 message='Мой ход:',
                                                 random_id=random.randint(0, 2 ** 64))
                            elif message == '6':
                                x_0_u[event.obj.message['from_id']][0][1][2] = 'X'
                                x_0_u[event.obj.message['from_id']][1] = build_keyboard(
                                    x_0_u[event.obj.message['from_id']][0])
                                x_0_u[event.obj.message['from_id']][3] = True
                                vk.messages.send(user_id=event.obj.message['from_id'],
                                                 message=x_0_u[event.obj.message['from_id']][2].format(
                                                     x_0_u[event.obj.message['from_id']][0][0][0],
                                                     x_0_u[event.obj.message['from_id']][0][0][1],
                                                     x_0_u[event.obj.message['from_id']][0][0][2],
                                                     x_0_u[event.obj.message['from_id']][0][1][0],
                                                     x_0_u[event.obj.message['from_id']][0][1][1],
                                                     x_0_u[event.obj.message['from_id']][0][1][2],
                                                     x_0_u[event.obj.message['from_id']][0][2][0],
                                                     x_0_u[event.obj.message['from_id']][0][2][1],
                                                     x_0_u[event.obj.message['from_id']][0][2][2]),
                                                 keyboard=x_0_u[event.obj.message['from_id']][1].get_keyboard(),
                                                 random_id=random.randint(0, 2 ** 64))
                                vk.messages.send(user_id=event.obj.message['from_id'],
                                                 message='Мой ход:',
                                                 random_id=random.randint(0, 2 ** 64))
                            elif message == '9':
                                x_0_u[event.obj.message['from_id']][0][2][2] = 'X'
                                x_0_u[event.obj.message['from_id']][1] = build_keyboard(
                                    x_0_u[event.obj.message['from_id']][0])
                                x_0_u[event.obj.message['from_id']][3] = True
                                vk.messages.send(user_id=event.obj.message['from_id'],
                                                 message=x_0_u[event.obj.message['from_id']][2].format(
                                                     x_0_u[event.obj.message['from_id']][0][0][0],
                                                     x_0_u[event.obj.message['from_id']][0][0][1],
                                                     x_0_u[event.obj.message['from_id']][0][0][2],
                                                     x_0_u[event.obj.message['from_id']][0][1][0],
                                                     x_0_u[event.obj.message['from_id']][0][1][1],
                                                     x_0_u[event.obj.message['from_id']][0][1][2],
                                                     x_0_u[event.obj.message['from_id']][0][2][0],
                                                     x_0_u[event.obj.message['from_id']][0][2][1],
                                                     x_0_u[event.obj.message['from_id']][0][2][2]),
                                                 keyboard=x_0_u[event.obj.message['from_id']][1].get_keyboard(),
                                                 random_id=random.randint(0, 2 ** 64))
                                vk.messages.send(user_id=event.obj.message['from_id'],
                                                 message='Мой ход:',
                                                 random_id=random.randint(0, 2 ** 64))
                            else:
                                vk.messages.send(user_id=event.obj.message['from_id'],
                                                 message='Место уже заполнено, выберите другое',
                                                 random_id=random.randint(0, 2 ** 64))
                else:
                    vk.messages.send(user_id=event.obj.message['from_id'],
                                     message='Место уже заполнено, выберите другое',
                                     random_id=random.randint(0, 2 ** 64))
                # Проверка на выигрыш
                t = won(x_0_u[event.obj.message['from_id']][0])
                if t[0]:
                    if t[1] == 'X':
                        vk.messages.send(user_id=event.obj.message['from_id'],
                                         message=x_0_u[event.obj.message['from_id']][2].format(
                                             x_0_u[event.obj.message['from_id']][0][0][0],
                                             x_0_u[event.obj.message['from_id']][0][0][1],
                                             x_0_u[event.obj.message['from_id']][0][0][2],
                                             x_0_u[event.obj.message['from_id']][0][1][0],
                                             x_0_u[event.obj.message['from_id']][0][1][1],
                                             x_0_u[event.obj.message['from_id']][0][1][2],
                                             x_0_u[event.obj.message['from_id']][0][2][0],
                                             x_0_u[event.obj.message['from_id']][0][2][1],
                                             x_0_u[event.obj.message['from_id']][0][2][2]),
                                         keyboard=x_0_u[event.obj.message['from_id']][1].get_keyboard(),
                                         random_id=random.randint(0, 2 ** 64))
                        vk.messages.send(user_id=event.obj.message['from_id'],
                                         message='Вы победили, я признаю поражение!',
                                         keyboard=a.get_keyboard(),
                                         random_id=random.randint(0, 2 ** 64))
                        del X_0_game[X_0_game.index(event.obj.message['from_id'])]
                    if t[1] == '0':
                        vk.messages.send(user_id=event.obj.message['from_id'],
                                         message=x_0_u[event.obj.message['from_id']][2].format(
                                             x_0_u[event.obj.message['from_id']][0][0][0],
                                             x_0_u[event.obj.message['from_id']][0][0][1],
                                             x_0_u[event.obj.message['from_id']][0][0][2],
                                             x_0_u[event.obj.message['from_id']][0][1][0],
                                             x_0_u[event.obj.message['from_id']][0][1][1],
                                             x_0_u[event.obj.message['from_id']][0][1][2],
                                             x_0_u[event.obj.message['from_id']][0][2][0],
                                             x_0_u[event.obj.message['from_id']][0][2][1],
                                             x_0_u[event.obj.message['from_id']][0][2][2]),
                                         keyboard=x_0_u[event.obj.message['from_id']][1].get_keyboard(),
                                         random_id=random.randint(0, 2 ** 64))
                        vk.messages.send(user_id=event.obj.message['from_id'],
                                         message='Я победил! Не отчаивайся, повезёт в следующий раз.',
                                         keyboard=a.get_keyboard(),
                                         random_id=random.randint(0, 2 ** 64))
                        del X_0_game[X_0_game.index(event.obj.message['from_id'])]
                    if t[1] == 'no':
                        vk.messages.send(user_id=event.obj.message['from_id'],
                                         message=x_0_u[event.obj.message['from_id']][2].format(
                                             x_0_u[event.obj.message['from_id']][0][0][0],
                                             x_0_u[event.obj.message['from_id']][0][0][1],
                                             x_0_u[event.obj.message['from_id']][0][0][2],
                                             x_0_u[event.obj.message['from_id']][0][1][0],
                                             x_0_u[event.obj.message['from_id']][0][1][1],
                                             x_0_u[event.obj.message['from_id']][0][1][2],
                                             x_0_u[event.obj.message['from_id']][0][2][0],
                                             x_0_u[event.obj.message['from_id']][0][2][1],
                                             x_0_u[event.obj.message['from_id']][0][2][2]),
                                         keyboard=x_0_u[event.obj.message['from_id']][1].get_keyboard(),
                                         random_id=random.randint(0, 2 ** 64))
                        vk.messages.send(user_id=event.obj.message['from_id'],
                                         message='Ничья. Конец игры!',
                                         keyboard=a.get_keyboard(),
                                         random_id=random.randint(0, 2 ** 64))
                        del X_0_game[X_0_game.index(event.obj.message['from_id'])]
                    continue
                # Ход компьютера
                if x_0_u[event.obj.message['from_id']][3]:
                    x_0_u[event.obj.message['from_id']][0] = comp_course(x_0_u[event.obj.message['from_id']][0])
                    x_0_u[event.obj.message['from_id']][1] = build_keyboard(
                        x_0_u[event.obj.message['from_id']][0])
                    x_0_u[event.obj.message['from_id']][3] = False
                    vk.messages.send(user_id=event.obj.message['from_id'],
                                     message=x_0_u[event.obj.message['from_id']][2].format(
                                         x_0_u[event.obj.message['from_id']][0][0][0],
                                         x_0_u[event.obj.message['from_id']][0][0][1],
                                         x_0_u[event.obj.message['from_id']][0][0][2],
                                         x_0_u[event.obj.message['from_id']][0][1][0],
                                         x_0_u[event.obj.message['from_id']][0][1][1],
                                         x_0_u[event.obj.message['from_id']][0][1][2],
                                         x_0_u[event.obj.message['from_id']][0][2][0],
                                         x_0_u[event.obj.message['from_id']][0][2][1],
                                         x_0_u[event.obj.message['from_id']][0][2][2]),
                                     keyboard=x_0_u[event.obj.message['from_id']][1].get_keyboard(),
                                     random_id=random.randint(0, 2 ** 64))
                    vk.messages.send(user_id=event.obj.message['from_id'],
                                     message='Ваш ход:',
                                     random_id=random.randint(0, 2 ** 64))
                # Снова проверка
                t = won(x_0_u[event.obj.message['from_id']][0])
                if t[0]:
                    if t[1] == 'X':
                        vk.messages.send(user_id=event.obj.message['from_id'],
                                         message=x_0_u[event.obj.message['from_id']][2].format(
                                             x_0_u[event.obj.message['from_id']][0][0][0],
                                             x_0_u[event.obj.message['from_id']][0][0][1],
                                             x_0_u[event.obj.message['from_id']][0][0][2],
                                             x_0_u[event.obj.message['from_id']][0][1][0],
                                             x_0_u[event.obj.message['from_id']][0][1][1],
                                             x_0_u[event.obj.message['from_id']][0][1][2],
                                             x_0_u[event.obj.message['from_id']][0][2][0],
                                             x_0_u[event.obj.message['from_id']][0][2][1],
                                             x_0_u[event.obj.message['from_id']][0][2][2]),
                                         keyboard=x_0_u[event.obj.message['from_id']][1].get_keyboard(),
                                         random_id=random.randint(0, 2 ** 64))
                        vk.messages.send(user_id=event.obj.message['from_id'],
                                         message='Вы победили, я признаю поражение!',
                                         keyboard=a.get_keyboard(),
                                         random_id=random.randint(0, 2 ** 64))
                        del X_0_game[X_0_game.index(event.obj.message['from_id'])]
                    if t[1] == '0':
                        vk.messages.send(user_id=event.obj.message['from_id'],
                                         message=x_0_u[event.obj.message['from_id']][2].format(
                                             x_0_u[event.obj.message['from_id']][0][0][0],
                                             x_0_u[event.obj.message['from_id']][0][0][1],
                                             x_0_u[event.obj.message['from_id']][0][0][2],
                                             x_0_u[event.obj.message['from_id']][0][1][0],
                                             x_0_u[event.obj.message['from_id']][0][1][1],
                                             x_0_u[event.obj.message['from_id']][0][1][2],
                                             x_0_u[event.obj.message['from_id']][0][2][0],
                                             x_0_u[event.obj.message['from_id']][0][2][1],
                                             x_0_u[event.obj.message['from_id']][0][2][2]),
                                         keyboard=x_0_u[event.obj.message['from_id']][1].get_keyboard(),
                                         random_id=random.randint(0, 2 ** 64))
                        vk.messages.send(user_id=event.obj.message['from_id'],
                                         message='Я победил! Не отчаивайся, повезёт в следующий раз.',
                                         keyboard=a.get_keyboard(),
                                         random_id=random.randint(0, 2 ** 64))
                        del X_0_game[X_0_game.index(event.obj.message['from_id'])]
                    if t[1] == 'no':
                        vk.messages.send(user_id=event.obj.message['from_id'],
                                         message=x_0_u[event.obj.message['from_id']][2].format(
                                             x_0_u[event.obj.message['from_id']][0][0][0],
                                             x_0_u[event.obj.message['from_id']][0][0][1],
                                             x_0_u[event.obj.message['from_id']][0][0][2],
                                             x_0_u[event.obj.message['from_id']][0][1][0],
                                             x_0_u[event.obj.message['from_id']][0][1][1],
                                             x_0_u[event.obj.message['from_id']][0][1][2],
                                             x_0_u[event.obj.message['from_id']][0][2][0],
                                             x_0_u[event.obj.message['from_id']][0][2][1],
                                             x_0_u[event.obj.message['from_id']][0][2][2]),
                                         keyboard=x_0_u[event.obj.message['from_id']][1].get_keyboard(),
                                         random_id=random.randint(0, 2 ** 64))
                        vk.messages.send(user_id=event.obj.message['from_id'],
                                         message='Ничья. Конец игры!',
                                         keyboard=a.get_keyboard(),
                                         random_id=random.randint(0, 2 ** 64))
                        del X_0_game[X_0_game.index(event.obj.message['from_id'])]
                    continue
            # Игра в "Угадай город"
            if event.obj.message['from_id'] in city_game:
                if not city_u[event.obj.message['from_id']][2] and city_u[event.obj.message['from_id']][0]:
                    f = random.choice(city_u[event.obj.message['from_id']][0])
                    city_u[event.obj.message['from_id']][1].append(city_u[event.obj.message['from_id']][0].pop(
                        city_u[event.obj.message['from_id']][0].index(f)
                    ))
                    response = requests.get(geo.format(f))
                    if response.json()["response"]["GeoObjectCollection"]["featureMember"]:
                        place = response.json()["response"]["GeoObjectCollection"]["featureMember"][0]["GeoObject"]
                        place = place["Point"]["pos"].split()
                        response_map = requests.get(map_resp.format(','.join(place)))
                        if response_map:
                            map_file = "map.png"
                            with open(map_file, "wb") as file:
                                file.write(response_map.content)
                            vk_up = VkUpload(vk_session)
                            id_photo = vk_up.photo_messages('map.png', event.obj.message['from_id'])
                            vk.messages.send(user_id=event.obj.message['from_id'],
                                             message='Что это за город?',
                                             attachment='photo{}_{}_{}'.format(id_photo[0]['owner_id'],
                                                                               id_photo[0]['id'],
                                                                               id_photo[0]['access_key']),
                                             random_id=random.randint(0, 2 ** 64))
                            os.remove(map_file)
                            city_u[event.obj.message['from_id']][2] = True
                        else:
                            vk.messages.send(user_id=event.obj.message['from_id'],
                                             message='Что-то пошло не так. Попробуйте написать '
                                                     'что-нибудь, чтобы перезапустить игру',
                                             random_id=random.randint(0, 2 ** 64))
                    else:
                        vk.messages.send(user_id=event.obj.message['from_id'],
                                         message='Что-то пошло не так. Попробуйте написать '
                                                 'что-нибудь, чтобы перезапустить игру',
                                         random_id=random.randint(0, 2 ** 64))
                elif city_u[event.obj.message['from_id']][2]:
                    if message.lower() == city_u[event.obj.message['from_id']][1][-1].lower():
                        vk.messages.send(user_id=event.obj.message['from_id'],
                                         message='Отлично. Если хочешь продолжить напиши любое слово, '
                                                 'если хочешь выйти - нажми на кнопку',
                                         random_id=random.randint(0, 2 ** 64))
                    else:
                        vk.messages.send(user_id=event.obj.message['from_id'],
                                         message=f'Неправильно. Это был город '
                                                 f'{city_u[event.obj.message["from_id"]][1][-1]}. Если хочешь '
                                                 f'продолжить напиши любое слово, если хочешь выйти - нажми на кнопку',
                                         random_id=random.randint(0, 2 ** 64))
                    city_u[event.obj.message['from_id']][2] = False
                elif not city_u[event.obj.message['from_id']][0]:
                    city_u[event.obj.message['from_id']][0], city_u[event.obj.message['from_id']][1] = \
                        city_u[event.obj.message['from_id']][1], city_u[event.obj.message['from_id']][0]
                    vk.messages.send(user_id=event.obj.message['from_id'],
                                     message='''Вот это да! У меня закончились столицы! Если хочешь
                                      сыграть снова - Напиши любое слово, хочешь выйти - нажми на кнопку''',
                                     random_id=random.randint(0, 2 ** 64))


if __name__ == '__main__':
    main()
