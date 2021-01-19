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
        json_string = request.get_data()
        update = Update.de_json(json_string).decode('utf-8')
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
