from django.shortcuts import render

# Create your views here.
def index(request):
    params = {'title': 'ECE Student Council AROUND'}
    return render(request, 'index.html', params)