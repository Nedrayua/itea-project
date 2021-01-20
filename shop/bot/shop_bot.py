import json
from telebot import TeleBot
from telebot.types import Update, ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardMarkup, Message
from mongoengine import NotUniqueError, ValidationError
from flask import Flask, request, abort

from shop.models import shop_models
from shop.models import extra_models
from . utils import inline_kb_from_iterable, inline_kb
from . config import TOKEN, WEBHOOK_URI
from . import constance

app = Flask(__name__)
bot = TeleBot(TOKEN)


@app.route(WEBHOOK_URI, methods=['POST'])
def handle_webhook():
    if request.headers.get('content-type') == 'application/json':
        json_string = request.get_data().decode('utf-8')
        update = Update.de_json(json_string)
        bot.process_new_updates([update])
        return ''
    abort(403)  # доступ запроса к боту не разрешен


@bot.message_handler(commands=['start'])
def handle_start(message):
    """
    Хэндлер обработки нажатия на кнопку /start
    """
    name = f', {message.from_user.first_name}!' if getattr(message.from_user, 'first_name') else "!"
    try:
        shop_models.User.objects.create(
            telegram_id=message.chat.id,
            username=getattr(message.from_user, 'username', None),
            first_name=getattr(message.from_user, 'first_name', None)
        )
    except NotUniqueError:
        greetings = constance.GREETINGS.format(name)
    else:
        greetings = constance.GREETINGS_ELSE.format(name)

    kb = ReplyKeyboardMarkup(resize_keyboard=True)
    buttons = [KeyboardButton(n) for n in constance.START_KB.values()]
    kb.add(*buttons)

    bot.send_message(
        message.chat.id,
        greetings, reply_markup=kb
    )


@bot.message_handler(func=lambda m: constance.START_KB[constance.CATEGORIES] == m.text)
def handle_categories(message):
    """
    Если пользователь жмет кнопку КАТЕГОРИЙ, идет поиск соответствия в словаре START_KB по конкретной категории
    и если текст равен категории, которая будет обслуживаться данным хэндлером выдается квэрисет категирий. Следует
    обратить внимание что категории должны быть рутовые (корневые), так как основная категория будет в
    первоначальном списке
    """
    root_category = shop_models.Category.get_root_categories()
    kb = inline_kb_from_iterable(constance.CATEGORY_TAG, root_category)

    bot.send_message(
        message.chat.id,
        constance.CHOICE_CATEGORY,
        reply_markup=kb
    )


@bot.message_handler(func=lambda message: constance.START_KB[constance.CART] == message.text)
def handle_cart(message: Message):
    """
    Хэндлер обрабатывающий кнопку "корзина". При нажати выводит товары которые находятся в корзине отдельными
    сообщениями с кнопкой удаления товара из корзины и кнопкой оформления заказа
    """
    user = shop_models.User.objects.get(telegram_id=message.chat.id)
    cart = user.get_active_cart()
    total_sum = sum(list(map(lambda x: x.product_price, cart.products)))
    num_of_prod = len(cart.products)
    product = 'товар' if str(num_of_prod)[-1] == "1" else 'товара' if str(num_of_prod)[-1] in ["2", "3", "4"]\
        else 'товаров'
    text = constance.CART_TEXT.format(num_of_prod, product, total_sum)

    for prod_id, count in cart.cart_product_dict().items():
        prod = shop_models.Product.objects.get(id=prod_id)
        prod_text = prod.formatted_product(True) + constance.CART_TEXT_2.format(count, prod.product_price * count)

        bot.send_photo(
            message.chat.id,
            prod.image.read(),
            caption=prod_text,
        )

    data = {'tag': constance.EDITING_CART_TAG}
    button1 = inline_kb(data, constance.EDIT_CART, True)

    data = {'tag': constance.START_ORDERING_TAG}
    button2 = inline_kb(data, constance.ORDERING, True)

    kb = InlineKeyboardMarkup(row_width=1)
    kb.add(button1, button2)

    bot.send_message(
        message.chat.id,
        text=text,
        reply_markup=kb
    )


