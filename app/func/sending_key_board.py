from math import ceil
import json
from func.alg import pr_digits
from func.getting_info import *
class ReplyKeyboardMarkup:

# ,{'text':'Админка'}
    @staticmethod
    def creation():
        keyboard= [[{'text':'Календарь'}],[{'text':'Контакты'}],[{'text':'Правила'}]]
        not_ready = {'keyboard': keyboard ,'resize_keyboard':True}
        ready = json.dumps(not_ready)
        return ready
    @staticmethod
    def creation_admin():
        keyboard= [[{'text':'Календарь'}],[{'text':'Контакты'}],[{'text':'Правила'}],[{'text':'Админка'}]]
        not_ready = {'keyboard': keyboard ,'resize_keyboard':True}
        ready = json.dumps(not_ready)
        return ready














class InlineKeyboardMarkup:
    @staticmethod
    def can_i_go(data,date,with_info_or_not=None,lists=None):
        texts = data_to_read.reading_json('texts').get(data['bot'])
        keyboard = []
        if with_info_or_not:
            for j,i in enumerate(lists):
                keyboard.append([{'text':f'{i}','callback_data':f'bt,{i[2:7]},{i[11:16]},{date}'}])
        keyboard.insert(0,[{'text':'🔙                                      📅                                      🔙','callback_data':'календарь'}])
        keyboard.insert(1,[{'text':'                                                                                                                             ','callback_data':'ffffew'}])
        keyboard.insert(1,[{'text':f'{texts.get("4")}','callback_data':'frtert'}])
        not_ready = {'inline_keyboard': keyboard }
        ready = json.dumps(not_ready)
        return ready
        # for j,i in enumerate(lists):
        #         keyboard.append([{'text':i,'callback_data':f'nothing{j}'},{'text':'Выбрать время-> 📝','callback_data':f'bt,{i[2:7]},{i[11:16]},{date}'}])
    @staticmethod
    def are_u_sure_create(data,date,wanted_start,wanted_end,start,end):
        keyboard = Time_manager.are_u_sure(data,date,wanted_start,wanted_end,start,end)
        not_ready = {'inline_keyboard': keyboard }
        ready = json.dumps(not_ready)
        return ready
    @staticmethod
    def choose_time_keyboard(data,start,end,date,wanted_start,wanted_end):
        keyboard = Time_manager.create(data,start,end,date,wanted_start,wanted_end)
        not_ready = {'inline_keyboard': keyboard }
        ready = json.dumps(not_ready)
        return ready

    @staticmethod
    def creation_calendar(data,month,year):
        keyboard= Calendar.create(data,month,year)
        not_ready = {'inline_keyboard': keyboard }
        print(not_ready,'+++++++++++++++++++++++++')
        ready = json.dumps(not_ready)
        return ready


    @staticmethod
    def admin_keyboard(data):
        panel = [{'text':'⏬ Панель Администратора ⏬','callback_data':'eeeeeee'}]
        space = [{'text':'                                                                                                                             ','callback_data':'bbbbbbb'}]
        texts = [{'text':'✏️                Установить надписи *                ✏️','callback_data':'set,texts'}]
        hours = [{'text':'✏️           Установить рабочие часы *            ✏️','callback_data':'set,hours'}]
        dayoff = [{'text':'✏️           Установить выходные дни *           ✏️','callback_data':'set,off'}]
        min_ord = [{'text':'✏️        Установить min время записи *        ✏️','callback_data':'set,ord'}]
        min_step =[{'text':'✏️     Установить шаг выбора времени *     ✏️','callback_data':'set,step'}]
        details_order =[{'text':'✏️    Посмотреть подробности записи *    ✏️','callback_data':'check,ord'}]
        user_orders =[{'text':'✏️ Посмотреть все записи пользователя * ✏️','callback_data':'check,user'}]
        orders_per_day =[{'text':'✏️ Установить max кол-во записей/день * ✏️','callback_data':'set,num'}]
        del_black_list = [{'text':'✏️  Удалить клиента из черного списка *  ✏️','callback_data':'set,del'}]
        change_main_photo = [{'text':'✏️                Сменить аватар бота                ✏️','callback_data':'set,photo'}]
        post =[{'text':'Сделать рассылку (пост). Только текст !','callback_data':'post,'}]
        keyboard = [panel,space,texts,hours,dayoff,min_ord,min_step,orders_per_day,details_order,user_orders,del_black_list,change_main_photo,post]
        not_ready = {'inline_keyboard': keyboard }
        ready = json.dumps(not_ready)
        return ready

    @staticmethod
    def confirmation(data,id,now,chat_id,date,time,has_phone,conf=None):
        if conf:
            keyboard = [
                [{'text':'❌ Отклонить ❌','callback_data':f'notconf,{id},{chat_id}'}],
                [{'text':'                                                                                                                             ','callback_data':'tttttttt'}],
                ]

        else:
            keyboard = [
                [{'text':'Принять','callback_data':f'conf,{id},{chat_id}'},{'text':'Отклонить','callback_data':f'notconf,{id},{chat_id}'}],
                [{'text':'                                                                                                                             ','callback_data':'tttttttt'}],
                [{'text':'🚯 Добавить в черный список клиентов! 🚯','callback_data':f'black,{chat_id}'}]
                ]
        not_ready = {'inline_keyboard': keyboard }
        ready = json.dumps(not_ready)
        return ready








