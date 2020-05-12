import datetime
import calendar
import vk_api
from vk_api.bot_longpoll import VkBotLongPoll, VkBotEventType
import random
LOGIN = "saichuckp@gmail.com"
PASSWORD = "8h8TPwnkjx"
TOKEN = "1467bebbbd6b9fe866defe649bc339248c34c4fdfa2882bd3131006bb9f6977671098a5574d4acf325e8a"

days = {"Mon": ["Понедельник", 0], "Tue": ["Вторник", 1], "Wed": ["Среда", 2], "Thu": ["Четверг", 3],
        "Fri": ["Пятница", 4], "Sat": ["Суббота", 5], "Sun": ["Воскресенье", 6]}


def picture(day):
    login, password, token = LOGIN, PASSWORD, TOKEN
    vk_session = vk_api.VkApi(login, password, token=token)
    vk = vk_session.get_api()
    album = "270750048"
    group = "-195259314"
    response = vk.photos.get(album_id=album, owner_id=group)
    if response['items']:
        print(response['items'])
        f = response['items'][days[day][1]]
        return f["id"], f["owner_id"], days[day][0]


def main():
    vk_session = vk_api.VkApi(
        token="c358537518da025557e9ad76fb685b6fb49d19fb3332176ff5b6db42c9849f02888979a1684d259545a29")

    longpoll = VkBotLongPoll(vk_session, 195259314)
    f1 = True
    f2 = False
    for event in longpoll.listen():
        if event.type == VkBotEventType.MESSAGE_NEW:
            if f1:
                print(event)
                print('Новое сообщение:')
                print('Для меня от:', event.obj.message['from_id'])
                print('Текст:', event.obj.message['text'])
                vk = vk_session.get_api()
                user = vk.users.get(user_ids=event.obj.message['from_id'])
                name = user[0]['first_name']
                vk.messages.send(user_id=event.obj.message['from_id'],
                    random_id=random.randint(0, 2 ** 64),
                    message=f"Привет {name}\nЯ могу сказать в какой день недели была дата (Формат YYYY.MM.DD)")
                f1 = False
                f2 = True
                continue
            if f2:
                print(event)
                print('Новое сообщение:')
                print('Для меня от:', event.obj.message['from_id'])
                print('Текст:', event.obj.message['text'])
                l = str(event.obj.message['text']).split(".")
                if len(l) == 3 and len(l[0]) == 4 and len(l[1]) == 2 and len(l[2]) == 2 and l[0].isdigit() and l[1].isdigit() and l[2].isdigit():
                    vk = vk_session.get_api()
                    f = picture(calendar.day_abbr[datetime.date(int(l[0]), int(l[1]), int(l[2])).weekday()])
                    vk.messages.send(user_id=event.obj.message['from_id'],
                                     random_id=random.randint(0, 2 ** 64),
                                     message=f[2],
                                     attachment=f"photo{f[1]}_{f[0]}")
                else:
                    vk = vk_session.get_api()
                    vk.messages.send(user_id=event.obj.message['from_id'],
                                     random_id=random.randint(0, 2 ** 64),
                                     message="Неверный формат")




if __name__ == '__main__':
    main()