@bot.message_handler(func=lambda message: constance.START_KB[constance.SETTINGS] == message.text)
def handle_settings(message: Message):
    """
    Хэндлер отрабатывающий кнопку "настройки"
    """
    user = shop_models.User.objects.get(telegram_id=message.chat.id)
    data = user.formatted_data()

    button_data = {"tag": constance.CHANGE_SETTINGS_TAG}
    kb = inline_kb(button_data, constance.CHANGE_SETTINGS_TEXT)

    bot.send_message(
        message.chat.id,
        data,
        reply_markup=kb
    )


@bot.message_handler(func=lambda message: constance.START_KB[constance.NEWS] == message.text)
def handler_news(message: Message):
    """
    Хэндлер отрабатывающий кнопку "новости"
    """
    news = sorted(extra_models.News.objects(), key=lambda obj: obj.created, reverse=True)
    for i in range(5):
        bot.send_message(
            message.chat.id,
            text=news[i].formatted_news()
        )


@bot.message_handler(func=lambda message: constance.START_KB[constance.PRODUCTS_WITH_DISCOUNT] == message.text)
def handler_news(message: Message):
    """
    Хэндлер отрабатывающий кнопку "продукты со скидкой"
    """
    products = shop_models.Product.objects(discount__gt=0)
    for product in products:
        prod_callback_data = {
            'id': str(product.id),
            'tag': constance.PRODUCT_TAG
            }
        kb = inline_kb(prod_callback_data, constance.ADD_TO_CART)

        bot.send_photo(
            message.chat.id,
            product.image.read(),
            caption=product.formatted_product(),
            reply_markup=kb
            )


@bot.callback_query_handler(lambda call: json.loads(call.data)['tag'] == constance.EDITING_CART_TAG)
def handle_change_content_cart(call):
    """
    Обрабатывает нажатие на кнопку изменения корзины
    """
    user = shop_models.User.objects.get(telegram_id=call.message.chat.id)
    cart = user.get_active_cart()
    total_sum = sum(list(map(lambda x: x.product_price, cart.products)))
    num_of_prod = len(cart.products)
    product = 'товар' if str(num_of_prod)[-1] == "1" else 'товара' if str(num_of_prod)[-1] in ["2", "3", "4"] \
        else 'товаров'

    bot.send_message(
         call.message.chat.id,
         text=constance.CART_TEXT.format(num_of_prod, product, total_sum)
    )

    for prod_id, count in cart.cart_product_dict().items():
        prod = shop_models.Product.objects.get(id=prod_id)
        prod_text = prod.formatted_product(True) + constance.CART_TEXT_2.format(count, prod.product_price * count)

        data = {
            'id': str(prod.id),
            'tag': constance.ADD_TO_CART_FROM_CART_TAG
                }
        button_add = inline_kb(data, constance.ADD_TO_CART, True)

        data = {
            'id': str(prod.id),
            'tag': constance.TAKE_AWAY_FROM_CART_TAG
        }
        button_out = inline_kb(data, constance.TAKE_AWAY_FROM_CART, True)

        kb = InlineKeyboardMarkup()
        kb.add(button_add, button_out)

        bot.send_photo(
            call.message.chat.id,
            prod.image.read(),
            caption=prod_text,
            reply_markup=kb
        )


@bot.callback_query_handler(lambda call: json.loads(call.data)['tag'] == constance.TAKE_AWAY_FROM_CART_TAG)
def handle_change_content_cart(call):
    """
    Обрабатывает нажатие на кнопку удаления товара
    """
    user = shop_models.User.objects.get(telegram_id=call.message.chat.id)
    cart = user.get_active_cart()
    cart.products.pop(cart.find_index_of_product(json.loads(call.data)['id']))
    cart.save()

    data = {"tag": constance.EDITING_CART_TAG}
    kb = inline_kb(data, constance.EDIT_CART_CONTINUE)

    bot.send_message(
        call.message.chat.id,
        text=constance.GOODS_WITHDRAWN,
        reply_markup=kb
    )