class Time_manager:
    @classmethod
    def create(cls,data,start,end,date,wanted_start,wanted_end):

        back = [{'text':'🔙  Выбрать другой промежуток  🔙','callback_data':f'*{date}'}]
        text1 = [{'text':'Начать в:','callback_data':'form0'}]
        start_time_label = [{'text':f'{wanted_start[:2]} ч.','callback_data':'form1'},{'text':f'{wanted_start[3:5]} мин.','callback_data':'form2'}]
        start_time_control = [{'text':'<','callback_data':'start,◀️,h'},{'text':'>','callback_data':'start,▶️,h'}, \
            {'text':'<','callback_data':'start,◀️,m'},{'text':'>','callback_data':'start,▶️,m'}]
        text2 = [{'text':'Закончить в:','callback_data':'form3'}]
        end_time_label = [{'text':f'{wanted_end[:2]} ч.','callback_data':'form4'},{'text':f'{wanted_end[3:5]} мин.','callback_data':'form5'}]
        end_time_control = [{'text':'<','callback_data':'end,◀️,h'},{'text':'>','callback_data':'end,▶️,h'}, \
            {'text':'<','callback_data':'end,◀️,m'},{'text':'>','callback_data':'end,▶️,m'}]
        space = [{'text':'                                                                                                                             ','callback_data':f'{start},{end}'}]
        make_order = [{'text':'Записаться','callback_data':'new_client'}]#need to put callback!!!!!!!!NOT READY

        return [back,text1,start_time_label,start_time_control,text2,end_time_label,end_time_control,space,make_order]
    @classmethod
    def are_u_sure(cls,data,date,wanted_start,wanted_end,start,end):
        back = [{'text': '🔙  Выбрать другое время  🔙','callback_data':f'bt,{start},{end},{date}'}]
        text1 = [{'text':f'Записаться на {wanted_start}-{wanted_end} {date}?','callback_data':'form8'}]
        space = [{'text':'                                                                                                                             ','callback_data':'ffffew'}]
        conf = [{'text':'✅','callback_data':f'make_order,{wanted_start}-{wanted_end},{date}'},{'text':'🔴','callback_data':'календарь'}]
        return [back,text1,space,conf]










class Calendar:

    @classmethod
    def create(cls,data,month,year):
        month=str(month)
        counted_days_in_month = cls.understand_how_many_days(month,year)
        first_day_in_first_week = cls.first_day_of(month,year)
        days = [{'text':str(i),'callback_data':str(i)+'day'} for i in range(1,counted_days_in_month+1)]
        xs =[{'text':' ','callback_data':str(i)+','} for i in range(first_day_in_first_week - 1)] +days \
            +[{'text':' ','callback_data':str(i)+'.'} for i in range(42 - len(days))]
        calendar = [xs[7*k:7*(k+1)] for k in range(6)]
        monthes,years,year_now = data_to_read.get_date()
        navigation_month = [{'text':'◀️','callback_data':'<'},{'text':monthes.get(month)[0],'callback_data':monthes.get(month)[1]}, \
            {'text':'▶️','callback_data':'>'}]
        navigation_year = [{'text':'◀️','callback_data':'<<'},{'text':years.get(year),'callback_data':'None'}, \
            {'text':'▶️','callback_data':'>>'}]
        days_of = ['пн','вт','ср','чт','пт','сб','вс']
        days_of_final = []
        for each in days_of:
            each = {'text':f'| {each} |','callback_data':'{each}'}
            days_of_final.append(each)

        calendar.insert(0,days_of_final)
        calendar.insert(0,navigation_month)
        calendar.insert(0,navigation_year)
        calendar.append([{'text':'Сегодня','callback_data':'day today'}])
        return calendar



    @classmethod
    def first_day_of(cls,month, year,day=None):
        month = int(month)
        year = int(year)
        if not day:
            day = 1
        if month == 1 or month == 10:
            kod_month = 1
        elif month == 5:
            kod_month = 2
        elif month == 8:
            kod_month = 3
        elif month == 2 or month == 3 or month == 11:
            kod_month = 4
        elif month == 6:
            kod_month = 5
        elif month == 12 or month == 9:
            kod_month = 6
        elif month == 4 or month == 7:
            kod_month = 0
        kod_year = (6 + year % 100 + (year % 100)// 4) % 7
        day = (day + kod_month + kod_year) % 7
        if year % 400 == 0 or year % 4 == 0 and year % 100 != 0:
            if month == 1 or month == 2:
                day -= 1
        day = (day + 5) % 7 + 1
        return day


    @classmethod
    def understand_how_many_days(cls,number, year):
        number = int(number)
        year = int(year)
        if number == 2:
            if year % 400 == 0 or year % 4 == 0 and year % 100 != 0:
                return 29
            else:
                return 28
        else:
            if number == 1 or number==3 or number ==  5 or number == 7 \
            or number ==  8 or number ==  10 or number ==  12:
                return 31
            else:
                return 30


