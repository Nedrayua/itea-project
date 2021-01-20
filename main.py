import time
from shop.bot.shop_bot import bot, app
# from shop.models.shop_models import *
from shop.api.app_restful import app as app2

from shop.bot.config import WEBHOOK_URL

# me.connect('SHOP')

bot.remove_webhook()
time.sleep(0.5)
bot.set_webhook(WEBHOOK_URL, certificate=open('webhook_cert.pem'))
#app.run(debug=True)

app2.run(debug=True)