@bot.callback_query_handler(lambda call: json.loads(call.data)['tag'] == constance.ADD_TO_CART_FROM_CART_TAG)
def handle_change_content_cart(call):
    """
    Обрабатывает нажатие на кнопку добавления товара в КОРЗИНЕ с кнопкой возврата к редактированию корзины
    """
    product = shop_models.Product.objects.get(id=json.loads(call.data)['id'])
    user = shop_models.User.objects.get(telegram_id=call.message.chat.id)
    cart = user.get_active_cart()
    cart.add_product(product)

    data = {"tag": constance.EDITING_CART_TAG}
    kb = inline_kb(data, constance.EDIT_CART_CONTINUE)

    bot.send_message(
        call.message.chat.id,
        text=constance.ADD_TO_CART_COMPLETED,
        reply_markup=kb
    )


@bot.callback_query_handler(lambda call: json.loads(call.data)['tag'] == constance.START_ORDERING_TAG)
def handle_change_content_cart(call):
    """
    Обрабатывает нажатие на кнопку Оформление заказа
    """
    user = shop_models.User.objects.get(telegram_id=call.message.chat.id)
    cart = user.get_active_cart()
    order = user.get_order_in_clearance_status()
    order.products = cart.products
    order.save()
    cart.is_active = False
    cart.save()
    fill_in_callback_data = {
        'tag': constance.FILLING_IN_THE_ORDER_TAG,
    }
    kb = inline_kb(fill_in_callback_data, constance.ORDERED_NAMES_B[constance.start_order])

    bot.edit_message_text(
            constance.ORDERED_MESSAGE[constance.start_order],
            chat_id=call.message.chat.id,
            message_id=call.message.id,
            reply_markup=kb
    )


@bot.callback_query_handler(lambda call: json.loads(call.data)['tag'] == constance.FILLING_IN_THE_ORDER_TAG)
def handle_change_content_cart(call):
    """
    Обработчик заполнения информаци о получателе заказа. Отображает текущий статус заполнения. Формирует кнопки
    для перехода к соответствующим разделам
    """
    user = shop_models.User.objects.get(telegram_id=call.message.chat.id)
    order = user.get_order_in_clearance_status()
    text = order.get_delivery_data()

    bot.edit_message_text(
        text=text,
        chat_id=call.message.chat.id,
        message_id=call.message.id,
    )

    kb = InlineKeyboardMarkup(row_width=1)
    data_recipient = {
        'tag': constance.FILLING_IN_SPECIFIC_ORDER_TAG,
        'command': constance.recipient
        }
    button_recipient = inline_kb(data_recipient, constance.ORDERED_NAMES_B[constance.recipient], True)

    data_destination = {
        'tag': constance.FILLING_IN_SPECIFIC_ORDER_TAG,
        'command': constance.destination
        }
    button_destination = inline_kb(data_destination, constance.ORDERED_NAMES_B[constance.destination], True)

    data_delivery_method = {
        'tag': constance.FILLING_IN_SPECIFIC_ORDER_TAG,
        'command': constance.delivery_method
        }
    button_delivery_method = inline_kb(data_delivery_method, constance.ORDERED_NAMES_B[constance.delivery_method], True)

    data_branch_number = {
        'tag': constance.FILLING_IN_SPECIFIC_ORDER_TAG,
        'command': constance.branch_number
        }
    button_branch_number = inline_kb(data_branch_number, constance.ORDERED_NAMES_B[constance.branch_number], True)

    data_phone_number = {
        'tag': constance.FILLING_IN_SPECIFIC_ORDER_TAG,
        'command': constance.phone_number
        }
    button_phone_number = inline_kb(data_phone_number, constance.ORDERED_NAMES_B[constance.phone_number], True)

    data_complete_order = {
        'tag': constance.COMPLETE_ORDERING_TAG,
        }
    button_complete_order = inline_kb(data_complete_order, constance.ORDERED_NAMES_B[constance.complete_order], True)

    if "" in order.delivery_data.values():
        kb.add(button_recipient, button_destination, button_delivery_method, button_branch_number, button_phone_number)
    else:
        kb.add(button_recipient, button_destination, button_delivery_method, button_branch_number, button_phone_number,
               button_complete_order)
    bot.send_message(
        text=constance.CHANGE_SETTINGS_NAMES_B[constance.choice_category],
        chat_id=call.message.chat.id,
        reply_markup=kb
    )


