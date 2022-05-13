from func.interceptor_requests import *
from func.sending import *
from func.sending_key_board import ReplyKeyboardMarkup,InlineKeyboardMarkup,Calendar
from func.object_to_send import Object
import json
import time
import datetime
import pytz
from func.AUTH  import get_creditionals
from func.alg import time_generation,output,creating_events,convert_str_date_to_real,creating_body_for_google_api

from func.getting_info import *


class Handler(object):
    @staticmethod
    def if_start(data):
        method = 'sendMessage'
        if data['chat_id'] in data['admins']:
            for_json =ReplyKeyboardMarkup.creation_admin()
        else:
            for_json =ReplyKeyboardMarkup.creation()
        text1 = data_to_read.reading_json('texts').get(data['bot']).get('2') +f'\nВаш персональный id - {data["chat_id"]}'
        obj = Object.return_obj(chat_id = data['chat_id'],text=text1,reply_markup=for_json)#chat_id,text,photo=None,reply_markup=None,message_id=None
        Send(data['main_url'],method,obj) #url,method_api,obj,*args,**kwargs


    @staticmethod
    def if_rules(data):
        method = 'sendMessage'
        text = data_to_read.reading_json('texts').get(data['bot']).get('0')
        obj1 = Object.return_obj(chat_id = data['chat_id'],text=text)#chat_id,text,photo=None,reply_markup=None,message_id=None
        Send(data['main_url'],method,obj1)



    @staticmethod
    def if_contacts(data):
        method = 'sendMessage'
        text = data_to_read.reading_json('texts').get(data['bot']).get('1')
        obj = Object.return_obj(chat_id = data['chat_id'],text=text)
        Send(data['main_url'],method,obj)


    @staticmethod
    def if_calendar(data):
        method = 'sendMessage'
        real_time = datetime.datetime.now(pytz.timezone('Europe/Minsk')).strftime('%Y-%m')
        year= real_time[:4]
        month = real_time[5:]
        for_json =InlineKeyboardMarkup.creation_calendar(data,int(month),year)
        text = data_to_read.reading_json('texts').get(data['bot']).get('3')
        obj = Object.return_obj(chat_id = data['chat_id'],text=text,reply_markup=for_json)#chat_id,text,photo=None,reply_markup=None,message_id=None
        Send(data['main_url'],method,obj)


    @staticmethod
    def update_calendar(data,month=None,year=None):
        method = 'editMessageReplyMarkup'
        if not month and not year:
            method = 'editMessageText'
            real_time = datetime.datetime.now(pytz.timezone('Europe/Minsk')).strftime('%Y-%m')
            year= real_time[:4]
            month = real_time[5:]
        for_json =InlineKeyboardMarkup.creation_calendar(data,int(month),year)
        text = data_to_read.reading_json('texts').get(data['bot']).get('3')
        obj = Object.return_obj(chat_id = data['chat_id'],reply_markup=for_json,message_id=data['message_id'],text=text)#chat_id,text,photo=None,reply_markup=None,message_id=None
        Send(data['main_url'],method,obj)

    @staticmethod
    def api_worker(data,date,today=False):
        if today:
            today=True
        date=[convert_str_date_to_real(i) for i in date]
        time_from_telegram = f'{date[0]}-{date[1]}-{date[2]}'

        #---------google_id-------
        service = get_creditionals()

        #---------google_id-------
        #-------real_time---------
        real_time_obj = datetime.datetime.now(pytz.timezone('Europe/Minsk'))
        hour_now = real_time_obj.strftime('%H:%M')
        real_time_without_time =real_time_obj.strftime('%Y-%m-%d')[:10]
        real_time = datetime.datetime.strptime(real_time_without_time +' '+ hour_now,'%Y-%m-%d %H:%M') #hour_now changes for text to '15:00'
        work_day_started =False
        work_time = data_to_read.reading_json('admin').get(data['bot']).get('work_time')
        chosen_date = datetime.datetime.strptime(time_from_telegram,'%Y-%m-%d')
        now = datetime.datetime.strptime(real_time_without_time,'%Y-%m-%d')
        if data['chat_id'] not in data_to_read.reading_json('clients').get(data['bot']).get('black_list'):
            if chosen_date >= now :
                if str(Calendar.first_day_of(date[1],date[0],int(date[2]))) not in data_to_read.reading_json('admin').get(data['bot']).get('not_work_day'):
                    if real_time_without_time == time_from_telegram:#IF TODAY
                        today = True
                        work_day_started =True
                    text11=False
                    #-------real_time---------
                    #-------working_day_datetime-------
                    start_working_day = datetime.datetime.strptime(real_time_without_time+' '+work_time[0], '%Y-%m-%d %H:%M')
                    end_working_day = datetime.datetime.strptime(real_time_without_time+' '+work_time[1], '%Y-%m-%d %H:%M')
                    #-------working_day_datetime-------
                    #-------google-sending--------
                    body = creating_body_for_google_api(data['google_id'],date,work_time[1],work_time[0])# для гугла если сейчас не рабочий день
                    if today:
                        if end_working_day > real_time > start_working_day: # для гугла если рабочий день сейчас
                            body =creating_body_for_google_api(data['google_id'],date,work_time[1],hour_now)#hour_now changes for text to '15:00'
                    result1 = service.freebusy().query(body=body).execute()

                    #-------google-sending--------
                    #-------output--------
                    list_of_ev = result1.get('calendars').get(data['google_id']).get('busy')
                    not_working = False
                    print('here')
                    finish_list = creating_events(data,list_of_ev,work_time,work_day_started,hour_now)#hour_now changes for text to '15:00'#если рабочий день
                    print(finish_list)
                    if today:#если сегодня
                        work_day_started = False
                        if end_working_day < real_time: #если конец рабочего дня
                            not_working = True
                            text11 = data_to_read.reading_json('texts').get(data['bot']).get('5')
                            finish_list = []
                        elif start_working_day > real_time:# если рабочий день не началася
                            finish_list = creating_events(data,list_of_ev,work_time,work_day_started,hour_now)
                    #-------output--------
                    method = 'editMessageText'

                    if len(finish_list)==0:# если рабочий день забит
                        text10 = data_to_read.reading_json('texts').get(data['bot']).get('6')

                    if len(finish_list)>0:
                        list_battons = []
                        for each in finish_list:
                            new_str_list =f'{each[0]} {each[1]}     🆓'
                            list_battons.append(new_str_list)
                        markup = InlineKeyboardMarkup.can_i_go(data,time_from_telegram,True,list_battons)
                        text10 = f'❗Выбранная дата: {time_from_telegram}❗️\n\n'
                        obj = Object.return_obj(chat_id = data['chat_id'],text=text10,reply_markup=markup,message_id=data['message_id'])
                    else:
                        markup = InlineKeyboardMarkup.can_i_go(data,time_from_telegram,False)
                        if text11:
                            text10 = f'❗Выбранная дата: {time_from_telegram}❗️\n\n'+ text11
                        else:
                            text10 = f'❗Выбранная дата: {time_from_telegram}❗️\n\n'+ text10

                        obj = Object.return_obj(chat_id = data['chat_id'],text=text10,reply_markup=markup,message_id=data['message_id'])#chat_id,text,photo=None,reply_markup=None,message_id=None
                    Send(data['main_url'],method,obj)
                else:
                    Handler.message(data,'Нерабочий день.')
            else:
                Handler.message(data,'Запись на прошедший день не ведется.')
        #-------output--------


    #bt,19:00,20:30,2020-06-02 delta = 30
    @staticmethod
    def choose_time(data,start=None,end=None,date=None,wanted_start=None,wanted_end=None):
        delta = data_to_read.reading_json('admin').get(data['bot']).get('delta')
        min_order = data_to_read.reading_json('admin').get(data['bot']).get('min_order')
        work_time= data_to_read.reading_json('admin').get(data['bot']).get('work_time')
        print(start,end,wanted_start,wanted_end)
        method = 'editMessageText'
        if (int(start[:2])*60+int(start[3:5])) % int(delta)!=0:
            count =int(start[3:5])
            while count % int(delta) !=0:
                count += 1
            start =  convert_str_date_to_real(str((int(start[:2])*60+count)//60))+':'+  convert_str_date_to_real(str((int(start[:2])*60+count)%60))
        if not wanted_start:
            wanted_start = start
            wanted_end = convert_str_date_to_real(str((int(start[:2])*60+int(start[3:5])+int(min_order))//60))+':'+ convert_str_date_to_real(str((int(start[:2])*60+int(start[3:5])+int(min_order))%60))
        try:
            text = data_to_read.reading_json('texts').get(data['bot']).get('7')# для админки настроить!!!!NOT READY
            markup = InlineKeyboardMarkup.choose_time_keyboard(data,start,end,date,wanted_start,wanted_end)
            obj = Object.return_obj(chat_id = data['chat_id'],text=text,reply_markup=markup,message_id=data['message_id'])
            Send(data['main_url'],method,obj)
        except:
            Handler.message(data,'Администратор указал неправильное время работы, поэтому приложение сломалось. Сообщите ему о проблеме.')


    @staticmethod
    def are_u_sure(data,date,wanted_start,wanted_end,start,end):
        orders = data_to_read.reading_json('orders')
        how_many_orders_today = []
        today_is =datetime.datetime.now(pytz.timezone('Europe/Minsk')).strftime('%Y-%m-%d')[:10]
        client_orders = data_to_read.reading_json('clients').get(data['bot']).get('ids').get(data['chat_id'])[1]


        if len(orders.get(data['bot']))>0:
            if len(client_orders)>0:
                for each_order in client_orders:
                    if today_is == orders[data['bot']][each_order][0]:
                        if data['chat_id'] == orders[data['bot']][each_order][1]:
                            how_many_orders_today.append(each_order)
        method = 'editMessageText'

        if data_to_read.reading_json('admin').get(data['bot']).get('orders_today') == '' or data_to_read.reading_json('admin').get(data['bot']).get('orders_today').isdigit()==False or \
            int(data_to_read.reading_json('admin').get(data['bot']).get('orders_today')) < 1:
            orders_today = 5
        else:
            orders_today = int(data_to_read.reading_json('admin').get(data['bot']).get('orders_today'))
        if len(how_many_orders_today) <  orders_today:
            text = data_to_read.reading_json('texts').get(data['bot']).get('10')
            markup = InlineKeyboardMarkup.are_u_sure_create(data,date,wanted_start,wanted_end,start,end)
            obj = Object.return_obj(chat_id = data['chat_id'],text=text,reply_markup=markup,message_id=data['message_id'])
            Send(data['main_url'],method,obj)
        else:
            text= data_to_read.reading_json('texts').get(data['bot']).get('9')
            obj = Object.return_obj(chat_id = data['chat_id'],text=text,message_id=data['message_id'])
            Send(data['main_url'],method,obj)


    @staticmethod
    def message(data,text=None,is_changable=False,chat_id=None,media=None):
        if media:
            method ='sendMediaGroup'
            obj = Object.return_obj(chat_id=data['chat_id'],media=media)
        if text:
            if chat_id:
                data['chat_id'] = chat_id
            if is_changable:
                method = 'editMessageText'
                obj = Object.return_obj(chat_id = data['chat_id'],text=text,message_id=data['message_id'])
            else:
                method = 'sendMessage'
                obj = Object.return_obj(chat_id = data['chat_id'],text=text)
        Send(data['main_url'],method,obj)


    @staticmethod
    def confirmation(data,id,now,chat_id,date,time,has_phone,conf=None):
        if conf:
            method = 'editMessageText'
            markup = InlineKeyboardMarkup.confirmation(data,id,now,chat_id,date,time,has_phone,True)
        else:
            markup = InlineKeyboardMarkup.confirmation(data,id,now,chat_id,date,time,has_phone)
            method = 'sendMessage'
        name = data['from']
        text = f'Заказ №{id} оформленный {now} от пользователя {chat_id} с указанным номером телефона:{has_phone} на {date} на {time}.'
        if conf:
            obj = Object.return_obj(chat_id = chat_id,text=text,reply_markup=markup,message_id=data['message_id'])
        else:
            obj = Object.return_obj(chat_id = chat_id,text=text,reply_markup=markup)
        Send(data['main_url'],method,obj)

    @staticmethod
    def if_busy(data,date,time,cancel=None):
        orders=data_to_read.reading_json('orders')
        time_start =  datetime.datetime.strptime(time[:5],'%H:%M')
        time_end =  datetime.datetime.strptime(time[6:11],'%H:%M')
        for order in orders.get(data['bot']):
            container = orders.get(data['bot']).get(order)
            if container[2] == date:
                start = datetime.datetime.strptime(container[3][:5],'%H:%M')
                end = datetime.datetime.strptime(container[3][6:11],'%H:%M')
                print(start,end,time_start,time_end)
                print(container[5])
                if start == time_start or end == time_end or start < time_start < end or start < time_end < end:
                    if container[5] == '0':
                        orders.get(data['bot']).get(order)[5]= '2'
                        id_order=order
                        chat_id = container[1]
                        text = f'Ваша запись №{order} на {container[2]} на {container[3]} была отклонена.'+data_to_read.reading_json('texts').get(data['bot']).get('12')
                        Handler.message(data,text,chat_id=chat_id)
                        data_to_read.writting_json(orders,'orders')
                    if container[5] == '2' and cancel:
                        orders.get(data['bot']).get(order)[5]= '0'
                        data_to_read.writting_json(orders,'orders')





    @classmethod
    def text_admin(cls,data=None):
        r=data_to_read.reading_json('texts')
        #what to change
        data_to_read.writting_json(r,'texts')

    @classmethod
    def addAdmin(cls,data):
        admin_json=data_to_read.reading_json('admin')
        admin_json[data['bot']]['chat_id'].append(data['chat_id'])
        data_to_read.writting_json(admin_json,'admin')
        Handler.message(data,'Теперь вы администратор!')
        method = 'sendMessage'
        remove_keyboard = [[{'remove_keyboard':True}]]
        for_json =ReplyKeyboardMarkup.creation_admin()
        text1 = 'Панель пользователя удалена'
        obj = Object.return_obj(chat_id = data['chat_id'],text=text1,reply_markup=remove_keyboard)#chat_id,text,photo=None,reply_markup=None,message_id=None
        Send(data['main_url'],method,obj)
        text1 = 'Панель администратора установлена'
        obj = Object.return_obj(chat_id = data['chat_id'],text=text1,reply_markup=for_json)#chat_id,text,photo=None,reply_markup=None,message_id=None
        Send(data['main_url'],method,obj)



    @classmethod
    def show_admin_widget(cls,data):
        if data['chat_id'] in data['admins']:
            for_json = InlineKeyboardMarkup.admin_keyboard(data)
            admin = data_to_read.reading_json('admin').get(data['bot'])
            clients = data_to_read.reading_json('clients').get(data['bot']).get('ids')
            not_work_day = 'Нет выходных дней' if len(admin.get("not_work_day"))==0 else admin.get("not_work_day")
            text = f'Выберите пункт. И внимательно дочитайте описание пункта до конца. Пишите по аналогии с примером, приведенным в описании.\n\n\
Рабочее время: {admin.get("work_time")[0]}-{admin.get("work_time")[1]}\nМинимальное время записи: {admin.get("min_order")} мин.\n\
Шаг выбора времени: {admin.get("delta")} мин.\nНерабочие дни: {not_work_day}\nКол-во заявок/день от клиента: {admin.get("orders_today")} раз.\n\
Ботом пользуется {str(len(clients))} человек(а)'
            method = 'sendMessage'
            obj = Object.return_obj(chat_id = data['chat_id'],text=text,reply_markup=for_json)
            Send(data['main_url'],method,obj)









