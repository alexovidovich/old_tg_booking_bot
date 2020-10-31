from app import *
from func.getting_info import *
from func.interceptor_requests import *
from func.handler import *
from func.sending_key_board import *
from func.admin import Admin
import requests
from flask import request
from flask import jsonify

@app.route('/',methods=['POST','GET'])

def index():
    if request.method =="POST":
        data_for_creation = request.get_json()
        print(data_for_creation)
        if data_for_creation.get('google_id') and data_for_creation.get('token') and data_for_creation.get('admin_key'):


            init_api = data_to_read.reading_json('init')

            token = data_for_creation.get('token')
            admin_key = data_for_creation.get('admin_key')
            google_id = data_for_creation.get('google_id')



            texts = data_to_read.reading_json('texts')
            admin = data_to_read.reading_json('admin')
            clients = data_to_read.reading_json('clients')
            orders = data_to_read.reading_json('orders')

            bot_n = str(len(admin)+1)

            admin[bot_n] = init_api.get('admin')
            admin[bot_n]['admin_key'] = [admin_key]
            admin[bot_n]['telegram_token'] = token
            admin[bot_n]['calendar_id'] = google_id

            texts[bot_n]=init_api.get('texts')

            orders[bot_n]={}

            clients[bot_n]=init_api.get('clients')


            data_to_read.writting_json(admin,'admin')
            data_to_read.writting_json(clients,'clients')
            data_to_read.writting_json(texts,'texts')
            data_to_read.writting_json(orders,'orders')

            main_url =f'https://api.telegram.org/bot{token}/'

            hook = requests.get(main_url+f'setWebhook?url=alexvenv.pythonanywhere.com/{bot_n}')

        return jsonify(data_for_creation)
    return '404 Not found'


@app.route('/<slug>',methods=['POST','GET'])

def bot(slug):
    print(type(slug),slug)
    if str(slug).isdigit():

        if request.method == 'POST':
            data = data_to_read.getting_info(slug)
            try:
                if data:
                    admin = data_to_read.reading_json('admin').get(data['bot'])
                    token = admin.get('telegram_token')
                    google_id = admin.get('calendar_id')
                    admin_key = admin.get('admin_key')
                    admin_name = admin.get('name')
                    data['main_url']= main_url = f'https://api.telegram.org/bot{token}/'
                    data['google_id']= google_id
                    data['admins'] = data_to_read.reading_json('admin').get(data['bot']).get('chat_id')
                    data['delta'] = data_to_read.reading_json('admin').get(data['bot']).get('delta')
                    data['min_order'] = data_to_read.reading_json('admin').get(data['bot']).get('min_order')
                    print(data['text'])
                    patterns = data_to_read.reading_json('texts')


                    if Admin.admin_interceptor(data=data):
                        print('admin command')
                    elif Interceptor.interceptor(data=data,pattern=patterns.get(data['bot']).get('13'),worker=Handler.if_start) == True:
                        print('старт')#1
                    elif Interceptor.interceptor(data=data,pattern=patterns.get(data['bot']).get('14'),worker=Handler.if_rules)==True:
                        print('правила')#2
                    elif Interceptor.interceptor(data=data,pattern=patterns.get(data['bot']).get('15'),worker=Handler.if_contacts)==True:
                        print('контакты')#3
                    elif Interceptor.interceptor(data=data,pattern=patterns.get(data['bot']).get('16'),worker=Handler.if_calendar)==True:
                        print('календарь')#4
                    elif Interceptor.interceptor_for_callback(data=data,worker=[Handler.update_calendar,Handler.api_worker,Handler.choose_time,Handler.are_u_sure])==True:
                        print('обновить календарь')#5
                    elif Interceptor.interceptor(data=data,pattern=admin_key,worker=Handler.addAdmin)==True:
                        print('admin check')
                    elif Interceptor.interceptor(data=data,pattern=['админка'],worker=Handler.show_admin_widget)==True:
                        print('admin check')
            except:
                Handler.message(data,'Возникли неполадки, не связанные с алгоритмом исполнения. Обратитесь в поддержку.')

    return '404 Not found'

    # slug = '1'

    # if request.method == 'POST':
    #     slug = '1'
    #     data = data_to_read.getting_info(slug)
    #     if data:
    #         admin = data_to_read.reading_json('admin').get(data['bot'])
    #         token = admin.get('telegram_token')
    #         google_id = admin.get('calendar_id')
    #         admin_key = admin.get('admin_key')
    #         admin_name = admin.get('name')
    #         data['main_url']= main_url = f'https://api.telegram.org/bot{token}/'
    #         data['google_id']= google_id
    #         data['admins'] = data_to_read.reading_json('admin').get(data['bot']).get('chat_id')
    #         data['delta'] = data_to_read.reading_json('admin').get(data['bot']).get('delta')
    #         data['min_order'] = data_to_read.reading_json('admin').get(data['bot']).get('min_order')
    #         print(data['text'])
    #         patterns = data_to_read.reading_json('texts')


    #         if Admin.admin_interceptor(data=data):
    #             print('admin command')
    #         elif Interceptor.interceptor(data=data,pattern=patterns.get(data['bot']).get('13'),worker=Handler.if_start) == True:
    #             print('старт')#1
    #         elif Interceptor.interceptor(data=data,pattern=patterns.get(data['bot']).get('14'),worker=Handler.if_rules)==True:
    #             print('правила')#2
    #         elif Interceptor.interceptor(data=data,pattern=patterns.get(data['bot']).get('15'),worker=Handler.if_contacts)==True:
    #             print('контакты')#3
    #         elif Interceptor.interceptor(data=data,pattern=patterns.get(data['bot']).get('16'),worker=Handler.if_calendar)==True:
    #             print('календарь')#4
    #         elif Interceptor.interceptor_for_callback(data=data,worker=[Handler.update_calendar,Handler.api_worker,Handler.choose_time,Handler.are_u_sure])==True:
    #             print('обновить календарь')#5
    #         elif Interceptor.interceptor(data=data,pattern=admin_key,worker=Handler.addAdmin)==True:
    #             print('admin check')
    #         elif Interceptor.interceptor(data=data,pattern=['админка'],worker=Handler.show_admin_widget)==True:
    #             print('admin check')