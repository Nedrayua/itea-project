import time

from telebot.apihelper import ApiException

from shop.bot.shop_bot import bot
from shop.models import shop_models


class Sender:

    def __init__(self, users, **message_data):
        """
        Принимаем переменные users, message_data и инициализируем внутри себя
        :users: queryset of users from mongodb
        :** message_data: именнованные аргументы, которые дают возможность использовать как клавиатуру так и
        кнопки для оправки сообщений
        """
        self._users = users
        self._message_data = message_data

    def send_message(self):
        """
        По созданному объекту делает рассылку юзерам. Во избежания блокировки перегрузки сервера собщениями,
        используем time.sleep()
        """
        blocked_ids = []  # создаем список юзеров, которых отлавливаем в процессе отправки сообщения
        users = self._users.filter(is_block=False)
        for u in users:
            try:
                bot.send_message(
                    u.telegram_id,
                    **self._message_data
                )
            except ApiException as e:
                # print(dir(e))   # вначале проверим где именно лежит исключение 403, так как ApiException вляется
                # параметром ошбки. Для этого вызываем метод дир, который покажет все содержимое от ApiException
                if e.error_code == 403:
                    blocked_ids.append(u.telegram_id)
                else:
                    raise e
            time.sleep(0.1)
        shop_models.User.objects(telegram_id__in=blocked_ids).update(is_block=True)


def cron_unlock_users():
    """
    Функция, которая предназначена для переодичной разблокировки заблокированных пользователей.
    1. Обработка всех юзеров;
    2. Два дня сон;
    3. Обрабртка всех юзеров;
    4. ...
    """
    while True:
        shop_models.User.objects(is_block=True).update(is_block=False)
        minute = 60
        hour = 60 * minute
        day = 24 * hour
        time.sleep(2 * day)


# Thread(target=cron_unlock_users).start()

# Запускает фнкцию cron_unlock_users в отдельном потоке, который не останавливается а фнкция ссрабатыает раз
# в два дня
# =
