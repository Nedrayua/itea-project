import os

from shop.models.shop_models import Category, Product
from mongoengine import DoesNotExist

CATEGORIES = [
    {
        'title': 'Нутбуки, компьютеры',
        'description': 'Предлагаем небольшой выбор товаров для работы и развлечений',
        'parent': 0,
    },
    {
        'title': 'Бытовая техника',
        'description': 'Предлагаем небольшой выбор товаров для улучшения Вашего домашнего быта',
        'parent': 0,
    },
    {
        'title': 'Нутбуки',
        'description': 'Предлагаем небольшой выбор нутбуков',
        'parent': 'Нутбуки, компьютеры',
    },
    {
        'title': 'Планшеты',
        'description': 'Предлагаем небольшой выбор планшетов',
        'parent': 'Нутбуки, компьютеры',
    },
    {
        'title': 'Холодильники',
        'description': 'Предлагаем небольшой выбор надежных холодильников',
        'parent': 'Бытовая техника',
    },
    {
        'title': 'Стиральные машины',
        'description': 'Предлагаем небольшой выбор стиральных машин',
        'parent': 'Бытовая техника',
    },
    {
        'title': 'Холодильники Indesit',
        'description': 'Предлагаем небольшой выбор надежных холодильников от итальянского производителя',
        'parent': 'Холодильники',
    },
    {
        'title': 'Холодильники SAMSUNG',
        'description': 'Предлагаем небольшой выбор надежных холодильников от корейского производителя',
        'parent': 'Холодильники',
    },
    {
        'title': 'Стиральные машины WHIRPOOL',
        'description': 'Предлагаем небольшой выбор стиральных машин',
        'parent': 'Стиральные машины',
    },
    {
        'title': 'Стиральные машины INDESIT',
        'description': 'Предлагаем небольшой выбор стиральных машин итальянского производителя',
        'parent': 'Стиральные машины',
    },
    {
        'title': 'Стиральные машины SAMSUNG',
        'description': 'Предлагаем небольшой выбор стиральных машин от корейского производителя',
        'parent': 'Стиральные машины',
    },
    {
        'title': 'Стиральные машины LG',
        'description': 'Предлагаем небольшой выбор стиральных машин от корейского производителя',
        'parent': 'Стиральные машины',
    },
    {
        'title': 'Нутбуки MSI',
        'description': 'Предлагаем небольшой выбор Нутбуков от MSI',
        'parent': 'Нутбуки',
    },
    {
        'title': 'Нутбуки Acer',
        'description': 'Предлагаем небольшой выбор Нутбуков от Acer',
        'parent': 'Нутбуки',
    },
    {
        'title': 'Нутбуки Asus',
        'description': 'Предлагаем небольшой выбор Нутбуков от ASUS',
        'parent': 'Нутбуки',
    },
    {
        'title': 'Планшеты Samsung',
        'description': 'Предлагаем небольшой выбор планшетов из Кореи',
        'parent': 'Планшеты',
    },
    {
        'title': 'Планшеты Huawei',
        'description': 'Предлагаем небольшой выбор планшетов из Китая',
        'parent': 'Планшеты',
    },
    {
        'title': 'Планшеты Lenovo',
        'description': 'Предлагаем небольшой выбор планшетов из Китая',
        'parent': 'Планшеты',
    },
    {
        'title': 'Планшеты Apple',
        'description': 'Предлагаем небольшой планшетов от самого модного производителя:))',
        'parent': 'Планшеты',
    }
]


