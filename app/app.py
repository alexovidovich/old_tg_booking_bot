
from flask import Flask
import json
import requests

import re
import requests
from flask_sslify import SSLify



from config import configuration 

from func.getting_info import data_to_read


app = Flask(__name__,static_folder='static')
sslify = SSLify(app)

app.config.from_object(configuration)

# admin = data_to_read.reading_json('admin').get('1')
# token = admin.get('telegram_token')
# main_url = f'https://api.telegram.org/bot{token}/'
# hook = requests.get(main_url+'deleteWebhook')
# hook = requests.get(main_url+'setWebhook?url=https://1e105167f3c2.ngrok.io')


