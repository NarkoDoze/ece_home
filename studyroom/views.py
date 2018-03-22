from django.shortcuts import render, redirect
from django.http import HttpResponse
from . import index
import datetime

# Create your views here.
def sroom_home(request):
    params = {'title': 'StudyRoom Reservation'}
    params['sroom'] = index.sroomIndex
    return render(request, 'studyroom/home.html', params)

def sroom_rsv(request, idx):
    params = {'title': 'StudyRoom Reservation'}
    if request.method == "POST":
        query = dict(request.POST)
        # check if the input is valid
        if len(query['sid'][0]) == 0 or len(query['sid'][1]) == 0 or len(query['sid'][2]) == 0:
            params['error'] = "Please enter student ID."
            return render(request, 'error.html', params)
        if len(set([x for x in query['sid'] if query['sid'].count(x) > 1])) != 0:
            params['error'] = "You cannot use same student ID."
            return render(request, 'error.html', params)
        # check in DB
        params['error'] = ""
        error_detect = False
        if not {'sid': query['sid'][0], 'name': query['name'][0]} in index.sidIndex:
            params['error'] += query['name'][0] + "(" + query['sid'][0] + "), "
            error_detect = True
        if not {'sid': query['sid'][1], 'name': query['name'][1]} in index.sidIndex:
            params['error'] += query['name'][1] + "(" + query['sid'][1] + "), "
            error_detect = True
        if not {'sid': query['sid'][2], 'name': query['name'][2]} in index.sidIndex:
            params['error'] += query['name'][2] + "(" + query['sid'][2] + "), "
            error_detect = True
        if error_detect:
            params['error'] = params['error'][:-2]
            params['error'] += " is not registered."
            return render(request, 'error.html', params)

        selectDate = []
        for select in query['select']:
            time = select.split('-')
            selectDate.append(datetime.datetime(int(time[0]), int(time[1]), int(time[2]), int(time[3])))

        selectNum = len(selectDate)
        if selectNum > 3:
            params['error'] = "You can select under 3 hours."
            return render(request, 'error.html', params)

        for sroom in index.sroomIndex:
            if sroom['var'] == idx:
                today = datetime.date.today()
                after = today + datetime.timedelta(days=3)
                rsvlist = sroom['model'].objects.filter(
                    reserved__range=(today, after),
                )

                for rsv in rsvlist:
                    rsvTime = datetime.datetime(rsv.reserved.year, rsv.reserved.month, rsv.reserved.day, rsv.reserved.hour)
                    if rsvTime in selectDate:
                        params['error'] = "잘못된 쿼리입니다."
                        return render(request, 'error.html', params)
                rsvlist = sroom['model'].objects.filter(
                    reserved__range=(today, after),
                    sid=query['sid'][0],
                )

                if len(rsvlist) + selectNum > 3:
                    params['error'] = query['name'][0] + "(" + query['sid'][0] + ")" + " exceeds 3 hours today."
                    return render(request, 'error.html', params)

                rsvlist = sroom['model'].objects.filter(
                    reserved__range=(today, after),
                    sid=query['sid'][1],
                )

                if len(rsvlist) + selectNum > 3:
                    params['error'] = query['name'][1] + "(" + query['sid'][1] + ")" + " exceeds 3 hours today."
                    return render(request, 'error.html', params)

                for date in selectDate:
                    diff = date - datetime.datetime.combine(datetime.date.today(), datetime.datetime.min.time())
                    if diff > datetime.timedelta(days=3) or diff < datetime.timedelta(days=0):
                        params['error'] = "잘못된 쿼리입니다."
                        return render(request, 'error.html', params)

                for date in selectDate:
                    sroom['model'](
                        reserved=date + datetime.timedelta(hours=9),
                        sid=query['sid'][1],
                    ).save()
                    sroom['model'](
                        reserved=date + datetime.timedelta(hours=9),
                        sid=query['sid'][0],
                    ).save()

                params['error'] = "Successfully reserved."
                return render(request, 'error.html', params)

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
                        check[rsv.reserved.hour] = 1
                checkenum = []
                for i, c in enumerate(check):
                    checkenum.append({"check": c, "id": i})
                output.append({
                    "name": today.strftime("%Y-%m-%d"),
                    "heatmap": checkenum
                })
                today += datetime.timedelta(days=1)
            params['table'] = output
            params['var'] = sroom['var']
            return render(request, 'studyroom/reserve.html', params)

    return render(request, 'example.html', params)

def sroom_chk(request):
    params = {'title': 'StudyRoom Checking'}
    if request.method == "POST":
        query = dict(request.POST)
        if len(query['sid'][0]) == 0:
            params['error'] = "Please enter student ID."
            return render(request, 'error.html', params)
        if not {'sid': query['sid'][0], 'name': query['name'][0]} in index.sidIndex:
            params['error'] = query['name'][0] + "(" + query['sid'][0] + ") is not registered."
            return render(request, 'error.html', params)
            
        today = datetime.date.today()
        after = today + datetime.timedelta(days=3)
        output = []
        for sroom in index.sroomIndex:
            today = datetime.date.today()
            after = today + datetime.timedelta(days=3)
            params['name'] = sroom['name']
            rsvlist = sroom['model'].objects.filter(
                reserved__range=(today, after)
            )
            while today < after:
                check = [0] * 24
                for rsv in list(rsvlist):
                    rsvDate = datetime.date(rsv.reserved.year, rsv.reserved.month, rsv.reserved.day)
                    if today == rsvDate:
                        check[rsv.reserved.hour] = 1
                checkenum = []
                for i, c in enumerate(check):
                    checkenum.append({"check": c, "id": i})
                output.append({
                    "name": today.strftime("%Y-%m-%d"),
                    "heatmap": checkenum
                })
                today += datetime.timedelta(days=1)
        params['table'] = output
        return render(request, "studyroom/check_result.html", params)
    return render(request, 'studyroom/check.html', params)