@bot.callback_query_handler(func=lambda call: json.loads(call.data)['tag'] == constance.FILLING_IN_SPECIFIC_ORDER_TAG)
def handle_change_specifically(call):
    """
    хэендлер обработки нажатия кнопок для заполнения параметров получателя заказа
    """
    call_dict = json.loads(call.data)
    if call_dict['command'] == constance.recipient:
        msg = bot.send_message(call.message.chat.id, constance.ORDERED_MESSAGE[call_dict['command']])
        bot.register_next_step_handler(msg, handle_enter_recipient)

    elif call_dict['command'] == constance.destination:
        msg = bot.send_message(call.message.chat.id, constance.ORDERED_MESSAGE[call_dict['command']])
        bot.register_next_step_handler(msg, handle_enter_destination)

    elif call_dict['command'] == constance.delivery_method:
        kb = InlineKeyboardMarkup(row_width=1)
        data_new_post = {
            'tag': constance.CHOICE_DELIVERY_METHOD,
            'command': constance.new_post
        }
        button_new_post = inline_kb(data_new_post, constance.DELIVERY_COMPANIES[constance.new_post], True)
        data_delivery = {
            'tag': constance.CHOICE_DELIVERY_METHOD,
            'command': constance.delivery
        }
        button_delivery = inline_kb(data_delivery, constance.DELIVERY_COMPANIES[constance.delivery], True)
        data_meest_express = {
            'tag': constance.CHOICE_DELIVERY_METHOD,
            'command': constance.meest_express
        }
        button_meest_express = inline_kb(data_meest_express, constance.DELIVERY_COMPANIES[constance.meest_express],
                                         True)
        data_autolux = {
            'tag': constance.CHOICE_DELIVERY_METHOD,
            'command': constance.autolux
        }
        button_autolux = inline_kb(data_autolux, constance.DELIVERY_COMPANIES[constance.autolux], True)
        kb.add(button_new_post, button_delivery, button_meest_express, button_autolux)
        bot.edit_message_text(
            text=constance.ORDERED_MESSAGE[call_dict['command']],
            chat_id=call.message.chat.id,
            message_id=call.message.id,
            reply_markup=kb
        )
    elif call_dict['command'] == constance.branch_number:
        msg = bot.send_message(call.message.chat.id, constance.ORDERED_MESSAGE[call_dict['command']])
        bot.register_next_step_handler(msg, handle_enter_branch_number)

    elif call_dict['command'] == constance.phone_number:
        msg = bot.send_message(call.message.chat.id, constance.ORDERED_MESSAGE[call_dict['command']])
        bot.register_next_step_handler(msg, handle_enter_phone_number)


def handle_enter_recipient(message):
    """
    Хэндлер отработки получателя заказа
    """
    user = shop_models.User.objects.get(telegram_id=message.from_user.id)
    order = user.get_order_in_clearance_status()
    try:
        order.delivery_data[str(constance.recipient)] = message.text
        print(order.delivery_data[str(constance.recipient)])
        order.save()
        message_text = constance.CHANGE_COMPLETED
    except ValidationError:
        message_text = constance.CHANGE_SETTINGS_MESSAGE[constance.wrong_change]

    data = {"tag": constance.FILLING_IN_THE_ORDER_TAG}
    kb = inline_kb(data, constance.ORDERED_NAMES_B[constance.continue_order])

    bot.send_message(
        message.chat.id,
        text=message_text,
        reply_markup=kb
    )


