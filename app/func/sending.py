
import requests 
import time
from app import *
from func.AUTH import *
from func.getting_info import *
class Send:
    def __init__(self,url,method_api,obj,*args,**kwargs):
        self.url = url
        self.method_api = method_api
        self.obj = obj
        self.list = args
        self.dict = kwargs
        self.send()
    def send(self):
        self.route = self.url + self.method_api
        print(self.route,self.obj)
        begin = time.time()
        print('start sanding')
        sending_info = requests.post(self.route,json=self.obj)
        print('sent')
        print(time.time()-begin)
        
       

class Send_google:
    def __init__(self,data,id,date,time,from_whom):
        self.id = id 
        self.date = date
        self.time = time 
        self.from_whom = from_whom
        self.data= data
        self.send()
    
    def send(self):
        event = {
            'summary':f'{self.date} №{self.id} от {self.from_whom}',
            # 'id':f'{self.id}',
            'start': {
                'dateTime': '{}T{}:00+03:00'.format(self.date,self.time[:5]),
                'timeZone': 'Europe/Minsk',
            },
            'end': {
                'dateTime': '{}T{}:00+03:00'.format(self.date,self.time[6:11]),
                'timeZone': 'Europe/Minsk',
            }
        }
        service = get_creditionals()
        self.event = service.events().insert(calendarId=self.data['google_id'], body=event).execute()
        print('Event created: %s' % (self.event.get('id')))
       
    def __str__(self):
        return self.event.get('id')
