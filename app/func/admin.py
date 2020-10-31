
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

class Admin:
    @classmethod
    def representation_order(cls,order,number):
        if '0' in  order[5]:
            status = 'Не подтвержден'
        if '1' in  order[5]:
            status = 'Одобрен'
        if '2' in  order[5]:
            status = 'Отклонен'
        text = f'Заказ #{number}\nCоздан: {order[0]}\nПользователем c id {order[1]}\nНа {order[2]} на {order[3]}\nНомер телефона: {order[4]}\nСтатус: {status}'
        return text

    @classmethod
    def admin_interceptor(cls,data):
        if not data.get('my') and data['chat_id'] in data['admins']:
                if data.get('text'):
                    text=data['text']
                    admin_json = data_to_read.reading_json('admin')
                    text_json = data_to_read.reading_json('texts')
                    orders_json = data_to_read.reading_json('orders')
                    clients_json = data_to_read.reading_json('clients')
                    try:
                        got_text=None
                        if 'post=' in text.lower():
                            got_text = text[5:]
                            Handler.message(data,text='Пост сделан')
                            for each_chat_id in clients_json.get(data['bot']).get('ids'):
                                Handler.message(data,text=got_text,chat_id=each_chat_id)

                        if 'text' in text.lower():
                            if text[4:5].isdigit() and '=' in text[4:8]:
                                num_of_text = re.sub('=','',text[4:6])
                                if int(num_of_text) < 10:
                                    got_text = re.sub('=','',text[6:])
                                    text_json[data['bot']][num_of_text]=got_text
                                    data_to_read.writting_json(text_json,'texts')
                                    Handler.message(data,f'Вы сменили {num_of_text} текст')
                                else:
                                    raise BaseException
                            else:
                                raise BaseException
                        text=re.sub(' ','',text)
                        if 'time=' in text.lower():
                            got_text = text[5:]
                            if datetime.datetime.strptime(got_text[:5],'%H:%M') and datetime.datetime.strptime(got_text[6:11],'%H:%M') \
                                and datetime.datetime.strptime(got_text[:5],'%H:%M')<datetime.datetime.strptime(got_text[6:11],'%H:%M'):
                                admin_json[data['bot']]['work_time']=[got_text[:5],got_text[6:11]]
                                Handler.message(data,f'Вы установили рабочее время на {got_text[:5]}-{got_text[6:11]}')
                                data_to_read.writting_json(admin_json,'admin')
                            else:
                                raise BaseException
                        if 'off=' in text.lower():
                            got_text = text[4:]
                            list_days = got_text.split(',')
                            for each in list_days:
                                if each.isdigit()==False:
                                    raise BaseException
                                elif int(each)>7:
                                    raise BaseException
                            if '0' in list_days:
                                admin_json[data['bot']]['not_work_day']=''
                                Handler.message(data,text='У вас теперь нет нерабочих дней')
                            else:
                                admin_json[data['bot']]['not_work_day']=list_days
                                Handler.message(data,text=f'Нерабочие дни установлены.')
                            data_to_read.writting_json(admin_json,'admin')

                        if 'min_order=' in text.lower():
                            got_text = text[10:]
                            if got_text.isdigit():
                                if len(got_text)<4 and int(got_text)%5==0 and 60%int(got_text)==0:
                                    admin_json[data['bot']]['min_order']=got_text
                                    Handler.message(data,text=f'Минимальное время записи теперь {got_text} мин.')
                            data_to_read.writting_json(admin_json,'admin')
                        if 'step=' in text.lower():
                            got_text = text[5:]
                            if got_text.isdigit():
                                if len(got_text)<4 and int(got_text)%5==0 and 60%int(got_text)==0:
                                    admin_json[data['bot']]['delta']=got_text
                                    Handler.message(data,text=f'Шаг установлен на {got_text} мин.')
                            data_to_read.writting_json(admin_json,'admin')
                        if 'num=' in text.lower():
                            got_text = text[4:]
                            if got_text.isdigit():
                                admin_json[data['bot']]['orders_today']=got_text
                                Handler.message(data,text=f'Максимальное кол-во заказов теперь {got_text}')
                            data_to_read.writting_json(admin_json,'admin')
                        if '#=' in text.lower():
                            got_text = text[2:]
                            if got_text.isdigit():
                                try:
                                    got_text = cls.representation_order(orders_json.get(data['bot']).get(got_text),got_text)
                                    Handler.message(data,got_text)
                                except:
                                    Handler.message(data,'Такого(ой) заказа(записи) не существует.')
                        if 'id=' in text.lower():
                            got_text = text[3:]
                            if got_text.isdigit():
                                try:
                                    orders = clients_json.get(data['bot']).get('ids').get(got_text)[1]
                                    for each_order in orders:
                                        got_text = cls.representation_order(orders_json.get(data['bot']).get(each_order),each_order)
                                        Handler.message(data,got_text)
                                except:
                                    Handler.message(data,'Такой клиент не делал еще заказов(записей).')
                        if 'del=' in text.lower():
                            got_text = text[4:]
                            if got_text.isdigit():
                                if got_text in clients_json.get(data['bot']).get('black_list'):
                                    clients_json[data['bot']]['black_list'].remove(got_text)
                                    Handler.message(data,'Пользователь был удален из черного списка.')
                            data_to_read.writting_json(clients_json,'clients')
                        if got_text:
                            return True

                    except:
                        Handler.message(data,'Неверная команда администратора')
                        return True