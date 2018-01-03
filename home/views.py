from django.shortcuts import render

# Create your views here.
def index(request):
    params = {'title': 'ECE 학생회 AROUND 입니다'}
    return render(request, 'index.html', params)