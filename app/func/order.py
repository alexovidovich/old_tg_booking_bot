
import datetime
from func.handler import Handler
import pytz
from func.getting_info import *



class Order:
    def __init__(self,data,chat_id,date,time,has_phone=None,conf='0'):
        self.data = data
        self.has_phone = has_phone 
        self.chat_id = chat_id
       
        self.date = date
        
        self.time = time 
        self.conf = conf
        self.create_order()
    
    def create_order(self):
        orders = data_to_read.reading_json('orders')
        self.id = str(len(orders.get(self.data['bot']))+1)
        self.now = datetime.datetime.now(pytz.timezone('Europe/Minsk')).strftime('%Y-%m-%d')
        clients = data_to_read.reading_json('clients')
        if clients.get(self.data['bot']).get('ids').get(self.chat_id)[0] != '':
            self.has_phone = clients[self.data['bot']]['ids'][self.chat_id][0]
            orders[self.data['bot']][self.id]=[self.now,self.chat_id,self.date,self.time,self.has_phone,self.conf,self.data['from']]
            data_to_read.writting_json(orders,'orders')
            if len(clients.get(self.data['bot']).get('ids').get(self.chat_id))>1:
                clients[self.data['bot']]['ids'][self.chat_id][1].append(self.id)
            else:
                clients[self.data['bot']]['ids'][self.chat_id].append([self.id,])
            data_to_read.writting_json(clients,'clients')

            if self.data.get('my'):
                Handler.message(self.data,data_to_read.reading_json('texts').get(self.data['bot']).get('8'),True)
            else:
                Handler.message(self.data,data_to_read.reading_json('texts').get(self.data['bot']).get('8'),False)
            remember = data_to_read.reading_json('remember_date')
            for each in remember:
                if each == self.chat_id:
                    del remember[each]
                    break
            data_to_read.writting_json(remember,'remember_date')
            for ch_id in data_to_read.reading_json('admin').get(self.data['bot']).get('chat_id'):
                Handler.confirmation(self.data,self.id,self.now,ch_id,self.date,self.time,self.has_phone)
        else:
            remember = data_to_read.reading_json('remember_date')
            remember[self.chat_id]=[self.date,self.time]
            data_to_read.writting_json(remember,'remember_date')
            Handler.message(self.data,data_to_read.reading_json('texts').get(self.data['bot']).get('11'),True)
    
# service.events().delete(calendarId=google_id, eventId='putf1ti27kceedfv0521354bek').execute()