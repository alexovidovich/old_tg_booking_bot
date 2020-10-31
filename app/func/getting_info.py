import json
from flask import request
import datetime
import pytz
from func.object_to_send import Object
from func.sending import *

class data_to_read(object):


    @classmethod
    def getting_info(cls,slug=None):
        data = request.get_json()
        if 'edited_message' not in data :
            cls.writting_json(data,'api-request')
            if slug:
                return cls.mapping_info_user(data,slug)
            return cls.mapping_info_user(data)
        return None


    @staticmethod
    def writting_json(data,name):
        with open(f'/home/alexvenv/new_wattson/app/static/{name}.json','w',encoding='utf-8') as f:
            json.dump(data,f,indent=2,ensure_ascii=False)
    @classmethod
    def reading_json(cls,name):
        with open(f'/home/alexvenv/new_wattson/app/static/{name}.json','r',encoding='utf-8') as f:
            data = json.load(f)
        return data
    @staticmethod
    def add_json(data,name):
        with open(f'/home/alexvenv/new_wattson/app/static/{name}.json','a',encoding='utf-8') as f:
            json.dump(data,f,indent=2,ensure_ascii=False)


    @classmethod
    def mapping_info_user(cls,comming_data=None,slug=None):
        data = comming_data or cls.reading_json(name = 'json_api_update')
        if data!=None:

            dict_data = {}
            #--------------------TELEGA--------------------
            if 'callback_query' in data:
                data = data['callback_query']
                dict_data['call_back']=cls.check('data',data)
                dict_data['my']=True
                dict_data['from']=cls.check('first_name',data['from'])


            if 'message' in data:
                dict_data['from']=cls.check('first_name',data['message']['from'])
                dict_data['date']=cls.check('reply_markup',data['message'])
                dict_data['teleg_id']=cls.check('username',data['message']['from'])
                dict_data['message_id']=cls.check('message_id',data['message'])
                dict_data['name']=cls.check('first_name',data['message']['from'])
                dict_data['chat_id']=str(cls.check('id',data['message']['chat']))
                dict_data['text']=cls.check('text',data['message'])
                if 'photo' in data['message']:
                    dict_data['photo']=cls.check('photo',data['message'])[-1]['file_id']
                    dict_data['caption']=cls.check('caption',data['message'])
            #--------------------TELEGA--------------------
            clients = cls.reading_json('clients')
            if dict_data['chat_id'] not in clients.get(slug).get('ids'):
                clients[slug]['ids'][dict_data['chat_id']]=['',[]]
                print(clients)
                cls.writting_json(clients,'clients')
            if slug:
                dict_data['bot']=slug
            return dict_data
    @classmethod
    def check(cls,x:str,route):
        back = route[x] if x in route else None
        return back



    @staticmethod
    def get_date(data=None,Today=False):
        monthes=['Январь','Февраль','Март','Апрель','Май','Июнь','Июль','Август','Сентябрь','Октябрь','Ноябрь','Декабрь']
        monthes={str(it+1):[mon,str(it+1)] for it,mon in enumerate(monthes)}
        year_now = int(datetime.datetime.now(pytz.timezone('Europe/Minsk')).strftime('%Y'))
        years = {y:y for y in [str(y) for y in range(year_now,2056)]}
        if data:
            try:
                if Today:
                    year = str(int(datetime.datetime.now(pytz.timezone('Europe/Minsk')).strftime('%Y')))
                    month = str(int(datetime.datetime.now(pytz.timezone('Europe/Minsk')).strftime('%m')))
                else:
                    year = data['date']["inline_keyboard"][0][1].get('text')
                    month =data['date']["inline_keyboard"][1][1].get('callback_data')

                return monthes,years,year_now,year,month
            except:
                pass
        else:
            return monthes,years,year_now
