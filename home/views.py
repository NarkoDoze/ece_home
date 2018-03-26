from django.shortcuts import render
from event.models import Event
from notice.models import Post

# Create your views here.
def index(request):
    params = {'title': 'ECE Student Council AROUND'}

    events = Event.objects.all().order_by('-id')[:3]
    params['firstEvent'] = events[0]
    params['events'] = events[1:]

    posts = Post.objects.all().order_by('-id')[:5]
    for post in posts:
        post.date = str(post.created_at.month) + "-" + str(post.created_at.day)
    params['posts'] = posts
    params['announcelink'] = '/announce'

    return render(request, 'index.html', params)