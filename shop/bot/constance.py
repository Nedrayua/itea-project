GREETINGS = 'Рады тебя снова видеть в нашем магазине{}'
GREETINGS_ELSE = 'Привет{} Рады тебя приветствовать в нашем магазине-боте'

CHOICE_CATEGORY = 'Выберете категорию'

CART_TEXT = 'В корзине {} {} на общую сумму {:0.2f} гривен\n\n'
CART_TEXT_2 = 'Всего в корзине {} ед. данного товара на общую сумму {:0.2f}'
ADD_TO_CART = 'Добавить товар в корзину'
ADD_TO_CART_COMPLETED = "Продукт добавлен в корзину"
CHANGE_COMPLETED = "Изменения сохранены"
GOODS_WITHDRAWN = "Товар изъят"
TAKE_AWAY_FROM_CART = "Убрать товар из корзины"
EDIT_CART = "Изменить содержимое корзины"
EDIT_CART_CONTINUE = "Продолжить изменение содержимого корзины"

ORDERING = "Офрмление заказа"
ORDER_TEXT = 'В Вашем заказе {} {} на общую сумму {:0.2f} гривен\n\n'
ORDER_TEXT_FINALLY = "В ближайшее время с Вами свяжется наш сотрудник для подтверждения заказа"
CHANGE_SETTINGS = "Change_settings"
CHANGE_SETTINGS_TEXT = "Изменить настройки"

change_name = 4
change_phone = 5
change_email = 6
change_post = 7
choice_category = 8
back_to_settings = 9
wrong_change = 10

CHANGE_SETTINGS_COMMAND = {
    change_name: 'first_name',
    change_phone: 'phone_number',
    change_email: 'email',
    change_post: 'user_address'
}

CHANGE_SETTINGS_NAMES_B = {
    change_name: "Изменить имя",
    change_phone: "Изменить номер телефона",
    change_email: "Изменить email",
    change_post: "Изменить адресс",
    choice_category: "Выберете категорию изменений",
    back_to_settings: "Вернуться к настройкам"
}

CHANGE_SETTINGS_MESSAGE = {
    change_name: 'Введите Ваше имя',
    change_phone: 'Введите Ваш номер телефона, не более 13 символов',
    change_email: 'Введите Ваш email',
    change_post: 'Введите Ваш адресс на примере: 10000, г. Киев, ул. Житомирская, 270. кв. 15',
    wrong_change: 'Данные введены не верно'
}

start_order = 1
recipient = 2
destination = 3
delivery_method = 4
branch_number = 5
phone_number = 6
complete_order = 7
continue_order = 8

ORDERED_MESSAGE = {
    start_order: "Для дальнейшего оформления заказа необходимо уточнить данные для доставки заказа",
    recipient: "Укажите фамилию и имя получателя",
    destination: 'Введите пунк назначения для доставки заказа (область, район, город/село)',
    delivery_method: 'Выберите название фирмы-курьера',
    branch_number: 'Укажите номер отделения курьера',
    phone_number: 'Введите контактный номер телефона, для уведомления о доставке',
    complete_order: 'Для завершения заказа нажмите...',
    continue_order: "Продолжить"
}

ORDERED_DELIVERY_PARAMETERS = {
    recipient: "Получатель",
    destination: 'Пункт доставки',
    delivery_method: 'Курьер',
    branch_number: 'Отделение',
    phone_number: 'Телефон'
}

ORDERED_NAMES_B = {
    start_order: 'Приступить к заполнению нформация для доставки',
    recipient: "Получатель",
    destination: 'Пункт доставки',
    delivery_method: 'Выбор компании-доставщика',
    branch_number: 'Номер отделения компании-доставщика',
    phone_number: 'Контактный номер телефона',
    complete_order: 'Завершить заказ',
    continue_order: "Продолжить"
}

new_post = 1
delivery = 2
meest_express = 3
autolux = 4

DELIVERY_COMPANIES = {
    new_post: "Новая почта",
    delivery: "Деливери",
    meest_express: "Мист-експресс",
    autolux: "Автолюкс"
}

CATEGORIES = 1
CART = 2
SETTINGS = 3
NEWS = 4
PRODUCTS_WITH_DISCOUNT = 5

START_KB = {
    CATEGORIES: 'Категории',
    CART: 'Корзина',
    SETTINGS: 'Настройки',
    NEWS: 'Новости',
    PRODUCTS_WITH_DISCOUNT: 'Продукты со скидкой'
}

CATEGORY_TAG = 1
PRODUCT_TAG = 2
CHANGE_SETTINGS_TAG = 3
CHANGE_SPECIFIC_SETTINGS_TAG = 4
ADD_TO_CART_TAG = 5
ADD_TO_CART_FROM_CART_TAG = 6
TAKE_AWAY_FROM_CART_TAG = 7
EDITING_CART_TAG = 8
START_ORDERING_TAG = 9
FILLING_IN_THE_ORDER_TAG = 10
FILLING_IN_SPECIFIC_ORDER_TAG = 11
COMPLETE_ORDERING_TAG = 12
CHOICE_DELIVERY_METHOD = 13

