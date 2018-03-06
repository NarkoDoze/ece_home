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
        query = dict(request.POST)
        if not {'sid': query['sid'][0], 'name': query['name'][0]} in index.sidIndex:
            params['error'] = query['sid'][0] + " " + query['name'][0] + " 등록되지 않은 학번입니다."
            return render(request, 'error.html', params)
        if not {'sid': query['sid'][1], 'name': query['name'][1]} in index.sidIndex:
            params['error'] = query['sid'][1] + " " + query['name'][1] + " 등록되지 않은 학번입니다."
            return render(request, 'error.html', params)
        if query['sid'][0] == query['sid'][1]:
            params['error'] = "같은 학번을 사용하실수 없습니다."
            return render(request, 'error.html', params)

        selectDate = []
        for select in query['select']:
            time = select.split('-')
            selectDate.append(datetime.datetime(int(time[0]), int(time[1]), int(time[2]), int(time[3])))

        selectNum = len(selectDate)
        if selectNum > 3:
            params['error'] = "3시간 이하만 선택 가능합니다."
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
                        print("HEY2")
                        params['error'] = "잘못된 쿼리입니다."
                        return render(request, 'error.html', params)
                rsvlist = sroom['model'].objects.filter(
                    reserved__range=(today, after),
                    sid=query['sid'][0],
                )

                if len(rsvlist) + selectNum > 3:
                    params['error'] = query['sid'][0] + " " + query['name'][0] + " 대여 시간(3시간)을 초과하였습니다."
                    return render(request, 'error.html', params)

                rsvlist = sroom['model'].objects.filter(
                    reserved__range=(today, after),
                    sid=query['sid'][1],
                )

                if len(rsvlist) + selectNum > 3:
                    params['error'] = query['sid'][1] + " " + query['name'][1] + " 대여 시간(3시간)을 초과하였습니다."
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

                params['error'] = "성공적으로 신청되었습니다."
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
    params = {'title': '스터디룸 확인'}
    # TODO: Get student id and check it
    return render(request, 'example.html', params)
