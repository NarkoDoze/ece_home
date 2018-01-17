from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'notice', views.notice_home, name='notice_home'),
]