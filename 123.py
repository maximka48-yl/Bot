import os
import random

import requests
import vk_api
from vk_api.bot_longpoll import VkBotLongPoll, VkBotEventType
from vk_api.keyboard import VkKeyboard
from vk_api.upload import VkUpload

TYPE = {'смешанная': 'sat,skl', 'спутник': 'sat', 'схема': 'map'}
resp = None
geo = "http://geocode-maps.yandex.ru/1.x/?apikey=40d1649f-0493-4b70-98ba-98533de7710b&geocode={}&format=json"
map_resp = "http://static-maps.yandex.ru/1.x/?ll={}&spn=0.01,0.01&l={}"


def main():
    vk_session = vk_api.VkApi(
        token='b0509e54657471c56c239686f09a8322a37846b19769e902e69bf1136cc2f9c254a26499001c3e15f3dca')

    longpoll = VkBotLongPoll(vk_session, 194502422)
    f = False
    place = None
    resp = None
    people = set()

    a = VkKeyboard(True)
    a.add_button('Спутник')
    a.add_button('Схема')
    a.add_button('Смешанная')

    vk = vk_session.get_api()

    for event in longpoll.listen():
        if event.type == VkBotEventType.MESSAGE_NEW:
            data = vk.messages.getHistory(offset=0,
                                          count=1,
                                          user_id=event.obj.message['from_id'])
            message = data['items'][0]['text']
            if event.obj.message['from_id'] not in people:
                vk.messages.send(user_id=event.obj.message['from_id'],
                                 message="Привет! На самоизоляции, но хочешь повидать мир? Скажи, какую местность ты хочешь увидеть",
                                 random_id=random.randint(0, 2 ** 64))
                people.add(event.obj.message['from_id'])
            elif f:
                if message.lower() not in TYPE.keys():
                    vk.messages.send(user_id=event.obj.message['from_id'],
                                     message='Данного типа карты не существует. Пожалуйста, выберите тип из предложенных',
                                     keyboard=a.get_keyboard(),
                                     random_id=random.randint(0, 2 ** 64))
                    continue
                response_map = requests.get(map_resp.format(','.join(place), TYPE[message.lower()]))
                if response_map:
                    map_file = "map.png"
                    with open(map_file, "wb") as file:
                        file.write(response_map.content)
                    vk_up = VkUpload(vk_session)
                    id_photo = vk_up.photo_messages('map.png', event.obj.message['from_id'])
                    vk.messages.send(user_id=event.obj.message['from_id'],
                                     message=f'Это {resp}. Что ещё хотите увидеть?',
                                     attachment='photo{}_{}_{}'.format(id_photo[0]['owner_id'], id_photo[0]['id'],
                                                                       id_photo[0]['access_key']),
                                     random_id=random.randint(0, 2 ** 64))
                    os.remove(map_file)
                else:
                    vk.messages.send(user_id=event.obj.message['from_id'],
                                     message='К сожалению, мы не нашли фото этой местности. Попропуй найти что-нибудь другое',
                                     random_id=random.randint(0, 2 ** 64))
                f = False
            else:
                response = requests.get(geo.format(message))
                if response.json()["response"]["GeoObjectCollection"]["featureMember"]:
                    place = response.json()["response"]["GeoObjectCollection"]["featureMember"][0]["GeoObject"]
                    place = place["Point"]["pos"].split()
                    resp = response.json()["response"]["GeoObjectCollection"]["featureMember"][0]["GeoObject"]
                    resp = resp["metaDataProperty"]["GeocoderMetaData"]["text"]
                    vk.messages.send(user_id=event.obj.message['from_id'],
                                     message='Какой тип карты?',
                                     keyboard=a.get_keyboard(),
                                     random_id=random.randint(0, 2 ** 64))
                    f = True
                else:
                    vk.messages.send(user_id=event.obj.message['from_id'],
                                     message='Такого места нет, попробуй ещё',
                                     random_id=random.randint(0, 2 ** 64))


if __name__ == '__main__':
    main()
