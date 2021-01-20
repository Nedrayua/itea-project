import time
from flask import Flask

from shop.bot.shop_bot import app_tg, bot
from shop.api.app_restful import app_api
from shop.bot.config import WEBHOOK_URL

bot.remove_webhook()
time.sleep(0.5)
bot.set_webhook(WEBHOOK_URL, certificate=open('webhook_cert.pem'))

app = Flask(__name__)
app.register_blueprint(app_tg)
app.register_blueprint(app_api)

app.run(debug=True)