def handle_enter_destination(message):
    """
    Хэндлер отработки для указания населенного пункта для отправления заказа
    """
    user = shop_models.User.objects.get(telegram_id=message.from_user.id)
    order = user.get_order_in_clearance_status()
    try:
        order.delivery_data[str(constance.destination)] = message.text
        order.save()
        message_text = constance.CHANGE_COMPLETED
    except ValidationError:
        message_text = constance.CHANGE_SETTINGS_MESSAGE[constance.wrong_change]

    data = {"tag": constance.FILLING_IN_THE_ORDER_TAG}
    kb = inline_kb(data, constance.ORDERED_NAMES_B[constance.continue_order])

    bot.send_message(
        message.chat.id,
        text=message_text,
        reply_markup=kb
    )


def handle_enter_branch_number(message):
    """
    Хэндлер отработки номера отделения фирмы-курьера
    """
    user = shop_models.User.objects.get(telegram_id=message.from_user.id)
    order = user.get_order_in_clearance_status()
    try:
        order.delivery_data[str(constance.branch_number)] = message.text
        order.save()
        message_text = constance.CHANGE_COMPLETED
    except ValidationError:
        message_text = constance.CHANGE_SETTINGS_MESSAGE[constance.wrong_change]

    data = {"tag": constance.FILLING_IN_THE_ORDER_TAG}
    kb = inline_kb(data, constance.ORDERED_NAMES_B[constance.continue_order])

    bot.send_message(
        message.chat.id,
        text=message_text,
        reply_markup=kb
    )


def handle_enter_phone_number(message):
    """
    Хэндлер отработки номера телефона получателя заказа
    """
    user = shop_models.User.objects.get(telegram_id=message.from_user.id)
    order = user.get_order_in_clearance_status()
    try:
        order.delivery_data[str(constance.phone_number)] = message.text
        order.save()
        message_text = constance.CHANGE_COMPLETED
    except ValidationError:
        message_text = constance.CHANGE_SETTINGS_MESSAGE[constance.wrong_change]

    data = {"tag": constance.FILLING_IN_THE_ORDER_TAG}
    kb = inline_kb(data, constance.ORDERED_NAMES_B[constance.continue_order])

    bot.send_message(
        message.chat.id,
        text=message_text,
        reply_markup=kb
    )


@bot.callback_query_handler(lambda call: json.loads(call.data)['tag'] == constance.CHOICE_DELIVERY_METHOD)
def handle_choice_delivery_method(call):
    """
    Обработка кнопки выбора фирмы-курьера
    """
    user = shop_models.User.objects.get(telegram_id=call.message.chat.id)
    order = user.get_order_in_clearance_status()
    order.delivery_data[str(constance.delivery_method)] = constance.DELIVERY_COMPANIES[json.loads(call.data)["command"]]
    order.save()

    data = {"tag": constance.FILLING_IN_THE_ORDER_TAG}
    kb = inline_kb(data, constance.ORDERED_NAMES_B[constance.continue_order])

    bot.send_message(
        call.message.chat.id,
        text=constance.CHANGE_COMPLETED,
        reply_markup=kb
    )


