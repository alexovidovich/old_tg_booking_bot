import datetime
# start = f0
# close = s0
# times = [f0,s1,f1,s2,f2,s3,f3,s0]
# empty = []
def time_generation(times):
    empty = []
    i = 0
    while i < len(times):
        if times[i+1] == times[i]:
            i+=2
            continue
        else:
            empty.append(times[i])
            empty.append(times[i+1])
            i+=2
            continue
    return empty


def output(finish):
    finish_list=[]
    construct=[]
    for i,obj in enumerate(finish):
        print(obj,i)
        if i%2 != 0:
            obj = f'до {obj}'
            construct.append(obj)
            finish_list.append(construct)
            construct =[]
        else:
            obj = f'C {obj}'
            construct.append(obj)
    return finish_list



def creating_events(data,list_of_ev,hours_of_work,work_day_started,hour_now):
    events = []

    for each in list_of_ev:
        start = each.get('start')[11:16]
        end = each.get('end')[11:16]
        events.append(start)
        events.append(end)

    if work_day_started:
        events.insert(0,hour_now)
    else:
        events.insert(0,hours_of_work[0])
    events.append(hours_of_work[1])
    finish = time_generation(events)
    print(finish)
    i=0
    while i < len(finish):
        if 0 < (int(finish[i+1][:2])*60+(int(finish[i+1][3:5]))) - (int(finish[i][:2])*60+(int(finish[i][3:5]))) < int(data['min_order']):
            print(str((int(finish[i+1][:2])*60+(int(finish[i+1][3:5]))) - (int(finish[i][:2])*60+(int(finish[i][3:5])))))
            finish.pop(i)
            finish.pop(i)

            print(finish)
        elif i!=len(finish)-2:
            i+=1
        else:
            break
    finish_list = output(finish)
    return finish_list


def delta_hour(delta,hour_or_minute,plus=False,wanted_end=None,wanted_start=None):
    if wanted_end:
        if hour_or_minute:
            if plus:
                var = (int(wanted_end[:2])*60+int(wanted_end[3:5])+int(delta))
            else:
                var = (int(wanted_end[:2])*60+int(wanted_end[3:5])-int(delta))
        else:
            if plus:
                var = (int(wanted_end[:2])*60+int(wanted_end[3:5])+60)
            else:
                var = (int(wanted_end[:2])*60+int(wanted_end[3:5])-60)
    else:
        if hour_or_minute:
            if plus:
                var = (int(wanted_start[:2])*60+int(wanted_start[3:5])+int(delta))
            else:
                var = (int(wanted_start[:2])*60+int(wanted_start[3:5])-int(delta))
        else:
            if plus:
                var = (int(wanted_start[:2])*60+int(wanted_start[3:5])+60)
            else:
                var = (int(wanted_start[:2])*60+int(wanted_start[3:5])-60)
    hour = convert_str_date_to_real(str(var//60))
    minute =  convert_str_date_to_real(str(var%60))
    time = f'{hour}:{minute}'
    return time


def convert_str_date_to_real(stri):
    if len(stri)<2:
        stri = f'0{stri}'
        print(stri)
        return stri
    return stri


def creating_body_for_google_api(google_id,date,hours_of_work1,start_time):
    body = {
        'timeMin': "{}-{}-{}T{}:00+03:00".format(date[0],date[1],date[2],start_time),
        'timeMax': "{}-{}-{}T{}:00+03:00".format(date[0],date[1],date[2],hours_of_work1),
        'timeZone': "Europe/Minsk",
        'items': [
            {
                "id": google_id
            }
        ]
    }
    print(body,'?????????????????????????????????????????????????????????????????')
    return body


def pr_digits(digits):
    if len(digits)>4:
        digits = links(digits[:3])+links(digits[3:6])
    else:
        digits = links(digits[:1])+links(digits[1:2])
    return digits


def links(digit):
    if digit=='0':
        digit='0️⃣'
    elif digit=='0️⃣':
        digit='0'
    if digit=='1':
        digit='1️⃣'
    elif digit=='1️⃣':
        digit='1'
    if digit=='2':
        digit='2️⃣'
    elif digit=='2️⃣':
        digit='2'
    if digit=='3':
        digit='3️⃣'
    elif digit=='3️⃣':
        digit='3'
    if digit=='4':
        digit='4️⃣'
    elif digit=='4️⃣':
        digit='4'
    if digit=='5':
        digit='5️⃣'
    elif digit=='5️⃣':
        digit='5'
    if digit=='6':
        digit='6️⃣'
    elif digit=='6️⃣':
        digit='6'
    if digit=='7':
        digit='7️⃣'
    elif digit=='7️⃣':
        digit='7'
    if digit=='8':
        digit='8️⃣'
    elif digit=='8️⃣':
        digit='8'
    if digit=='9':
        digit='9️⃣'
    elif digit=='9️⃣':
        digit='9'
    return digit
