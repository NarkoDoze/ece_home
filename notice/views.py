from django.shortcuts import render
from .models import Post

# Create your views here.
def notice_home(request):
    params = {'title': '공지사항'}
    params['recent'] = Post.objects.all().order_by('-id')[:10]
    return render(request, 'catalog.html', params)