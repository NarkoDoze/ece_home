from django.shortcuts import render

# Create your views here.
def about(request):
    params = {'title': 'About AROUND'}
    return render(request, 'about.html', params)