@bot.callback_query_handler(lambda call: json.loads(call.data)['tag'] == constance.CHANGE_SETTINGS_TAG)
def handle_change_settings(call):
    """
    Обрабатывает нажатие на кнопку изменения настроек. Создает кнопки соответствующие необходимым изменениям
    на выбор клиенту
    """
    kb = InlineKeyboardMarkup(row_width=1)
    data_name = {
            'tag': constance.CHANGE_SPECIFIC_SETTINGS_TAG,
            'command': constance.change_name
        }
    button_change_name = inline_kb(data_name, constance.CHANGE_SETTINGS_NAMES_B[constance.change_name], True)
    data_phone = {
            'tag': constance.CHANGE_SPECIFIC_SETTINGS_TAG,
            'command': constance.change_phone
        }
    button_change_phone = inline_kb(data_phone, constance.CHANGE_SETTINGS_NAMES_B[constance.change_phone], True)
    data_change_email = {
            'tag': constance.CHANGE_SPECIFIC_SETTINGS_TAG,
            'command': constance.change_email
        }
    button_change_email = inline_kb(data_change_email, constance.CHANGE_SETTINGS_NAMES_B[constance.change_email], True)
    data_change_post = {
            'tag': constance.CHANGE_SPECIFIC_SETTINGS_TAG,
            'command': constance.change_post
        }
    button_change_post = inline_kb(data_change_post, constance.CHANGE_SETTINGS_NAMES_B[constance.change_post], True)

    kb.add(button_change_name, button_change_phone, button_change_email, button_change_post)

    bot.edit_message_text(
        text=constance.CHANGE_SETTINGS_NAMES_B[constance.choice_category],
        chat_id=call.message.chat.id,
        message_id=call.message.id,
        reply_markup=kb
    )


@bot.callback_query_handler(func=lambda call: json.loads(call.data)['tag'] == constance.CHANGE_SPECIFIC_SETTINGS_TAG)
def handle_change_specifically(call):
    """
    хэендлер обработки нажатия кнопки изменения параметров юзера с последующим перенаправлением в хэндлер обработки
    изменения
    """
    call_dict = json.loads(call.data)
    if call_dict['command'] == constance.change_name:
        msg = bot.send_message(call.message.chat.id, constance.CHANGE_SETTINGS_MESSAGE[call_dict['command']])
        bot.register_next_step_handler(msg, handle_change_first_name)

    elif call_dict['command'] == constance.change_phone:
        msg = bot.send_message(call.message.chat.id, constance.CHANGE_SETTINGS_MESSAGE[call_dict['command']])
        bot.register_next_step_handler(msg, handle_change_phone)

    elif call_dict['command'] == constance.change_email:
        msg = bot.send_message(call.message.chat.id, constance.CHANGE_SETTINGS_MESSAGE[call_dict['command']])
        bot.register_next_step_handler(msg, handle_change_email)

    elif call_dict['command'] == constance.change_post:
        msg = bot.send_message(call.message.chat.id, constance.CHANGE_SETTINGS_MESSAGE[call_dict['command']])
        bot.register_next_step_handler(msg, handle_change_post)


def handle_change_first_name(message):
    """
    Хэндлел отработки изменения имени пользователя
    """
    user = shop_models.User.objects.get(telegram_id=message.from_user.id)
    try:
        user.first_name = message.text
        user.save()
        message_text = constance.CHANGE_COMPLETED
    except ValidationError:
        message_text = constance.CHANGE_SETTINGS_MESSAGE[constance.wrong_change]

    data = {"tag": constance.CHANGE_SETTINGS_TAG}
    kb = inline_kb(data, constance.CHANGE_SETTINGS_NAMES_B[constance.back_to_settings])

    bot.send_message(
        message.chat.id,
        text=message_text,
        reply_markup=kb
    )


def handle_change_phone(message):
    """
    Хэндлер отработки изменения номера телефона пользователя
    """
    user = shop_models.User.objects.get(telegram_id=message.from_user.id)
    try:
        user.phone_number = message.text
        user.save()
        message_text = constance.CHANGE_COMPLETED
    except ValidationError:
        message_text = constance.CHANGE_SETTINGS_MESSAGE[constance.wrong_change]

    data = {"tag": constance.CHANGE_SETTINGS_TAG}
    kb = inline_kb(data, constance.CHANGE_SETTINGS_NAMES_B[constance.back_to_settings])

    bot.send_message(
            message.chat.id,
            text=message_text,
            reply_markup=kb
    )


