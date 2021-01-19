
import mongoengine as me

from shop.bot.utils import return_content_args as rca
from shop.models.extra_models import Time
from shop.bot import constance


me.connect('SHOP')


class User(me.Document):
    telegram_id = me.IntField(primary_key=True)
    username = me.StringField(min_length=2, max_length=128)
    first_name = me.StringField(min_length=2, max_length=128)
    phone_number = me.StringField(max_length=13)
    email = me.EmailField()
    user_address = me.StringField(min_length=12, max_length=128)
    is_block = me.BooleanField(default=False)

    def __str__(self):
        return str(self.telegram_id)

    def formatted_data(self):
        """
        Вывод данных о юзере
        """
        return f'{rca("Id", self.telegram_id, "Отсутствует")}\n{rca("Никнейм", self.username, "Отсутствует")}\n' \
               f'{rca("Имя", self.first_name, "Отсутствует")}\n{rca("Телефон", self.phone_number, "Отсутствует")}\n' \
               f'{rca("email", self.email, "Отсутствует")}\n{rca("Адресс", self.user_address, "Отсутствует")}'

    def get_active_cart(self):
        """
        Метод получения корзины, принадлежащий данному юзеру и имеющую статус is_active=True. .first() - выбор первой.
        Если ее нет, создает и возвращает ее.
        """
        cart = Cart.objects(user=self, is_active=True).first()
        if not cart:
            cart = Cart.objects.create(
                user=self

            )
            cart.reload()
            return cart
        return cart

    def get_order_in_clearance_status(self):
        """
        Метод получения экземпляра класса Order, принадлежащий данному юзеру и имеющую статус in_work_status=False и
        sent_to_client=False, тоесть не принятой в работу оператору и не отравленную клиенту .first() - выбор первой
        из списка существующих.
        Если ее нет, создает и возвращает ее.
        """
        order = Order.objects(user=self, in_work_status=False, sent_to_client=False).first()
        if not order:
            order = Order.objects.create(
                user=self
            )
            return order
        return order


class Category(me.Document):
    title = me.StringField()
    description = me.StringField(max_length=512)
    parent = me.ReferenceField('Category')
    subcategories = me.ListField(me.ReferenceField('self'))

    def __str__(self):
        return str(self.id)

    def get_products(self):
        """
        Возвращаем кверисет продуктов, у которых категория в параметре category равна self
        """
        return Product.objects(category=self)

    @classmethod
    def get_root_categories(cls):
        """
        Возвращает кверисет категорий, где парент равен None, тоесть ищем корневую категорию
        """
        return cls.objects(
            parent=None
        )

    def is_root(self):
        """
        Возвращет True, если у категории parent не имеет ссылку на категорию. Тоесть категория является root
        """
        return not bool(self.parent)

    def add_subcategory(self, category):
        """
        метод, который добавляет в список подкатегорий принимаемую в аргументе категорию, и в этой категоии
        в поле parent будет ставить саму себя
        """
        category.parent = self
        category.save()
        self.subcategories.append(category)
        self.save()


class Parameters(me.EmbeddedDocument):
    height = me.FloatField()
    width = me.FloatField()
    weight = me.FloatField()
    additional_description = me.StringField()


class Product(me.Document):
    title = me.StringField(required=True, max_length=256)
    description = me.StringField(max_length=512)
    in_stock = me.BooleanField(default=True)
    discount = me.IntField(min_value=0, max_value=100, default=0)
    price = me.IntField(required=True)
    image = me.FileField()
    category = me.ReferenceField(Category, required=True)
    parameters = me.EmbeddedDocumentField(Parameters)

    def __str__(self):
        return str(self.id)

    def formatted_product(self, short=False):
        """
        Строковый интерпритатор объекта Product. Значение short меняет полноту отображения объекта
        """
        text = f'{rca("Название товара", self.title)}\n' \
               f'{rca("Описание товара", self.description)}\n\n' \
               f'Цена: {self.price:.2f} гривен;\nскидка {self.discount}%;\nцена со скидкой ' \
               f'{self.price*(self.discount/100) if self.discount > 0 else self.price:.2f} гривен\n\n' \

        # add_text = f'Параметры:\n{rca("Высота", self.parameters.height)}\n' \
        #            f'{rca("Длинна", self.parameters.width)}\n' \
        #            f'{rca("Вес", self.parameters.weight)}\n' \
        #            f'{rca("Описание", self.parameters.additional_description)}\n'
        if short:
            return text
        else:
            return text #+ add_text

    @property
    def product_price(self):
        """
        Стоимость товара за минусом дисконта
        """
        return (100 - self.discount) / 100 * self.price


class Cart(Time):
    user = me.ReferenceField(User, required=True)
    products = me.ListField(me.ReferenceField(Product))
    is_active = me.BooleanField(default=True)

    def find_index_of_product(self, id_prod):
        """
        Поиск индекса продукта в находящегося в объекте Cart
        """
        index = 0
        for i in self.products:
            if str(i.id) == id_prod:
                return index
            else:
                index += 1

    def cart_product_dict(self):
        """
        Создание списка продуктов в новом проедставлении для определения колличества повторяющихся продуктов
        """
        dict_refuge = {}
        for product in self.products:
            if product.id in dict_refuge.keys():
                dict_refuge[product.id] += 1
            else:
                dict_refuge.setdefault(product.id, 1)
        return dict_refuge

    def add_product(self, product):
        """
        Метод, который добавляет в корзину продукт
        """
        self.products.append(product)
        self.save()


class Order(me.Document):
    user = me.ReferenceField(User, required=True)
    products = me.ListField(me.ReferenceField(Product))
    delivery_data = me.DictField()
    in_work_status = me.BooleanField(default=False)
    sent_to_client = me.BooleanField(default=False)

    def get_delivery_data(self):
        recipient = self.delivery_data.setdefault(str(constance.recipient), "")
        destination = self.delivery_data.setdefault(str(constance.destination), "")
        delivery_method = self.delivery_data.setdefault(str(constance.delivery_method), "")
        branch_number = self.delivery_data.setdefault(str(constance.branch_number), "")
        phone_number = self.delivery_data.setdefault(str(constance.phone_number), "")
        self.save()
        text = f"{constance.ORDERED_DELIVERY_PARAMETERS[constance.recipient]}: {recipient}\n" \
               f"{constance.ORDERED_DELIVERY_PARAMETERS[constance.destination]}: {destination}\n" \
               f"{constance.ORDERED_DELIVERY_PARAMETERS[constance.delivery_method]}: {delivery_method}\n"\
               f"{constance.ORDERED_DELIVERY_PARAMETERS[constance.branch_number]}: №{branch_number}\n"\
               f"{constance.ORDERED_DELIVERY_PARAMETERS[constance.phone_number]}: {phone_number}\n"
        return text

    def order_product_dict(self):
        """
        Создание списка продуктов в новом проедставлении для определения колличества повторяющихся продуктов
        """
        dict_refuge = {}
        for product in self.products:
            if product.id in dict_refuge.keys():
                dict_refuge[product.id] += 1
            else:
                dict_refuge.setdefault(product.id, 1)
        return dict_refuge

