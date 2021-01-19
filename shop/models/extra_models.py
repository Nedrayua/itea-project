import datetime
import time

from telebot.apihelper import ApiException
from . import me
# from shop.models import shop_models
#
# from shop.bot.shop_bot import bot


# class Sender:
#
#     def __init__(self, users, **message_data):
#         """
#         Принимаем переменные users, message_data и инициализируем внутри себя
#         :users: queryset of users from mongodb
#         :** message_data: именнованные аргументы, которые дают возможность использовать как клавиатуру так и
#         кнопки для оправки сообщений
#         """
#         self._users = users
#         self._message_data = message_data
#
#     def send_message(self):
#         """
#         По созданному объекту делает рассылку юзерам. Во избежания блокировки при перегрузки сервера собщениями,
#         используем time.sleep()
#         В случае отсылки новости заблокированному пользователю, формирует список заблокированных пользователей и
#         в конце выполнения программы рассылки ставить статус всем пользователям из списка is_block = True
#         """
#         blocked_ids = []  # создаем список юзеров, которых отлавливаем в процессе отправки сообщения
#         users = self._users.filter(is_block=False)
#         for user in users:
#             try:
#                 bot.send_message(
#                     user.telegram_id,
#                     **self._message_data
#                 )
#             except ApiException as e:
#                 # print(dir(e))   # вначале проверим где именно лежит исключение 403, так как ApiException вляется
#                 # параметром ошбки. Для этого вызываем метод дир, который покажет все содержимое от ApiException
#                 if e.error_code == 403:
#                     blocked_ids.append(user.telegram_id)
#                 else:
#                     raise e
#             time.sleep(0.1)
#         shop_models.User.objects(telegram_id__in=blocked_ids).update(is_block=True)


class Time(me.Document):
    """
    Миксин, для привязки к объекту времени создания и модификации
    """
    created = me.StringField()
    modified = me.StringField()
    meta = {'allow_inheritance': True}  # необходимо для того, что бы использовать класс монго ДБ как миксин

    def save(self, *args, **kwargs):
        if not self.created:
            self.created = str(datetime.datetime.now())[:-7]
        self.modified = str(datetime.datetime.now())[:-7]
        super().save(*args, **kwargs)


class News(Time):
    title = me.StringField(required=True, min_length=2, max_length=128)
    body = me.StringField(required=True, min_length=2, max_length=2048)

    def formatted_news(self):
        return f'{self.created}\n' \
               f'{self.title}\n' \
               f'{self.body}'

    # def save(self, *args, **kwargs):
    #     users = User.objects()
    #     sender = Sender(users, text=self.formatted_news())
    #     sender.send_message()
    #     super().save(*args, **kwargs)