def handle_change_email(message):
    """
    Хэндлер отработки изменения электронного адреса пользователя
    """
    user = shop_models.User.objects.get(telegram_id=message.from_user.id)
    try:
        user.email = message.text
        user.save()
        message_text = constance.CHANGE_COMPLETED
    except ValidationError:
        message_text = constance.CHANGE_SETTINGS_MESSAGE[constance.wrong_change]

    data = {"tag": constance.CHANGE_SETTINGS_TAG}
    kb = inline_kb(data, constance.CHANGE_SETTINGS_NAMES_B[constance.back_to_settings])

    bot.send_message(
        message.chat.id,
        text=message_text,
        reply_markup=kb
    )


def handle_change_post(message):
    """
    Хзндлер отработки изменения адреса пользователя
    """
    user = shop_models.User.objects.get(telegram_id=message.from_user.id)
    try:
        user.user_address = message.text
        user.save()
        message_text = constance.CHANGE_COMPLETED
    except ValidationError:
        message_text = constance.CHANGE_SETTINGS_MESSAGE[constance.wrong_change]
    data = json.dumps({"tag": constance.CHANGE_SETTINGS_TAG})
    kb = inline_kb(data, constance.CHANGE_SETTINGS_NAMES_B[constance.back_to_settings])

    bot.send_message(
        message.chat.id,
        text=message_text,
        reply_markup=kb
    )


@bot.callback_query_handler(lambda call: json.loads(call.data)['tag'] == constance.CATEGORY_TAG)
def handle_category_click(call):
    """
    Хэндлер отрабатывающий клик по категории. Если у категории есть подкатегории - выодится списк кнопок, если нет -
    выводится список продуктов закрепленных в категории
    """
    category = shop_models.Category.objects.get(
         id=json.loads(call.data)['id']
    )
    if category.subcategories:
        kb = inline_kb_from_iterable(constance.CATEGORY_TAG, category.subcategories, category.parent, row=1)

        bot.edit_message_text(
            category.title,
            chat_id=call.message.chat.id,
            message_id=call.message.id,
            reply_markup=kb
        )
    else:
        products = category.get_products()
        for product in products:
            prod_callback_data = {
                'id': str(product.id),
                'tag': constance.PRODUCT_TAG
                }
            kb = inline_kb(prod_callback_data, constance.ADD_TO_CART)

            bot.send_photo(
                call.message.chat.id,
                product.image.read(),
                caption=product.formatted_product(),
                reply_markup=kb
            )


@bot.callback_query_handler(lambda call: json.loads(call.data)['tag'] == constance.PRODUCT_TAG)
def handle_add_product(call):
    """
    Кнопка добавления продукта в корзину
    """
    product = shop_models.Product.objects.get(id=json.loads(call.data)['id'])
    user = shop_models.User.objects.get(telegram_id=call.message.chat.id)
    cart = user.get_active_cart()
    cart.add_product(product)

    bot.answer_callback_query(
        call.id,
        text=constance.ADD_TO_CART_COMPLETED
    )


@bot.callback_query_handler(lambda call: json.loads(call.data)['tag'] == constance.COMPLETE_ORDERING_TAG)
def handle_add_product(call):
    """
    Хєндлер сообщения о завершениии оформления заказа. Выводит колличество заказанного товара и общую сумму заказа
    """
    user = shop_models.User.objects.get(telegram_id=call.message.chat.id)
    order = user.get_order_in_clearance_status()
    order.in_work_status = True
    order.save()

    total_sum = sum(list(map(lambda x: x.product_price, order.products)))
    num_of_prod = len(order.products)
    product = 'товар' if str(num_of_prod)[-1] == "1" else 'товара' if str(num_of_prod)[-1] in ["2", "3", "4"] \
        else 'товаров'
    text = constance.ORDER_TEXT.format(num_of_prod, product, total_sum) + constance.ORDER_TEXT_FINALLY

    bot.send_message(
        call.message.chat.id,
        text=text
    )