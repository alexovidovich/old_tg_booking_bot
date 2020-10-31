
from func.object_to_send import *
import os.path
import datetime
import pytz
from func.handler import *
from func.alg import *
from func.order import Order
import re
from func.sending import Send_google
from func.AUTH import *
from func.getting_info import *











class Interceptor:

    @staticmethod
    def interceptor_for_callback(data,worker):
        if 'call_back' in data:
            if data['chat_id'] in data['admins']:#admin area
                text = None
                text_ex = data_to_read.reading_json('texts').get('admin')
                if ','  in data['call_back']:
                    callback = data['call_back'].split(',')
                    extra = False
                    if callback[0] == 'check':
                        if callback[1]=='ord':
                            text = text_ex.get('0')
                        else:
                            text = text_ex.get('1')
                    if callback[0] == 'set':
                        if callback[1] == 'hours':
                            text = text_ex.get('2')
                        if callback[1] == 'off':
                            text = text_ex.get('3')
                        if callback[1] == 'num':
                            text = text_ex.get('4')
                        if callback[1] == 'del':
                            text = text_ex.get('5')
                        if callback[1] == 'ord':
                            text = text_ex.get('6')
                        if callback[1] == 'step':
                            text = text_ex.get('7')
                        if callback[1] == 'texts':
                            list_text = [f'{pr_digits(str(i))}.\n'+ data_to_read.reading_json('texts').get(data['bot']).get(str(i))+'\n\n' for i in range(1,11)]
                            text=''
                            for i in list_text:
                                text += i
                            extra = f'❗️{text_ex.get("8")}❗️\n\n\n\n\n 0️⃣.\n'+ data_to_read.reading_json('texts').get(data['bot']).get('0')+'\n\n'
                        if callback[1] =='photo':
                            text=text_ex.get('9')
                    if callback[0] == 'post':
                        text = text_ex.get('10')
                        print(text)
                    if text:
                        if extra:
                            Handler.message(data,extra)
                        Handler.message(data,text)

            if data['call_back'] in ['<','>','>>','<<']:
                Helper_Handler_for_interceptor.change_date_in_calendar(data,worker)

            if 'day' in data['call_back']:
                if 'today'in data['call_back']:
                    Helper_Handler_for_interceptor.get_selected_date(data,worker,today=True)
                else:
                    Helper_Handler_for_interceptor.get_selected_date(data,worker)

            if 'календарь' in data['call_back']:
                worker[0](data)

            if 'bt' in data['call_back']:
                data['call_back']= data['call_back'].split(',')
                start = data['call_back'][1]
                end = data['call_back'][2]
                date = data['call_back'][3]
                worker[2](data,start,end,date)

            if '*' in data['call_back']:
                date=data['call_back'][1:]
                date = [date[:4],date[5:7],date[8:10]]
                worker[1](data,date)

            if 'start' in data['call_back'] or 'end' in data['call_back'] or 'new_client' in data['call_back']:
                Helper_Handler_for_interceptor.change_time(data,worker)

            if 'make_order' in data['call_back']:
                callback=data['call_back'].split(',')
                Order(data,data['chat_id'],callback[2],callback[1])
            if 'black' in data['call_back']:
                callback = data['call_back'].split(',')[1]
                clients=data_to_read.reading_json('clients')
                clients[data["bot"]]['black_list'].append(callback)
                data_to_read.writting_json(clients,'clients')
                Handler.message(data,'Пользователь был добавлен в черный список.')

            if 'conf' in data['call_back'] or 'notconf' in data['call_back']:
                callback = data['call_back'].split(',')
                id_order = callback[1]
                orders = data_to_read.reading_json('orders')
                order = orders.get(data['bot']).get(id_order)
                if callback[0]=='conf':
                    status = order[5]
                    if status != '2':
                        orders.get(data['bot']).get(id_order)[5]='1'
                        data_to_read.writting_json(orders,'orders')
                        Handler.if_busy(data,order[2],order[3])# проверка занято ли это уже время другим заказом
                        orders = data_to_read.reading_json('orders')
                        chat_id = order[1]
                        text = f'Ваша запись №{id_order} на {order[2]} на {order[3]} была одобрена.'
                        Handler.message(data,text,chat_id=chat_id)
                        event_id = Send_google(data,id_order,order[2],order[3],order[1])
                        text = f'Запись №{id_order} на {order[2]} на {order[3]} была одобрена.'
                        for ch_id in data['admins']:
                            Handler.confirmation(data,id_order,order[0],ch_id,order[2],order[3],order[4],conf=True)
                            Handler.message(data,text,False,chat_id=ch_id)
                        orders[data['bot']][id_order].append(str(event_id))
                    else:
                        text = 'На это время вы уже одобрили заявление или заказ уже отменил другой администратор, если таковой имеется.'
                        Handler.message(data,text,False)
                else:
                    if orders.get(data['bot']).get(id_order)[5] == '1':
                        Handler.if_busy(data,order[2],order[3],cancel=True)
                        orders = data_to_read.reading_json('orders')
                        service = get_creditionals()
                        event_id = orders.get(data['bot']).get(id_order)[7]
                        service.events().delete(calendarId=data['google_id'], eventId=event_id).execute()
                        text = f'Запись №{id_order} на {order[2]} на {order[3]} была отклонена.'
                        Handler.message(data,text,True)
                    else:
                        text = f'Запись №{id_order} на {order[2]} на {order[3]} была отклонена.'
                        Handler.message(data,text,True)
                    text = f'Ваша запись №{id_order} на {order[2]} на {order[3]} была отклонена.'+data_to_read.reading_json('texts').get(data['bot']).get('12')
                    orders.get(data['bot']).get(id_order)[5]='2'
                    chat_id = order[1]
                    Handler.message(data,text,chat_id=chat_id)

                data_to_read.writting_json(orders,'orders')




















    @staticmethod
    def interceptor(data,pattern,worker):
        if not data.get('my'):
            if data.get('text'):

                for each in pattern:
                    if each.lower() in data['text'].lower() or each.lower()==data['text'].lower():
                        worker(data)
                        return True

                if data['text'][0] == "+":
                    data['text']= data['text'][1:]
                    find = re.findall(r'\d{9}',r'{}'.format(data['text']))
                    client_json = data_to_read.reading_json('clients')
                    client_json[data['bot']]['ids'][data['chat_id']].pop(0)
                    client_json[data['bot']]['ids'][data['chat_id']].insert(0,"+" + data['text'])
                    data_to_read.writting_json(client_json,'clients')
                    remember = data_to_read.reading_json('remember_date')
                    if data['chat_id'] in remember:
                        date = remember[data['chat_id']][0]
                        time = remember[data['chat_id']][1]
                        Order(data,data['chat_id'],date,time)
                return False














