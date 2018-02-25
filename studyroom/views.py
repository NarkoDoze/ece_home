from django.shortcuts import render, redirect
from . import index
import datetime

# Create your views here.
def sroom_home(request):
    params = {'title': '스터디룸'}
    params['sroom'] = index.sroomIndex
    return render(request, 'studyroom/home.html', params)

def sroom_rsv(request, idx):
    params = {'title': '스터디룸 예약'}
    if request.method == "POST":
        # TODO: Get student id and save it
        return redirect('/home')

    for sroom in index.sroomIndex:
        if sroom['var'] == idx:
            params['name'] = sroom['name']
            today = datetime.date.today()
            after = today + datetime.timedelta(days=3)
            rsvlist = sroom['model'].objects.filter(
                reserved__range=(today, after)
            )
            output = []
            while today < after:
                check = [0] * 24
                if today == datetime.date.today():
                    check[0:datetime.datetime.now().hour+1] = [1]*(datetime.datetime.now().hour+1)
                for rsv in list(rsvlist):
                    rsvDate = datetime.date(rsv.reserved.year, rsv.reserved.month, rsv.reserved.day)
                    if today == rsvDate:
                        check[rsv.reserved.hour+9] = 1
                output.append({
                    "name": today.strftime("%Y-%m-%d"),
                    "heatmap": check
                })
                today += datetime.timedelta(days=1)
            params['table'] = output
            return render(request, 'studyroom/reserve.html', params)

    return render(request, 'example.html', params)

def sroom_chk(request):
    params = {'title': '스터디룸 확인'}
    # TODO: Get student id and check it
    return render(request, 'example.html', params)