PRODUCTS = [
    {
        'title': 'Ноутбук Acer Aspire 5 A515-55G (NX.HZFEU.009) Pure Silver',
        'description': 'Экран 15.6" IPS (1920x1080) Full HD, матовый / Intel Core i5-1035G1 (1.0 - 3.6 ГГц) / RAM 8 ГБ'
                       ' / SSD 512 ГБ / nVidia GeForce MX350, 2 ГБ / без ОД / LAN / Wi-Fi / Bluetooth / веб-камера /'
                       ' без ОС / 1.8 кг / серебристый',
        'price': 15000,
        'photo': 'shop\\filling_module\\img_for_bot\\nb_ac_01.jpg',
        'category': 'Нутбуки Acer'
    },
    {
        'title': 'Ноутбук Asus ROG Strix G15 G512LI-HN094 (90NR0381-M01620) Black',
        'description': 'Экран 15.6" IPS (1920x1080) Full HD 144 Гц, матовый / Intel Core i5-10300H (2.5 - 4.5 ГГц) /'
                       ' RAM 8 ГБ / SSD 512 ГБ / nVidia GeForce GTX 1650 Ti, 4 ГБ / без ОД / LAN / Wi-Fi / Bluetooth /'
                       ' без ОС / 2.39 кг / черный',
        'price': 18000,
        'category': 'Нутбуки Asus',
        'photo': 'shop\\filling_module\\img_for_bot\\nb_as_01.jpg'
    },
    {
        'title': 'Ноутбук MSI Modern 14 B4MW Luxury Black',
        'description': 'Экран 14" IPS (1920x1080) Full HD, матовый / AMD Ryzen 5 4500U (2.3 - 4.0 ГГц) / RAM 8 ГБ / '
                       'SSD 256 ГБ / AMD Radeon Graphics / без ОД / Wi-Fi / Bluetooth / веб-камера / DOS / 1.3 кг /'
                       ' черный',
        'price': 13000,
        'category': 'Нутбуки MSI',
        'photo': 'shop\\filling_module\\img_for_bot\\nb_mc_01.jpg'
    },
    {
        'title': 'Ноутбук Acer Nitro 5 AN515-55-56WH (NH.Q7PEU.00L) Obsidian Black',
        'description': 'Экран 15.6” IPS (1920x1080) Full HD 144 Гц, матовый / Intel Core i5-10300H (2.5 - 4.5 ГГц) /'
                       ' RAM 16 ГБ / SSD 512 ГБ / nVidia GeForce GTX 1660 Ti, 6 ГБ / без ОД / LAN / Wi-Fi / Bluetooth /'
                       ' веб-камера / без ОС / 2.3 кг / черный',
        'price': 21000,
        'category': 'Нутбуки Acer',
        'photo': 'shop\\filling_module\\img_for_bot\\nb_as_02.jpg'
    },
    {
        'title': 'Ноутбук Asus ROG Strix G15 G512LI-HN057 (90NR0381-M01640) Black',
        'description': 'Экран 15.6" IPS (1920x1080) Full HD 144 Гц, матовый / Intel Core i7-10750H (2.6 - 5.0 ГГц) /'
                       ' RAM 16 ГБ / SSD 512 ГБ / nVidia GeForce GTX 1650 Ti, 4 ГБ / без ОД / LAN / Wi-Fi / Bluetooth /'
                       ' без ОС / 2.39 кг / черный',
        'price': 15000,
        'category': 'Нутбуки Asus',
        'photo': 'shop\\filling_module\\img_for_bot\\nb_as_02.jpg'
    },
    {
        'title': 'Планшет Samsung Galaxy Tab S6 Lite Wi-Fi 64GB Gray (SM-P610NZAASEK)',
        'description': 'Экран 10.4" TFT (2000x1200) MultiTouch / Samsung Exynos 9611 (2.3 ГГц + 1.7 ГГц) / RAM 4 ГБ / '
                       '64 ГБ встроенной памяти + microSD / Wi-Fi / Bluetooth 5.0 / основная камера 8 Мп, фронтальная'
                       ' - 5 Мп / GPS / Android 10.0 (Q) / 465 г / серый',
        'price': 5400,
        'category': 'Планшеты Samsung',
        'photo': 'shop\\filling_module\\img_for_bot\\tb_sg_1.jpg'
    },
    {
        'title': 'Планшет Huawei MatePad T10 Wi-Fi 32GB Deepsea Blue',
        'description': 'Экран 9.7" IPS (1280x800) MultiTouch / Huawei Kirin 710A (2.0 ГГц + 1.7 ГГц) / RAM 2 ГБ /'
                       ' 32 ГБ встроенной памяти + MicroSD / Wi-Fi / Bluetooth 5.0 / основная камера 5 Мп, фронтальная'
                       ' 2 Мп / GPS / ГЛОНАСС / Android 10 (EMUI) / 450 г',
        'price': 3900,
        'category': 'Планшеты Huawei',
        'photo': 'shop\\filling_module\\img_for_bot\\tb_hw_1.jpg'
    },
    {
        'title': 'Планшет Lenovo Tab M8 HD 2/32 WiFi Iron Grey (ZA5G0054UA)',
        'description': 'Экран 8" (1280х800) IPS, емкостный MultiTouch / MediaTek Helio A22 (2 ГГц) / RAM 2 ГБ / 32 ГБ'
                       ' встроенной памяти + microSD (до 128 ГБ) / Wi-Fi / Bluetooth 5.0 / основная камера 5 Мп +'
                       ' фронтальная 2 Мп / GPS / Android 9.0 (Pie) / 305 г / серый',
        'price': 8000,
        'category': 'Планшеты Lenovo',
        'photo': 'shop\\filling_module\\img_for_bot\\tb_lo_1.jpg'
    },
    {
        'title': 'Планшет Apple iPad 10.2" Wi-Fi + Cellular 32GB Space Gray 2020 (MYMH2RK/A)',
        'description': 'Экран 10.2" IPS (2160x1620) MultiTouch / Apple A12 Bionic (2.49 ГГц) / 32 ГБ встроенной памяти'
                       ' / 3G / 4G / Wi-Fi / Bluetooth 4.2 / основная камера 8 Мп, фронтальная - 1.2 Мп / GPS / ГЛОНАСС'
                       ' / iPadOS 14 / 495 г / серый космос',
        'price': 18700,
        'category': 'Планшеты Apple',
        'photo': 'shop\\filling_module\\img_for_bot\\tb_ap_1.jpg'
    },
    {
        'title': 'Планшет Lenovo Yoga Smart Tab 4/64 LTE Iron Grey (ZA530006UA)',
        'description': 'Экран 10.1" (1920x1200) IPS емкостный, MultiTouch / Qualcomm Snapdragon 439 (2 ГГц) / RAM 4 ГБ'
                       ' / 64 ГБ встроенной памяти + microSD (до 256 ГБ) / Wi-Fi / 3G / 4G LTE / Bluetooth 4.2 / '
                       'основная камера 8 Мп, фронтальная - 5 Мп / A-GPS / ГЛОНАСС / Android 9.0 (Pie) / 570 г / серый',
        'price': 6400,
        'category': 'Планшеты Lenovo',
        'photo': 'shop\\filling_module\\img_for_bot\\tb_lo_2.jpg'
    },
    {
        'title': 'Стиральная машина узкая WHIRLPOOL FWSG 61083 WBV',
        'description': 'Максимальная загрузка белья: 6 кг\nКоличество программ: 15\n'
                       'Габариты (ВхШхГ): 83.7 х 59.5 х 42.5 см\nКласс энергопотребления: А+++\n'
                       'Тип двигателя: Инверторный\nМаксимальная скорость отжима, об/мин:1000 об/мин\n'
                       'Способ установки: Отдельностоящая (соло)',
        'price': 8600,
        'category': 'Стиральные машины WHIRPOOL',
        'photo': 'shop\\filling_module\\img_for_bot\\wm_wp_1.jpg'
    },
    {
        'title': 'Стиральная машина узкая INDESIT OMTWSA 61052 W UA ',
        'description': 'Максимальная загрузка белья: 6 кг\nКоличество программ: 16\nГабариты (ВхШхГ): 85 х 59.5 х'
                       ' 42.5 см\nКласс энергопотребления; А++\nМаксимальная скорость отжима, об/мин: 1000 об/мин',
        'price': 6900,
        'category': 'Стиральные машины INDESIT',
        'photo': 'shop\\filling_module\\img_for_bot\\wm_it_1.jpg'
    },
    {
        'title': 'Стиральная машина узкая SAMSUNG WW60J30J0LW/UA',
        'description': 'Максимальная загрузка белья: 6 кг\nКоличество программ: 13\nГабариты (ВхШхГ): 85 x 60 x 45 см\n'
                       'Класс энергопотребления: А+\nМаксимальная скорость отжима, об/мин: 1000 об/мин\n'
                       'Способ установки: Отдельностоящая (соло)',
        'price': 8300,
        'category': 'Стиральные машины SAMSUNG',
        'photo': 'shop\\filling_module\\img_for_bot\\wm_sg_1.jpg'
    },
    {
        'title': 'Стиральная машина узкая LG F2J3WS2W',
        'description': 'Максимальная загрузка белья: 6.5 кг\nКоличество программ: 10\n'
                       'Габариты (ВхШхГ): 85 х 60 х 44 см\nКласс энергопотребления: А+++\nТип двигателя: Инверторный\n'
                       'Максимальная скорость отжима, об/мин:1200 об/мин\nСпособ установки: Отдельностоящая (соло)',
        'price': 10500,
        'category': 'Стиральные машины LG',
        'photo': 'shop\\filling_module\\img_for_bot\\wm_lg_1.jpg'
    },
    {
        'title': 'Стиральная машина узкая SAMSUNG WW70K42101WDUA',
        'description': 'Количество программ: 12\nГабариты (ВхШхГ): 85х60х45 см\nКласс энергопотребления: А+++\n'
                       'Максимальная скорость отжима, об/мин: 1200 об/мин.\nСпособ установки: Отдельностоящая (соло)',
        'price': 8700,
        'category': 'Стиральные машины SAMSUNG',
        'photo': 'shop\\filling_module\\img_for_bot\\wm_sg_2.jpg'
    },
    {
        'title': 'Холодильник SAMSUNG RB29FSRNDSA/UA',
        'description': 'Тип холодильника: Двухкамерный\nЦвет: Серебристый\nПолезный объем холодильной камеры; 192 л\n'
                       'Система разморозки No Frost (Frost Free): Холодильное+морозильное отделения\n'
                       'Полезный объем морозильной камеры: 98 л\nКоличество компрессоров: 1\n'
                       'Тип управления: Электронное',
        'price': 10999,
        'category': 'Холодильники SAMSUNG',
        'photo': 'shop\\filling_module\\img_for_bot\\fr_sg-1.jpg',
        'parameters': [178, 59.5, 63]
    },
    {
        'title': 'Холодильник SAMSUNG RB29FSRNDWW/UA',
        'description': 'Тип холодильника: Двухкамерный\nЦвет: Белый\nПолезный объем холодильной камеры:192 л.\n'
                       'Система разморозки No Frost (Frost Free): Холодильное+морозильное отделения\n'
                       'Полезный объем морозильной камеры: 98 л\nКоличество компрессоров:1',
        'price': 12000,
        'category': 'Холодильники SAMSUNG',
        'photo': 'shop\\filling_module\\img_for_bot\\fr_sg-2.jpg',
        'parameters': [178, 59.5, 67]
    },
    {
        'title': 'Двухкамерный холодильник INDESIT LI8 FF2 K',
        'description': 'Тип холодильника: Двухкамерный\nЦвет: Черный\nПолезный объем холодильной камеры: 215 л.\n'
                       'Система разморозки No Frost (Frost Free): Морозильное отделение\n'
                       'Полезный объем морозильной камеры: 88 л.\nКоличество компрессоров: 1\n'
                       'Тип управления: Механическое',
        'price': 9999,
        'category': 'Холодильники Indesit',
        'photo': 'shop\\filling_module\\img_for_bot\\fr_it-1.jpg',
        'parameters': [189, 59.6, 70]
    },
    {
        'title': 'Двухкамерный холодильник INDESIT XIT8 T2E X',
        'description': 'Тип холодильника: Двухкамерный\nЦвет: Нержавеющая сталь\nПолезный объем холодильной камеры:'
                       ' 223 л\nСистема разморозки No Frost (Frost Free): Холодильное+морозильное отделения\n'
                       'Полезный объем морозильной камеры: 97 л.\nКоличество компрессоров: 1\nТип управления:'
                       ' Электронное',
        'price': 10000,
        'category': 'Холодильники Indesit',
        'photo': 'shop\\filling_module\\img_for_bot\\fr_it-2.jpg',
        'parameters': [188.8, 59.5, 65.5]
    },
    {
        'title': 'Холодильник SAMSUNG RB33J3200SA',
        'description': 'Тип холодильника: Двухкамерный\nЦвет: Серебристый\nПолезный объем холодильной камеры: 230 л.\n'
                       'Система разморозки No Frost (Frost Free): Холодильное+морозильное отделения\n'
                       'Полезный объем морозильной камеры: 98 л.\nКоличество компрессоров: 1\n'
                       'Тип управления: Электронное',
        'price': 12999,
        'category': 'Холодильники SAMSUNG',
        'photo': 'shop\\filling_module\\img_for_bot\\fr_sg-3.jpg',
        'parameters': [185, 59.5, 66.8]
    }
]


def create_category(list_data):

    for i in list_data:
        try:
            Category.objects.get(title=i['title'])
            continue
        except DoesNotExist:
            Category(title=i['title'], description=i['description']).save()

    for cat in list_data:
        sub_category = Category.objects.get(title=cat['title'])
        try:
            category = Category.objects.get(title=cat['parent'])
        except DoesNotExist:
            continue
        if sub_category not in category.subcategories:
            category.add_subcategory(sub_category)

    return 'Categories created'


def create_product(list_data):

    for prod in list_data:
        try:
            Product.objects.get(title=prod['title'])
            continue
        except DoesNotExist:
            product = Product(title=prod['title'], description=prod['description'], price=prod['price'],
                              category=Category.objects.get(title=prod['category']))
        way = os.path.abspath(prod['photo'])
        with open(way, 'rb') as file:
            product.image.put(file, content_type='image/jpg')
            product.save()

    return 'Products created'