class Helper_Handler_for_interceptor:
    @staticmethod
    def change_time(data,worker):
        delta =data.get('delta')
        min_order = data.get('min_order')
        date = data['date']["inline_keyboard"][0][0].get('callback_data')[1:]
        print(date,'!!!!!!!!')
        start = data['date']["inline_keyboard"][-2][0].get('callback_data').split(',')[0]
        end = data['date']["inline_keyboard"][-2][0].get('callback_data').split(',')[1]
        wanted_end = data['date']["inline_keyboard"][5][0].get('text')[:2]+':' \
            +data['date']["inline_keyboard"][5][1].get('text')[:2]
        wanted_start = data['date']["inline_keyboard"][2][0].get('text')[:2]+':' \
            +data['date']["inline_keyboard"][2][1].get('text')[:2]
        callback = data['call_back'].split(',')

        if callback[0] == 'new_client':
            worker[3](data,date,wanted_start,wanted_end,start,end)
        else:
            if callback[0]=='start':
                print(wanted_start,wanted_end,start,end)
                if callback[1]=='◀️':

                    if callback[2]=='m':

                        if datetime.datetime.strptime(wanted_start,'%H:%M') > datetime.datetime.strptime(start,'%H:%M'):
                            wanted_start = delta_hour(delta,hour_or_minute=True,wanted_start=wanted_start)
                            wanted_end= delta_hour(delta,hour_or_minute=True,wanted_end=wanted_end)
                    else:
                        if (int(wanted_start[:2])*60+int(wanted_start[3:5])-60)-(int(start[:2])*60+int(start[3:5])) >= 0:
                            wanted_start= delta_hour(delta,hour_or_minute=False,wanted_start=wanted_start)
                            wanted_end = delta_hour(delta,hour_or_minute=False,wanted_end=wanted_end)
                else:
                    if callback[2]=='m':
                        if (int(wanted_end[:2])*60+int(wanted_end[3:5]))-(int(wanted_start[:2])*60+int(wanted_start[3:5])+int(delta)) >= int(min_order):
                            wanted_start = delta_hour(delta,hour_or_minute=True,plus=True,wanted_start=wanted_start)
                        elif (int(wanted_end[:2])*60+int(wanted_end[3:5])+int(delta))-(int(end[:2])*60+int(end[3:5])) <= 0:
                            wanted_end = delta_hour(delta,hour_or_minute=True,plus=True,wanted_end=wanted_end)
                            wanted_start = delta_hour(delta,hour_or_minute=True,plus=True,wanted_start=wanted_start)
                    else:
                        if (int(wanted_end[:2])*60+int(wanted_end[3:5]))-(int(wanted_start[:2])*60+int(wanted_start[3:5])+60) >= int(min_order):
                            wanted_start= delta_hour(delta,hour_or_minute=False,plus=True,wanted_start=wanted_start)
                        elif (int(wanted_end[:2])*60+int(wanted_end[3:5])+60)-(int(end[:2])*60+int(end[3:5])) <= 0:
                            wanted_end = delta_hour(delta,hour_or_minute=False,plus=True,wanted_end=wanted_end)
                            wanted_start= delta_hour(delta,hour_or_minute=False,plus=True,wanted_start=wanted_start)
            else:
                if callback[1]=='◀️':
                    if callback[2]=='m':
                        if (int(wanted_end[:2])*60+int(wanted_end[3:5]))-(int(wanted_start[:2])*60+int(wanted_start[3:5])+int(delta)) >=int(min_order):
                            wanted_end= delta_hour(delta,hour_or_minute=True,wanted_end=wanted_end)
                    else:
                        if (int(wanted_end[:2])*60+int(wanted_end[3:5]))-(int(wanted_start[:2])*60+int(wanted_start[3:5])+60) >=int(min_order):
                            wanted_end = delta_hour(delta,hour_or_minute=False,wanted_end=wanted_end)
                else:
                    if callback[2]=='m':
                        if (int(wanted_end[:2])*60+int(wanted_end[3:5])+int(delta))-(int(end[:2])*60+int(end[3:5])) <= 0:
                            wanted_end = delta_hour(delta,hour_or_minute=True,plus=True,wanted_end=wanted_end)
                    else:
                        if (int(wanted_end[:2])*60+int(wanted_end[3:5])+60)-(int(end[:2])*60+int(end[3:5])) <= 0:
                            wanted_end = delta_hour(delta,hour_or_minute=False,plus=True,wanted_end=wanted_end)

            worker[2](data,start=start,end=end,date=date,wanted_start=wanted_start,wanted_end=wanted_end)


















    @staticmethod
    def change_date_in_calendar(data,worker):
        monthes, years, year_now, year,month = data_to_read.get_date(data)
        minsk_time_delta = str(datetime.datetime.now(pytz.timezone('Europe/Minsk'))+datetime.timedelta(hours=1))
        callback =  data['call_back']
        if callback == '>':
            if month == '12':
                month = '1'
            else:
                month = str(int(month)+1)
        if  callback == '<':
            if month == '1':
                month = '12'
            else:
                month = str(int(month)-1)
        if  callback == '>>':
            if year =='2055':
                year = str(year_now)
            else:
                year = years.get(str(int(year)+1))
        if  callback == '<<':
            if year ==str(year_now):
                year = '2055'
            else:
                year = years.get(str(int(year)-1))
        worker[0](data,month,year)


    @staticmethod
    def get_selected_date(data,worker,today=None):
        try:


            if today:
                monthes,years,year_now,year,month = data_to_read.get_date(data,True)
                day = datetime.datetime.now(pytz.timezone('Europe/Minsk')).strftime('%d')
            else:
                monthes,years,year_now,year,month = data_to_read.get_date(data)
                day = data['call_back'][:2] if data['call_back'][:2].isdigit() else data['call_back'][:1]
            date = [year,month,day]
            worker[1](data,date,today)
        except:
            pass







