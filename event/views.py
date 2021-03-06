from django.shortcuts import render
from .models import Event

# Create your views here.
def event_home(request):
    params = {'title': 'Event'}
    Postlen = len(Event.objects.all())
    Postlen = Postlen // 4 + 1 if Postlen % 4 else Postlen // 4
    if Postlen >= 4:
        PostOrder = {
            "1": ["1", "2", "3", "..."],
            "2": ["1", "2", "3", "..."],
            str(Postlen - 1): ["...", str(Postlen - 2), str(Postlen - 1), str(Postlen)],
            str(Postlen): ["...", str(Postlen - 2), str(Postlen - 1), str(Postlen)],
        }
        for i in range(3, Postlen - 1):
            PostOrder[str(i)] = ["...", str(i - 1), str(i), str(i + 1), "..."]
    else:
        PostOrder = {
            "1": ["1", "2", "3"],
            "2": ["1", "2", "3"],
            "3": ["1", "2", "3"]
        }
    lo = request.GET.get('lo')
    lo = 1 if lo == None else int(lo)
    start = (lo - 1) * 4
    end = lo * 4
    if start < 0 or end < 0:
        return render(request, 'example.html', params)
    params['recent'] = Event.objects.all().order_by('-id')[start:end]
    params['link'] = '/event'
    params['lo'] = str(lo)
    params['order'] = PostOrder[str(lo)]
    return render(request, 'catalog.html', params)

def event_content(request, idx):
    params = {'title': 'Event'}
    params['post'] = Event.objects.filter(id=idx)[0]
    return render(request, 'post.html', params)
